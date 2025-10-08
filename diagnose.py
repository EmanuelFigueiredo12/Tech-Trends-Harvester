#!/usr/bin/env python3
"""
Diagnostic script for Tech Trends Harvester
Checks if everything is set up correctly
"""

import sys
import os

def check_python_version():
    print("[PYTHON] Python Version Check")
    version = sys.version_info
    print(f"   Version: {version.major}.{version.minor}.{version.micro}")
    if version.major >= 3 and version.minor >= 9:
        print("   [OK] Python version is OK (>=3.9)")
        return True
    else:
        print("   [ERROR] Python version too old (need >=3.9)")
        return False

def check_imports():
    print("\n[DEPS] Dependency Check")
    required = [
        ("PySide6", "PySide6"),
        ("requests", "requests"),
        ("yaml", "PyYAML"),
        ("pandas", "pandas"),
        ("feedparser", "feedparser"),
        ("bs4", "beautifulsoup4"),
    ]
    
    all_ok = True
    for module, package in required:
        try:
            __import__(module)
            print(f"   [OK] {package}")
        except ImportError:
            print(f"   [ERROR] {package} - not installed")
            all_ok = False
    
    return all_ok

def check_project_structure():
    print("\n[FILES] Project Structure Check")
    required_files = [
        "config/sources.yaml",
        "src/app/controller.py",
        "src/app/mainwindow.py",
        "src/aggregate.py",
        "run_app.py",
    ]
    
    all_ok = True
    for file in required_files:
        if os.path.exists(file):
            print(f"   [OK] {file}")
        else:
            print(f"   [ERROR] {file} - missing")
            all_ok = False
    
    return all_ok

def check_config():
    print("\n[CONFIG] Configuration Check")
    try:
        import yaml
        with open("config/sources.yaml", "r") as f:
            cfg = yaml.safe_load(f)
        
        if "collectors" in cfg:
            enabled = sum(1 for v in cfg["collectors"].values() if v.get("enabled", False))
            total = len(cfg["collectors"])
            print(f"   [OK] Config loaded: {enabled}/{total} sources enabled")
        else:
            print("   [WARN] Config loaded but no collectors found")
        
        if "weights" in cfg:
            print(f"   [OK] Weights defined for {len(cfg['weights'])} sources")
        
        return True
    except Exception as e:
        print(f"   [ERROR] Config error: {e}")
        return False

def test_collector():
    print("\n[NETWORK] Network Test (Hacker News)")
    try:
        from src.collectors import hackernews
        print("   Testing fetch...")
        rows = hackernews.fetch(top_n=3)
        if rows:
            print(f"   [OK] Successfully fetched {len(rows)} items")
            print(f"   Sample: {rows[0]['term']} ({rows[0]['metric_value']} points)")
            return True
        else:
            print("   [WARN] No items returned (network issue?)")
            return False
    except Exception as e:
        print(f"   [ERROR] Fetch failed: {e}")
        return False

def main():
    print("=" * 60)
    print("Tech Trends Harvester - Diagnostic Tool")
    print("=" * 60)
    
    checks = [
        check_python_version(),
        check_imports(),
        check_project_structure(),
        check_config(),
        test_collector(),
    ]
    
    print("\n" + "=" * 60)
    if all(checks):
        print("[SUCCESS] All checks passed! You're ready to run the app.")
        print("\nRun: uv run python run_app.py")
        print("Or:  ./start.sh")
    else:
        print("[FAILED] Some checks failed. Fix the issues above.")
        print("\nTry: uv sync")
        sys.exit(1)
    print("=" * 60)

if __name__ == "__main__":
    main()

