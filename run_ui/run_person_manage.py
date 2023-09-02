# !/usr/bin/env python
# _*_ coding: utf-8 _*_
import sys
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QIcon, QPixmap
from run_ui.run_add_person_info import Ui_DigAddPersonInfoAction
from PyQt5.QtWidgets import QWidget, QApplication, QMessageBox, QHeaderView, QDialog, QTableWidgetItem, QPushButton, \
    QHBoxLayout

from run_ui.run_personal_center import Ui_WgtPersonCenterAction
from ui.person_manage import Ui_WgtPersonManage
from utils_tools.JSONTools import Config


class Ui_WgtPersonManageAction(QWidget, Ui_WgtPersonManage):
    def __init__(self):
        QWidget.__init__(self)
        Ui_WgtPersonManage.__init__(self)
        self.setupUi(self)
        self.setAttribute(Qt.WA_StyledBackground, True)  # 激活背景
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.count = 0
        self.page = 1
        self.line_num = 9
        self.nCurScroller = 0  # 翻页时的当时滑动条位置
        self.comboBox_page_count.addItems(['15', '17', '19'])
        self.comboBox_page_count.setCurrentIndex(1)
        self.pageValue = int(self.comboBox_page_count.currentText())  # 一页显示条数
        self.setup_ui()
        self._initUI()
        self.init_action()

    def init_action(self):
        self.btn_query.clicked.connect(self.btn_query_action)
        self.btn_add_person.clicked.connect(self.btn_add_person_action)
        self.btn_pre_page.clicked.connect(self.btn_pre_page_action)
        self.btn_next_page.clicked.connect(self.btn_next_page_action)

    def _initUI(self):
        """
        初始化窗口设置
        """
        self.setWindowFlags(Qt.FramelessWindowHint)  # 无边框

    def setup_ui(self):
        self.show_user_info(None)
        self.tableWidget.horizontalHeader().setCascadingSectionResizes(False)
        self.tableWidget.verticalHeader().setVisible(False)
        self.comboBox_page_count.currentTextChanged[str].connect(self.current_page)

    def show_user_info(self, user_datas):
        if user_datas is None or len(user_datas) == 0:
            user_datas = Config.read_user_info()
        if user_datas is None or len(user_datas) == 0:
            return
        self.tableWidget.clearContents()
        self.tableWidget.setRowCount(0)

        for key in user_datas.keys():
            data = user_datas[key]
            name = data['name']
            post = data['role']
            mail = data['email']
            phone = data['phone_number']
            state = data['state']
            portrait = data['portrait']
            try:
                row_cnt = self.tableWidget.rowCount()  # 返回当前行数（尾部）
                self.tableWidget.insertRow(row_cnt)  # 尾部插入一行新行表格
                item1 = QTableWidgetItem(name)
                item2 = QTableWidgetItem(post)
                item3 = QTableWidgetItem(mail)
                item4 = QTableWidgetItem(phone)
                self.tableWidget.setItem(row_cnt, 0, item1)  # 最后，将(行，列，内容)配置
                self.tableWidget.setItem(row_cnt, 1, item2)  # 最后，将(行，列，内容)配置
                self.tableWidget.setItem(row_cnt, 2, item3)  # 最后，将(行，列，内容)配置
                self.tableWidget.setItem(row_cnt, 3, item4)  # 最后，将(行，列，内容)配置

                self.tableWidget.setCellWidget(row_cnt, 4, self.btn_select())  # 最后，将(行，列，内容)配置
                self.tableWidget.setCellWidget(row_cnt, 5, self.button_for_row(state))
            except Exception as e:
                print(f"[run_person_manage.show_user_info]Error for appending table list. 表格异常： {e}")

        total_num = len(user_datas)
        page = total_num // self.pageValue + int(total_num % self.pageValue > 0)
        self.label_total_page.setText(f'共{page}页')
        self.label_total_count.setText(f'共{total_num}条')

    def btn_query_action(self):
        """add_query"""
        phone = self.edt_phone.text()
        if len(phone) > 0:
            data = Config.read_user_info()
            if data is None or len(data) == 0:
                QMessageBox(QMessageBox.Critical, '警告', '无用户信息，请先添加用户').exec_()
            else:
                query_data = {key: val for key, val in data.items() if phone in key}
                print("[run_person_manage.btn_query_action]query_data: ", query_data)
                if len(query_data) == 0:
                    QMessageBox(QMessageBox.Critical, '警告', '无满足查询条件的数据').exec_()
                else:
                    self.show_user_info(query_data)
        else:
            # QMessageBox(QMessageBox.Critical, '警告', '无满足查询条件的数据').exec_()
            self.show_user_info(None)

    def btn_add_person_action(self):
        self.add_win = Ui_DigAddPersonInfoAction()
        self.add_win.add_user_info_send_signal.connect(self.fill_received_user_info)
        self.add_win.show()

    def fill_received_user_info(self, user_info):
        """add_person_info
        user_info = {
            "name": name,
            "password": password,
            "role": post,
            "email": mail,
            "phone_number": phone,
            "state": self.state,
            "portrait": self.portrait
        } or bool
        """
        print("[run_person_manage.fill_received_user_info]reveived user_info: ", user_info)
        if user_info is None or user_info is False or len(user_info) == 0:
            self.show_user_info(None)
        else:
            data = Config.read_user_info()
            phone_number = user_info["phone_number"]
            data[phone_number] = user_info
            Config.write_user_info(data)
            self.show_user_info(data)

    def btn_select(self):
        """btn_select"""
        btn_state = QPushButton()
        btn_state.setGeometry(QRect(190, 160, 31, 21))
        btn_state.setStyleSheet("")
        btn_state.setText("已启动")
        icon = QIcon()
        icon.addPixmap(QPixmap(":/image/已启动.png"), QIcon.Normal, QIcon.Off)
        icon.addPixmap(QPixmap(":/image/已禁用.png"), QIcon.Normal, QIcon.On)
        btn_state.setIcon(icon)
        btn_state.setCheckable(True)
        btn_state.setAutoRepeat(True)
        btn_state.setAutoExclusive(False)
        btn_state.setObjectName("pushButton")
        btn_state.setStyleSheet('background-color: rgb(255, 255, 255);\nborder:none;')
        btn_state.clicked.connect(lambda checked: self.button_checked(btn_state, checked))
        return btn_state

    def button_for_row(self, state):
        widget = QWidget(self)
        # 修改
        self.btn_edt = QPushButton()
        self.btn_edt.setObjectName(state)
        self.btn_edt.setStyleSheet('''text-align: center;
           background-color: rgb(255, 255, 255);
           height: 30px;
           border-style: outset;
           font: 13px;''')
        icon1 = QIcon()
        icon1.addPixmap(QPixmap(":/image/编辑.png"), QIcon.Normal, QIcon.Off)
        self.btn_edt.setIcon(icon1)
        # 删除
        self.btn_del = QPushButton()
        self.btn_del.setStyleSheet('''text-align: center;
           background-color: rgb(255, 255, 255);
           height: 30px;
           border-style: outset;
           font: 13px;''')
        icon2 = QIcon()
        icon2.addPixmap(QPixmap(":/image/删除.png"), QIcon.Normal, QIcon.Off)
        # icon2.addPixmap(QPixmap(":/image/删除.png"), QIcon.Normal, QIcon.On)
        self.btn_del.setIcon(icon2)
        self.btn_del.clicked.connect(self.btn_delete_row)
        self.btn_edt.clicked.connect(self.btn_edit_item)

        hLayout = QHBoxLayout()
        hLayout.addWidget(self.btn_edt)
        hLayout.addWidget(self.btn_del)
        hLayout.setContentsMargins(5, 2, 5, 2)
        widget.setLayout(hLayout)
        return widget

    def btn_edit_item(self):
        """btn_edit_item"""
        button = self.sender()
        cell_widget = self.tableWidget.indexAt(button.parent().pos())
        if cell_widget.isValid():
            row = cell_widget.row()
            # name = self.tableWidget.item(row, 0).text()
            # post = self.tableWidget.item(row, 1).text()
            # mail = self.tableWidget.item(row, 2).text()
            # state = self.tableWidget.cellWidget(row, 4).text()
            phone = self.tableWidget.item(row, 3).text()
            # self.edit_signal.emit([name, post, mail, phone, row, state, self.portrait])
            user_infos = Config.read_user_info()
            edited_user_info = user_infos[phone]
            self.personal_center = Ui_WgtPersonCenterAction()
            self.personal_center.login_user_info_received_signal.emit(edited_user_info)

    def btn_delete_row(self):
        """btn_delete_row"""
        button = self.sender()
        cell_widget = self.tableWidget.indexAt(button.parent().pos())
        if cell_widget.isValid():
            row = cell_widget.row()
            self.confirm_person_info(self.tableWidget, row)  # 删除指定行

    def del_json_data(self, key):
        """del_json_data"""
        data = Config.read_user_info()
        new_data = Config.delete_json_data(data, key)
        Config.write_user_info(new_data)

    def confirm_person_info(self, tableWidget, row):
        self.box = QMessageBox(QMessageBox.Icon(0), "确定删除", "<h3>确定删除当前行数据吗？</h3>")
        self.box.setObjectName('widget')
        self.box.setWindowFlags(Qt.FramelessWindowHint)
        qyes = self.box.addButton(self.box.tr("确定删除"), QMessageBox.YesRole)
        qno = self.box.addButton(self.box.tr("取消"), QMessageBox.NoRole)
        self.box.setStyleSheet(
            'QWidget#widget{background-color:#ffffff;border:2px solid rgb(55, 55, 235);border-radius:3.2px;}\nQPushButton{border:2px solid rgb(55, 55, '
            '235);min-width:68px;border-radius:3.2px;}')
        self.box.exec_()
        if self.box.clickedButton() == qyes:
            key = self.tableWidget.item(row, 3).text()
            tableWidget.removeRow(row)
            self.del_json_data(key)
        else:
            return

    def button_checked(self, btn, checked):
        """button_checked"""
        if checked:
            text = '已禁用'
            btn.setText(text)
        else:
            text = '已启动'
            btn.setText(text)

    def btn_pre_page_action(self):
        """点击上一页信号"""
        self.page_controller(["上一页", self.label_cur_page.text()])

    def btn_next_page_action(self):
        """点击下一页信号"""
        self.page_controller(["下一页", self.label_cur_page.text()])

    def current_page(self, text):
        """current_page"""
        self.label_cur_page.setText('1')
        self.tableWidget.verticalScrollBar().setSliderPosition(0)
        self.count = int(self.label_total_count.text()[1:-1])
        self.pageValue = int(text)
        page = self.page + self.count // self.pageValue
        self.label_total_page.setText(f'共{page}页')

    def show_total_page(self):
        """返回当前总页数"""
        return int(self.label_total_page.text()[1:-1])

    def page_controller(self, signal):
        """信号处理"""
        total_page = self.show_total_page()
        cur_page = int(signal[1])
        if "上一页" == signal[0]:
            if 1 == cur_page:
                QMessageBox.information(self, "提示", "已经是第一页了", QMessageBox.Yes)
                return
            self.label_cur_page.setText(str(cur_page - 1))
            self.tableWidget.verticalScrollBar().setSliderPosition(self.nCurScroller - self.pageValue)
        elif "下一页" == signal[0]:
            if total_page == cur_page:
                QMessageBox.information(self, "提示", "已经是最后一页了", QMessageBox.Yes)
                return
            self.label_cur_page.setText(str(cur_page + 1))
            self.tableWidget.verticalScrollBar().setSliderPosition(self.nCurScroller + self.pageValue)
        self.nCurScroller = self.tableWidget.verticalScrollBar().value()  # 获得当前scroller值


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = Ui_WgtPersonManageAction()
    window.show()
    # window.showMaximized()    # 窗口最大化
    sys.exit(app.exec_())
