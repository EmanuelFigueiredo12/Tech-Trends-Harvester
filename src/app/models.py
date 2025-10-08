
from PySide6 import QtCore, QtGui

class RowsTableModel(QtCore.QAbstractTableModel):
    def __init__(self, columns, rows=None, parent=None):
        super().__init__(parent)
        self.columns = columns
        self.rows = rows or []

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self.rows)

    def columnCount(self, parent=QtCore.QModelIndex()):
        return len(self.columns)

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if not index.isValid():
            return None
        
        key = self.columns[index.column()][1]
        val = self.rows[index.row()].get(key, "")
        
        # Handle display role
        if role == QtCore.Qt.DisplayRole:
            if isinstance(val, float):
                return f"{val:.3f}"
            if isinstance(val, list):
                def sig_to_s(s):
                    if isinstance(s, dict):
                        return f"{s.get('source','')}:{s.get('metric_name','')}={s.get('metric_value','')}"
                    return str(s)
                return ", ".join(sig_to_s(v) for v in val)
            return str(val)
        
        # Make URL column clickable with blue underlined text
        if role == QtCore.Qt.ForegroundRole and key == "url" and val:
            return QtGui.QColor("blue")
        
        if role == QtCore.Qt.FontRole and key == "url" and val:
            font = QtGui.QFont()
            font.setUnderline(True)
            return font
        
        # Store URL for tooltip and interaction
        if role == QtCore.Qt.ToolTipRole and key == "url" and val:
            return f"Click to open:\n{val}"
        
        return None

    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        if role != QtCore.Qt.DisplayRole:
            return None
        if orientation == QtCore.Qt.Horizontal:
            return self.columns[section][0]
        return str(section + 1)

    def set_rows(self, rows):
        self.beginResetModel()
        self.rows = rows or []
        self.endResetModel()
