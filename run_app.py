
"""
Entry point for Tech Trends Harvester GUI application
Author: Rich Lewis
"""

import os
import sys

from PySide6 import QtWidgets, QtGui

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # dotenv not installed, environment variables must be set manually
    pass

from src.app.mainwindow import MainWindow

def main():
    app = QtWidgets.QApplication(sys.argv)
    
    # Set application icon (shows in dock/taskbar)
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Try PNG first (better compatibility), then SVG
    icon_files = [
        os.path.join(base_dir, "assets", "icon.png"),
        os.path.join(base_dir, "assets", "icon.svg")
    ]
    
    for icon_path in icon_files:
        if os.path.exists(icon_path):
            app_icon = QtGui.QIcon(icon_path)
            # Set on application (dock/taskbar)
            app.setWindowIcon(app_icon)
            # Set application name
            app.setApplicationName("Tech Trends Harvester")
            if hasattr(app, 'setApplicationDisplayName'):
                app.setApplicationDisplayName("Tech Trends Harvester")
            break
    
    w = MainWindow()
    w.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
