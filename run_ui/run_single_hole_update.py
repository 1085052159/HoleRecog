import sys
from PyQt5 import QtGui
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget
from utils_tools.img_util import ImageUtils
from ui.single_hole_update import Ui_WgtSingleHoleUpdate


class Ui_WgtSingleHoleUpdateAction(QWidget, Ui_WgtSingleHoleUpdate):
    data2_single_hole_display_signal = pyqtSignal(dict)

    def __init__(self):
        QWidget.__init__(self)
        Ui_WgtSingleHoleUpdate.__init__(self)
        self.init_ui()
        self.btn_edit.clicked.connect(self.btn_edit_action)
        self.btn_save.clicked.connect(self.btn_save_action)
        self.edt_height_input.textChanged.connect(self.show_area_dynamically)
        self.edt_width_input.textChanged.connect(self.show_area_dynamically)

        self.img_util = ImageUtils()
        self.hole_info = {}

    def init_ui(self):
        self.setFixedSize(700, 430)
        self.setupUi(self)

    def show_area_dynamically(self):
        """
        动态计算面积
        """
        h_str = self.edt_height_input.text()
        w_str = self.edt_width_input.text()
        if len(h_str) > 0 and len(w_str) > 0:
            h = float(h_str)
            w = float(w_str)
            area = self.img_util.compute_area(h, w)
            self.edt_area_input.setText(str(area))

    def btn_edit_action(self):
        self.edt_duration_input.setEnabled(True)
        self.edt_duration_input.setValidator(QtGui.QIntValidator())
        self.edt_height_input.setEnabled(True)
        self.edt_height_input.setValidator(QtGui.QDoubleValidator())
        self.edt_width_input.setEnabled(True)
        self.edt_width_input.setValidator(QtGui.QDoubleValidator())
        self.edt_depth_input.setEnabled(True)
        self.edt_depth_input.setValidator(QtGui.QDoubleValidator())

    def btn_save_action(self):
        duration = int(self.edt_duration_input.text())
        height = float(self.edt_height_input.text())
        width = float(self.edt_width_input.text())
        area = self.img_util.compute_area(height, width)
        self.edt_area_input.setText(str(area))
        depth = float(self.edt_depth_input.text())
        hole_info = {
            "duration": duration,
            "height": height,
            "width": width,
            "area": area,
            "depth": depth,
        }
        self.hole_info.update(hole_info)
        self.data2_single_hole_display_signal.emit(self.hole_info)
        self.deleteLater()

    def draw_hole_info(self, hole_info):
        self.hole_info.update(hole_info)
        crop_img = self.img_util.base64_str2QImage(hole_info["img_str"])[0]
        self.lab_hole_id.setText(hole_info["hole_id"])
        self.lab_hole_img_display.setScaledContents(True)
        self.lab_hole_img_display.setPixmap(QPixmap.fromImage(crop_img))
        self.edt_duration_input.setText(str(hole_info["duration"]))
        self.edt_height_input.setText("%s" % hole_info["height"])
        self.edt_width_input.setText("%s" % hole_info["width"])
        self.edt_area_input.setText("%.2f" % hole_info["area"])
        self.edt_depth_input.setText("%s" % hole_info["depth"])
        if hole_info["from"] == 1:
            self.lab_from_display.show()
        else:
            self.lab_from_display.hide()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = Ui_WgtSingleHoleUpdateAction()
    ui.show()
    sys.exit(app.exec_())
