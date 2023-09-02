# !/usr/bin/env python
# _*_ coding: utf-8 _*_
import sys
from PyQt5.QtCore import Qt, QPoint, pyqtSignal
from PyQt5.QtGui import QMouseEvent

from run_ui.run_add_person_info import Ui_DigAddPersonInfoAction
from ui.login import Ui_WgtLogin
from PyQt5.QtWidgets import QWidget, QApplication, QMessageBox

from utils_tools.JSONTools import Config


class Ui_WgtLoginAction(QWidget, Ui_WgtLogin):
    login_user_info_send_signal = pyqtSignal(dict)

    def __init__(self):
        QWidget.__init__(self)
        Ui_WgtLogin.__init__(self)
        self.setupUi(self)
        self.setAttribute(Qt.WA_StyledBackground, True)    # 激活背景
        self.setup_ui()
        # self._initUI()

    def _initUI(self):
        """
        初始化窗口设置
        """
        self.setWindowFlags(Qt.FramelessWindowHint)    # 无边框

    """重写移动事件，不需要改变这里面的东西"""
    def mouseMoveEvent(self, e: QMouseEvent):    # 重写移动事件
        if self._startPos is not None:
            self._endPos = e.pos() - self._startPos
            self.move(self.pos() + self._endPos)

    def mousePressEvent(self, e: QMouseEvent):
        if e.button() == Qt.LeftButton:
            self._isTracking = True
            self._startPos = QPoint(e.x(), e.y())

    def mouseReleaseEvent(self, e: QMouseEvent):
        if e.button() == Qt.LeftButton:
            self._isTracking = False
            self._startPos = None

    def setup_ui(self):
        self.btn_login.clicked.connect(self.checked_login)

    def checked_login(self):
        """checked_login"""
        phone_number = self.edt_username.text()
        if len(phone_number) == 0:
            QMessageBox(QMessageBox.Critical, '错误', '手机号不能为空').exec_()
            return
        pwd = self.edt_password.text()
        if len(pwd) == 0:
            QMessageBox(QMessageBox.Critical, '错误', '密码不能为空').exec_()
            return
        user_infos = Config.read_user_info()
        if user_infos is None or len(user_infos) == 0:
            QMessageBox(QMessageBox.Critical, '错误', '账号信息不存在，请先添加用户！').exec_()
            self.add_person = Ui_DigAddPersonInfoAction()
            self.add_person.show()
        else:
            print("[run_login.checked_login]user_infos: ", user_infos)
            login_user_info = Config.query_user_info(user_infos, phone_number, pwd)
            if login_user_info is None or len(login_user_info) == 0:
                QMessageBox(QMessageBox.Critical, '错误', '手机号与密码不匹配').exec_()
            else:
                self.login_user_info_send_signal.emit(login_user_info)
                QMessageBox(QMessageBox.Information, '消息', '登录成功').exec_()
                self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = Ui_WgtLoginAction()
    window.show()
    # window.showMaximized()    # 窗口最大化
    sys.exit(app.exec_())

