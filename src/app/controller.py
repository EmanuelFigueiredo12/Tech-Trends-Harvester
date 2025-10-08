
"""
Tech Trends Harvester - Application Controller
Author: Rich Lewis
"""

import time, traceback, os, json, datetime as dt
from dataclasses import dataclass, field
from typing import Dict, List, Set
from PySide6 import QtCore
from ..aggregate import aggregate, compute_movers, as_markdown, get_blog_topics
from .registry import REGISTRY

@dataclass
class SourceState:
    enabled: bool = True
    last_error: str = ""
    last_run_ms: int = 0
    rows: List[dict] = field(default_factory=list)
    status: str = "idle"  # idle, fetching, done, error

class FetchWorker(QtCore.QObject):
    resultReady = QtCore.Signal(str, list, int)  # source_key, rows, elapsed_ms
    errorReady = QtCore.Signal(str, str)         # source_key, error
    finished = QtCore.Signal()

    def __init__(self, source_key: str, params: dict):
        super().__init__()
        self.source_key = source_key
        self.params = params or {}

    @QtCore.Slot()
    def run(self):
        t0 = time.time()
        try:
            spec = REGISTRY[self.source_key]
            rows = spec.fetch_fn(**self.params)
            elapsed = int((time.time() - t0) * 1000)
            self.resultReady.emit(self.source_key, rows or [], elapsed)
        except Exception as e:
            tb = traceback.format_exc(limit=3)
            self.errorReady.emit(self.source_key, f"{e}\n{tb}")
        finally:
            self.finished.emit()

class AppController(QtCore.QObject):
    allRefreshDone = QtCore.Signal()
    aggregatedReady = QtCore.Signal(list)
    bySourceReady = QtCore.Signal(dict)
    moversReady = QtCore.Signal(list)
    blogTopicsReady = QtCore.Signal(list)  # New signal for blog-worthy topics
    sourceStatusChanged = QtCore.Signal(str, object)  # source_key, SourceState
    progressUpdate = QtCore.Signal(str)  # progress message

    def __init__(self, cfg: dict, base_dir: str, parent=None):
        super().__init__(parent)
        self.cfg = cfg
        self.base_dir = base_dir
        self.weights = cfg.get("weights", {})
        self.collectors_cfg = cfg.get("collectors", {})
        self.out_dir = cfg.get("run", {}).get("output_dir", "data")
        self.abs_out = os.path.join(base_dir, self.out_dir)
        os.makedirs(self.abs_out, exist_ok=True)
        self.history_dir = os.path.join(self.abs_out, "history")
        os.makedirs(self.history_dir, exist_ok=True)
        self._active_threads: Set[str] = set()
        self._expected_threads: Set[str] = set()
        self.state: Dict[str, SourceState] = {}
        for key in REGISTRY:
            enabled = bool(self.collectors_cfg.get(key, {}).get("enabled", False))
            self.state[key] = SourceState(enabled=enabled)

    def set_enabled(self, key: str, enabled: bool):
        self.state[key].enabled = enabled
        self.sourceStatusChanged.emit(key, self.state[key])

    def _make_params(self, key: str):
        params = {k: v for k, v in self.collectors_cfg.get(key, {}).items() if k != "enabled"}
        return params

    def refresh_one(self, key: str):
        """Refresh a single source in a background thread."""
        if key in self._active_threads:
            self.progressUpdate.emit(f"[{key}] already running, skipping...")
            return
        
        self.state[key].status = "fetching"
        self._active_threads.add(key)
        self.progressUpdate.emit(f"[{key}] Starting fetch...")
        
        # Don't set parent for QThread to avoid macOS issues
        th = QtCore.QThread()
        worker = FetchWorker(key, self._make_params(key))
        worker.moveToThread(th)
        
        th.started.connect(worker.run)
        worker.resultReady.connect(self._on_result)
        worker.errorReady.connect(self._on_error)
        worker.finished.connect(lambda: self._on_thread_finished(key, th, worker))
        
        # Store reference to prevent GC
        if not hasattr(self, '_thread_refs'):
            self._thread_refs = {}
        self._thread_refs[key] = (th, worker)
        
        th.start()

    def _on_thread_finished(self, key: str, thread: QtCore.QThread, worker: QtCore.QObject):
        """Clean up after a thread finishes."""
        # Don't call wait() here - it causes "thread tried to wait on itself" error
        # The thread will clean itself up when quit() is called
        thread.quit()
        
        # Schedule cleanup using deleteLater
        worker.deleteLater()
        thread.deleteLater()
        
        if key in self._active_threads:
            self._active_threads.remove(key)
        if hasattr(self, '_thread_refs') and key in self._thread_refs:
            del self._thread_refs[key]
        
        # Check if all expected threads are done
        if self._expected_threads and len(self._active_threads) == 0:
            self.progressUpdate.emit("All sources complete!")
            self._expected_threads.clear()
            self.allRefreshDone.emit()
    
    def refresh_all(self):
        """Refresh all sources regardless of enabled status."""
        keys = list(REGISTRY.keys())
        self._expected_threads = set(keys)
        self.progressUpdate.emit(f"Starting refresh of {len(keys)} sources...")
        for key in keys:
            self.refresh_one(key)

    def refresh_selected(self):
        """Refresh only enabled sources."""
        keys = [k for k, st in self.state.items() if st.enabled]
        if not keys:
            self.progressUpdate.emit("No sources enabled!")
            return
        self._expected_threads = set(keys)
        self.progressUpdate.emit(f"Starting refresh of {len(keys)} enabled sources...")
        for key in keys:
            self.refresh_one(key)

    @QtCore.Slot(str, list, int)
    def _on_result(self, key: str, rows: list, elapsed_ms: int):
        st = self.state[key]
        st.rows = rows
        st.last_run_ms = elapsed_ms
        st.last_error = ""
        st.status = "done"
        self.sourceStatusChanged.emit(key, st)
        self._publish()

    @QtCore.Slot(str, str)
    def _on_error(self, key: str, err: str):
        st = self.state[key]
        st.last_error = err
        st.rows = []
        st.status = "error"
        self.sourceStatusChanged.emit(key, st)
        self._publish()

    def _load_prev_agg(self):
        path = os.path.join(self.abs_out, "last_agg.json")
        if not os.path.exists(path):
            return []
        try:
            return json.load(open(path, "r", encoding="utf-8"))
        except Exception:
            return []

    def _save_curr_agg(self, agg_rows):
        last_path = os.path.join(self.abs_out, "last_agg.json")
        json.dump(agg_rows, open(last_path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
        ts = dt.datetime.utcnow().strftime("%Y%m%d-%H%M%S")
        hist_path = os.path.join(self.history_dir, f"agg-{ts}.json")
        json.dump(agg_rows, open(hist_path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)

    def _publish(self):
        by_source = {k: st.rows for k, st in self.state.items() if st.rows}
        all_rows = [r for rows in by_source.values() for r in rows]
        agg_rows, _ = aggregate(all_rows, self.weights, min_score_threshold=0.5) if all_rows else ([], None)
        prev = self._load_prev_agg()
        movers = compute_movers(prev, agg_rows) if agg_rows else []
        blog_topics = get_blog_topics(agg_rows, top_n=100) if agg_rows else []
        if agg_rows:
            self._save_curr_agg(agg_rows)
        self.bySourceReady.emit(by_source)
        self.aggregatedReady.emit(agg_rows)
        self.moversReady.emit(movers)
        self.blogTopicsReady.emit(blog_topics)

    def export_markdown(self, path: str):
        by_source = {k: st.rows for k, st in self.state.items() if st.rows}
        all_rows = [r for rows in by_source.values() for r in rows]
        agg_rows, _ = aggregate(all_rows, self.weights) if all_rows else ([], None)
        prev = self._load_prev_agg()
        movers = compute_movers(prev, agg_rows) if agg_rows else []
        md = as_markdown(agg_rows, by_source, movers)
        with open(path, "w", encoding="utf-8") as f:
            f.write(md)
        return path
