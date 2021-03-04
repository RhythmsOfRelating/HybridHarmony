# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'bridge_gui.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
import pyqtgraph as pg
from pyqtgraph import PlotWidget

class Ui_bridge_main(object):
    def setupUi(self, bridge_main):
        bridge_main.setObjectName("bridge_main")
        bridge_main.resize(480, 640)
        self.centralwidget = QtWidgets.QWidget(bridge_main)
        self.centralwidget.setObjectName("centralwidget")
        self.graphicsView = PlotWidget(self.centralwidget)
        self.graphicsView.setGeometry(QtCore.QRect(10, 20, 461, 201))
        self.graphicsView.setObjectName("graphicsView")
        self.norm_methods = QtWidgets.QTabWidget(self.centralwidget)
        self.norm_methods.setGeometry(QtCore.QRect(20, 280, 411, 241))
        self.norm_methods.setObjectName("norm_methods")
        self.norm1 = QtWidgets.QWidget()
        self.norm1.setObjectName("norm1")
        self.gridLayoutWidget = QtWidgets.QWidget(self.norm1)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(30, 20, 321, 91))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalSlider_3 = QtWidgets.QSlider(self.gridLayoutWidget)
        self.horizontalSlider_3.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_3.setObjectName("horizontalSlider_3")
        self.gridLayout.addWidget(self.horizontalSlider_3, 2, 1, 1, 1)
        self.horizontalSlider = QtWidgets.QSlider(self.gridLayoutWidget)
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setObjectName("horizontalSlider")
        self.gridLayout.addWidget(self.horizontalSlider, 0, 1, 1, 1)
        self.horizontalSlider_2 = QtWidgets.QSlider(self.gridLayoutWidget)
        self.horizontalSlider_2.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_2.setObjectName("horizontalSlider_2")
        self.gridLayout.addWidget(self.horizontalSlider_2, 1, 1, 1, 1)
        self.label = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.norm_methods.addTab(self.norm1, "")
        self.norm2 = QtWidgets.QWidget()
        self.norm2.setObjectName("norm2")
        self.norm_methods.addTab(self.norm2, "")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(10, 230, 75, 23))
        self.pushButton.setObjectName("pushButton")
        bridge_main.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(bridge_main)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 480, 22))
        self.menubar.setObjectName("menubar")
        bridge_main.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(bridge_main)
        self.statusbar.setObjectName("statusbar")
        bridge_main.setStatusBar(self.statusbar)

        self.retranslateUi(bridge_main)
        self.norm_methods.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(bridge_main)

    def retranslateUi(self, bridge_main):
        _translate = QtCore.QCoreApplication.translate
        bridge_main.setWindowTitle(_translate("bridge_main", "MainWindow"))
        self.label.setText(_translate("bridge_main", "window"))
        self.label_2.setText(_translate("bridge_main", "max"))
        self.label_3.setText(_translate("bridge_main", "min"))
        self.norm_methods.setTabText(self.norm_methods.indexOf(self.norm1), _translate("bridge_main", "Tab 1"))
        self.norm_methods.setTabText(self.norm_methods.indexOf(self.norm2), _translate("bridge_main", "Tab 2"))
        self.pushButton.setText(_translate("bridge_main", "display"))
    def setup(self):
        # actions
        self.pushButton.clicked.connect(self.display_btn)
    def display_btn(self):
        # pushButton function to display incoming stream (rvals)
if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_bridge_main()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
