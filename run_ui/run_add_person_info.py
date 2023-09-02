import sys
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QDialog, QApplication, QMessageBox
from ui.add_person_info import Ui_DigAddPersonInfo
from utils_tools.JSONTools import Config


class Ui_DigAddPersonInfoAction(QDialog, Ui_DigAddPersonInfo):
    add_user_info_send_signal = pyqtSignal(dict)

    def __init__(self):
        QDialog.__init__(self)
        Ui_DigAddPersonInfo.__init__(self)
        self.setupUi(self)
        self.setWindowTitle("添加用户信息")
        self.setAttribute(Qt.WA_StyledBackground | Qt.WA_TranslucentBackground)  # 激活背景
        self.setWindowFlags(Qt.FramelessWindowHint)  # 无边框
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

    """重写移动事件，不需要改变这里面的东西"""

    def mousePressEvent(self, e):
        self.start_point = e.globalPos()
        self.window_point = self.frameGeometry().topLeft()

    def mouseMoveEvent(self, e):
        height = self.height()
        width = self.width()
        old_size = (self.h, self.w)
        new_size = (height, width)
        if new_size == old_size:
            self.ismoving = True
            relpos = e.globalPos() - self.start_point
            self.move(self.window_point + relpos)
        else:
            self.h = height
            self.w = width

    def mouseReleaseEvent(self, e):
        self.ismoving = False

    def setup_ui(self):
        self.btn_person_edit.clicked.connect(self.btn_person_edit_action)
        self.btn_quit.clicked.connect(self.btn_quit_action)

    def back2default_ui(self):
        self.lineEdit_name.clear()
        self.lineEdit_mail.clear()
        self.lineEdit_phone.clear()
        self.lineEdit_password.clear()
        self.comboBox_position.setCurrentIndex(0)
        self.close()

    def btn_quit_action(self):
        self.back2default_ui()

    def btn_person_edit_action(self):
        name = self.lineEdit_name.text()
        post = self.comboBox_position.currentText()
        mail = self.lineEdit_mail.text()
        phone = self.lineEdit_phone.text()
        password = self.lineEdit_password.text()
        if name != '' and post != '' and mail != '' and phone != '' and password != '':
            val = {
                "name": name,
                "password": password,
                "role": post,
                "email": mail,
                "phone_number": phone,
                "state": "已启用",
                "portrait": ""
            }
            data = Config.read_user_info()
            if data is not None and phone in data.keys():
                self.show_msg("添加失败", "<h3>手机号已存在，请更换手机号！</p></h3>")
            else:
                if data is None:
                    data = {phone: val}
                else:
                    data[phone] = val
                Config.write_user_info(data)
                self.add_user_info_send_signal.emit(val)
                self.back2default_ui()
        else:
            self.show_msg("添加失败", "<h3>用户信息不能为空，<p>请填写用户信息！</p></h3>")

    def show_msg(self, title, text):
        """show_msg"""
        box = QMessageBox(QMessageBox.Icon(0), title, text)
        box.setObjectName('widget')
        box.setWindowFlags(Qt.FramelessWindowHint)
        qyes = box.addButton(box.tr("确定"), QMessageBox.YesRole)
        # qno = box.addButton(box.tr("取消"), QMessageBox.NoRole)
        box.setStyleSheet(
            'QWidget#widget{background-color:#ffffff;border:2px solid rgb(55, 55, 235);border-radius:3.2px;}\nQPushButton{border:2px solid rgb(55, 55, '
            '235);min-width:68px;border-radius:3.2px;color:#ffffff;background-color:rgb(55, 55, 235);}')
        box.exec_()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = Ui_DigAddPersonInfoAction()
    window.show()
    # window.showMaximized()    # 窗口最大化
    sys.exit(app.exec_())
