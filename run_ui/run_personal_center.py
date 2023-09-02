# !/usr/bin/env python
# _*_ coding: utf-8 _*_
import os
import shutil
import sys
from PyQt5.QtCore import Qt, QPoint, pyqtSignal
from PyQt5.QtGui import QMouseEvent, QImage, QPixmap, QIcon, QPalette, QBrush

from ui.personal_center import Ui_WgtPersonalCenter
from PyQt5.QtWidgets import QWidget, QApplication, QMessageBox, QFileDialog, QDialog

from utils_tools.JSONTools import Config


class Ui_WgtPersonCenterAction(QWidget, Ui_WgtPersonalCenter):
    login_user_info_received_signal = pyqtSignal(dict)
    login_user_info_send_signal = pyqtSignal(dict)

    def __init__(self):
        QWidget.__init__(self)
        Ui_WgtPersonalCenter.__init__(self)
        self.setupUi(self)
        self.setWindowTitle("个人中心")
        self.setAttribute(Qt.WA_StyledBackground, True)  # 激活背景
        self.btn_update_image.clicked.connect(self.btn_update_image_action)
        self.btn_change_user_info.clicked.connect(self.btn_change_user_info_action)
        self.btn_change_pwd.clicked.connect(self.btn_change_pwd_action)
        self.login_user_info_received_signal.connect(self.fill_received_data)

    def _initUI(self):
        """
        初始化窗口设置
        """
        self.setWindowFlags(Qt.FramelessWindowHint)  # 无边框

    def btn_update_image_action(self):
        portrait, _ = QFileDialog.getOpenFileName(QDialog(), '选择图像文件', './', '所有文件 (*);;图片文件 *.jpg *.png *.jpeg *.tif',
                                                  '图片文件 *.jpg *.png *.jpeg *.tif')
        phone = self.edt_phone_number.text()
        if len(portrait) > 0 and len(phone) > 0:
            dst_portrait_path = "%s/%s" % (Config.user_portrait_save_path(), os.path.basename(portrait))
            try:
                shutil.copyfile(portrait, dst_portrait_path)
            except:
                pass
            user_infos = Config.read_user_info()
            file_dir = str(Config.get_file_dir())
            print("[run_personal_center.btn_update_image_action]portrait_path: ", dst_portrait_path, file_dir)
            user_infos[phone]["portrait"] = dst_portrait_path.replace("\\", "/")
            Config.write_user_info(user_infos)
            QMessageBox(QMessageBox.Information, '消息', '上传成功').exec_()
        else:
            QMessageBox(QMessageBox.Information, '消息', '上传失败，用户信息不存在').exec_()

    def btn_change_user_info_action(self):
        """user_info"""
        user_infos = Config.read_user_info()
        phone_number = self.edt_phone_number.text()
        if len(phone_number) == 0 or phone_number not in user_infos.keys():
            QMessageBox(QMessageBox.Information, '通知', '手机号为空或用户不存在，无法修改').exec_()
            return
        user_info = user_infos[phone_number]
        portrait = user_info["portrait"]
        if portrait is None or len(portrait) == 0:
            QMessageBox(QMessageBox.Information, '修改失败', '头像未上传！').exec_()
        else:
            name_ = self.edt_name.text()
            if len(name_) > 0:
                name = name_
            else:
                QMessageBox(QMessageBox.Information, '通知', '用户名为空').exec_()
                return

            role_ = self.edt_role.text()
            if role_ in ["管理员", "用户"]:
                role = role_
            else:
                QMessageBox(QMessageBox.Information, '通知', '角色必须是"管理员"或"用户"').exec_()
                return

            phone_number_ = self.edt_phone_number.text()
            if len(phone_number_) > 0:
                phone_number = phone_number_
            else:
                QMessageBox(QMessageBox.Information, '通知', '手机号为空').exec_()
                return
            email_ = self.edt_mail.text()
            if len(email_) > 0:
                email = email_
            else:
                QMessageBox(QMessageBox.Information, '通知', '邮箱为空，默认使用原邮箱').exec_()
                return

            user_info["name"] = name
            user_info["phone_number"] = phone_number
            user_info["role"] = role
            user_info["email"] = email
            user_infos[phone_number] = user_info
            Config.write_user_info(user_infos)
            self.login_user_info_send_signal.emit(user_info)
            QMessageBox(QMessageBox.Information, '消息', '修改成功').exec_()

    def btn_change_pwd_action(self):
        """pwd_info"""
        phone = self.edt_phone_number.text()
        if len(phone) > 0:
            user_infos = Config.read_user_info()
            user_info = user_infos[phone]
            print("[run_personal_center.btn_change_pwd_action]user_info: ", user_info)
            old_pwd = self.edt_old_pwd.text()
            new_pwd = self.edt_new_pwd.text()
            confirm_pwd = self.edt_confirm_pwd.text()
            if len(old_pwd) == 0 or len(new_pwd) == 0 or len(confirm_pwd) == 0:
                QMessageBox(QMessageBox.Information, '修改失败', '新旧密码不能为空！').exec_()
            else:
                if old_pwd != user_info["password"]:
                    QMessageBox(QMessageBox.Information, '修改失败', '旧密码与原密码不相同，修改失败！').exec_()
                elif old_pwd == new_pwd:
                    QMessageBox(QMessageBox.Information, '修改失败', '新旧密码相同，修改失败！').exec_()
                elif new_pwd != confirm_pwd:
                    QMessageBox(QMessageBox.Information, '修改失败', '两次密码不一致，修改失败！').exec_()
                elif new_pwd == confirm_pwd:
                    password = new_pwd
                    user_info["password"] = password
                    user_infos[phone] = user_info
                    Config.write_user_info(user_infos)
                    QMessageBox(QMessageBox.Information, '消息', '重置成功').exec_()
        else:
            QMessageBox(QMessageBox.Information, '消息', '重置失败，用户信息不存在').exec_()

    def fill_received_data(self, user_info):
        """update_image"""
        print("[run_personal_center.fill_received_data]received user_info: ", user_info)
        name = user_info["name"]
        role = user_info["role"]
        email = user_info["email"]
        phone_number = user_info["phone_number"]
        portrait = user_info["portrait"]
        self.edt_name.setText(name)
        self.edt_role.setText(role)
        self.edt_mail.setText(email)
        self.edt_phone_number.setText(phone_number)
        if portrait != '':
            QImg = QImage(portrait)
            self.btn_update_image.setIcon(QIcon(QPixmap.fromImage(QImg).scaled(self.btn_update_image.size(),
                                                                               Qt.KeepAspectRatio,
                                                                               Qt.SmoothTransformation)))
        self.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = Ui_WgtPersonCenterAction()
    window.show()
    # window.showMaximized()    # 窗口最大化
    sys.exit(app.exec_())
