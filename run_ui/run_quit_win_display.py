# !/usr/bin/env python
# _*_ coding: utf-8 _*_
import sys
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QDialog, QApplication
from ui.quit_win_display import Ui_WgtQuitWinDisplay


class Ui_WgtQuitWinDisplayAction(QDialog, Ui_WgtQuitWinDisplay):
    close_signal = pyqtSignal()

    def __init__(self):
        QDialog.__init__(self)
        Ui_WgtQuitWinDisplay.__init__(self)
        self.setupUi(self)
        self.setAttribute(Qt.WA_StyledBackground, True)  # 激活背景

        self.h = self.height()
        self.w = self.width()
        self.window_point = None

        self._initUI()
        self.setup_ui()

    def _initUI(self):
        """
        初始化窗口设置
        """
        self.setWindowFlags(Qt.FramelessWindowHint)  # 无边框

    def setup_ui(self):
        self.btn_exit.clicked.connect(self.btn_exit_action)
        self.btn_cancel.clicked.connect(self.btn_cancel_action)

    def btn_cancel_action(self):
        self.close()

    def btn_exit_action(self):
        sys.exit().accept()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = Ui_WgtQuitWinDisplayAction()
    window.show()
    # window.showMaximized()    # 窗口最大化
    sys.exit(app.exec_())
