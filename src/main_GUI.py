# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets
from acquisition import Discovery
from analysis import Analysis
from support import SampleGeneration, load_xdf
import time
import numpy as np
import logging.config
import logging
import os, traceback
from math import factorial
import sys
import os.path as path
def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)
LOGO_PATH = resource_path('./headMutualBrainwavesLabWhite.ico')

class Ui_MainWindow(object):
    """
    Class for setting up the GUI
    """
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1004, 591)
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
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3)
        self.freqTable = QtWidgets.QTableWidget(self.centralwidget)
        self.freqTable.setMinimumSize(QtCore.QSize(355, 193))
        self.freqTable.setColumnCount(4)
        self.freqTable.setObjectName("freqTable")
        self.freqTable.setRowCount(0)
        self.verticalLayout.addWidget(self.freqTable)
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.verticalLayout.addWidget(self.label_4)
        self.infoTable = QtWidgets.QTableWidget(self.centralwidget)
        self.infoTable.setMinimumSize(QtCore.QSize(355, 192))
        self.infoTable.setCornerButtonEnabled(True)
        self.infoTable.setRowCount(0)
        self.infoTable.setColumnCount(4)
        self.infoTable.setObjectName("infoTable")
        self.verticalLayout.addWidget(self.infoTable)
        self.btn_loadStreams = QtWidgets.QPushButton(self.centralwidget)
        self.btn_loadStreams.setToolTipDuration(7000)
        self.btn_loadStreams.setObjectName("btn_loadStreams")
        self.verticalLayout.addWidget(self.btn_loadStreams)
        self.horizontalLayout_3.addLayout(self.verticalLayout)
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.horizontalLayout_3.addWidget(self.line)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.verticalLayout_2.addWidget(self.label_5)
        self.params = QtWidgets.QGridLayout()
        self.params.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.params.setContentsMargins(0, -1, -1, -1)
        self.params.setSpacing(2)
        self.params.setObjectName("params")
        self.label_oscPort = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        self.label_oscPort.setFont(font)
        self.label_oscPort.setObjectName("label_oscPort")
        self.params.addWidget(self.label_oscPort, 9, 0, 1, 1)
        self.label_input = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(8)
        self.label_input.setFont(font)
        self.label_input.setObjectName("label_input")
        self.params.addWidget(self.label_input, 1, 0, 1, 1)
        self.lineEdit_oscIP = QtWidgets.QLineEdit(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        self.lineEdit_oscIP.setFont(font)
        self.lineEdit_oscIP.setStatusTip("")
        self.lineEdit_oscIP.setObjectName("lineEdit_oscIP")
        self.params.addWidget(self.lineEdit_oscIP, 8, 2, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.params.addWidget(self.label_7, 4, 0, 1, 1)
        self.comboBox_input = QtWidgets.QComboBox(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        self.comboBox_input.setFont(font)
        self.comboBox_input.setObjectName("comboBox_input")
        self.comboBox_input.addItem("")
        self.params.addWidget(self.comboBox_input, 1, 2, 1, 1)
        self.lineEdit_oscCH = QtWidgets.QLineEdit(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        self.lineEdit_oscCH.setFont(font)
        self.lineEdit_oscCH.setObjectName("lineEdit_oscCH")
        self.params.addWidget(self.lineEdit_oscCH, 9, 2, 1, 1)
        self.comboBox_chn = QtWidgets.QComboBox(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        self.comboBox_chn.setFont(font)
        self.comboBox_chn.setObjectName("comboBox_chn")
        self.comboBox_chn.addItem("")
        self.comboBox_chn.addItem("")
        self.params.addWidget(self.comboBox_chn, 2, 2, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.comboBox_wsize = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_wsize.setObjectName("comboBox_wsize")
        self.comboBox_wsize.addItem("")
        self.comboBox_wsize.addItem("")
        self.comboBox_wsize.addItem("")
        self.comboBox_wsize.addItem("")
        self.comboBox_wsize.addItem("")
        self.comboBox_wsize.addItem("")
        self.horizontalLayout.addWidget(self.comboBox_wsize)
        self.params.addLayout(self.horizontalLayout, 4, 2, 1, 1)
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
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.params.addWidget(self.label_6, 3, 0, 1, 1)
        self.line_2 = QtWidgets.QFrame(self.centralwidget)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.params.addWidget(self.line_2, 5, 0, 1, 1)
        self.label_chn = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(8)
        self.label_chn.setFont(font)
        self.label_chn.setObjectName("label_chn")
        self.params.addWidget(self.label_chn, 2, 0, 1, 1)
        self.checkBox_osc = QtWidgets.QCheckBox(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        self.checkBox_osc.setFont(font)
        self.checkBox_osc.setTristate(False)
        self.checkBox_osc.setObjectName("checkBox_osc")
        self.params.addWidget(self.checkBox_osc, 7, 0, 1, 1)
        self.label_oscIP = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        self.label_oscIP.setFont(font)
        self.label_oscIP.setObjectName("label_oscIP")
        self.params.addWidget(self.label_oscIP, 8, 0, 1, 1)
        self.verticalLayout_2.addLayout(self.params)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout_2.addItem(spacerItem)
        self.label_normparam = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_normparam.setFont(font)
        self.label_normparam.setObjectName("label_normparam")
        self.verticalLayout_2.addWidget(self.label_normparam)
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_manMin = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        self.label_manMin.setFont(font)
        self.label_manMin.setObjectName("label_manMin")
        self.horizontalLayout_2.addWidget(self.label_manMin)
        self.lineEdit_manMin = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_manMin.setObjectName("lineEdit_manMin")
        self.horizontalLayout_2.addWidget(self.lineEdit_manMin)
        self.label_manMax = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        self.label_manMax.setFont(font)
        self.label_manMax.setObjectName("label_manMax")
        self.horizontalLayout_2.addWidget(self.label_manMax)
        self.lineEdit_manMax = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_manMax.setObjectName("lineEdit_manMax")
        self.horizontalLayout_2.addWidget(self.lineEdit_manMax)
        self.gridLayout_2.addLayout(self.horizontalLayout_2, 1, 1, 1, 1)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.pushButton_openfile = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        self.pushButton_openfile.setFont(font)
        self.pushButton_openfile.setObjectName("pushButton_openfile")
        self.horizontalLayout_4.addWidget(self.pushButton_openfile)
        self.lineEdit_filename = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_filename.setObjectName("lineEdit_filename")
        self.horizontalLayout_4.addWidget(self.lineEdit_filename)
        self.pushButton_computefile = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        self.pushButton_computefile.setFont(font)
        self.pushButton_computefile.setObjectName("pushButton_computefile")
        self.horizontalLayout_4.addWidget(self.pushButton_computefile)
        self.label_fileMin = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setBold(True)
        font.setWeight(75)
        self.label_fileMin.setFont(font)
        self.label_fileMin.setObjectName("label_fileMin")
        self.horizontalLayout_4.addWidget(self.label_fileMin)
        self.label_fileMindis = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        self.label_fileMindis.setFont(font)
        self.label_fileMindis.setObjectName("label_fileMindis")
        self.horizontalLayout_4.addWidget(self.label_fileMindis)
        self.label_fileMax = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setBold(True)
        font.setWeight(75)
        self.label_fileMax.setFont(font)
        self.label_fileMax.setObjectName("label_fileMax")
        self.horizontalLayout_4.addWidget(self.label_fileMax)
        self.label_fileMaxdis = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        self.label_fileMaxdis.setFont(font)
        self.label_fileMaxdis.setObjectName("label_fileMaxdis")
        self.horizontalLayout_4.addWidget(self.label_fileMaxdis)
        self.gridLayout_2.addLayout(self.horizontalLayout_4, 4, 1, 1, 1)
        self.label_file = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        self.label_file.setFont(font)
        self.label_file.setObjectName("label_file")
        self.gridLayout_2.addWidget(self.label_file, 4, 0, 1, 1)
        self.label_man = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        self.label_man.setFont(font)
        self.label_man.setObjectName("label_man")
        self.gridLayout_2.addWidget(self.label_man, 1, 0, 1, 1)
        self.label_normweight = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        self.label_normweight.setFont(font)
        self.label_normweight.setObjectName("label_normweight")
        self.gridLayout_2.addWidget(self.label_normweight, 0, 0, 1, 1)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.horizontalSlider_normweight = QtWidgets.QSlider(self.centralwidget)
        self.horizontalSlider_normweight.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_normweight.setObjectName("horizontalSlider_normweight")
        self.horizontalLayout_5.addWidget(self.horizontalSlider_normweight)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_5.addWidget(self.label_2)
        self.label_normMin = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        self.label_normMin.setFont(font)
        self.label_normMin.setObjectName("label_normMin")
        self.horizontalLayout_5.addWidget(self.label_normMin)
        self.label_9 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setBold(True)
        font.setWeight(75)
        self.label_9.setFont(font)
        self.label_9.setObjectName("label_9")
        self.horizontalLayout_5.addWidget(self.label_9)
        self.label_normMax = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        self.label_normMax.setFont(font)
        self.label_normMax.setObjectName("label_normMax")
        self.horizontalLayout_5.addWidget(self.label_normMax)
        self.gridLayout_2.addLayout(self.horizontalLayout_5, 0, 1, 1, 1)
        self.verticalLayout_2.addLayout(self.gridLayout_2)
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.param_check = QtWidgets.QTextBrowser(self.centralwidget)
        self.param_check.setObjectName("param_check")
        self.gridLayout_3.addWidget(self.param_check, 1, 1, 1, 1)
        self.rval_display = QtWidgets.QTextBrowser(self.centralwidget)
        self.rval_display.setObjectName("rval_display")
        self.gridLayout_3.addWidget(self.rval_display, 1, 2, 1, 1)
        self.checkBox_display = QtWidgets.QCheckBox(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        self.checkBox_display.setFont(font)
        self.checkBox_display.setObjectName("checkBox_display")
        self.gridLayout_3.addWidget(self.checkBox_display, 0, 2, 1, 1)
        self.label = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.gridLayout_3.addWidget(self.label, 0, 1, 1, 1)
        self.verticalLayout_2.addLayout(self.gridLayout_3)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.checkBox_pow = QtWidgets.QCheckBox(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        self.checkBox_pow.setFont(font)
        self.checkBox_pow.setObjectName("checkBox_pow")
        self.gridLayout.addWidget(self.checkBox_pow, 0, 0, 1, 1)
        self.btn_start = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        self.btn_start.setFont(font)
        self.btn_start.setObjectName("btn_start")
        self.gridLayout.addWidget(self.btn_start, 2, 0, 1, 1)
        self.btn_stop = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        self.btn_stop.setFont(font)
        self.btn_stop.setObjectName("btn_stop")
        self.gridLayout.addWidget(self.btn_stop, 3, 0, 1, 1)
        self.verticalLayout_2.addLayout(self.gridLayout)
        self.horizontalLayout_3.addLayout(self.verticalLayout_2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1004, 22))
        self.menubar.setObjectName("menubar")
        self.menusupport = QtWidgets.QMenu(self.menubar)
        self.menusupport.setObjectName("menusupport")
        self.menuabout = QtWidgets.QMenu(self.menubar)
        self.menuabout.setObjectName('menuabout')
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actiongenerate_random_data = QtWidgets.QAction(MainWindow)
        self.actiongenerate_random_data.setObjectName("actiongenerate_random_data")
        self.actionplay_a_sample_recording_as_test_data = QtWidgets.QAction(MainWindow)
        self.actionplay_a_sample_recording_as_test_data.setObjectName("actionplay_a_sample_recording_as_test_data")
        self.actionstop_generating = QtWidgets.QAction(MainWindow)
        self.actionstop_generating.setObjectName("actionstop_generating")
        self.action_help = QtWidgets.QAction(MainWindow)
        self.action_help.setObjectName('action_help')
        self.action_about = QtWidgets.QAction(MainWindow)
        self.action_about.setObjectName('action_about')
        self.menusupport.addSeparator()
        self.menusupport.addAction(self.actiongenerate_random_data)
        self.menusupport.addAction(self.actionplay_a_sample_recording_as_test_data)
        self.menusupport.addAction(self.actionstop_generating)
        self.menubar.addAction(self.menusupport.menuAction())
        self.menubar.addAction(self.action_help)
        self.menubar.addAction(self.action_about)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Hybrid Harmony"))
        MainWindow.setWindowIcon(QtGui.QIcon(LOGO_PATH))
        self.label_3.setText(_translate("MainWindow", "Frequency bands for analysis"))
        self.label_4.setText(_translate("MainWindow", "Input data streams"))
        self.btn_loadStreams.setToolTip(_translate("MainWindow", "detect LSL streams for analysis. Streams should be displayed on the table above."))
        self.btn_loadStreams.setText(_translate("MainWindow", "1. load LSL streams"))
        self.label_5.setText(_translate("MainWindow", "Parameters"))
        self.label_oscPort.setText(_translate("MainWindow", "OSC port (optional) "))
        self.label_input.setText(_translate("MainWindow", "Input type"))
        self.lineEdit_oscIP.setText(_translate("MainWindow", "10.0.0.24"))
        self.label_7.setText(_translate("MainWindow", "Window size (seconds)"))
        self.comboBox_input.setItemText(0, _translate("MainWindow", "EEG"))
        self.lineEdit_oscCH.setText(_translate("MainWindow", "9000"))
        self.comboBox_wsize.setItemText(0, _translate("MainWindow", "3"))
        self.comboBox_wsize.setItemText(1, _translate("MainWindow", "4"))
        self.comboBox_wsize.setItemText(2, _translate("MainWindow", "5"))
        self.comboBox_wsize.setItemText(3, _translate("MainWindow", "6"))
        self.comboBox_wsize.setItemText(4, _translate("MainWindow", "7"))
        self.comboBox_wsize.setItemText(5, _translate("MainWindow", "8"))
        self.comboBox_chn.setItemText(0, _translate("MainWindow", "one-to-one (e.g. Fp1 is only correlated with Fp1 and so on.)"))
        self.comboBox_chn.setItemText(1, _translate("MainWindow", "all-to-all (e.g. each channel is correlated with all the other available channels in the selection.)"))
        self.comboBox_conn.setItemText(0, _translate("MainWindow", "Coherence"))
        self.comboBox_conn.setItemText(1, _translate("MainWindow", "Imaginary Coherence"))
        self.comboBox_conn.setItemText(2, _translate("MainWindow", "Envelope Correlation"))
        self.comboBox_conn.setItemText(3, _translate("MainWindow", "Power Correlation"))
        self.comboBox_conn.setItemText(4, _translate("MainWindow", "PLV"))
        self.comboBox_conn.setItemText(5, _translate("MainWindow", "CCorr"))
        self.label_6.setText(_translate("MainWindow", "Connectivity metric"))
        self.label_chn.setText(_translate("MainWindow", "Connectivity type"))
        self.checkBox_osc.setText(_translate("MainWindow", "sending through OSC"))
        self.label_oscIP.setText(_translate("MainWindow", "OSC IP address (optional)"))
        self.label_normparam.setText(_translate("MainWindow", "Normalization parameters"))
        self.label_manMin.setText(_translate("MainWindow", "Min."))
        self.lineEdit_manMin.setText(_translate("MainWindow", "0"))
        self.label_manMax.setText(_translate("MainWindow", "Max."))
        self.lineEdit_manMax.setText(_translate("MainWindow", "1"))
        self.pushButton_openfile.setText(_translate("MainWindow", "Open..."))
        self.pushButton_computefile.setText(_translate("MainWindow", "compute"))
        self.label_fileMin.setText(_translate("MainWindow", "Min."))
        self.label_fileMindis.setText(_translate("MainWindow", "N/A"))
        self.label_fileMax.setText(_translate("MainWindow", "Max."))
        self.label_fileMaxdis.setText(_translate("MainWindow", "N/A"))
        self.label_file.setText(_translate("MainWindow", "from File"))
        self.label_man.setText(_translate("MainWindow", "Manual"))
        self.label_normweight.setText(_translate("MainWindow", "Weight"))
        self.label_2.setText(_translate("MainWindow", "Min."))
        self.label_normMin.setText(_translate("MainWindow", "0, 0, 0"))
        self.label_9.setText(_translate("MainWindow", "Max."))
        self.label_normMax.setText(_translate("MainWindow", "1, 1, 1"))
        self.checkBox_display.setText(_translate("MainWindow", "display connectivity values"))
        self.label.setText(_translate("MainWindow", "console"))
        self.checkBox_pow.setText(_translate("MainWindow", "sending power values"))
        self.btn_start.setText(_translate("MainWindow", "2. start analysis"))
        self.btn_stop.setText(_translate("MainWindow", "stop analysis"))
        self.menusupport.setTitle(_translate("MainWindow", "Tools"))
        self.actiongenerate_random_data.setText(_translate("MainWindow", "play a random signal for testing"))
        self.actionplay_a_sample_recording_as_test_data.setText(_translate("MainWindow", "play a sample recording for testing"))
        self.action_help.setText(_translate("MainWindow", "Help"))
        self.action_about.setText(_translate("MainWindow", "About"))
        self.actionstop_generating.setText(_translate("MainWindow", "stop generating"))

class Mainprogram(QtWidgets.QMainWindow):
    def __init__(self, app, *args, **kwargs):
        super(Mainprogram, self).__init__(*args, **kwargs)
        app.aboutToQuit.connect(self._stop)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setup()

    def setup(self):
        """
        function to set up the GUI components
        """
        # log_path = path.join(path.dirname(path.abspath(__file__)), 'log')
        # log_path = path.join(log_path, 'logging.conf')
        # logging.config.fileConfig(log_path)
        logging.config.fileConfig(resource_path('log/logging.conf'))
        # initialization
        self.conn_params = []
        self.analysis_running = False
        self.ui.btn_stop.setEnabled(False)
        self.ui.checkBox_osc.setChecked(True)
        self.ui.checkBox_pow.setChecked(False)
        self.p = None
        self.ui.actionstop_generating.setVisible(False)

        # table content
        self.ui.infoTable.setHorizontalHeaderLabels(['Stream ID', "channel count", 'sampling rate', 'theta', 'alpha', 'beta'])
        self.ui.freqTable.setHorizontalHeaderLabels(['Freq. Band', "Min. Freq.", 'Max. Freq.', 'weight'])
        # fill freTable with default options
        self.ui.freqTable.setRowCount(4)
        default_freqTable = [['theta', '4', '8', '1'], ['alpha', '8', '12', '1'], ['beta', '12', '30', '1']]
        for n_row in range(3):
            for n_col in range(4):
                self.ui.freqTable.setItem(n_row, n_col, QtWidgets.QTableWidgetItem(default_freqTable[n_row][n_col]))
        # initializing actions
        self.ui.btn_loadStreams.clicked.connect(self.fun_load_streams)
        self.ui.btn_start.clicked.connect(self.fun_analyze)
        self.ui.btn_stop.clicked.connect(self.fun_stop)
        self.ui.pushButton_openfile.clicked.connect(self._openfile)
        self.ui.pushButton_computefile.clicked.connect(self._computefile)
        self.ui.checkBox_osc.toggled.connect(self.ui.lineEdit_oscIP.setEnabled)
        self.ui.checkBox_osc.toggled.connect(self.ui.lineEdit_oscCH.setEnabled)
        self.ui.actiongenerate_random_data.triggered.connect(self._run_generate_random_samples)
        self.ui.actionplay_a_sample_recording_as_test_data.triggered.connect(self._run_generate_xdf_samples)
        self.ui.actionstop_generating.triggered.connect(self._stop_generating)
        self.ui.action_help.triggered.connect(self._open_help)
        self.ui.action_about.triggered.connect(self._open_about)
        # getting value changed signal
        self.ui.horizontalSlider_normweight.valueChanged.connect(self._weightslider)
        self.ui.lineEdit_manMax.textChanged.connect(self._weightslider)
        self.ui.lineEdit_manMin.textChanged.connect(self._weightslider)

        # initializing params
        self.fileMin, self.fileMax = None, None

    def _stop(self):
        """
        stopping threads
        """
        if self.analysis:
            self.analysis.stop()
        if self.discovery:
            self.discovery.stop()

    def _open_about(self):
        """
        function to open 'about' information
        """
        msg = QtWidgets.QMessageBox()
        msg.setWindowTitle('About')
        msg.setText('lsl: version\nApp: 1.0\nLicense:\nCopyright (c) 2021 Phoebe Chen\n\nPermission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:\n\nThe above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.')
        msg.setIcon(QtWidgets.QMessageBox.Information)
        msg.exec()
    def _open_help(self):
        """
        function to open online tutorial
        """
        linkStr = "https://github.com/RhythmsOfRelating/HybridHarmony/wiki/Software-Manual"
        QtGui.QDesktopServices.openUrl(QtCore.QUrl(linkStr))

    def _weightslider(self):
        """
        function to update normalization parameters based on the weight slider and inputs
        """
        try:
            w = 100 - self.ui.horizontalSlider_normweight.sliderPosition()
            if self.fileMax is not None:
                filemins = [float(x) for x in self.ui.label_fileMindis.text().split(', ')]
                filemaxs = [float(x) for x in self.ui.label_fileMaxdis.text().split(', ')]
                minn = [w/100 * float(self.ui.lineEdit_manMin.text()) + (100-w)/100 * m for m in filemins]
                maxx = [w/100 * float(self.ui.lineEdit_manMax.text()) + (100-w)/100 * m for m in filemaxs]
            else:
                n_freq = 0
                for i in range(self.ui.freqTable.rowCount()):
                    if self.ui.freqTable.item(i, 0):
                        n_freq += 1
                minn = [w/100 * float(self.ui.lineEdit_manMin.text())] * n_freq
                maxx = [w/100 * float(self.ui.lineEdit_manMax.text())] * n_freq
            self.ui.label_normMax.setText(', '.join(["%.2f" % l for l in list(maxx)]))
            self.ui.label_normMin.setText(', '.join(["%.2f" % l for l in list(minn)]))
        except Exception as e:
            self.ui.param_check.append(str(e))

    def play_display(self):
        """
        set up a thread for displaying connectivity values in real time
        """
        self.playthread = QtCore.QThread(parent=self)
        self.displayer = Display(self.analysis.que)
        self.displayer.moveToThread(self.playthread)

        self.displayer.finished.connect(self.playthread.quit)  # connect the workers finished signal to stop thread
        self.displayer.finished.connect(
            self.displayer.deleteLater)  # connect the workers finished signal to clean up worker
        self.displayer.finished.connect(
            self.playthread.deleteLater)  # connect threads finished signal to clean up thread
        self.displayer.progress.connect(self.reportProgress)
        self.playthread.started.connect(self.displayer.do_display)
        self.playthread.finished.connect(self.displayer.stop)
        self.playthread.start()

    def reportProgress(self, r):
        """
        display connectivity values
        """
        self.ui.rval_display.append(str(r))

    def fun_unlock(self):
        """
        button unlock after analysis is stopped
        """
        if self.analysis_running:  # stop analysis if running
            self.fun_stop()

        # reset buttons
        self.ui.btn_loadStreams.setEnabled(True)
        # unlock tables
        self.ui.infoTable.setEditTriggers(QtWidgets.QAbstractItemView.AllEditTriggers)
        self.ui.freqTable.setEditTriggers(QtWidgets.QAbstractItemView.AllEditTriggers)
        # set label text
        self.ui.param_check.append("Parameters are editable now.\n")

    def _read_osc(self):
        """
        set up osc port
        """
        IP = None
        port = None
        # reading params
        if self.ui.checkBox_osc.isChecked():
            IP = self.ui.lineEdit_oscIP.text()
            port = self.ui.lineEdit_oscCH.text()
        return IP, port

    def _run_generate_random_samples(self):
        """
        thread to run random samples
        """
        self.run_samples = SampleGeneration('random')
        self.run_samples.start()
        self.ui.actiongenerate_random_data.setEnabled(False)  # gray out the button
        self.ui.actionplay_a_sample_recording_as_test_data.setEnabled(False)
        self.ui.actionstop_generating.setVisible(True)
        self.ui.param_check.append('Sending random samples for testing...')

    def _run_generate_xdf_samples(self):
        """
        thread to run testing samples
        """
        self.run_samples = SampleGeneration('sample')
        self.run_samples.start()
        self.ui.actiongenerate_random_data.setEnabled(False)  # gray out the button
        self.ui.actionplay_a_sample_recording_as_test_data.setEnabled(False)
        self.ui.actionstop_generating.setVisible(True)
        self.ui.param_check.append('Sending a sample recording for testing...')

    def _stop_generating(self):
        """
        stop the threads for running test samples, if any
        """
        self.run_samples.stop()
        self.ui.actiongenerate_random_data.setEnabled(True)
        self.ui.actionplay_a_sample_recording_as_test_data.setEnabled(True)
        self.ui.actionstop_generating.setVisible(False)
        self.ui.param_check.append('Stopped sending samples.')

    def fun_load_streams(self):
        """
        load EEG streams and display in the information table
        """
        # determine columns based on freq bands
        cols = ['Stream ID', "channel count", 'sampling rate']
        for i in range(self.ui.freqTable.rowCount()):
            if self.ui.freqTable.item(i,0):
                cols.append(self.ui.freqTable.item(i,0).text()+' channels')

        self.ui.infoTable.setColumnCount(len(cols))
        self.ui.infoTable.setHorizontalHeaderLabels(cols)
        # update normalization texts
        self._weightslider()
        # discover streams
        self.ui.infoTable.setRowCount(0)
        self.discovery = Discovery(
            discard_timestamps=True,
            correct_timestamps=False
        )
        self.discovery.start()
        time.sleep(3)
        streams = list(self.discovery.streams_by_uid.keys())

        # update the table
        self.ui.infoTable.setRowCount(len(streams))
        for n_row, id in enumerate(streams):
            self.ui.infoTable.insertRow(n_row)
            # display stream ID
            item = QtWidgets.QTableWidgetItem(str(id))
            item.setFlags(QtCore.Qt.ItemIsEnabled)
            item.setBackground(QtGui.QColor(220, 220, 220))
            self.ui.infoTable.setItem(n_row, 0, item)
            # display channel count
            item = QtWidgets.QTableWidgetItem(str(self.discovery.channel_count))
            item.setFlags(QtCore.Qt.ItemIsEnabled)
            item.setBackground(QtGui.QColor(220, 220, 220))
            self.ui.infoTable.setItem(n_row, 1, item)
            # display sample rate
            item = QtWidgets.QTableWidgetItem(str(self.discovery.streams_by_uid[id].sample_rate))
            item.setFlags(QtCore.Qt.ItemIsEnabled)
            item.setBackground(QtGui.QColor(220, 220, 220))
            self.ui.infoTable.setItem(n_row, 2, item)
            # display chosen channels (editable)
            for n_freq in range(len(cols)-3):
                if n_row == 0:  # only making the first line editable, because every stream is using the same channel selection
                    item = QtWidgets.QTableWidgetItem('1:%s' % self.discovery.channel_count)
                else:
                    item = QtWidgets.QTableWidgetItem('Same as above')
                    item.setFlags(QtCore.Qt.ItemIsEnabled)
                    item.setBackground(QtGui.QColor(220, 220, 220))
                self.ui.infoTable.setItem(n_row, n_freq + 3, item)

    def fun_retrieve_params(self):
        """
        retrieve input parameters from the tables
        """
        freqloaded = True
        infoloaded = True
        # read freq table
        freq_names = []
        ranges = []
        weights = []
        for i in range(self.ui.freqTable.rowCount()):
            if self.ui.freqTable.item(i,0):
                try:
                    assert int(self.ui.freqTable.item(i,1).text()) < int(self.ui.freqTable.item(i,2).text())
                    freq_names.append(self.ui.freqTable.item(i, 0).text())
                    ranges.append((int(self.ui.freqTable.item(i, 1).text()), int(self.ui.freqTable.item(i, 2).text())))
                    weights.append(float(self.ui.freqTable.item(i, 3).text()))
                except Exception as e:
                    self.ui.param_check.append("Frequency table input type error.\n")
                    freqloaded = False
                    break

        # read info table
        n_freq = len(freq_names)
        chn_list = []
        for j in range(n_freq):
            if self.ui.infoTable.item(0, 3+j):
                try:
                    chns = self._str2list(self.ui.infoTable.item(0, 3+j).text())
                    chn_list.append(chns)
                except:
                    self.ui.param_check.append("Selected channel format error.\n")
                    infoloaded = False
                    break

        # integrate params
        try:
            freqParams = dict(zip(freq_names, ranges))
            chnParams = dict(zip(freq_names, chn_list))
            weightParams = dict(zip(freq_names, weights))
        except:
            self.ui.param_check.append("Parameter format error.\n")
            infoloaded = False

        # if no error message, continue to lock buttons and read params into analysis
        if freqloaded and infoloaded:
            self.ui.param_check.append("Successfully loaded parameters.\n")
            self.conn_params = [freqParams, chnParams, weightParams]
            # grey out loading buttons
            self.ui.btn_loadStreams.setEnabled(False)
            # lock tables
            self.ui.infoTable.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
            self.ui.freqTable.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

    def _read_input(self):
        """
        retrieve parameters from the text fields
        :return:
        """
        # device = self.comboBox_device.currentText()
        chn_type = self.ui.comboBox_chn.currentText()
        mode = self.ui.comboBox_conn.currentText()
        window_size = self.ui.comboBox_wsize.currentText()

        # weighted normalization
        norm_min = [float(x) for x in self.ui.label_normMin.text().split(', ')]
        norm_max = [float(x) for x in self.ui.label_normMax.text().split(', ')]
        device = None

        return device, chn_type, mode, window_size, norm_min, norm_max

    def _openfile(self):
        """
        pop up a dialog to open file
        """
        fileName,_ = QtWidgets.QFileDialog.getOpenFileName(self, 'OpenFile')
        # self.myTextBox.setText(fileName)
        self.ui.lineEdit_filename.setText(str(fileName))

    def _computefile(self):
        """
        compute Min. and Max. from a previously recorded xdf file.
        Note that the file must contain a marker stream named "RValues"
        """
        try:
            self.ui.param_check.append('Loading baseline file...')
            filename = self.ui.lineEdit_filename.text()
            raw_file = load_xdf(filename)[0]
            raw_file = [f for f in raw_file if ('RValues' in f['info']['name'][0]) and (f['time_series'].size > 0)]
            if len(raw_file) != 1:
                self.ui.param_check.append('Duplicated Rvalue streams or empty data. Please record baseline again.')
            else:
                self.ui.param_check.append(str(' | '.join(['ID','info','n_freq','data_size'])))
                person = raw_file[0]
                f_id = person['info']['source_id']
                f_name,f_chn_count,f_data = person['info']['name'][0], \
                                                           int(person['info']['channel_count'][0]),\
                                                            person['time_series'].T
                self.ui.param_check.append(str(' | '.join([str(f_id),str(f_name),str(f_chn_count),str(f_data.shape)])))
                # compute min max
                self.fileMin = np.min(f_data, axis=1)
                self.fileMax = np.max(f_data, axis=1)
                self.ui.label_fileMaxdis.setText(', '.join(["%.2f" % l for l in list(self.fileMax)]))
                self.ui.label_fileMindis.setText(', '.join(["%.2f" % l for l in list(self.fileMin)]))
                self._weightslider()
        except Exception as e:
            self.ui.param_check.append(str(e))

    def fun_analyze(self):
        """
        run the analysis
        """
        device, chn_type, mode, window_size, norm_min, norm_max = self._read_input()
        IP, port = self._read_osc()
        # making sure first button was pressed
        if not hasattr(self, 'discovery'):
            self.ui.param_check.append('Please make sure EEG streams have been loaded first.\n')
        # making sure input is not empty
        elif len(list(self.discovery.streams_by_uid.keys()))<1:
            self.ui.param_check.append('Please make sure EEG streams have been loaded first.\n')
        else:
            self.fun_retrieve_params()
            # proceed only if load stream button is locked
            if not self.ui.btn_loadStreams.isEnabled():
                try:
                    # starting analysis
                    self.analysis = Analysis(discovery=self.discovery, mode=mode, chn_type=chn_type,
                                             corr_params=self.conn_params, OSC_params=[IP, port],
                                             compute_pow=self.ui.checkBox_pow.isChecked(),
                                             window_params=float(window_size),  # baseline lag not implemented
                                             norm_params=[norm_min, norm_max])
                    self.analysis.start()
                    n_freq, n_ppl = len(self.conn_params[0]), self._factorial(len(list(self.discovery.streams_by_uid.keys())),2)
                    self.ui.param_check.append("Sending connectivity values for %s frequency bands and %s pairs...\n" % (n_freq,n_ppl))
                    # update state variable and buttons
                    self.analysis_running = True
                    self.ui.btn_stop.setEnabled(True)
                    self._enableEdit(False)
                    if self.ui.checkBox_display.isChecked():
                        self.play_display()
                except Exception as e:
                    self.ui.param_check.append('Error with analysis. The Error message is:'\
                                             +'\n'+str(e)+'\n')

    def _factorial(self, n, k):
        # n choose k
        return int(factorial(n) / factorial(k) / factorial(n - k))

    def _enableEdit(self, bool):
        """
        make the buttons and fields (non)editable
        """
        self.ui.btn_start.setEnabled(bool)
        self.ui.comboBox_conn.setEnabled(bool)
        self.ui.comboBox_chn.setEnabled(bool)
        self.ui.comboBox_input.setEnabled(bool)
        self.ui.comboBox_wsize.setEnabled(bool)
        self.ui.lineEdit_oscCH.setEnabled(bool)
        self.ui.lineEdit_oscIP.setEnabled(bool)
        self.ui.checkBox_display.setEnabled(bool)
        self.ui.horizontalSlider_normweight.setEnabled(bool)
        self.ui.lineEdit_manMin.setEnabled(bool)
        self.ui.lineEdit_manMax.setEnabled(bool)
        self.ui.lineEdit_filename.setEnabled(bool)
        self.ui.pushButton_computefile.setEnabled(bool)
        self.ui.pushButton_openfile.setEnabled(bool)

    def fun_stop(self):
        """
        function to stop analysis
        """
        # stop analysis
        if self.ui.checkBox_display.isChecked():
            self.displayer.stop()
            time.sleep(1)
        self.analysis.stop()
        self.analysis_running = False
        self.discovery.stop()
        self.ui.btn_stop.setEnabled(False)
        self.ui.btn_start.setEnabled(True)
        self.ui.btn_loadStreams.setEnabled(True)
        # set parameter area editable
        self._enableEdit(True)
        self.fun_unlock()
        self.ui.param_check.append("Analysis stopped.\n")


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
        assert max(ind) < int(self.ui.infoTable.item(0,1).text())  # index cannot be larger than channel count
        ind = list(dict.fromkeys(ind))  # remove duplicates
        ind.sort()  # sort
        return ind

class Display(QtCore.QObject):
    finished =QtCore.pyqtSignal()  # give worker class a finished signal
    progress = QtCore.pyqtSignal(list)
    error = QtCore.pyqtSignal(tuple)
    def __init__(self, que):
        """
        Class to display connectivity values
        """
        QtCore.QObject.__init__(self, parent=None)
        self.continue_run = True  # provide a bool run condition for the class
        try:
            self.que = que
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.error.emit((exctype, value, traceback.format_exc()))

    def do_display(self):
        while self.continue_run:  # give the loop a stoppable condition
            try:
                time.sleep(0.3)
                self.progress.emit(self.que.get())
            except:
                traceback.print_exc()
                exctype, value = sys.exc_info()[:2]
                self.error.emit((exctype, value, traceback.format_exc()))

    def stop(self):
        self.continue_run = False  # set the run condition to false on stop
        self.finished.emit()  # emit the finished signal when the loop is done


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Main = Mainprogram(app)
    Main.show()
    sys.exit(app.exec_())

