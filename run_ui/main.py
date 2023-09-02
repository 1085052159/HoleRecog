# !/usr/bin/env python
# _*_ coding: utf-8 _*_
import os
import sys
from pathlib import Path

from PyQt5.QtCore import Qt, QCoreApplication
from PyQt5.QtWidgets import QApplication, QMessageBox
from run_ui.run_login import Ui_WgtLoginAction
from run_ui.run_homepage import Ui_MainWindowsAction


class App_Exec:
    def __init__(self):
        QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
        self.app = QApplication(sys.argv)
        self.login_win = Ui_WgtLoginAction()
        self.login_win.setWindowFlags(Qt.FramelessWindowHint)
        self.login_win.login_user_info_send_signal.connect(self.login_success_action)

    def login_success_action(self, login_user_info):
        self.login_win.close()
        self.homepage_win = Ui_MainWindowsAction()
        self.homepage_win.login_user_info_received_signal.emit(login_user_info)
        self.homepage_win.show()

    def quit_btn(self):
        self.box = QMessageBox(QMessageBox.Warning, "系统提示信息", "<h3>是否退出系统？</h3>")
        qyes = self.box.addButton(self.box.tr("是"), QMessageBox.YesRole)
        qno = self.box.addButton(self.box.tr("否"), QMessageBox.NoRole)
        self.box.exec_()
        if self.box.clickedButton() == qyes:
            sys.exit().accept()
        else:
            return

    def startProgram(self):
        self.login_win.show()
        sys.exit(self.app.exec_())


if __name__ == '__main__':
    App_Exec().startProgram()
