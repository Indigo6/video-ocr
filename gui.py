# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_VideoOCR(object):
    def setupUi(self, VideoOCR):
        VideoOCR.setObjectName("VideoOCR")
        VideoOCR.resize(1013, 579)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        VideoOCR.setFont(font)
        self.centralwidget = QtWidgets.QWidget(VideoOCR)
        self.centralwidget.setObjectName("centralwidget")
        self.genTime = QtWidgets.QPushButton(self.centralwidget)
        self.genTime.setGeometry(QtCore.QRect(270, 450, 110, 41))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        self.genTime.setFont(font)
        self.genTime.setObjectName("genTime")
        self.genSub = QtWidgets.QPushButton(self.centralwidget)
        self.genSub.setGeometry(QtCore.QRect(760, 450, 110, 41))
        self.genSub.setObjectName("genSub")
        self.saveFrames = QtWidgets.QCheckBox(self.centralwidget)
        self.saveFrames.setGeometry(QtCore.QRect(160, 450, 101, 41))
        self.saveFrames.setObjectName("saveFrames")
        self.ocrMethod = QtWidgets.QComboBox(self.centralwidget)
        self.ocrMethod.setGeometry(QtCore.QRect(660, 455, 87, 28))
        self.ocrMethod.setObjectName("ocrMethod")
        self.ocrMethod.addItem("")
        self.ocrMethod.addItem("")
        self.ocrMethod.addItem("")
        self.minValue = QtWidgets.QLineEdit(self.centralwidget)
        self.minValue.setGeometry(QtCore.QRect(760, 300, 110, 21))
        self.minValue.setObjectName("minValue")
        self.segMethod = QtWidgets.QComboBox(self.centralwidget)
        self.segMethod.setGeometry(QtCore.QRect(660, 220, 87, 28))
        self.segMethod.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.segMethod.setObjectName("segMethod")
        self.segMethod.addItem("")
        self.segMethod.addItem("")
        self.isSrt = QtWidgets.QLabel(self.centralwidget)
        self.isSrt.setGeometry(QtCore.QRect(660, 130, 201, 21))
        self.isSrt.setAlignment(QtCore.Qt.AlignCenter)
        self.isSrt.setObjectName("isSrt")
        self.srtLabel = QtWidgets.QLabel(self.centralwidget)
        self.srtLabel.setGeometry(QtCore.QRect(670, 340, 72, 15))
        self.srtLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.srtLabel.setObjectName("srtLabel")
        self.chgLabel = QtWidgets.QLabel(self.centralwidget)
        self.chgLabel.setGeometry(QtCore.QRect(670, 380, 72, 20))
        self.chgLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.chgLabel.setObjectName("chgLabel")
        self.srtThres = QtWidgets.QLineEdit(self.centralwidget)
        self.srtThres.setGeometry(QtCore.QRect(760, 340, 110, 21))
        self.srtThres.setAlignment(QtCore.Qt.AlignCenter)
        self.srtThres.setObjectName("srtThres")
        self.chgThres = QtWidgets.QLineEdit(self.centralwidget)
        self.chgThres.setGeometry(QtCore.QRect(760, 380, 110, 21))
        self.chgThres.setAlignment(QtCore.Qt.AlignCenter)
        self.chgThres.setObjectName("chgThres")
        self.videoBar = QtWidgets.QSlider(self.centralwidget)
        self.videoBar.setGeometry(QtCore.QRect(20, 300, 480, 22))
        self.videoBar.setOrientation(QtCore.Qt.Horizontal)
        self.videoBar.setObjectName("videoBar")
        self.maxValue = QtWidgets.QLineEdit(self.centralwidget)
        self.maxValue.setGeometry(QtCore.QRect(760, 260, 110, 21))
        self.maxValue.setObjectName("maxValue")
        self.testButton = QtWidgets.QPushButton(self.centralwidget)
        self.testButton.setGeometry(QtCore.QRect(760, 220, 110, 28))
        self.testButton.setObjectName("testButton")
        self.maxLabel = QtWidgets.QLabel(self.centralwidget)
        self.maxLabel.setGeometry(QtCore.QRect(670, 260, 72, 20))
        self.maxLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.maxLabel.setObjectName("maxLabel")
        self.minLabel = QtWidgets.QLabel(self.centralwidget)
        self.minLabel.setGeometry(QtCore.QRect(670, 300, 72, 20))
        self.minLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.minLabel.setObjectName("minLabel")
        self.videoView = QtWidgets.QGraphicsView(self.centralwidget)
        self.videoView.setGeometry(QtCore.QRect(20, 20, 480, 270))
        self.videoView.setObjectName("videoView")
        self.clipView = QtWidgets.QGraphicsView(self.centralwidget)
        self.clipView.setGeometry(QtCore.QRect(520, 20, 480, 100))
        self.clipView.setObjectName("clipView")
        VideoOCR.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(VideoOCR)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1013, 26))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        VideoOCR.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(VideoOCR)
        self.statusbar.setObjectName("statusbar")
        VideoOCR.setStatusBar(self.statusbar)
        self.openFile = QtWidgets.QAction(VideoOCR)
        self.openFile.setObjectName("openFile")
        self.menu.addAction(self.openFile)
        self.menubar.addAction(self.menu.menuAction())

        self.retranslateUi(VideoOCR)
        QtCore.QMetaObject.connectSlotsByName(VideoOCR)

    def retranslateUi(self, VideoOCR):
        _translate = QtCore.QCoreApplication.translate
        VideoOCR.setWindowTitle(_translate("VideoOCR", "Video OCR"))
        self.genTime.setText(_translate("VideoOCR", "generate\n"
"timeline"))
        self.genSub.setText(_translate("VideoOCR", "generate\n"
"subtitle"))
        self.saveFrames.setText(_translate("VideoOCR", "保存字幕帧"))
        self.ocrMethod.setItemText(0, _translate("VideoOCR", "paddle"))
        self.ocrMethod.setItemText(1, _translate("VideoOCR", "easy"))
        self.ocrMethod.setItemText(2, _translate("VideoOCR", "online"))
        self.minValue.setText(_translate("VideoOCR", "255,255,255"))
        self.segMethod.setItemText(0, _translate("VideoOCR", "RGB"))
        self.segMethod.setItemText(1, _translate("VideoOCR", "HSV"))
        self.isSrt.setText(_translate("VideoOCR", "Not a subtitle frame"))
        self.srtLabel.setText(_translate("VideoOCR", "srtThres"))
        self.chgLabel.setText(_translate("VideoOCR", "chgThres"))
        self.srtThres.setText(_translate("VideoOCR", "1.0"))
        self.chgThres.setText(_translate("VideoOCR", "5.0"))
        self.maxValue.setText(_translate("VideoOCR", "255,255,255"))
        self.testButton.setText(_translate("VideoOCR", "Test"))
        self.maxLabel.setText(_translate("VideoOCR", "max"))
        self.minLabel.setText(_translate("VideoOCR", "min"))
        self.menu.setTitle(_translate("VideoOCR", "文件"))
        self.openFile.setText(_translate("VideoOCR", "打开视频"))