from PyQt5.QtCore import QObject


class LigatureItem(QObject):

    def __init__(self, name, ligature, parent=None):
        super(LigatureItem, self).__init__(parent)
        self.data = [name, ligature]

    def get(self, index):
        return self.data[index]

    def get_name(self):
        return self.get(0)

    def get_ligature(self):
        return self.get(1)

    def set_ligature(self, ligature):
        self.data[1] = ligature
