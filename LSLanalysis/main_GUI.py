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
from analysis import OutputAnalysis
import numpy as np
import logging.config
import logging


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(855, 579)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(855, 579))
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
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.infoTable = QtWidgets.QTableWidget(self.centralwidget)
        self.infoTable.setMinimumSize(QtCore.QSize(355, 192))
        self.infoTable.setCornerButtonEnabled(True)
        self.infoTable.setRowCount(0)
        self.infoTable.setColumnCount(4)
        self.infoTable.setObjectName("infoTable")
        self.gridLayout_2.addWidget(self.infoTable, 3, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem, 1, 1, 2, 1)
        self.btn_loadBands = QtWidgets.QPushButton(self.centralwidget)
        self.btn_loadBands.setObjectName("btn_loadBands")
        self.gridLayout_2.addWidget(self.btn_loadBands, 2, 0, 1, 1)
        self.btn_loadStreams = QtWidgets.QPushButton(self.centralwidget)
        self.btn_loadStreams.setObjectName("btn_loadStreams")
        self.gridLayout_2.addWidget(self.btn_loadStreams, 5, 0, 1, 1)
        self.btn_fixParams = QtWidgets.QPushButton(self.centralwidget)
        self.btn_fixParams.setObjectName("btn_fixParams")
        self.gridLayout_2.addWidget(self.btn_fixParams, 8, 0, 1, 1)
        self.btn_unlock = QtWidgets.QPushButton(self.centralwidget)
        self.btn_unlock.setObjectName("btn_unlock")
        self.gridLayout_2.addWidget(self.btn_unlock, 9, 0, 1, 1)
        self.freqTable = QtWidgets.QTableWidget(self.centralwidget)
        self.freqTable.setMinimumSize(QtCore.QSize(355, 193))
        self.freqTable.setColumnCount(4)
        self.freqTable.setObjectName("freqTable")
        self.freqTable.setRowCount(0)
        self.gridLayout_2.addWidget(self.freqTable, 1, 0, 1, 1)
        self.params = QtWidgets.QGridLayout()
        self.params.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.params.setContentsMargins(0, -1, -1, -1)
        self.params.setSpacing(2)
        self.params.setObjectName("params")
        self.comboBox_conn = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_conn.setObjectName("comboBox_conn")
        self.comboBox_conn.addItem("")
        self.comboBox_conn.addItem("")
        self.comboBox_conn.addItem("")
        self.comboBox_conn.addItem("")
        self.comboBox_conn.addItem("")
        self.comboBox_conn.addItem("")
        self.params.addWidget(self.comboBox_conn, 3, 2, 1, 1)
        self.comboBox_input = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_input.setObjectName("comboBox_input")
        self.comboBox_input.addItem("")
        self.params.addWidget(self.comboBox_input, 1, 2, 1, 1)
        self.label_device = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(36)
        self.label_device.setFont(font)
        self.label_device.setObjectName("label_device")
        self.params.addWidget(self.label_device, 0, 0, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.params.addItem(spacerItem1, 7, 0, 1, 1)
        self.checkBox_wlag = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_wlag.setEnabled(False)
        self.checkBox_wlag.setObjectName("checkBox_wlag")
        self.params.addWidget(self.checkBox_wlag, 5, 2, 1, 1)
        self.label_oscIP = QtWidgets.QLabel(self.centralwidget)
        self.label_oscIP.setObjectName("label_oscIP")
        self.params.addWidget(self.label_oscIP, 8, 0, 1, 1)
        self.comboBox_chn = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_chn.setObjectName("comboBox_chn")
        self.comboBox_chn.addItem("")
        self.comboBox_chn.addItem("")
        self.params.addWidget(self.comboBox_chn, 2, 2, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lineEdit_wsize = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_wsize.setObjectName("lineEdit_wsize")
        self.horizontalLayout.addWidget(self.lineEdit_wsize)
        self.label_wlag = QtWidgets.QLabel(self.centralwidget)
        self.label_wlag.setObjectName("label_wlag")
        self.horizontalLayout.addWidget(self.label_wlag)
        self.lineEdit_wlag = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_wlag.setEnabled(False)
        self.lineEdit_wlag.setText("")
        self.lineEdit_wlag.setObjectName("lineEdit_wlag")
        self.horizontalLayout.addWidget(self.lineEdit_wlag)
        self.params.addLayout(self.horizontalLayout, 4, 2, 1, 1)
        self.lineEdit_oscCH = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_oscCH.setObjectName("lineEdit_oscCH")
        self.params.addWidget(self.lineEdit_oscCH, 9, 2, 1, 1)
        self.lineEdit_oscIP = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_oscIP.setStatusTip("")
        self.lineEdit_oscIP.setObjectName("lineEdit_oscIP")
        self.params.addWidget(self.lineEdit_oscIP, 8, 2, 1, 1)
        self.comboBox_device = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_device.setObjectName("comboBox_device")
        self.comboBox_device.addItem("")
        self.comboBox_device.addItem("")
        self.comboBox_device.addItem("")
        self.comboBox_device.addItem("")
        self.params.addWidget(self.comboBox_device, 0, 2, 1, 1)
        self.label_conn = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(36)
        self.label_conn.setFont(font)
        self.label_conn.setObjectName("label_conn")
        self.params.addWidget(self.label_conn, 3, 0, 1, 1)
        self.label_oscPort = QtWidgets.QLabel(self.centralwidget)
        self.label_oscPort.setObjectName("label_oscPort")
        self.params.addWidget(self.label_oscPort, 9, 0, 1, 1)
        self.label_wsize = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(36)
        self.label_wsize.setFont(font)
        self.label_wsize.setObjectName("label_wsize")
        self.params.addWidget(self.label_wsize, 4, 0, 1, 1)
        self.label_input = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        self.label_input.setFont(font)
        self.label_input.setObjectName("label_input")
        self.params.addWidget(self.label_input, 1, 0, 1, 1)
        self.label_chn = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        self.label_chn.setFont(font)
        self.label_chn.setObjectName("label_chn")
        self.params.addWidget(self.label_chn, 2, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setObjectName("label_2")
        self.params.addWidget(self.label_2, 6, 0, 1, 1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_normMin = QtWidgets.QLabel(self.centralwidget)
        self.label_normMin.setObjectName("label_normMin")
        self.horizontalLayout_2.addWidget(self.label_normMin)
        self.lineEdit_normMin = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_normMin.setObjectName("lineEdit_normMin")
        self.horizontalLayout_2.addWidget(self.lineEdit_normMin)
        self.label_normMax = QtWidgets.QLabel(self.centralwidget)
        self.label_normMax.setObjectName("label_normMax")
        self.horizontalLayout_2.addWidget(self.label_normMax)
        self.lineEdit_normMax = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_normMax.setObjectName("lineEdit_normMax")
        self.horizontalLayout_2.addWidget(self.lineEdit_normMax)
        self.params.addLayout(self.horizontalLayout_2, 6, 2, 1, 1)
        self.gridLayout_2.addLayout(self.params, 2, 2, 2, 1)
        self.param_check = QtWidgets.QLabel(self.centralwidget)
        self.param_check.setText("")
        self.param_check.setObjectName("param_check")
        self.gridLayout_2.addWidget(self.param_check, 7, 0, 1, 1)
        self.label = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(36)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 3)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.checkBox_osc = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_osc.setTristate(False)
        self.checkBox_osc.setObjectName("checkBox_osc")
        self.gridLayout.addWidget(self.checkBox_osc, 1, 0, 1, 1)
        self.btn_stop = QtWidgets.QPushButton(self.centralwidget)
        self.btn_stop.setObjectName("btn_stop")
        self.gridLayout.addWidget(self.btn_stop, 2, 1, 1, 1)
        self.btn_start = QtWidgets.QPushButton(self.centralwidget)
        self.btn_start.setObjectName("btn_start")
        self.gridLayout.addWidget(self.btn_start, 2, 0, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 6, 2, 3, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 855, 18))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "RhythmOfRelating"))
        self.btn_loadBands.setText(_translate("MainWindow", "1. set frequency bands"))
        self.btn_loadStreams.setText(_translate("MainWindow", "2. load LSL streams"))
        self.btn_fixParams.setText(_translate("MainWindow", "3. Lock parameters"))
        self.btn_unlock.setText(_translate("MainWindow", "unlock parameters"))
        self.comboBox_conn.setItemText(0, _translate("MainWindow", "Coherence"))
        self.comboBox_conn.setItemText(1, _translate("MainWindow", "Imaginary Coherence"))
        self.comboBox_conn.setItemText(2, _translate("MainWindow", "Envelope Correlation"))
        self.comboBox_conn.setItemText(3, _translate("MainWindow", "Power Correlation"))
        self.comboBox_conn.setItemText(4, _translate("MainWindow", "PLV"))
        self.comboBox_conn.setItemText(5, _translate("MainWindow", "CCorr"))
        self.comboBox_input.setItemText(0, _translate("MainWindow", "EEG"))
        self.label_device.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:12pt;\">Device</span></p></body></html>"))
        self.checkBox_wlag.setText(_translate("MainWindow", "sending relative synchrony values based on *window lag* seconds ago."))
        self.label_oscIP.setText(_translate("MainWindow", "OSC IP address (optional)"))
        self.comboBox_chn.setItemText(0, _translate("MainWindow", "one-to-one (e.g. Fp1 is only correlated with Fp1 and so on.)"))
        self.comboBox_chn.setItemText(1, _translate("MainWindow", "all-to-all (e.g. each channel is correlated with all the other available channels in the selection.)"))
        self.lineEdit_wsize.setText(_translate("MainWindow", "3"))
        self.label_wlag.setText(_translate("MainWindow", "window lag (optional)"))
        self.lineEdit_oscCH.setText(_translate("MainWindow", "9000"))
        self.lineEdit_oscIP.setText(_translate("MainWindow", "10.0.0.24"))
        self.comboBox_device.setItemText(0, _translate("MainWindow", "MUSE"))
        self.comboBox_device.setItemText(1, _translate("MainWindow", "EMOTIV EPOC"))
        self.comboBox_device.setItemText(2, _translate("MainWindow", "EMOTIV EPOC+"))
        self.comboBox_device.setItemText(3, _translate("MainWindow", "Enobio"))
        self.label_conn.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:12pt;\">Connectivity metric   </span></p></body></html>"))
        self.label_oscPort.setText(_translate("MainWindow", "OSC port (optional) "))
        self.label_wsize.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:12pt;\">Window size </span></p></body></html>"))
        self.label_input.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:12pt;\">Input type</span></p></body></html>"))
        self.label_chn.setText(_translate("MainWindow", "Connectivity type"))
        self.label_2.setText(_translate("MainWindow", "Normalization (MinMax)"))
        self.label_normMin.setText(_translate("MainWindow", "Min."))
        self.lineEdit_normMin.setText(_translate("MainWindow", "0"))
        self.label_normMax.setText(_translate("MainWindow", "Max."))
        self.lineEdit_normMax.setText(_translate("MainWindow", "1"))
        self.label.setText(_translate("MainWindow", "Welcome, specify your values and press on \'Start\'"))
        self.checkBox_osc.setText(_translate("MainWindow", "sending through OSC"))
        self.btn_stop.setText(_translate("MainWindow", "stop"))
        self.btn_start.setText(_translate("MainWindow", "4. start"))

    def setup(self):
        logging.config.fileConfig('logging.conf')

        # initialization
        self.conn_params = []
        self.analysis_running = False
        self.btn_unlock.setEnabled(False)
        self.btn_stop.setEnabled(False)
        self.checkBox_osc.setChecked(True)

        # table content
        self.infoTable.setHorizontalHeaderLabels(['Stream ID', "channel count", 'sampling rate'])
        self.freqTable.setHorizontalHeaderLabels(['Freq. Band', "Min. Freq.", 'Max. Freq.', 'weight'])
        # fill freTable with default options
        self.freqTable.setRowCount(4)
        default_freqTable = [['theta', '4', '8', '1'], ['alpha', '8', '12', '1'], ['beta', '12', '30', '1']]
        for n_row in range(3):
            for n_col in range(4):
                self.freqTable.setItem(n_row, n_col, QtWidgets.QTableWidgetItem(default_freqTable[n_row][n_col]))
        # actions
        self.btn_loadStreams.clicked.connect(self.fun_load_streams)
        self.btn_fixParams.clicked.connect(self.fun_retrieve_params)
        self.btn_unlock.clicked.connect(self.fun_unlock)
        self.btn_start.clicked.connect(self.fun_analyze)
        self.btn_stop.clicked.connect(self.fun_stop)
        self.checkBox_osc.toggled.connect(self.lineEdit_oscIP.setEnabled)
        self.checkBox_osc.toggled.connect(self.lineEdit_oscCH.setEnabled)
        self.checkBox_wlag.toggled.connect(self.lineEdit_wlag.setEnabled)

    def fun_unlock(self):
        """
        button unlock
        """
        if self.analysis_running:  # stop analysis if running
            self.fun_stop()

        # reset buttons
        self.btn_unlock.setEnabled(False)
        self.btn_fixParams.setEnabled(True)
        self.btn_loadStreams.setEnabled(True)
        self.btn_loadBands.setEnabled(True)
        # unlock tables
        self.infoTable.setEditTriggers(QtWidgets.QAbstractItemView.AllEditTriggers)
        self.freqTable.setEditTriggers(QtWidgets.QAbstractItemView.AllEditTriggers)
        # set label text
        self.param_check.setText("Unlocked. Parameters are editable now.")

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
                    self.param_check.setText("Frequency table input type error.")
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
                    self.param_check.setText("Selected channel format error.")
                    infoloaded = False
                    break

        # integrate params
        try:
            freqParams = dict(zip(freq_names, ranges))
            chnParams = dict(zip(freq_names, chn_list))
            weightParams = dict(zip(freq_names, weights))
        except:
            self.param_check.setText('Format error')
            infoloaded = False

        # if no error message, continue to lock buttons and read params into analysis
        if freqloaded and infoloaded:
            self.param_check.setText("successfully loaded parameters.")
            self.conn_params = [freqParams, chnParams, weightParams]
            # grey out loading buttons
            self.btn_loadBands.setEnabled(False)
            self.btn_loadStreams.setEnabled(False)
            self.btn_fixParams.setEnabled(False)
            self.btn_unlock.setEnabled(True)
            # lock tables
            self.infoTable.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
            self.freqTable.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

    def _read_input(self):
        device = self.comboBox_device.currentText()
        chn_type = self.comboBox_chn.currentText()
        mode = self.comboBox_conn.currentText()
        window_size = self.lineEdit_wsize.text()
        window_lag = self.lineEdit_wlag.text()
        norm_min = self.lineEdit_normMin.text()
        norm_max = self.lineEdit_normMax.text()

        return device, chn_type, mode, window_size, window_lag, norm_min, norm_max

    def fun_analyze(self):
        if self.btn_fixParams.isEnabled():
            self.param_check.setText("please fix params before starting")
        else:
            device, chn_type, mode, window_size, window_lag, norm_min, norm_max = self._read_input()
            IP, port = self._read_osc()
            try:
                # starting analysis
                self.analysis = Analysis(discovery=self.discovery, mode=mode, chn_type=chn_type,
                                         corr_params=self.conn_params, OSC_params=[IP, port],
                                         window_params=[float(window_size), None],  # baseline lag not implemented
                                         norm_params=[float(norm_min), float(norm_max)])
                self.analysis.start()
                # starting output analysis
                # self.outputAnalysis = OutputAnalysis(self.analysis)
                # self.outputAnalysis.start()
                # update state variable and buttons
                self.analysis_running = True
                self.btn_stop.setEnabled(True)
                self._enableEdit(False)

            except Exception as e:
                self.param_check.setText("Error message: ", str(e))

    def _enableEdit(self, bool):
        self.btn_start.setEnabled(bool)
        self.comboBox_conn.setEnabled(bool)
        self.comboBox_device.setEnabled(bool)
        self.comboBox_chn.setEnabled(bool)
        self.comboBox_input.setEnabled(bool)
        self.lineEdit_wsize.setEnabled(bool)
        self.lineEdit_oscCH.setEnabled(bool)
        self.lineEdit_oscIP.setEnabled(bool)
        self.lineEdit_normMin.setEnabled(bool)
        self.lineEdit_normMax.setEnabled(bool)


    def fun_stop(self):
        # stop analysis
        self.analysis.stop()
        self.analysis_running = False
        # self.outputAnalysis.stop()
        self.btn_stop.setEnabled(False)
        self.btn_start.setEnabled(True)
        # set edit area editable
        self._enableEdit(True)

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

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    ui.setup()
    MainWindow.show()
    sys.exit(app.exec_())
