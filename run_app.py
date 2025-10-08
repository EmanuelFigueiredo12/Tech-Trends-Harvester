
"""
Entry point for Tech Trends Harvester GUI application
Author: Rich Lewis
"""

from PySide6 import QtWidgets
import sys
from src.app.mainwindow import MainWindow

def main():
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
