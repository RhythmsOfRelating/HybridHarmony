# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!
import sys, time
from PyQt5 import QtCore, QtGui, QtWidgets
from acquisition import Discovery
from analysis import Analysis
import time
from PyQt5.QtCore import QProcess
import numpy as np
import logging.config
import logging
import sys, os
from math import factorial

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowModality(QtCore.Qt.NonModal)
        MainWindow.resize(800, 600)
        MainWindow.setMinimumSize(QtCore.QSize(800, 600))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(99, 99, 99))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(246, 246, 246))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(207, 223, 248))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Midlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(80, 95, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(106, 127, 160))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(99, 99, 99))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.BrightText, brush)
        brush = QtGui.QBrush(QtGui.QColor(99, 99, 99))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(246, 246, 246))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(246, 246, 246))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Shadow, brush)
        brush = QtGui.QBrush(QtGui.QColor(207, 223, 248))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.AlternateBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ToolTipBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ToolTipText, brush)
        brush = QtGui.QBrush(QtGui.QColor(99, 99, 99, 128))
        brush.setStyle(QtCore.Qt.NoBrush)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.PlaceholderText, brush)
        brush = QtGui.QBrush(QtGui.QColor(99, 99, 99))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(246, 246, 246))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(207, 223, 248))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Midlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(80, 95, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(106, 127, 160))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(99, 99, 99))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.BrightText, brush)
        brush = QtGui.QBrush(QtGui.QColor(99, 99, 99))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(246, 246, 246))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(246, 246, 246))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Shadow, brush)
        brush = QtGui.QBrush(QtGui.QColor(207, 223, 248))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.AlternateBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ToolTipBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ToolTipText, brush)
        brush = QtGui.QBrush(QtGui.QColor(99, 99, 99, 128))
        brush.setStyle(QtCore.Qt.NoBrush)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.PlaceholderText, brush)
        brush = QtGui.QBrush(QtGui.QColor(99, 99, 99))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(99, 99, 99))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(207, 223, 248))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Midlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(80, 95, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(106, 127, 160))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(99, 99, 99))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.BrightText, brush)
        brush = QtGui.QBrush(QtGui.QColor(99, 99, 99))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(99, 99, 99))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(99, 99, 99))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Shadow, brush)
        brush = QtGui.QBrush(QtGui.QColor(160, 191, 241))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.AlternateBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ToolTipBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ToolTipText, brush)
        brush = QtGui.QBrush(QtGui.QColor(99, 99, 99, 128))
        brush.setStyle(QtCore.Qt.NoBrush)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.PlaceholderText, brush)
        MainWindow.setPalette(palette)
        MainWindow.setStyleSheet("")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.btn_loadStreams = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        self.btn_loadStreams.setFont(font)
        self.btn_loadStreams.setToolTipDuration(7000)
        self.btn_loadStreams.setObjectName("btn_loadStreams")
        self.gridLayout_2.addWidget(self.btn_loadStreams, 1, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem, 0, 0, 1, 1)
        self.gridLayout.addLayout(self.gridLayout_2, 4, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 0, 0, 1, 1)
        self.label = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 2, 1, 1, 1)
        self.param_check = QtWidgets.QTextBrowser(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(7)
        self.param_check.setFont(font)
        self.param_check.setObjectName("param_check")
        self.gridLayout.addWidget(self.param_check, 3, 1, 1, 1)
        self.infoTable = QtWidgets.QTableWidget(self.centralwidget)
        self.infoTable.setMinimumSize(QtCore.QSize(355, 192))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.infoTable.setFont(font)
        self.infoTable.setCornerButtonEnabled(True)
        self.infoTable.setRowCount(0)
        self.infoTable.setColumnCount(4)
        self.infoTable.setObjectName("infoTable")
        self.gridLayout.addWidget(self.infoTable, 3, 0, 1, 1)
        self.freqTable = QtWidgets.QTableWidget(self.centralwidget)
        self.freqTable.setMinimumSize(QtCore.QSize(355, 193))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.freqTable.setFont(font)
        self.freqTable.setColumnCount(4)
        self.freqTable.setObjectName("freqTable")
        self.freqTable.setRowCount(0)
        self.gridLayout.addWidget(self.freqTable, 1, 0, 1, 1)
        self.params = QtWidgets.QGridLayout()
        self.params.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.params.setContentsMargins(0, -1, -1, -1)
        self.params.setSpacing(2)
        self.params.setObjectName("params")
        self.comboBox_chn = QtWidgets.QComboBox(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        self.comboBox_chn.setFont(font)
        self.comboBox_chn.setObjectName("comboBox_chn")
        self.comboBox_chn.addItem("")
        self.comboBox_chn.addItem("")
        self.params.addWidget(self.comboBox_chn, 2, 2, 1, 1)
        self.label_chn = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(8)
        self.label_chn.setFont(font)
        self.label_chn.setObjectName("label_chn")
        self.params.addWidget(self.label_chn, 2, 0, 1, 1)
        self.comboBox_device = QtWidgets.QComboBox(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        self.comboBox_device.setFont(font)
        self.comboBox_device.setObjectName("comboBox_device")
        self.comboBox_device.addItem("")
        self.comboBox_device.addItem("")
        self.comboBox_device.addItem("")
        self.comboBox_device.addItem("")
        self.params.addWidget(self.comboBox_device, 0, 2, 1, 1)
        self.label_input = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(8)
        self.label_input.setFont(font)
        self.label_input.setObjectName("label_input")
        self.params.addWidget(self.label_input, 1, 0, 1, 1)
        self.label_conn = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        self.label_conn.setFont(font)
        self.label_conn.setObjectName("label_conn")
        self.params.addWidget(self.label_conn, 3, 0, 1, 1)
        self.lineEdit_wsize = QtWidgets.QLineEdit(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        self.lineEdit_wsize.setFont(font)
        self.lineEdit_wsize.setObjectName("lineEdit_wsize")
        self.params.addWidget(self.lineEdit_wsize, 4, 2, 1, 1)
        self.label_device = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(8)
        self.label_device.setFont(font)
        self.label_device.setObjectName("label_device")
        self.params.addWidget(self.label_device, 0, 0, 1, 1)
        self.comboBox_conn = QtWidgets.QComboBox(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        self.comboBox_conn.setFont(font)
        self.comboBox_conn.setObjectName("comboBox_conn")
        self.comboBox_conn.addItem("")
        self.comboBox_conn.addItem("")
        self.comboBox_conn.addItem("")
        self.comboBox_conn.addItem("")
        self.comboBox_conn.addItem("")
        self.comboBox_conn.addItem("")
        self.params.addWidget(self.comboBox_conn, 3, 2, 1, 1)
        self.label_oscPort = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        self.label_oscPort.setFont(font)
        self.label_oscPort.setObjectName("label_oscPort")
        self.params.addWidget(self.label_oscPort, 7, 0, 1, 1)
        self.comboBox_input = QtWidgets.QComboBox(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        self.comboBox_input.setFont(font)
        self.comboBox_input.setObjectName("comboBox_input")
        self.comboBox_input.addItem("")
        self.params.addWidget(self.comboBox_input, 1, 2, 1, 1)
        self.lineEdit_oscIP = QtWidgets.QLineEdit(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        self.lineEdit_oscIP.setFont(font)
        self.lineEdit_oscIP.setStatusTip("")
        self.lineEdit_oscIP.setObjectName("lineEdit_oscIP")
        self.params.addWidget(self.lineEdit_oscIP, 6, 2, 1, 1)
        self.lineEdit_oscCH = QtWidgets.QLineEdit(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        self.lineEdit_oscCH.setFont(font)
        self.lineEdit_oscCH.setObjectName("lineEdit_oscCH")
        self.params.addWidget(self.lineEdit_oscCH, 7, 2, 1, 1)
        self.label_wsize = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        self.label_wsize.setFont(font)
        self.label_wsize.setObjectName("label_wsize")
        self.params.addWidget(self.label_wsize, 4, 0, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(40, 10, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.params.addItem(spacerItem1, 5, 0, 1, 2)
        self.label_oscIP = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        self.label_oscIP.setFont(font)
        self.label_oscIP.setObjectName("label_oscIP")
        self.params.addWidget(self.label_oscIP, 6, 0, 1, 1)
        self.gridLayout.addLayout(self.params, 1, 1, 1, 1)
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.btn_start = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        self.btn_start.setFont(font)
        self.btn_start.setObjectName("btn_start")
        self.gridLayout_3.addWidget(self.btn_start, 1, 0, 1, 1)
        self.checkBox_osc = QtWidgets.QCheckBox(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        self.checkBox_osc.setFont(font)
        self.checkBox_osc.setTristate(False)
        self.checkBox_osc.setObjectName("checkBox_osc")
        self.gridLayout_3.addWidget(self.checkBox_osc, 0, 0, 1, 1)
        self.btn_stop = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        self.btn_stop.setFont(font)
        self.btn_stop.setObjectName("btn_stop")
        self.gridLayout_3.addWidget(self.btn_stop, 1, 1, 1, 1)
        self.gridLayout.addLayout(self.gridLayout_3, 4, 1, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 2, 0, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 0, 1, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName("menubar")
        self.menusupport = QtWidgets.QMenu(self.menubar)
        self.menusupport.setObjectName("menusupport")
        self.menufunctions = QtWidgets.QMenu(self.menubar)
        self.menufunctions.setObjectName("menufunctions")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actiongenerate_random_data = QtWidgets.QAction(MainWindow)
        self.actiongenerate_random_data.setObjectName("actiongenerate_random_data")
        self.actionplay_a_sample_recording_as_test_data = QtWidgets.QAction(MainWindow)
        self.actionplay_a_sample_recording_as_test_data.setObjectName("actionplay_a_sample_recording_as_test_data")
        self.actionbridge = QtWidgets.QAction(MainWindow)
        self.actionbridge.setObjectName("actionbridge")
        self.menusupport.addSeparator()
        self.menusupport.addAction(self.actiongenerate_random_data)
        self.menusupport.addAction(self.actionplay_a_sample_recording_as_test_data)
        self.menufunctions.addAction(self.actionbridge)
        self.menubar.addAction(self.menusupport.menuAction())
        self.menubar.addAction(self.menufunctions.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "RhythmOfRelating"))
        MainWindow.setToolTip(_translate("MainWindow", "helphelphelp"))
        self.btn_loadStreams.setToolTip(_translate("MainWindow", "detect LSL streams for analysis. Streams should be displayed on the table above."))
        self.btn_loadStreams.setText(_translate("MainWindow", "1. load LSL streams"))
        self.label_3.setText(_translate("MainWindow", "Frequency bands for analysis"))
        self.label.setText(_translate("MainWindow", "Console"))
        self.comboBox_chn.setItemText(0, _translate("MainWindow", "one-to-one (e.g. Fp1 is only correlated with Fp1 and so on.)"))
        self.comboBox_chn.setItemText(1, _translate("MainWindow", "all-to-all (e.g. each channel is correlated with all the other available channels in the selection.)"))
        self.label_chn.setText(_translate("MainWindow", "Connectivity type"))
        self.comboBox_device.setItemText(0, _translate("MainWindow", "MUSE"))
        self.comboBox_device.setItemText(1, _translate("MainWindow", "EMOTIV EPOC"))
        self.comboBox_device.setItemText(2, _translate("MainWindow", "EMOTIV EPOC+"))
        self.comboBox_device.setItemText(3, _translate("MainWindow", "Enobio"))
        self.label_input.setText(_translate("MainWindow", "Input type"))
        self.label_conn.setText(_translate("MainWindow", "Connectivity metric"))
        self.lineEdit_wsize.setText(_translate("MainWindow", "3"))
        self.label_device.setText(_translate("MainWindow", "Device"))
        self.comboBox_conn.setItemText(0, _translate("MainWindow", "Coherence"))
        self.comboBox_conn.setItemText(1, _translate("MainWindow", "Imaginary Coherence"))
        self.comboBox_conn.setItemText(2, _translate("MainWindow", "Envelope Correlation"))
        self.comboBox_conn.setItemText(3, _translate("MainWindow", "Power Correlation"))
        self.comboBox_conn.setItemText(4, _translate("MainWindow", "PLV"))
        self.comboBox_conn.setItemText(5, _translate("MainWindow", "CCorr"))
        self.label_oscPort.setText(_translate("MainWindow", "OSC port (optional) "))
        self.comboBox_input.setItemText(0, _translate("MainWindow", "EEG"))
        self.lineEdit_oscIP.setText(_translate("MainWindow", "10.0.0.24"))
        self.lineEdit_oscCH.setText(_translate("MainWindow", "9000"))
        self.label_wsize.setText(_translate("MainWindow", "Window size (seconds)"))
        self.label_oscIP.setText(_translate("MainWindow", "OSC IP address (optional)"))
        self.btn_start.setText(_translate("MainWindow", "2. start"))
        self.checkBox_osc.setText(_translate("MainWindow", "sending through OSC"))
        self.btn_stop.setText(_translate("MainWindow", "stop"))
        self.label_4.setText(_translate("MainWindow", "Input data streams"))
        self.label_5.setText(_translate("MainWindow", "Parameters"))
        self.menusupport.setTitle(_translate("MainWindow", "support"))
        self.menufunctions.setTitle(_translate("MainWindow", "functions"))
        self.actiongenerate_random_data.setText(_translate("MainWindow", "play a random signal for testing"))
        self.actionplay_a_sample_recording_as_test_data.setText(_translate("MainWindow", "play a sample recording for testing"))
        self.actionbridge.setText(_translate("MainWindow", "bridge"))


    def setup(self):
        # log_path = path.join(path.dirname(path.abspath(__file__)), 'log')
        # log_path = path.join(log_path, 'logging.conf')
        # logging.config.fileConfig(log_path)
        logging.config.fileConfig(resource_path('log/logging.conf'))
        # initialization
        self.conn_params = []
        self.analysis_running = False
        self.btn_stop.setEnabled(False)
        self.checkBox_osc.setChecked(True)

        # table content
        self.infoTable.setHorizontalHeaderLabels(['Stream ID', "channel count", 'sampling rate', 'theta', 'alpha', 'beta'])
        self.freqTable.setHorizontalHeaderLabels(['Freq. Band', "Min. Freq.", 'Max. Freq.', 'weight'])
        # fill freTable with default options
        self.freqTable.setRowCount(4)
        default_freqTable = [['theta', '4', '8', '1'], ['alpha', '8', '12', '1'], ['beta', '12', '30', '1']]
        for n_row in range(3):
            for n_col in range(4):
                self.freqTable.setItem(n_row, n_col, QtWidgets.QTableWidgetItem(default_freqTable[n_row][n_col]))
        # actions
        self.btn_loadStreams.clicked.connect(self.fun_load_streams)
        self.btn_start.clicked.connect(self.fun_analyze)
        self.btn_stop.clicked.connect(self.fun_stop)
        self.checkBox_osc.toggled.connect(self.lineEdit_oscIP.setEnabled)
        self.checkBox_osc.toggled.connect(self.lineEdit_oscCH.setEnabled)
        self.actiongenerate_random_data.triggered.connect(self._run_generate_random_samples)

    def fun_unlock(self):
        """
        button unlock
        """
        if self.analysis_running:  # stop analysis if running
            self.fun_stop()

        # reset buttons
        self.btn_loadStreams.setEnabled(True)
        # unlock tables
        self.infoTable.setEditTriggers(QtWidgets.QAbstractItemView.AllEditTriggers)
        self.freqTable.setEditTriggers(QtWidgets.QAbstractItemView.AllEditTriggers)
        # set label text
        self.param_check.append("Parameters are editable now.\n")

    def _read_osc(self):
        """
        set up osc port
        """
        IP = None
        port = None
        # reading params
        if self.checkBox_osc.isChecked():
            IP = self.lineEdit_oscIP.text()
            port = self.lineEdit_oscCH.text()
        return IP, port

    def _run_generate_random_samples(self):
        # generate_random_samples()
        filepath = resource_path('support/fun_generate_random_samples.py')
        QProcess.startDetached(filepath)
    #TODO
    def fun_load_streams(self):
        """
        button 2. Scan for LSL streams
        """
        # determine columns based on freq bands
        cols = ['Stream ID', "channel count", 'sampling rate']
        for i in range(self.freqTable.rowCount()):
            if self.freqTable.item(i,0):
                cols.append(self.freqTable.item(i,0).text()+' channels')

        self.infoTable.setColumnCount(len(cols))
        self.infoTable.setHorizontalHeaderLabels(cols)

        # discover streams
        self.infoTable.setRowCount(0)
        self.discovery = Discovery(
            discard_timestamps=True,
            correct_timestamps=False
        )
        self.discovery.start()
        time.sleep(3)
        streams = list(self.discovery.streams_by_uid.keys())

        # update the table
        self.infoTable.setRowCount(len(streams))
        for n_row, id in enumerate(streams):
            self.infoTable.insertRow(n_row)
            # display stream ID
            item = QtWidgets.QTableWidgetItem(str(id))
            item.setFlags(QtCore.Qt.ItemIsEnabled)
            item.setBackground(QtGui.QColor(220, 220, 220))
            self.infoTable.setItem(n_row, 0, item)
            # display channel count
            item = QtWidgets.QTableWidgetItem(str(self.discovery.channel_count))
            item.setFlags(QtCore.Qt.ItemIsEnabled)
            item.setBackground(QtGui.QColor(220, 220, 220))
            self.infoTable.setItem(n_row, 1, item)
            # display sample rate
            item = QtWidgets.QTableWidgetItem(str(self.discovery.streams_by_uid[id].sample_rate))
            item.setFlags(QtCore.Qt.ItemIsEnabled)
            item.setBackground(QtGui.QColor(220, 220, 220))
            self.infoTable.setItem(n_row, 2, item)
            # display chosen channels (editable)
            for n_freq in range(len(cols)-3):
                if n_row == 0:  # only making the first line editable, because every stream is using the same channel selection
                    item = QtWidgets.QTableWidgetItem('1:%s' % self.discovery.channel_count)
                else:
                    item = QtWidgets.QTableWidgetItem('Same as above')
                    item.setFlags(QtCore.Qt.ItemIsEnabled)
                    item.setBackground(QtGui.QColor(220, 220, 220))
                self.infoTable.setItem(n_row, n_freq + 3, item)

    def fun_retrieve_params(self):
        freqloaded = True
        infoloaded = True
        # read freq table
        freq_names = []
        ranges = []
        weights = []
        for i in range(self.freqTable.rowCount()):
            if self.freqTable.item(i,0):
                try:
                    assert int(self.freqTable.item(i,1).text()) < int(self.freqTable.item(i,2).text())
                    freq_names.append(self.freqTable.item(i, 0).text())
                    ranges.append((int(self.freqTable.item(i, 1).text()), int(self.freqTable.item(i, 2).text())))
                    weights.append(float(self.freqTable.item(i, 3).text()))
                except Exception as e:
                    self.param_check.append("Frequency table input type error.\n")
                    freqloaded = False
                    break

        # read info table
        n_freq = len(freq_names)
        chn_list = []
        for j in range(n_freq):
            if self.infoTable.item(0, 3+j):
                try:
                    chns = self._str2list(self.infoTable.item(0, 3+j).text())
                    chn_list.append(chns)
                except:
                    self.param_check.append("Selected channel format error.\n")
                    infoloaded = False
                    break

        # integrate params
        try:
            freqParams = dict(zip(freq_names, ranges))
            chnParams = dict(zip(freq_names, chn_list))
            weightParams = dict(zip(freq_names, weights))
        except:
            self.param_check.append("Parameter format error.\n")
            infoloaded = False

        # if no error message, continue to lock buttons and read params into analysis
        if freqloaded and infoloaded:
            self.param_check.append("Successfully loaded parameters.\n")
            self.conn_params = [freqParams, chnParams, weightParams]
            # grey out loading buttons
            self.btn_loadStreams.setEnabled(False)
            # lock tables
            self.infoTable.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
            self.freqTable.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

    def _read_input(self):
        device = self.comboBox_device.currentText()
        chn_type = self.comboBox_chn.currentText()
        mode = self.comboBox_conn.currentText()
        window_size = self.lineEdit_wsize.text()
        # window_lag = self.lineEdit_wlag.text()
        window_lag = None
        # deprecated (normalization is implemented in bridge)
        norm_min = 0
        norm_max = 1

        return device, chn_type, mode, window_size, window_lag, norm_min, norm_max

    def fun_analyze(self):
        device, chn_type, mode, window_size, window_lag, norm_min, norm_max = self._read_input()
        IP, port = self._read_osc()
        # making sure first button was pressed
        if not hasattr(self, 'discovery'):
            self.param_check.append('Please make sure EEG streams have been loaded first.\n')
        # making sure input is not empty
        elif len(list(self.discovery.streams_by_uid.keys()))<1:
            self.param_check.append('Please make sure EEG streams have been loaded first.\n')
        else:
            self.fun_retrieve_params()
            # proceed only if load stream button is locked
            if not self.btn_loadStreams.isEnabled():
                try:
                    # starting analysis
                    self.analysis = Analysis(discovery=self.discovery, mode=mode, chn_type=chn_type,
                                             corr_params=self.conn_params, OSC_params=[IP, port],
                                             window_params=[float(window_size), None],  # baseline lag not implemented
                                             norm_params=[float(norm_min), float(norm_max)])
                    self.analysis.start()
                    n_freq, n_ppl = len(self.conn_params[0]), self._factorial(len(list(self.discovery.streams_by_uid.keys())),2)
                    self.param_check.append("Sending connectivity values for %s frequency bands and %s pairs...\n" % (n_freq,n_ppl))
                    # update state variable and buttons
                    self.analysis_running = True
                    self.btn_stop.setEnabled(True)
                    self._enableEdit(False)
                except Exception as e:
                    self.param_check.append('Error with analysis. The Error message is:'\
                                             +'\n'+str(e)+'\n')

    def _factorial(self, n, k):
        # n choose k
        return int(factorial(n) / factorial(k) / factorial(n - k))

    def _enableEdit(self, bool):
        self.btn_start.setEnabled(bool)
        self.comboBox_conn.setEnabled(bool)
        self.comboBox_device.setEnabled(bool)
        self.comboBox_chn.setEnabled(bool)
        self.comboBox_input.setEnabled(bool)
        self.lineEdit_wsize.setEnabled(bool)
        self.lineEdit_oscCH.setEnabled(bool)
        self.lineEdit_oscIP.setEnabled(bool)

    def fun_stop(self):
        # stop analysis
        self.analysis.stop()
        self.analysis_running = False
        self.discovery.stop()
        self.btn_stop.setEnabled(False)
        self.btn_start.setEnabled(True)
        self.btn_loadStreams.setEnabled(True)
        # set edit area editable
        self._enableEdit(True)
        self.fun_unlock()
        self.param_check.append("Analysis stopped.\n")

    def _str2list(self, text):
        """
        convert an input string to a python list
        e.g. '6:10,1:3,16,31'  --> '5:10,0:3,15,30' --> [0, 1, 2, 5, 6, 7, 8, 9, 15, 30]
        """
        ind = []
        for item in text.replace(' ','').split(','):
            if ':' in item:
                ind.extend(np.arange(int(item.split(':')[0])-1, int(item.split(':')[1]), 1))
            else:
                ind.extend([int(item)-1])
        assert max(ind) < int(self.infoTable.item(0,1).text())  # index cannot be larger than channel count
        ind = list(dict.fromkeys(ind))  # remove duplicates
        ind.sort()  # sort
        return ind

if __name__ == "__main__":
    import sys
    # Back up the reference to the exceptionhook
    # sys._excepthook = sys.excepthook
    # def my_exception_hook(exctype, value, traceback):
    #     # Print the error and traceback
    #     print(exctype, value, traceback)
    #     # Call the normal Exception hook after
    #     sys._excepthook(exctype, value, traceback)
    #     sys.exit(1)
    # # Set the exception hook to our wrapping function
    # sys.excepthook = my_exception_hook
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    ui.setup()
    MainWindow.show()
    sys.exit(app.exec_())

