# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:\MainControl_QA\TestDevelopment\BootAssistant\BootAssistant.ui'
#
# Created: Thu Jun 30 16:05:05 2016
#      by: PyQt4 UI code generator 4.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_BootAssistant(object):
    def setupUi(self, BootAssistant):
        BootAssistant.setObjectName(_fromUtf8("BootAssistant"))
        BootAssistant.resize(449, 478)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("./ba.ico")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("./ba.ico")), QtGui.QIcon.Normal, QtGui.QIcon.On)
        BootAssistant.setWindowIcon(icon)
        self.centralwidget = QtGui.QWidget(BootAssistant)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.groupBox = QtGui.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(20, 50, 411, 81))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.pushButton_GetBoot = QtGui.QPushButton(self.groupBox)
        self.pushButton_GetBoot.setGeometry(QtCore.QRect(80, 50, 61, 23))
        self.pushButton_GetBoot.setObjectName(_fromUtf8("pushButton_GetBoot"))
        self.pushButton_openBootDir = QtGui.QPushButton(self.groupBox)
        self.pushButton_openBootDir.setGeometry(QtCore.QRect(180, 50, 61, 23))
        self.pushButton_openBootDir.setObjectName(_fromUtf8("pushButton_openBootDir"))
        self.layoutWidget = QtGui.QWidget(self.groupBox)
        self.layoutWidget.setGeometry(QtCore.QRect(20, 20, 331, 24))
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout_3.setMargin(0)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.label = QtGui.QLabel(self.layoutWidget)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout_3.addWidget(self.label)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.lineEdit_getDir = QtGui.QLineEdit(self.layoutWidget)
        self.lineEdit_getDir.setMinimumSize(QtCore.QSize(196, 20))
        self.lineEdit_getDir.setObjectName(_fromUtf8("lineEdit_getDir"))
        self.horizontalLayout_2.addWidget(self.lineEdit_getDir)
        self.toolButton_getDir = QtGui.QToolButton(self.layoutWidget)
        self.toolButton_getDir.setObjectName(_fromUtf8("toolButton_getDir"))
        self.horizontalLayout_2.addWidget(self.toolButton_getDir)
        self.horizontalLayout_3.addLayout(self.horizontalLayout_2)
        self.groupBox_2 = QtGui.QGroupBox(self.centralwidget)
        self.groupBox_2.setGeometry(QtCore.QRect(20, 140, 411, 61))
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.layoutWidget1 = QtGui.QWidget(self.groupBox_2)
        self.layoutWidget1.setGeometry(QtCore.QRect(20, 20, 370, 25))
        self.layoutWidget1.setObjectName(_fromUtf8("layoutWidget1"))
        self.horizontalLayout_5 = QtGui.QHBoxLayout(self.layoutWidget1)
        self.horizontalLayout_5.setMargin(0)
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.label_2 = QtGui.QLabel(self.layoutWidget1)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout_5.addWidget(self.label_2)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.lineEdit_localBootDir = QtGui.QLineEdit(self.layoutWidget1)
        self.lineEdit_localBootDir.setMinimumSize(QtCore.QSize(176, 20))
        self.lineEdit_localBootDir.setObjectName(_fromUtf8("lineEdit_localBootDir"))
        self.horizontalLayout_4.addWidget(self.lineEdit_localBootDir)
        self.toolButton_localBootDir = QtGui.QToolButton(self.layoutWidget1)
        self.toolButton_localBootDir.setObjectName(_fromUtf8("toolButton_localBootDir"))
        self.horizontalLayout_4.addWidget(self.toolButton_localBootDir)
        self.horizontalLayout_5.addLayout(self.horizontalLayout_4)
        self.pushButton_upload = QtGui.QPushButton(self.layoutWidget1)
        self.pushButton_upload.setObjectName(_fromUtf8("pushButton_upload"))
        self.horizontalLayout_5.addWidget(self.pushButton_upload)
        self.textEdit = QtGui.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(20, 280, 411, 161))
        self.textEdit.setAutoFillBackground(True)
        self.textEdit.setTextInteractionFlags(QtCore.Qt.TextSelectableByKeyboard|QtCore.Qt.TextSelectableByMouse)
        self.textEdit.setObjectName(_fromUtf8("textEdit"))
        self.groupBox_3 = QtGui.QGroupBox(self.centralwidget)
        self.groupBox_3.setGeometry(QtCore.QRect(20, 210, 411, 51))
        self.groupBox_3.setObjectName(_fromUtf8("groupBox_3"))
        self.layoutWidget2 = QtGui.QWidget(self.groupBox_3)
        self.layoutWidget2.setGeometry(QtCore.QRect(30, 20, 325, 25))
        self.layoutWidget2.setObjectName(_fromUtf8("layoutWidget2"))
        self.gridLayout = QtGui.QGridLayout(self.layoutWidget2)
        self.gridLayout.setMargin(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.pushButton_updateBoot = QtGui.QPushButton(self.layoutWidget2)
        self.pushButton_updateBoot.setObjectName(_fromUtf8("pushButton_updateBoot"))
        self.gridLayout.addWidget(self.pushButton_updateBoot, 0, 1, 1, 1)
        self.pushButton_resetPLC = QtGui.QPushButton(self.layoutWidget2)
        self.pushButton_resetPLC.setObjectName(_fromUtf8("pushButton_resetPLC"))
        self.gridLayout.addWidget(self.pushButton_resetPLC, 0, 2, 1, 1)
        self.pushButton_cleanData = QtGui.QPushButton(self.layoutWidget2)
        self.pushButton_cleanData.setObjectName(_fromUtf8("pushButton_cleanData"))
        self.gridLayout.addWidget(self.pushButton_cleanData, 0, 3, 1, 1)
        self.pushButton_MotifyXML = QtGui.QPushButton(self.layoutWidget2)
        self.pushButton_MotifyXML.setObjectName(_fromUtf8("pushButton_MotifyXML"))
        self.gridLayout.addWidget(self.pushButton_MotifyXML, 0, 0, 1, 1)
        self.pushButton_clean = QtGui.QPushButton(self.centralwidget)
        self.pushButton_clean.setGeometry(QtCore.QRect(340, 450, 75, 23))
        self.pushButton_clean.setObjectName(_fromUtf8("pushButton_clean"))
        self.layoutWidget3 = QtGui.QWidget(self.centralwidget)
        self.layoutWidget3.setGeometry(QtCore.QRect(30, 20, 332, 25))
        self.layoutWidget3.setObjectName(_fromUtf8("layoutWidget3"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.layoutWidget3)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label_3 = QtGui.QLabel(self.layoutWidget3)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.horizontalLayout.addWidget(self.label_3)
        self.lineEdit_ip = QtGui.QLineEdit(self.layoutWidget3)
        self.lineEdit_ip.setMinimumSize(QtCore.QSize(201, 20))
        self.lineEdit_ip.setObjectName(_fromUtf8("lineEdit_ip"))
        self.horizontalLayout.addWidget(self.lineEdit_ip)
        self.pushButton_ping = QtGui.QPushButton(self.layoutWidget3)
        self.pushButton_ping.setObjectName(_fromUtf8("pushButton_ping"))
        self.horizontalLayout.addWidget(self.pushButton_ping)
        BootAssistant.setCentralWidget(self.centralwidget)

        self.retranslateUi(BootAssistant)
        QtCore.QMetaObject.connectSlotsByName(BootAssistant)

    def retranslateUi(self, BootAssistant):
        BootAssistant.setWindowTitle(_translate("BootAssistant", "BootAssistant", None))
        self.groupBox.setTitle(_translate("BootAssistant", "Boot 提取", None))
        self.pushButton_GetBoot.setText(_translate("BootAssistant", "Boot提取", None))
        self.pushButton_openBootDir.setText(_translate("BootAssistant", "打开路径", None))
        self.label.setText(_translate("BootAssistant", "提取至：", None))
        self.toolButton_getDir.setText(_translate("BootAssistant", "...", None))
        self.groupBox_2.setTitle(_translate("BootAssistant", "Boot 上传", None))
        self.label_2.setText(_translate("BootAssistant", "本地路径：", None))
        self.toolButton_localBootDir.setText(_translate("BootAssistant", "...", None))
        self.pushButton_upload.setText(_translate("BootAssistant", "上传", None))
        self.groupBox_3.setTitle(_translate("BootAssistant", "PLC 操作", None))
        self.pushButton_updateBoot.setText(_translate("BootAssistant", "启用发布包", None))
        self.pushButton_resetPLC.setText(_translate("BootAssistant", "重启PLC", None))
        self.pushButton_cleanData.setText(_translate("BootAssistant", "清理数据盘", None))
        self.pushButton_MotifyXML.setText(_translate("BootAssistant", "导入变更参数", None))
        self.pushButton_clean.setText(_translate("BootAssistant", "清空", None))
        self.label_3.setText(_translate("BootAssistant", "PLC IP:", None))
        self.pushButton_ping.setText(_translate("BootAssistant", "PING", None))



if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    BootAssistant = QtGui.QMainWindow()
    ui = Ui_BootAssistant()
    ui.setupUi(BootAssistant)
    BootAssistant.show()
    sys.exit(app.exec_())

