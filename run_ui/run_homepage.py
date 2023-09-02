# !/usr/bin/env python
# _*_ coding: utf-8 _*_
import sys
from pathlib import Path

from PyQt5.QtCore import QCoreApplication, Qt, QUrl, pyqtSignal
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QMainWindow, QApplication, QDialog, QFileDialog, QWidget, QGridLayout, QMessageBox

from run_ui.run_personal_center import Ui_WgtPersonCenterAction
from ui.homepage import Ui_MainWindow
from run_ui.run_video_analysis_result_manage import Ui_WgtVideoAnalysisResultManageAction
from run_ui.run_single_vid_analysis import Ui_WgtSingleVidAnalysisAction
from run_ui.run_person_manage import Ui_WgtPersonManageAction
from run_ui.run_quit_win_display import Ui_WgtQuitWinDisplayAction


class Ui_MainWindowsAction(QMainWindow, Ui_MainWindow):
    login_user_info_received_signal = pyqtSignal(dict)

    def __init__(self):
        QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.setAttribute(Qt.WA_StyledBackground, True)  # 激活背景
        self.gridLayout_analysis = QGridLayout(self.page)
        self.gridLayout_report = QGridLayout(self.page_2)
        self.gridLayout_person = QGridLayout(self.page_3)

        self.single_vid_analysis_win = Ui_WgtSingleVidAnalysisAction()
        self.video_analysis_result_manage_win = Ui_WgtVideoAnalysisResultManageAction()
        self.person_mange_win = Ui_WgtPersonManageAction()

        self.gridLayout_report.addWidget(self.single_vid_analysis_win, 0, 0, 1, 1)
        self.gridLayout_analysis.addWidget(self.video_analysis_result_manage_win, 0, 0, 1, 1)
        self.gridLayout_person.addWidget(self.person_mange_win, 0, 0, 1, 1)

        self.h = self.height()
        self.w = self.width()
        self.window_point = None

        self.setup_ui()
        self._initUI()

        self.btn_name.clicked.connect(self.btn_name_click_action)
        self.login_user_info_received_signal.connect(self.fill_received_data)

        self.btn_name.setStyleSheet("QPushButton{\n"
                                    "    font: 18pt \"SimSun\";\n"
                                    "    background:transparent;\n"
                                    "}\n")

    def _initUI(self):
        """
        初始化窗口设置
        """
        self.setWindowFlags(Qt.FramelessWindowHint)  # 无边框

    def setup_ui(self):
        self.display(0)
        self.btn_quit.clicked.connect(self.close_win)
        self.btn_resolve_report.clicked.connect(lambda: self.display(1))
        self.btn_resolve_vid.clicked.connect(lambda: self.display(0))
        self.btn_person_manage.clicked.connect(lambda: self.display(2))

    def close_win(self):
        self.quit_action = Ui_WgtQuitWinDisplayAction()
        self.quit_action.show()

    def display(self, i):
        """
        展示窗口
        :param i:
        :return:
        """
        if i == 1:
            self.single_vid_analysis_win.back2default_ui()
        self.stackedWidget.setCurrentIndex(i)

    def btn_name_click_action(self):
        self.personal_center = Ui_WgtPersonCenterAction()
        self.personal_center.login_user_info_received_signal.emit(self.user_info)
        self.personal_center.login_user_info_send_signal.connect(self.fill_received_data)
        self.personal_center.show()

    def fill_received_data(self, user_info):
        if user_info is not None and len(user_info) > 0:
            self.user_info = user_info

            self.single_vid_analysis_win.login_user_info_received.emit(user_info)
            self.video_analysis_result_manage_win.login_user_info_received.emit(user_info)

            name = user_info["name"]
            portrait = user_info["portrait"]
            self.btn_name.setText(name)
            if len(portrait) > 0:
                QImg = QImage(portrait)
                self.lab_head.setPixmap(QPixmap.fromImage(QImg).scaled(self.lab_head.size(),
                                                                       Qt.KeepAspectRatio,
                                                                       Qt.SmoothTransformation))
                self.lab_head.setScaledContents(True)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = Ui_MainWindowsAction()
    window.show()
    # window.showMaximized()    # 窗口最大化
    sys.exit(app.exec_())
