# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Daten\Documents\Projekte\LigaFont\ui\views\mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.7
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setObjectName("groupBox")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.groupBox)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.input_button = QtWidgets.QToolButton(self.groupBox)
        self.input_button.setObjectName("input_button")
        self.horizontalLayout_2.addWidget(self.input_button)
        self.reopen_input = QtWidgets.QToolButton(self.groupBox)
        self.reopen_input.setObjectName("reopen_input")
        self.horizontalLayout_2.addWidget(self.reopen_input)
        self.input_file = QtWidgets.QLineEdit(self.groupBox)
        self.input_file.setReadOnly(True)
        self.input_file.setObjectName("input_file")
        self.horizontalLayout_2.addWidget(self.input_file)
        self.verticalLayout.addWidget(self.groupBox)
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_2.setObjectName("groupBox_2")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.groupBox_2)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.output_button = QtWidgets.QToolButton(self.groupBox_2)
        self.output_button.setObjectName("output_button")
        self.horizontalLayout_3.addWidget(self.output_button)
        self.reopen_output = QtWidgets.QToolButton(self.groupBox_2)
        self.reopen_output.setObjectName("reopen_output")
        self.horizontalLayout_3.addWidget(self.reopen_output)
        self.output_dir = QtWidgets.QLineEdit(self.groupBox_2)
        self.output_dir.setReadOnly(True)
        self.output_dir.setObjectName("output_dir")
        self.horizontalLayout_3.addWidget(self.output_dir)
        self.save_button = QtWidgets.QPushButton(self.groupBox_2)
        self.save_button.setObjectName("save_button")
        self.horizontalLayout_3.addWidget(self.save_button)
        self.verticalLayout.addWidget(self.groupBox_2)
        self.item_table = QtWidgets.QTableView(self.centralwidget)
        self.item_table.setObjectName("item_table")
        self.item_table.horizontalHeader().setSortIndicatorShown(True)
        self.item_table.horizontalHeader().setStretchLastSection(True)
        self.item_table.verticalHeader().setStretchLastSection(False)
        self.verticalLayout.addWidget(self.item_table)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.groupBox.setTitle(_translate("MainWindow", "Input file"))
        self.input_button.setText(_translate("MainWindow", "..."))
        self.reopen_input.setText(_translate("MainWindow", "<"))
        self.groupBox_2.setTitle(_translate("MainWindow", "Output directory"))
        self.output_button.setText(_translate("MainWindow", "..."))
        self.reopen_output.setText(_translate("MainWindow", "<"))
        self.save_button.setText(_translate("MainWindow", "Save now!"))

