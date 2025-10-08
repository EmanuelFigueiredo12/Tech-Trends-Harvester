
"""
Tech Trends Harvester - Main Window
Author: Rich Lewis
test ci comment
"""

from PySide6 import QtWidgets, QtCore, QtGui
import yaml, os
try:
    import tomllib  # Python 3.11+
except ImportError:
    import tomli as tomllib  # type: ignore  # Python 3.9-3.10
from .controller import AppController
from .models import RowsTableModel
from .registry import REGISTRY

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Read version from pyproject.toml
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        pyproject_path = os.path.join(base_dir, "pyproject.toml")
        try:
            with open(pyproject_path, "rb") as f:
                pyproject = tomllib.load(f)
                version = pyproject.get("project", {}).get("version", "")
            title = f"Tech Trends Harvester v{version}" if version else "Tech Trends Harvester"
        except:
            title = "Tech Trends Harvester"
        
        self.setWindowTitle(title)
        self.resize(1280, 820)
        
        # Set application icon
        icon_path = os.path.join(base_dir, "assets", "icon.svg")
        if os.path.exists(icon_path):
            self.setWindowIcon(QtGui.QIcon(icon_path))

        cfg_path = os.path.join(base_dir, "config", "sources.yaml")
        with open(cfg_path, "r", encoding="utf-8") as f:
            cfg = yaml.safe_load(f)

        self.controller = AppController(cfg, base_dir)
        self._build_ui()
        self._wire()
        self.controller._publish()

    def _build_ui(self):
        central = QtWidgets.QWidget()
        self.setCentralWidget(central)
        layout = QtWidgets.QHBoxLayout(central)

        # Left controls
        left = QtWidgets.QWidget()
        left.setFixedWidth(300)
        lytL = QtWidgets.QVBoxLayout(left)
        lytL.addWidget(QtWidgets.QLabel("Sources"))
        self.checks = {}
        scroll = QtWidgets.QScrollArea()
        scroll.setWidgetResizable(True)
        inner = QtWidgets.QWidget()
        innerL = QtWidgets.QVBoxLayout(inner)
        for key in sorted(REGISTRY.keys()):
            row = QtWidgets.QWidget()
            hl = QtWidgets.QHBoxLayout(row)
            cb = QtWidgets.QCheckBox(key)
            cb.setChecked(self.controller.state[key].enabled)
            cb.stateChanged.connect(lambda s, k=key: self.controller.set_enabled(k, bool(s)))
            btn = QtWidgets.QPushButton("↻")
            btn.setFixedWidth(30)
            btn.setToolTip("Refresh this source")
            btn.clicked.connect(lambda _=None, k=key: self.controller.refresh_one(k))
            hl.addWidget(cb)
            hl.addWidget(btn)
            innerL.addWidget(row)
            self.checks[key] = cb
        innerL.addStretch(1)
        scroll.setWidget(inner)
        lytL.addWidget(scroll)

        self.btn_sel = QtWidgets.QPushButton("Refresh Selected")
        self.btn_all = QtWidgets.QPushButton("Refresh ALL (all sources)")
        self.btn_export = QtWidgets.QPushButton("Export → Markdown")
        lytL.addWidget(self.btn_sel)
        lytL.addWidget(self.btn_all)
        lytL.addWidget(self.btn_export)

        lytL.addWidget(QtWidgets.QLabel("Errors / Status"))
        self.txt = QtWidgets.QTextEdit()
        self.txt.setReadOnly(True)
        self.txt.setMinimumHeight(200)
        lytL.addWidget(self.txt)

        layout.addWidget(left)

        # Right tabs
        tabs = QtWidgets.QTabWidget()

        # Aggregated
        tabA = QtWidgets.QWidget()
        vA = QtWidgets.QVBoxLayout(tabA)
        self.tblA = QtWidgets.QTableView()
        self.modelA = RowsTableModel([("Term","term"),("Score","score"),("Sources","sources"),("Top signals","top_signals")], [])
        self.tblA.setModel(self.modelA)
        self.tblA.setSortingEnabled(True)
        vA.addWidget(self.tblA)
        tabs.addTab(tabA, "Aggregated")

        # By Source
        tabS = QtWidgets.QWidget()
        vS = QtWidgets.QVBoxLayout(tabS)
        hl = QtWidgets.QHBoxLayout()
        hl.addWidget(QtWidgets.QLabel("Source:"))
        self.cmb = QtWidgets.QComboBox()
        for key in sorted(REGISTRY.keys()):
            self.cmb.addItem(key)
        hl.addWidget(self.cmb, 1)
        vS.addLayout(hl)
        self.tblS = QtWidgets.QTableView()
        self.modelS = RowsTableModel([("Term","term"),("Kind","kind"),("Metric","metric_name"),("Value","metric_value"),("URL","url")], [])
        self.tblS.setModel(self.modelS)
        self.tblS.setSortingEnabled(True)
        self.tblS.clicked.connect(self._onTableClick)
        vS.addWidget(self.tblS)
        tabs.addTab(tabS, "By Source")

        # Blog Topics (NEW - Most Important Tab!)
        tabB = QtWidgets.QWidget()
        vB = QtWidgets.QVBoxLayout(tabB)
        info = QtWidgets.QLabel("<b>Blog-Worthy Topics</b> - Now with Reddit posts & Google Trends! Questions marked with [?]")
        info.setStyleSheet("padding: 8px; background-color: #e3f2fd; border-radius: 4px;")
        vB.addWidget(info)
        self.tblB = QtWidgets.QTableView()
        self.modelB = RowsTableModel([("Topic/Question","term"),("Type","question_type"),("Category","category"),("Score","blog_worthiness"),("Words","word_count"),("Sources","source_count")], [])
        self.tblB.setModel(self.modelB)
        self.tblB.setSortingEnabled(True)
        self.tblB.clicked.connect(self._onTableClick)  # Make clickable
        vB.addWidget(self.tblB)
        tabs.addTab(tabB, "Blog Topics")

        # Movers
        tabM = QtWidgets.QWidget()
        vM = QtWidgets.QVBoxLayout(tabM)
        self.tblM = QtWidgets.QTableView()
        self.modelM = RowsTableModel([("Term","term"),("Δ","delta"),("Δ%","pct"),("Now","score_now"),("Prev","score_prev"),("Sources","sources")], [])
        self.tblM.setModel(self.modelM)
        self.tblM.setSortingEnabled(True)
        vM.addWidget(self.tblM)
        tabs.addTab(tabM, "Movers (WoW)")

        # Debug
        tabD = QtWidgets.QWidget()
        vD = QtWidgets.QVBoxLayout(tabD)
        self.debugOut = QtWidgets.QPlainTextEdit(); self.debugOut.setReadOnly(True)
        vD.addWidget(self.debugOut)
        tabs.addTab(tabD, "Debug")

        layout.addWidget(tabs, 1)

        self.btn_sel.clicked.connect(lambda: (_disable(), self.controller.refresh_selected()))
        self.btn_all.clicked.connect(lambda: (_disable(), self.controller.refresh_all()))  # all sources
        self.btn_export.clicked.connect(self._export)
        def _disable():
            self.btn_sel.setEnabled(False); self.btn_all.setEnabled(False); self.btn_export.setEnabled(False)
        def _enable():
            self.btn_sel.setEnabled(True); self.btn_all.setEnabled(True); self.btn_export.setEnabled(True)
        self.controller.allRefreshDone.connect(_enable)

    def _wire(self):
        self.controller.aggregatedReady.connect(self._onAgg)
        self.controller.bySourceReady.connect(self._onBySrc)
        self.controller.moversReady.connect(self._onMovers)
        self.controller.blogTopicsReady.connect(self._onBlogTopics)
        self.controller.sourceStatusChanged.connect(self._onStatus)
        self.controller.progressUpdate.connect(self._onProgress)
        self.cmb.currentTextChanged.connect(lambda _: self.controller._publish())

    def _onAgg(self, rows):
        self.modelA.set_rows(rows)
        self.tblA.resizeColumnsToContents()

    def _onBySrc(self, by):
        key = self.cmb.currentText()
        self.modelS.set_rows(by.get(key, []))
        self.tblS.resizeColumnsToContents()

    def _onMovers(self, rows):
        self.modelM.set_rows(rows)
        self.tblM.resizeColumnsToContents()
    
    def _onBlogTopics(self, rows):
        self.modelB.set_rows(rows)
        self.tblB.resizeColumnsToContents()

    def _onStatus(self, key, st):
        if st.last_error:
            msg = f"[{key}] ERROR: {st.last_error.splitlines()[0]}"; self.txt.append(msg); self.debugOut.appendPlainText(msg)
        else:
            msg = f"[{key}] OK - {len(st.rows)} rows in {st.last_run_ms} ms"; self.txt.append(msg); self.debugOut.appendPlainText(msg)
    
    def _onProgress(self, msg):
        """Handle progress updates from controller."""
        self.txt.append(msg)
        self.debugOut.appendPlainText(msg)
    
    def _onTableClick(self, index):
        """Handle clicks on table cells to open URLs."""
        if not index.isValid():
            return
        
        # Get the column key
        model = index.model()
        if not hasattr(model, 'columns'):
            return
        
        col_key = model.columns[index.column()][1]
        
        # If it's a URL column, open it
        if col_key == "url":
            url = model.rows[index.row()].get("url", "")
            if url:
                QtGui.QDesktopServices.openUrl(QtCore.QUrl(url))

    def _export(self):
        dlg = QtWidgets.QFileDialog(self, "Export Markdown")
        dlg.setAcceptMode(QtWidgets.QFileDialog.AcceptSave)
        dlg.setNameFilter("Markdown (*.md)")
        dlg.selectFile("tech-trends-report.md")
        if dlg.exec():
            path = dlg.selectedFiles()[0]
            if not path.lower().endswith(".md"):
                path += ".md"
            self.controller.export_markdown(path)
