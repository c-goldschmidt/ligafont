import hashlib
import os
import traceback

import logging

import sys
from PyQt5.QtCore import QObject, pyqtSlot
from PyQt5.QtWidgets import QFileDialog

from ui.itemlistcontroller import ItemListController
from ui.settings import get_setting, set_setting
from ui.views.mainwindow import Ui_MainWindow

_logger = logging.getLogger(__name__)


class MainUIController(QObject):

    def __init__(self, window, app):
        super(MainUIController, self).__init__()

        self._window = window
        self._app = app

        self.ui = Ui_MainWindow()
        self.ui.setupUi(window)

        self.item_list_ctrl = ItemListController(self)

        self._init()

    def _init(self):
        sys.excepthook = lambda ex_type, value, trace: self.handle_exception(ex_type, value, trace)

        self.ui.input_button.clicked.connect(self.load_input_file)
        self.ui.output_button.clicked.connect(self.open_output_dir)
        self.ui.save_button.clicked.connect(self.item_list_ctrl.save)
        self.ui.reopen_output.clicked.connect(self.reopen_output_dir)
        self.ui.reopen_input.clicked.connect(self.reopen_input_file)

    def log(self, message):
        message = str(message)
        self.ui.statusbar.showMessage(message)
        print(message)

    @staticmethod
    def _get_search_path(name):
        search_path = get_setting('file_path_' + name)
        if not search_path:
            search_path = get_setting('file_path')

        return search_path

    @staticmethod
    def _save_search_path(name, value):
        set_setting('file_path_' + name, value)
        set_setting('file_path', value)

    @pyqtSlot()
    def load_input_file(self):
        path = self._get_search_path('input_file')
        suffix = 'All files (*);;Webfont files (*.woff, *.woff2);;TTF files (*.ttf)'
        file_name = QFileDialog.getOpenFileName(None, 'Open file', path, suffix, '',  QFileDialog.DontUseNativeDialog)

        if file_name:
            self._save_search_path('input_file', file_name[0])
            self.ui.input_file.setText(file_name[0])
            self.item_list_ctrl.load_file(file_name[0])

    @pyqtSlot()
    def reopen_input_file(self):
        path = self._get_search_path('input_file')
        self.ui.input_file.setText(path)
        self.item_list_ctrl.load_file(path)

    @pyqtSlot()
    def open_output_dir(self):
        path = self._get_search_path('output_dir')
        dirname = QFileDialog.getExistingDirectory(None, 'Open directory', path, QFileDialog.ShowDirsOnly)

        if dirname:
            self._save_search_path('output_dir', dirname)
            self.ui.output_dir.setText(dirname)
            self.item_list_ctrl.output_dir = dirname

    @pyqtSlot()
    def reopen_output_dir(self):
        path = self._get_search_path('output_dir')
        self.ui.output_dir.setText(path)
        self.item_list_ctrl.output_dir = path

    def handle_exception(self, ex_type, value, trace):
        filename, line, _, _ = traceback.extract_tb(trace).pop()

        self.log('an exception occured, i am very sorry.')
        self.log('details: {}: {} ({}:{})'.format(
            ex_type.__name__,
            value,
            os.path.basename(filename),
            line,
        ))

        _logger.error('EXCEPTION', exc_info=(ex_type, value, trace))