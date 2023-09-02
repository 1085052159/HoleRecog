# !/usr/bin/env python
# _*_ coding: utf-8 _*_
import sys
from pathlib import Path

from run_ui.run_gen_report import Ui_WgtGenReportWinAction
from run_ui.run_single_vid_analysis import Ui_WgtSingleVidAnalysisAction
from utils_tools.JSONTools import Config
from PyQt5.QtCore import Qt, pyqtSignal
from ui.video_analysis_result_manage import Ui_WgtVideoAnalysisResultManage
from PyQt5.QtWidgets import QWidget, QApplication, QMessageBox, QTableWidgetItem, QHBoxLayout, QPushButton, QHeaderView


class Ui_WgtVideoAnalysisResultManageAction(QWidget, Ui_WgtVideoAnalysisResultManage):
    login_user_info_received = pyqtSignal(dict)

    def __init__(self):
        QWidget.__init__(self)
        Ui_WgtVideoAnalysisResultManage.__init__(self)
        self.setupUi(self)
        self.setAttribute(Qt.WA_StyledBackground, True)  # 激活背景

        self.count = 0
        self.page = 1
        self.comboBox_page_count.addItems(['12', '14', '16'])
        self.comboBox_page_count.setCurrentIndex(1)
        self.pageValue = int(self.comboBox_page_count.currentText())  # 一页显示条数
        self.nCurScroller = 0  # 翻页时的当时滑动条位置
        self.tableWidget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.tableWidget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.setup_ui()
        self._initUI()

    def _initUI(self):
        """
        初始化窗口设置
        """
        self.setWindowFlags(Qt.FramelessWindowHint)  # 无边框

    def setup_ui(self):
        self.show_vid_infos(None)
        self.btn_query.clicked.connect(self.btn_query_action)
        self.btn_pre_page.clicked.connect(self.pre_page)
        self.btn_next_page.clicked.connect(self.next_page)
        self.comboBox_page_count.currentTextChanged[str].connect(self.current_page)
        self.login_user_info_received.connect(self.init_login_user)

    def show_vid_infos(self, vid_infos_data):
        if vid_infos_data is None or len(vid_infos_data) == 0:
            vid_infos_data = Config.read_vid_info()
        if vid_infos_data is None or len(vid_infos_data) == 0:
            return
        self.tableWidget.clearContents()
        self.tableWidget.setRowCount(0)
        for vid_name in vid_infos_data.keys():
            info = vid_infos_data[vid_name]
            base_infos = info["base_infos"]
            well_name = base_infos["well_name"]
            vid_gen_time = base_infos["vid_gen_time"]
            vid_gen_place = base_infos["vid_gen_place"]
            engineer = base_infos["engineer"]
            resolve_person = base_infos["resolve_person"]
            resolve_time = base_infos["resolve_time"]
            hole_number = base_infos["hole_number"]

            try:
                row_cnt = self.tableWidget.rowCount()
                self.tableWidget.insertRow(row_cnt)  # 尾部插入一行新行表格
                item1 = QTableWidgetItem(well_name)  # 井号名称
                item2 = QTableWidgetItem(vid_name)  # 文件名称
                item3 = QTableWidgetItem(vid_gen_time)  # 视频生成时间
                item4 = QTableWidgetItem(vid_gen_place)  # 视频生成地点
                item5 = QTableWidgetItem(engineer)  # 工程师(用户输入)
                item6 = QTableWidgetItem(resolve_person)  # 解析人(当前登录用户)
                item7 = QTableWidgetItem(resolve_time)  # 解析时间
                item8 = QTableWidgetItem(hole_number)  # 孔洞数量
                self.tableWidget.setItem(row_cnt, 0, item1)
                self.tableWidget.setItem(row_cnt, 1, item2)
                self.tableWidget.setItem(row_cnt, 2, item3)
                self.tableWidget.setItem(row_cnt, 3, item4)
                self.tableWidget.setItem(row_cnt, 4, item5)
                self.tableWidget.setItem(row_cnt, 5, item6)
                self.tableWidget.setItem(row_cnt, 6, item7)
                self.tableWidget.setItem(row_cnt, 7, item8)
                self.tableWidget.setCellWidget(row_cnt, 8, self.button_for_row())
            except Exception as e:
                print(f"Error for appending table list. 表格异常： {e}")

        total_num = len(vid_infos_data)
        page = total_num // self.pageValue + int(total_num % self.pageValue > 0)
        self.label_total_page.setText(f'共{page}页')
        self.label_total_count.setText(f'共{total_num}条')

    def btn_query_action(self):
        """
        查询
        dict_values([{'base_infos': {'vid_path': '文件名称', 'well_name': '井号名称', 'well_inner_radius': '井筒内径', 'vid_gen_time': '视频生成时间', 'cam_outer_radius': '摄像工具外径', 'vid_gen_place': '视频生成地点', 'engineer': '工程师(用户输入)', 'resolve_person': '解析人(当前登录用户)', 'resolve_time': '解析时间', 'hole_number': '孔洞数量'}}},
        :return:
        """
        data = Config.read_vid_info()
        if data is not None and len(data) > 0:
            query_data = {}
            valid_attr_num = 0  # 有效的查询属性
            well_name, vid_path, vid_gen_time, vid_gen_place, engineer, resolve_person, resolve_time = self.get_query_attr()
            for key in data.keys():
                query_num = 0
                base_infos = data[key]["base_infos"]
                if len(well_name) > 0:
                    valid_attr_num += 1
                    if well_name in base_infos["well_name"]:
                        query_num += 1
                if len(vid_path) > 0:
                    valid_attr_num += 1
                    if vid_path in base_infos["vid_path"]:
                        query_num += 1
                if len(vid_gen_time) > 0:
                    valid_attr_num += 1
                    if vid_gen_time in base_infos["vid_gen_time"]:
                        query_num += 1
                if len(engineer) > 0:
                    valid_attr_num += 1
                    if engineer in base_infos["engineer"]:
                        query_num += 1
                if len(resolve_person) > 0:
                    valid_attr_num += 1
                    if resolve_person in base_infos["resolve_person"]:
                        query_num += 1
                if len(resolve_time) > 0:
                    valid_attr_num += 1
                    if resolve_time in base_infos["resolve_time"]:
                        query_num += 1

                if query_num == valid_attr_num:
                    query_data[key] = data[key]
            if len(query_data) > 0:
                self.show_vid_infos(query_data)
            else:
                QMessageBox(QMessageBox.Critical, '警告', '无满足查询条件的数据').exec_()
        else:
            QMessageBox(QMessageBox.Critical, '警告', '无视频解析结果，请先上传').exec_()

    def get_query_attr(self):
        """get_query_attr"""
        engineer = self.ledt_engineer.text()
        resolve_time = self.ledt_resolve_time.text()
        vid_gen_place = self.ledt_vid_gen_place.text()
        well_name = self.ledt_well_name.text()
        resolve_person = self.ledt_resolve_person.text()
        vid_gen_time = self.ledt_vid_gen_time.text()
        vid_path = self.ledt_vid_path.text()
        return well_name, vid_path, vid_gen_time, vid_gen_place, engineer, resolve_person, resolve_time

    def button_for_row(self):
        widget = QWidget(self)
        # 查询
        btn_display = QPushButton()
        btn_display.setText('查询')
        btn_display.setMinimumSize(35, 28)
        btn_display.setMaximumSize(35, 28)
        btn_display.setStyleSheet('''text-align: center;
        color: rgb(255, 255, 255);
background-color: rgb(19, 89, 245);
border:0px solid rgb(19, 89, 245);
           height: 30px;
           border-style: outset;
           font: 13px;''')
        # 修改
        btn_edt = QPushButton()
        btn_edt.setText('修改')
        btn_edt.setMinimumSize(35, 28)
        btn_edt.setMaximumSize(35, 28)
        btn_edt.setStyleSheet('''text-align: center;
color: rgb(255, 255, 255);
background-color: rgb(253, 137, 50);
border:0px solid rgb(253, 137, 50);
           height: 30px;
           border-style: outset;
           font: 13px;''')
        # 删除
        btn_del = QPushButton()
        btn_del.setText('删除')
        btn_del.setMinimumSize(35, 28)
        btn_del.setMaximumSize(35, 28)
        btn_del.setStyleSheet('''text-align: center;
           color: rgb(0, 0, 0);
background-color: rgb(230, 230, 230);
border:1px solid rgb(230, 230, 230);
           height: 30px;
           border-style: outset;
           font: 13px;''')
        btn_del.clicked.connect(self.btn_delete_action)
        btn_display.clicked.connect(self.btn_display_action)
        btn_edt.clicked.connect(self.btn_edt_action)

        hLayout = QHBoxLayout()
        hLayout.addWidget(btn_display)
        hLayout.addWidget(btn_edt)
        hLayout.addWidget(btn_del)
        hLayout.setContentsMargins(0, 0, 0, 0)
        hLayout.setSpacing(0)
        widget.setLayout(hLayout)
        return widget

    def btn_edt_action(self):
        """btn_edit_vid_analysis"""
        button = self.sender()
        cell_widget = self.tableWidget.indexAt(button.parent().pos())
        if cell_widget.isValid():
            row = cell_widget.row()
            vid_name = self.tableWidget.item(row, 1).text()
            print("[run_video_analysis_result_manage.btn_edt_action]edit vid_name: ", vid_name)
            self.single_vid_analysis = Ui_WgtSingleVidAnalysisAction()
            self.single_vid_analysis.vid_name_received.emit(vid_name)
            self.single_vid_analysis.login_user_info_received.emit(self.user_info)
            self.single_vid_analysis.show()

    def btn_display_action(self):
        """btn_checked_item"""
        button = self.sender()
        cell_widget = self.tableWidget.indexAt(button.parent().pos())
        if cell_widget.isValid():
            row = cell_widget.row()
            vid_name = self.tableWidget.item(row, 1).text()
            print("display report: ", vid_name)
            self.gen_report_window = Ui_WgtGenReportWinAction()
            self.gen_report_window.vid_name_received_signal.emit(vid_name)
            self.gen_report_window.show()

    def btn_delete_action(self):
        """btn_delete_row"""
        button = self.sender()
        cell_widget = self.tableWidget.indexAt(button.parent().pos())
        if cell_widget.isValid():
            row = cell_widget.row()
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
                key = self.tableWidget.item(row, 1).text()
                data = Config.read_vid_info()
                new_data = Config.delete_json_data(data, key)
                Config.write_vid_info(new_data)
                self.tableWidget.removeRow(row)  # 删除指定行

    def init_login_user(self, user_info):
        print("[run_video_analysis_result_manage.py.init_login_user]init_login_user: ", user_info)
        self.user_info = user_info

    def current_page(self, text):
        """current_page"""
        self.label_cur_page.setText('1')
        self.tableWidget.verticalScrollBar().setSliderPosition(0)
        self.count = int(self.label_total_count.text()[1:-1])
        self.pageValue = int(text)
        page = self.page + self.count // self.pageValue
        self.label_total_page.setText(f'共{page}页')

    def pre_page(self):
        """点击上一页信号"""
        self.page_controller(["上一页", self.label_cur_page.text()])

    def next_page(self):
        """点击下一页信号"""
        self.page_controller(["下一页", self.label_cur_page.text()])

    def showTotalPage(self):
        """返回当前总页数"""
        return int(self.label_total_page.text()[1:-1])

    def page_controller(self, signal):
        """信号处理"""
        total_page = self.showTotalPage()
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

    window = Ui_WgtVideoAnalysisResultManageAction()
    window.show()
    # window.showMaximized()    # 窗口最大化
    sys.exit(app.exec_())
