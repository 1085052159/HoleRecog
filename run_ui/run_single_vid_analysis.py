import datetime
import os
import shutil
import sys
from pathlib import Path
import time
import json

from PyQt5.QtCore import pyqtSignal, QUrl
from PyQt5.QtGui import QPixmap
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from recog_alg.hole_recog_thread import InferThread
from run_ui.run_single_hole_display import Ui_WgtSingleHoleDisplayAction
from run_ui.run_gen_report import Ui_WgtGenReportWinAction
from ui.my_video_surface import MyVideoSurface
from ui.single_vid_analysis import Ui_WgtSingleVidAnalysis
# try:
#     from run_ui.hole_recog_thread import InferThread
#     from run_ui.run_single_hole_display import Ui_WgtSingleHoleDisplayAction
#     from ui.my_video_surface import MyVideoSurface
#     from ui.vid_analysiss import Ui_WgtVIDAnalysis
# except:
#     from hole_recog_thread import InferThread
#     from run_single_hole_display import Ui_WgtSingleHoleDisplayAction
#     from my_video_surface import MyVideoSurface
#     from vid_analysiss import Ui_WgtVIDAnalysis
from utils_tools.JSONTools import Config
from utils_tools.img_util import ImageUtils


class Ui_WgtSingleVidAnalysisAction(QMainWindow, Ui_WgtSingleVidAnalysis):
    vid_name_received = pyqtSignal(str)
    login_user_info_received = pyqtSignal(dict)

    def __init__(self):
        QMainWindow.__init__(self)
        Ui_WgtSingleVidAnalysis.__init__(self)
        self.init_ui()

        self.btn_choose_vid.clicked.connect(self.btn_choose_vid_action)
        self.btn_resolve.clicked.connect(self.btn_resolve_action)
        self.btn_gen_report.clicked.connect(self.btn_gen_report_action)
        self.player = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.player.setVideoOutput(self.wgt_vid_frame_grab)
        self.wgt_vid_frame_grab.frameAvailable.connect(self.vid_frame_process)
        self.player.durationChanged.connect(self.duration_change_action)
        self.player.positionChanged.connect(self.position_change_action)
        self.btn_vid_play.clicked.connect(self.btn_vid_play_action)
        self.sli_vid_process_bar.sliderMoved.connect(self.slider_move_action)
        self.btn_add_hole.clicked.connect(self.btn_add_hole_action)

        self.img_util = ImageUtils()
        self.infer_thread = InferThread()
        self.infer_thread.infer_finished.connect(self.infer_finished_action)
        self.btn_resolve_clicked_count = 0
        self.hole_infos = {}
        self.hole_count = 0
        self.vid_name_received.connect(self.fill_data_by_vid_name)
        self.login_user_info_received.connect(self.init_login_user)

    def init_ui(self):
        self.setupUi(self)
        self.btn_gen_report.setEnabled(True)
        self.wgt_vid_display_setting.hide()
        self.wgt_vid_frame_grab = MyVideoSurface(self)
        self.lab_vid_display.hide()
        self.sco_holes_display.hide()

    def back2default_ui(self):
        self.btn_gen_report.setEnabled(True)
        self.wgt_vid_display_setting.hide()
        self.wgt_vid_choose_setting.show()

        self.lab_vid_display.hide()
        self.sco_holes_display.hide()
        self.lab_vid_name_display.clear()
        self.edt_well_name.clear()
        self.edt_well_inner_radius.clear()
        self.edt_vid_gen_time.clear()
        self.edt_cam_outer_radius.clear()
        self.edt_vid_gen_place.clear()
        self.edt_engineer.clear()

        self.clear_gid_holes_display()
        self.lab_hint_hole_recog.setText("孔洞识别")
        self.lab_hint_start_resolve.show()
        self.btn_resolve.setText("开始解析")

    def btn_choose_vid_action(self):
        """
        选择文件按钮点击事件
        1. 打开文件选择器/拖动
        2. 隐藏提示信息
        3. 显示视频
        """
        file_url, _ = QFileDialog.getOpenFileUrl(self, "选择视频文件", filter="*.mp4;*.avi;*.mkv;*.mov")
        filename = file_url.fileName()
        if len(filename) == 0:
            QMessageBox(QMessageBox.Critical, '错误', '请选择视频文件').exec_()
            return
        file_path = file_url.path()[1:]
        vid_dst_path = "%s/%s" % (Config.videos_save_path(), filename)
        try:
            shutil.copyfile(file_path, vid_dst_path)
        except:
            pass
        self.play_video(vid_dst_path, filename)

    def play_video(self, file_url, filename):
        """play_video"""
        self.file_url = file_url
        self.lab_vid_name_display.setText(filename)
        self.wgt_vid_choose_setting.hide()
        self.wgt_vid_display_setting.show()
        self.lab_vid_display.show()
        self.player.setMedia(QMediaContent(QUrl(file_url)))
        self.player.pause()

    def btn_vid_play_action(self):
        """
        播放按钮点击事件
        """
        state = self.player.state()
        if state == 0:
            self.btn_vid_play.setStyleSheet("image: url(:/image/暂停.png);")
            self.player.play()
        elif state == 1:
            self.btn_vid_play.setStyleSheet("image: url(:/image/播放.png);")
            self.player.pause()
        elif state == 2:
            self.btn_vid_play.setStyleSheet("image: url(:/image/暂停.png);")
            self.player.play()

    def duration_change_action(self, d):
        """
        获取视频总时长后的点击事件
        """
        self.sli_vid_process_bar.setRange(0, d)
        self.sli_vid_process_bar.setEnabled(True)
        self.lab_vid_total_length.setText(time.strftime("%H:%M:%S", time.gmtime(d // 1000)))

    def position_change_action(self, p):
        """
        获取进度条位置后的点击事件
        """
        self.sli_vid_process_bar.setValue(p)
        self.lab_vid_cur_length.setText(time.strftime("%H:%M:%S", time.gmtime(p // 1000)))
        self.player.setPosition(p)
        if p == self.sli_vid_process_bar.maximum():
            self.btn_vid_play.setStyleSheet("image: url(:/image/播放.png);")
            self.sli_vid_process_bar.setValue(0)
            self.player.setPosition(0)

    def slider_move_action(self, v):
        self.player.setPosition(v)
        self.lab_vid_cur_length.setText(time.strftime("%H:%M:%S", time.gmtime(v // 1000)))

    def vid_frame_process(self, image):
        self.lab_vid_display.setScaledContents(True)
        self.lab_vid_display.setPixmap(QPixmap.fromImage(image))
        self.cur_image = image

    def wgt_single_hole_action_btn_delete(self, key):
        if key in self.hole_infos.keys():
            del self.hole_infos[key]
        self.print_hole_infos(self.hole_infos)
        self.update_gid_holes_display(self.hole_infos)

    def wgt_single_hole_action_double_click(self, hole_infos):
        self.hole_infos.update(hole_infos)
        self.print_hole_infos(self.hole_infos)

    def clear_gid_holes_display(self):
        count = self.gid_holes_display.count()  # 当前遍历的数量
        # 清空gid_holes_display
        if count > 0:
            item_list = list(range(count))
            item_list.reverse()  # 倒序删除，避免影响布局顺序
            for i in item_list:
                item = self.gid_holes_display.itemAt(i)
                self.gid_holes_display.removeItem(item)
                if item.widget():
                    item.widget().deleteLater()

    def update_gid_holes_display(self, hole_infos):
        self.clear_gid_holes_display()

        count = 0  # 当前遍历的数量
        line = 2  # 一行显示的数量
        for key in sorted(list(hole_infos.keys())):
            hole_info = hole_infos[key]
            single_hole = Ui_WgtSingleHoleDisplayAction()
            single_hole.draw_hole_info(hole_info)
            single_hole.btn_delete_signal.connect(self.wgt_single_hole_action_btn_delete)
            single_hole.data2vid_analysis_signal.connect(self.wgt_single_hole_action_double_click)
            self.gid_holes_display.addWidget(single_hole, count // line, count % line)
            count += 1
        self.lab_hint_hole_recog.setText("孔洞识别 (共识别到%d个孔洞)" % (count))
        self.lab_hint_start_resolve.hide()
        self.sco_holes_display.show()

    def btn_add_hole_action(self):
        selected_cur_image = self.img_util.QImage2bgr_img(self.cur_image)
        cur_count = self.hole_count + 1
        hole_infos = self.img_util.gen_hole_infos(selected_cur_image, cur_count=cur_count)
        self.hole_count += len(hole_infos)
        if len(hole_infos) == 0:
            return
        self.hole_infos.update(hole_infos)
        self.print_hole_infos(self.hole_infos)
        self.update_gid_holes_display(self.hole_infos)

    def get_vid_info(self):
        if (not hasattr(self, "file_url")) or len(self.file_url) == 0:
            QMessageBox(QMessageBox.Critical, '错误', '请选择视频文件').exec_()
            return
        well_name = self.edt_well_name.toPlainText()
        if len(well_name.strip().replace(" ", "")) == 0:
            QMessageBox(QMessageBox.Critical, '错误', '请输入井号名称').exec_()
            return
        well_inner_radius = self.edt_well_inner_radius.toPlainText()
        if len(well_inner_radius.strip().replace(" ", "")) == 0:
            QMessageBox(QMessageBox.Critical, '错误', '请输入井号内径').exec_()
            return
        vid_gen_time = self.edt_vid_gen_time.toPlainText()
        if len(vid_gen_time.strip().replace(" ", "")) == 0:
            QMessageBox(QMessageBox.Critical, '错误', '请输入视频生成时间').exec_()
            return
        cam_outer_radius = self.edt_cam_outer_radius.toPlainText()
        if len(cam_outer_radius.strip().replace(" ", "")) == 0:
            QMessageBox(QMessageBox.Critical, '错误', '请输入摄像工具外径').exec_()
            return
        vid_gen_place = self.edt_vid_gen_place.toPlainText()
        if len(vid_gen_place.strip().replace(" ", "")) == 0:
            QMessageBox(QMessageBox.Critical, '错误', '请输入视频生成地点').exec_()
            return
        engineer = self.edt_engineer.toPlainText()
        if len(engineer.strip().replace(" ", "")) == 0:
            QMessageBox(QMessageBox.Critical, '错误', '请输入工程师名称').exec_()
            return
        vid_info = {
            "vid_path": self.file_url,
            "well_name": well_name,
            "well_inner_radius": well_inner_radius,
            "vid_gen_time": vid_gen_time,
            "cam_outer_radius": cam_outer_radius,
            "vid_gen_place": vid_gen_place,
            "engineer": engineer,
        }
        return vid_info

    def print_hole_infos(self, hole_infos):
        for key in hole_infos.keys():
            print("[run_single_vid_analysis.print_hole_infos]", key, hole_infos[key]["hole_id"],
                  hole_infos[key]["height_pixel"], hole_infos[key]["width_pixel"],
                  hole_infos[key]["area"])

    def infer_finished_action(self, hole_infos):
        if len(hole_infos) == 0:
            QMessageBox(QMessageBox.Critical, "警告", "未识别到孔洞").exec_()
            self.btn_resolve.setText("开始解析")
        else:
            for key, value in hole_infos.items():
                self.hole_count += 1
                value["hole_id"] = "孔洞%d" % self.hole_count
                self.hole_infos["hole%04d" % self.hole_count] = value
            self.print_hole_infos(self.hole_infos)
            self.update_gid_holes_display(self.hole_infos)
        self.btn_resolve.setEnabled(True)

    def btn_resolve_action(self):
        vid_info = self.get_vid_info()
        if vid_info is not None:
            if self.btn_resolve_clicked_count > 0:
                self.clear_gid_holes_display()
            self.btn_resolve.setText("重新解析")
            self.btn_resolve.setEnabled(False)
            save_path = Config.hole_recog_save_path()
            print("[run_single_vid_analysis.btn_resolve_action]recog alg save_path: ", save_path)
            print("[run_single_vid_analysis.btn_resolve_action]vid info: ", vid_info)
            self.infer_thread.set_params(vid_info["vid_path"], batch_size=128, device="cuda",
                                         save_path=save_path, show_temp=True)
            self.infer_thread.start()
            QMessageBox(QMessageBox.Warning, "警告", "正在分析中,请不要点击界面").exec_()
            self.btn_resolve_clicked_count += 1

    def btn_gen_report_action(self):
        """
        生成报告
        :return:
        """
        if self.hole_infos is None or len(self.hole_infos) == 0:
            QMessageBox(QMessageBox.Critical, '错误', '未获取到解析结果，无法生成报告').exec_()
        else:
            vid_info = self.get_vid_info()
            print("[run_single_vid_analysis.btn_gen_report_action]vid_info: ", vid_info)
            if vid_info is not None:
                single_vid_data = self.get_single_vid_data(self.hole_infos, vid_info)
                file_name = str(Path(self.file_url).name).split('.')[0]
                vid_datas = Config.read_vid_info()
                if vid_datas is None:
                    vid_datas = {file_name: single_vid_data}
                else:
                    vid_datas[file_name] = single_vid_data
                Config.write_vid_info(vid_datas)
                self.show_report_window(single_vid_data)

    def show_report_window(self, single_vid_data):
        self.gen_report_window = Ui_WgtGenReportWinAction()
        self.gen_report_window.single_vid_info_received_signal.emit(single_vid_data)
        self.gen_report_window.show()

    def get_single_vid_data(self, hole_infos, vid_info):
        """write_base_info_file"""
        val = {}
        resolve_person = self.user_info["name"] if hasattr(self, "user_info") and self.user_info is not None and len(
            self.user_info) > 0 else ""
        vid_info["resolve_person"] = resolve_person
        vid_info["resolve_time"] = self.edt_vid_gen_time.toPlainText()
        vid_info["hole_number"] = str(len(hole_infos))  # "孔洞数量"
        val["base_infos"] = vid_info
        val["hole_infos"] = hole_infos
        return val

    def get_cur_time(self):
        now = datetime.datetime.now()
        year = now.year
        month = now.month
        day = now.day
        text = "{}-{}-{}".format(year, month, day)
        return text

    def set_current_time_text(self):
        """set_current_time_text"""
        time = self.edt_vid_gen_time.toPlainText()
        if time == '':
            text = self.get_cur_time()
            self.edt_vid_gen_time.setText(text)

    def set_user_info(self, vid_info):
        """set_user_info"""
        self.edt_vid_gen_time.setPlainText(vid_info["vid_gen_time"])
        self.edt_engineer.setPlainText(vid_info["engineer"])
        self.edt_vid_gen_place.setPlainText(vid_info["vid_gen_place"])
        self.edt_well_name.setPlainText(vid_info["well_name"])
        self.edt_cam_outer_radius.setPlainText(vid_info["cam_outer_radius"])
        self.edt_well_inner_radius.setPlainText(vid_info["well_inner_radius"])

    def fill_received_data(self, single_vid_data):
        base_infos = single_vid_data["base_infos"]

        file_url = base_infos["vid_path"]
        well_name = base_infos["well_name"]
        well_inner_radius = base_infos["well_inner_radius"]
        vid_gen_time = base_infos["vid_gen_time"]
        cam_outer_radius = base_infos["cam_outer_radius"]
        vid_gen_place = base_infos["vid_gen_place"]
        engineer = base_infos["engineer"]
        filename = os.path.basename(file_url).split(".")[0]
        self.play_video(file_url, filename)
        self.edt_well_name.setPlainText(well_name)
        self.edt_well_inner_radius.setPlainText(well_inner_radius)
        self.edt_vid_gen_time.setPlainText(vid_gen_time)
        self.edt_cam_outer_radius.setPlainText(cam_outer_radius)
        self.edt_vid_gen_place.setPlainText(vid_gen_place)
        self.edt_engineer.setPlainText(engineer)

        self.hole_infos = single_vid_data["hole_infos"]
        self.hole_count = len(self.hole_infos)
        self.print_hole_infos(self.hole_infos)
        self.update_gid_holes_display(self.hole_infos)

    def fill_data_by_vid_name(self, vid_name):
        print("[run_single_vid_analysis.fill_data_by_vid_name]vid_name: ", vid_name)
        vid_datas = Config.read_vid_info()
        single_vid_data = vid_datas[vid_name]
        self.fill_received_data(single_vid_data)

    def init_login_user(self, user_info):
        print("[run_single_vid_analysis.init_login_user]init_login_user: ", user_info)
        self.user_info = user_info


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # MyWin = DemoAction()
    MyWin = Ui_WgtSingleVidAnalysisAction()
    MyWin.show()
    sys.exit(app.exec())
