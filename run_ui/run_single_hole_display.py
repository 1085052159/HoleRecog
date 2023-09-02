import sys
import time

import cv2
from PyQt5 import QtGui
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox

from utils_tools.img_util import ImageUtils
from run_ui.run_single_hole_update import Ui_WgtSingleHoleUpdateAction
from ui.single_hole_display import Ui_WgtSingleHoleDisplay

class Ui_WgtSingleHoleDisplayAction(QWidget, Ui_WgtSingleHoleDisplay):
    btn_delete_signal = pyqtSignal(str)
    data2vid_analysis_signal = pyqtSignal(dict)  # 返回给父页面，用于更新父页面的数据
    data2single_hole_update_signal = pyqtSignal(dict)  # 将数据传递给孔洞更新界面

    def __init__(self):
        QWidget.__init__(self)
        Ui_WgtSingleHoleDisplay.__init__(self)
        self.init_ui()
        self.img_util = ImageUtils()
        self.hole_info = {}
        self.btn_delete.clicked.connect(self.btn_delete_action)
        self.single_hole_update = Ui_WgtSingleHoleUpdateAction()
        self.single_hole_update.data2_single_hole_display_signal.connect(self.draw_hole_info)
        self.data2single_hole_update_signal.connect(self.single_hole_update.draw_hole_info)

    def init_ui(self):
        self.setFixedSize(400, 240)
        self.setupUi(self)

    def mouseDoubleClickEvent(self, a0: QtGui.QMouseEvent):
        hole_id = self.lab_hole_id.text()
        # hole_infos's key
        key = "hole%04d" % int(hole_id.replace("孔洞", ""))
        hole_infos = {key: self.hole_info}
        self.data2vid_analysis_signal.emit(hole_infos)
        self.single_hole_update.show()
        self.data2single_hole_update_signal.emit(self.hole_info)

    def btn_delete_action(self):
        reply = QMessageBox(QMessageBox.Question, "确认", "确定删除该孔洞吗")

        btn_yes = reply.addButton(self.tr("确定"), QMessageBox.YesRole)
        reply.addButton(self.tr("取消"), QMessageBox.NoRole)
        reply.exec_()

        if reply.clickedButton() == btn_yes:
            self.deleteLater()
            hole_id = self.lab_hole_id.text()
            # hole_infos's key
            key = "hole%04d" % int(hole_id.replace("孔洞", ""))
            self.btn_delete_signal.emit(key)

    def update_ui_and_data(self, hole_info):
        self.draw_hole_info(hole_info)  # 重绘当前页面
        hole_id = self.lab_hole_id.text()
        # hole_infos's key
        key = "hole%04d" % int(hole_id.replace("孔洞", ""))
        hole_infos = {key: self.hole_info}
        self.data2vid_analysis_signal.emit(hole_infos)  # 将数据传给vid_analysis

    def draw_hole_info(self, hole_info):
        self.hole_info.update(hole_info)
        crop_img = self.img_util.base64_str2QImage(hole_info["img_str"])[0]
        self.lab_hole_id.setText(hole_info["hole_id"])
        self.lab_hole_img_display.setScaledContents(True)
        self.lab_hole_img_display.setPixmap(QPixmap.fromImage(crop_img))
        duration = time.strftime("%H:%M:%S", time.gmtime(int(hole_info["duration"])))
        self.lab_duration_display.setText(duration)
        self.lab_height_display.setText("%s mm" % hole_info["height"])
        self.lab_width_display.setText("%s mm" % hole_info["width"])
        self.lab_area_display.setText("%.2f mm²" % hole_info["area"])
        self.lab_depth_display.setText("%s m" % hole_info["depth"])
        if hole_info["from"] == 1:
            self.lab_from_display.show()
        else:
            self.lab_from_display.hide()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = Ui_WgtSingleHoleDisplayAction()
    img = cv2.imread("./login.jpg")
    hole_id = 2
    hole_infos = ui.img_util.gen_hole_infos(img, hole_id)
    count = 0
    for key, hole_info in hole_infos.items():
        ui.draw_hole_info(hole_info)
        count += 1
    ui.show()
    sys.exit(app.exec_())
