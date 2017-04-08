from PyQt5.QtCore import QAbstractTableModel, QVariant
from PyQt5.QtCore import Qt

from ui.ligatureitem import LigatureItem


class LigatureTableModel(QAbstractTableModel):
    def __init__(self, rows, headers, parent=None):
        super(LigatureTableModel, self).__init__(parent)

        self.rows = rows
        self.headers = headers
        self._previous_data = None

    def rowCount(self, parent=None, *args, **kwargs):
        return len(self.rows)

    def columnCount(self, parent=None, *args, **kwargs):
        return 2

    def data(self, index, role=None):
        if not index.isValid() or role != Qt.DisplayRole:
            return QVariant()

        return QVariant(self.rows[index.row()].get(index.column()))

    def headerData(self, col, orientation, role=None):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return QVariant(self.headers[col])
        return QVariant()

    def sort(self, column, order=None):
        """Sort table by given column number.
        """
        self.rows = sorted(self.rows, key=lambda x: x.get(column))
        if order == Qt.DescendingOrder:
            self.rows.reverse()

    def flags(self, index):
        if index.column() == 1:
            return Qt.ItemIsEditable | Qt.ItemIsEnabled | Qt.ItemIsSelectable
        else:
            return Qt.ItemIsEnabled | Qt.ItemIsSelectable

    def setData(self, index, data, role=None):
        self.rows[index.row()].set_ligature(data)
        return True

    def clear(self):
        self._previous_data = self.get_mapping()
        self.rows = []
        self.layoutChanged.emit()

    def restore_mapping(self):
        if not self._previous_data:
            return

        for row in self.rows:
            name = row.get_name()

            for lig in self._previous_data:
                if name == self._previous_data[lig]:
                    row.set_ligature(lig)
        self.layoutChanged.emit()

    def add(self, item):
        assert isinstance(item, LigatureItem)

        self.rows.append(item)
        self.layoutChanged.emit()

    def get_mapping(self):
        mapping = {}
        for row in self.rows:
            lig = row.get_ligature()
            if lig and not lig in mapping:
                mapping[lig] = row.get_name()
            elif lig:
                raise ReferenceError('{} already assigned'.format(lig))
        return mapping
