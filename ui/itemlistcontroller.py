import os
import tempfile

from PyQt5.QtCore import QObject, pyqtSlot
from fontTools.ttLib import TTFont

from ui.ligatureitem import LigatureItem
from ui.ligaturetablemodel import LigatureTableModel
from ui.processor import FontProcessor


class ItemListController(QObject):

    def __init__(self, parent):
        super(ItemListController, self).__init__()

        self._parent = parent
        self._items = []

        self.ttf = None

        self.font_name = None
        self.font_extension = None
        self.xml_file = None
        self.xml_out_file = None
        self.output_dir = None

        self._init_table()

    def load_file(self, filename):
        split_file = os.path.basename(filename).split('.')
        self.font_name = '.'.join(split_file[:-1])
        self.font_extension = split_file[-1]

        self.ttf = TTFont(filename)
        self._load_items()

    def _init_table(self):
        self.table = self._parent.ui.item_table

        self.table_model = LigatureTableModel([], ['Name', 'Ligature'], self.table)
        self.table.setModel(self.table_model)

        self.table.setSortingEnabled(True)

    def _load_items(self):
        self.table_model.clear()

        for name in self.ttf.getGlyphNames():
            self.table_model.add(LigatureItem(name, ''))

        self.table_model.restore_mapping()

    @pyqtSlot()
    def save(self):
        if not self.output_dir:
            self._parent.log('no dir!')
        else:
            self.save_to_dir(self.output_dir)

    def save_to_dir(self, directory):
        try:
            mapping = self.table_model.get_mapping()
            processor = FontProcessor(self.ttf, mapping)
            processor.save_files(directory, self.font_name)
            self._parent.log('OK!')
        except ReferenceError as e:
            self._parent.log(e)
