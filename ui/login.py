# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'login.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_WgtLogin(object):
    def setupUi(self, WgtLogin):
        WgtLogin.setObjectName("WgtLogin")
        WgtLogin.resize(1200, 900)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(WgtLogin.sizePolicy().hasHeightForWidth())
        WgtLogin.setSizePolicy(sizePolicy)
        WgtLogin.setMinimumSize(QtCore.QSize(1200, 900))
        WgtLogin.setMaximumSize(QtCore.QSize(1200, 900))
        WgtLogin.setStyleSheet("QWidget{background-image: url(:/image/background.jpg);}\n"
"/*QWidget#Form{\n"
"background-image: url(:/image/background.jpg);\n"
"}*/")
        self.listWidget = QtWidgets.QListWidget(WgtLogin)
        self.listWidget.setGeometry(QtCore.QRect(820, 230, 371, 361))
        self.listWidget.setObjectName("listWidget")
        self.edt_username = QtWidgets.QLineEdit(WgtLogin)
        self.edt_username.setGeometry(QtCore.QRect(860, 310, 301, 51))
        self.edt_username.setObjectName("edt_username")
        self.edt_password = QtWidgets.QLineEdit(WgtLogin)
        self.edt_password.setGeometry(QtCore.QRect(860, 420, 301, 51))
        self.edt_password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.edt_password.setObjectName("edt_password")
        self.label = QtWidgets.QLabel(WgtLogin)
        self.label.setGeometry(QtCore.QRect(859, 250, 301, 30))
        self.label.setMinimumSize(QtCore.QSize(60, 0))
        self.label.setStyleSheet("font: 12pt \"Arial\";\n"
"font: 87 20pt \"Arial Black\";\n"
"font: 87 9pt \"Arial\";\n"
"font: 87 16pt \"Arial Black\";")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.btn_login = QtWidgets.QPushButton(WgtLogin)
        self.btn_login.setGeometry(QtCore.QRect(860, 510, 301, 51))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_login.sizePolicy().hasHeightForWidth())
        self.btn_login.setSizePolicy(sizePolicy)
        self.btn_login.setStyleSheet("background-color: rgb(0, 85, 255);\n"
"\n"
"")
        self.btn_login.setObjectName("btn_login")

        self.retranslateUi(WgtLogin)
        QtCore.QMetaObject.connectSlotsByName(WgtLogin)

    def retranslateUi(self, WgtLogin):
        _translate = QtCore.QCoreApplication.translate
        WgtLogin.setWindowTitle(_translate("WgtLogin", "登录"))
        self.edt_username.setPlaceholderText(_translate("WgtLogin", "请输入您的手机号"))
        self.edt_password.setPlaceholderText(_translate("WgtLogin", "请输入您的密码"))
        self.label.setText(_translate("WgtLogin", "登录"))
        self.btn_login.setText(_translate("WgtLogin", "登录"))
import picture_rc