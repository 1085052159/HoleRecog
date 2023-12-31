# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'single_vid_analysis.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_WgtSingleVidAnalysis(object):
    def setupUi(self, WgtSingleVidAnalysis):
        WgtSingleVidAnalysis.setObjectName("WgtSingleVidAnalysis")
        WgtSingleVidAnalysis.resize(976, 756)
        WgtSingleVidAnalysis.setMinimumSize(QtCore.QSize(976, 756))
        WgtSingleVidAnalysis.setMaximumSize(QtCore.QSize(976, 756))
        WgtSingleVidAnalysis.setWindowTitle("")
        WgtSingleVidAnalysis.setAutoFillBackground(False)
        WgtSingleVidAnalysis.setStyleSheet("background-color: rgb(240, 241, 245);")
        self.lab_hint_vid_resolve = QtWidgets.QLabel(WgtSingleVidAnalysis)
        self.lab_hint_vid_resolve.setGeometry(QtCore.QRect(20, 10, 101, 31))
        self.lab_hint_vid_resolve.setStyleSheet("background-color: none;\n"
"font: 14pt \"黑体\";")
        self.lab_hint_vid_resolve.setObjectName("lab_hint_vid_resolve")
        self.wgt_vid_upload = QtWidgets.QWidget(WgtSingleVidAnalysis)
        self.wgt_vid_upload.setGeometry(QtCore.QRect(20, 50, 941, 271))
        self.wgt_vid_upload.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.wgt_vid_upload.setObjectName("wgt_vid_upload")
        self.lab_hint_vid_upload = QtWidgets.QLabel(self.wgt_vid_upload)
        self.lab_hint_vid_upload.setGeometry(QtCore.QRect(10, 10, 91, 21))
        self.lab_hint_vid_upload.setStyleSheet("background-color: none;\n"
"font: 12pt \"宋体\";")
        self.lab_hint_vid_upload.setObjectName("lab_hint_vid_upload")
        self.lab_hint_vid_name = QtWidgets.QLabel(self.wgt_vid_upload)
        self.lab_hint_vid_name.setGeometry(QtCore.QRect(620, 30, 71, 21))
        self.lab_hint_vid_name.setObjectName("lab_hint_vid_name")
        self.lab_hint_engineer = QtWidgets.QLabel(self.wgt_vid_upload)
        self.lab_hint_engineer.setGeometry(QtCore.QRect(790, 150, 121, 16))
        self.lab_hint_engineer.setObjectName("lab_hint_engineer")
        self.lab_hint_cam_outer_radius = QtWidgets.QLabel(self.wgt_vid_upload)
        self.lab_hint_cam_outer_radius.setGeometry(QtCore.QRect(790, 100, 121, 16))
        self.lab_hint_cam_outer_radius.setObjectName("lab_hint_cam_outer_radius")
        self.lab_hint_well_inner_radius = QtWidgets.QLabel(self.wgt_vid_upload)
        self.lab_hint_well_inner_radius.setGeometry(QtCore.QRect(790, 50, 121, 16))
        self.lab_hint_well_inner_radius.setObjectName("lab_hint_well_inner_radius")
        self.lab_hint_vid_gen_place = QtWidgets.QLabel(self.wgt_vid_upload)
        self.lab_hint_vid_gen_place.setGeometry(QtCore.QRect(620, 150, 121, 16))
        self.lab_hint_vid_gen_place.setObjectName("lab_hint_vid_gen_place")
        self.lab_hint_well_name = QtWidgets.QLabel(self.wgt_vid_upload)
        self.lab_hint_well_name.setGeometry(QtCore.QRect(620, 50, 111, 16))
        self.lab_hint_well_name.setObjectName("lab_hint_well_name")
        self.lab_hint_vid_gen_time = QtWidgets.QLabel(self.wgt_vid_upload)
        self.lab_hint_vid_gen_time.setGeometry(QtCore.QRect(620, 100, 121, 16))
        self.lab_hint_vid_gen_time.setObjectName("lab_hint_vid_gen_time")
        self.edt_well_name = QtWidgets.QTextEdit(self.wgt_vid_upload)
        self.edt_well_name.setGeometry(QtCore.QRect(620, 70, 121, 31))
        self.edt_well_name.setStyleSheet("font: 10pt \"宋体\";")
        self.edt_well_name.setObjectName("edt_well_name")
        self.edt_vid_gen_time = QtWidgets.QTextEdit(self.wgt_vid_upload)
        self.edt_vid_gen_time.setGeometry(QtCore.QRect(620, 120, 121, 31))
        self.edt_vid_gen_time.setStyleSheet("font: 10pt \"宋体\";")
        self.edt_vid_gen_time.setObjectName("edt_vid_gen_time")
        self.edt_vid_gen_place = QtWidgets.QTextEdit(self.wgt_vid_upload)
        self.edt_vid_gen_place.setGeometry(QtCore.QRect(620, 170, 121, 31))
        self.edt_vid_gen_place.setStyleSheet("font: 10pt \"宋体\";")
        self.edt_vid_gen_place.setObjectName("edt_vid_gen_place")
        self.edt_well_inner_radius = QtWidgets.QTextEdit(self.wgt_vid_upload)
        self.edt_well_inner_radius.setGeometry(QtCore.QRect(790, 70, 121, 31))
        self.edt_well_inner_radius.setStyleSheet("font: 10pt \"宋体\";")
        self.edt_well_inner_radius.setObjectName("edt_well_inner_radius")
        self.edt_cam_outer_radius = QtWidgets.QTextEdit(self.wgt_vid_upload)
        self.edt_cam_outer_radius.setGeometry(QtCore.QRect(790, 120, 121, 31))
        self.edt_cam_outer_radius.setStyleSheet("font: 10pt \"宋体\";")
        self.edt_cam_outer_radius.setObjectName("edt_cam_outer_radius")
        self.edt_engineer = QtWidgets.QTextEdit(self.wgt_vid_upload)
        self.edt_engineer.setGeometry(QtCore.QRect(790, 170, 121, 31))
        self.edt_engineer.setStyleSheet("font: 10pt \"宋体\";")
        self.edt_engineer.setObjectName("edt_engineer")
        self.lab_vid_name_display = QtWidgets.QLabel(self.wgt_vid_upload)
        self.lab_vid_name_display.setGeometry(QtCore.QRect(690, 30, 171, 21))
        self.lab_vid_name_display.setStyleSheet("color: rgb(0, 0, 0);\n"
"font:10pt \"宋体\";")
        self.lab_vid_name_display.setText("")
        self.lab_vid_name_display.setObjectName("lab_vid_name_display")
        self.widget = QtWidgets.QWidget(self.wgt_vid_upload)
        self.widget.setGeometry(QtCore.QRect(10, 40, 561, 161))
        self.widget.setStyleSheet("border:1px solid;\n"
"border-color: rgb(18, 89, 243);")
        self.widget.setObjectName("widget")
        self.wgt_vid_choose_setting = QtWidgets.QWidget(self.widget)
        self.wgt_vid_choose_setting.setGeometry(QtCore.QRect(100, 27, 361, 111))
        self.wgt_vid_choose_setting.setStyleSheet("border: none;")
        self.wgt_vid_choose_setting.setObjectName("wgt_vid_choose_setting")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.wgt_vid_choose_setting)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.lab_hint_choose_vid = QtWidgets.QLabel(self.wgt_vid_choose_setting)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lab_hint_choose_vid.sizePolicy().hasHeightForWidth())
        self.lab_hint_choose_vid.setSizePolicy(sizePolicy)
        self.lab_hint_choose_vid.setStyleSheet("color: rgb(76, 120, 243);\n"
"font: 10pt \"宋体\";")
        self.lab_hint_choose_vid.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.lab_hint_choose_vid.setObjectName("lab_hint_choose_vid")
        self.verticalLayout.addWidget(self.lab_hint_choose_vid)
        self.btn_choose_vid = QtWidgets.QPushButton(self.wgt_vid_choose_setting)
        self.btn_choose_vid.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_choose_vid.sizePolicy().hasHeightForWidth())
        self.btn_choose_vid.setSizePolicy(sizePolicy)
        self.btn_choose_vid.setMinimumSize(QtCore.QSize(0, 32))
        self.btn_choose_vid.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.btn_choose_vid.setStyleSheet("color: rgb(111, 144, 247);\n"
"background-color: rgb(255, 255, 255);\n"
"border:1px solid;\n"
"border-color: rgb(18, 89, 243);")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../icon/文件.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_choose_vid.setIcon(icon)
        self.btn_choose_vid.setIconSize(QtCore.QSize(30, 30))
        self.btn_choose_vid.setObjectName("btn_choose_vid")
        self.verticalLayout.addWidget(self.btn_choose_vid)
        self.lab_hint_vid_format = QtWidgets.QLabel(self.wgt_vid_choose_setting)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lab_hint_vid_format.sizePolicy().hasHeightForWidth())
        self.lab_hint_vid_format.setSizePolicy(sizePolicy)
        self.lab_hint_vid_format.setStyleSheet("color: rgb(152, 152, 152);\n"
"font: 10pt \"宋体\";")
        self.lab_hint_vid_format.setAlignment(QtCore.Qt.AlignCenter)
        self.lab_hint_vid_format.setObjectName("lab_hint_vid_format")
        self.verticalLayout.addWidget(self.lab_hint_vid_format)
        self.lab_vid_display = QtWidgets.QLabel(self.widget)
        self.lab_vid_display.setGeometry(QtCore.QRect(0, 0, 561, 161))
        self.lab_vid_display.setText("")
        self.lab_vid_display.setObjectName("lab_vid_display")
        self.lab_vid_display.raise_()
        self.wgt_vid_choose_setting.raise_()
        self.wgt_vid_display_setting = QtWidgets.QWidget(self.wgt_vid_upload)
        self.wgt_vid_display_setting.setGeometry(QtCore.QRect(10, 210, 531, 31))
        self.wgt_vid_display_setting.setObjectName("wgt_vid_display_setting")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.wgt_vid_display_setting)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.btn_vid_play = QtWidgets.QPushButton(self.wgt_vid_display_setting)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_vid_play.sizePolicy().hasHeightForWidth())
        self.btn_vid_play.setSizePolicy(sizePolicy)
        self.btn_vid_play.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"border: 0px;\n"
"image: url(:/image/播放.png);")
        self.btn_vid_play.setText("")
        self.btn_vid_play.setIconSize(QtCore.QSize(30, 30))
        self.btn_vid_play.setCheckable(False)
        self.btn_vid_play.setAutoDefault(False)
        self.btn_vid_play.setDefault(False)
        self.btn_vid_play.setFlat(True)
        self.btn_vid_play.setObjectName("btn_vid_play")
        self.horizontalLayout.addWidget(self.btn_vid_play)
        self.sli_vid_process_bar = QtWidgets.QSlider(self.wgt_vid_display_setting)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sli_vid_process_bar.sizePolicy().hasHeightForWidth())
        self.sli_vid_process_bar.setSizePolicy(sizePolicy)
        self.sli_vid_process_bar.setOrientation(QtCore.Qt.Horizontal)
        self.sli_vid_process_bar.setObjectName("sli_vid_process_bar")
        self.horizontalLayout.addWidget(self.sli_vid_process_bar)
        self.lab_vid_cur_length = QtWidgets.QLabel(self.wgt_vid_display_setting)
        self.lab_vid_cur_length.setObjectName("lab_vid_cur_length")
        self.horizontalLayout.addWidget(self.lab_vid_cur_length)
        self.lab_vid_total_length = QtWidgets.QLabel(self.wgt_vid_display_setting)
        self.lab_vid_total_length.setObjectName("lab_vid_total_length")
        self.horizontalLayout.addWidget(self.lab_vid_total_length)
        self.btn_add_hole = QtWidgets.QPushButton(self.wgt_vid_display_setting)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_add_hole.sizePolicy().hasHeightForWidth())
        self.btn_add_hole.setSizePolicy(sizePolicy)
        self.btn_add_hole.setMinimumSize(QtCore.QSize(60, 0))
        self.btn_add_hole.setStyleSheet("font: 10pt \"宋体\";\n"
"color: rgb(255, 255, 255);\n"
"background-color: rgb(18, 89, 243);\n"
"border: 0px;")
        self.btn_add_hole.setObjectName("btn_add_hole")
        self.horizontalLayout.addWidget(self.btn_add_hole)
        self.widget.raise_()
        self.lab_hint_vid_gen_place.raise_()
        self.lab_hint_vid_gen_time.raise_()
        self.lab_hint_vid_upload.raise_()
        self.lab_hint_vid_name.raise_()
        self.lab_hint_engineer.raise_()
        self.lab_hint_cam_outer_radius.raise_()
        self.lab_hint_well_inner_radius.raise_()
        self.lab_hint_well_name.raise_()
        self.edt_well_name.raise_()
        self.edt_vid_gen_place.raise_()
        self.edt_well_inner_radius.raise_()
        self.edt_engineer.raise_()
        self.lab_vid_name_display.raise_()
        self.wgt_vid_display_setting.raise_()
        self.edt_vid_gen_time.raise_()
        self.edt_cam_outer_radius.raise_()
        self.wgt_hole_recog = QtWidgets.QWidget(WgtSingleVidAnalysis)
        self.wgt_hole_recog.setGeometry(QtCore.QRect(20, 340, 941, 401))
        self.wgt_hole_recog.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.wgt_hole_recog.setObjectName("wgt_hole_recog")
        self.lab_hint_hole_recog = QtWidgets.QLabel(self.wgt_hole_recog)
        self.lab_hint_hole_recog.setGeometry(QtCore.QRect(10, 10, 811, 21))
        self.lab_hint_hole_recog.setStyleSheet("background-color: none;\n"
"font: 12pt \"宋体\";")
        self.lab_hint_hole_recog.setObjectName("lab_hint_hole_recog")
        self.lab_hint_start_resolve = QtWidgets.QLabel(self.wgt_hole_recog)
        self.lab_hint_start_resolve.setGeometry(QtCore.QRect(320, 140, 181, 21))
        self.lab_hint_start_resolve.setStyleSheet("color: rgb(76, 120, 243);\n"
"font: 10pt \"宋体\";")
        self.lab_hint_start_resolve.setObjectName("lab_hint_start_resolve")
        self.btn_resolve = QtWidgets.QPushButton(self.wgt_hole_recog)
        self.btn_resolve.setGeometry(QtCore.QRect(130, 360, 241, 23))
        self.btn_resolve.setStyleSheet("font: 12pt \"宋体\";\n"
"color: rgb(255, 255, 255);\n"
"background-color: rgb(19, 89, 245);\n"
"border: 0px;")
        self.btn_resolve.setObjectName("btn_resolve")
        self.btn_gen_report = QtWidgets.QPushButton(self.wgt_hole_recog)
        self.btn_gen_report.setGeometry(QtCore.QRect(540, 360, 251, 23))
        self.btn_gen_report.setStyleSheet("font: 12pt \"宋体\";\n"
"color: rgb(255, 255, 255);\n"
"background-color: rgb(253, 137, 50);\n"
"border: 0px;")
        self.btn_gen_report.setObjectName("btn_gen_report")
        self.sco_holes_display = QtWidgets.QScrollArea(self.wgt_hole_recog)
        self.sco_holes_display.setGeometry(QtCore.QRect(10, 40, 921, 311))
        self.sco_holes_display.setStyleSheet("border: none;")
        self.sco_holes_display.setWidgetResizable(True)
        self.sco_holes_display.setObjectName("sco_holes_display")
        self.wgt_holes_display = QtWidgets.QWidget()
        self.wgt_holes_display.setGeometry(QtCore.QRect(0, 0, 921, 311))
        self.wgt_holes_display.setObjectName("wgt_holes_display")
        self.gid_holes_display = QtWidgets.QGridLayout(self.wgt_holes_display)
        self.gid_holes_display.setGeometry(QtCore.QRect(0, 0, 921, 311))
        self.gid_holes_display.setObjectName("gid_holes_display")
        self.sco_holes_display.setWidget(self.wgt_holes_display)

        self.retranslateUi(WgtSingleVidAnalysis)
        QtCore.QMetaObject.connectSlotsByName(WgtSingleVidAnalysis)

    def retranslateUi(self, WgtSingleVidAnalysis):
        _translate = QtCore.QCoreApplication.translate
        self.lab_hint_vid_resolve.setText(_translate("WgtSingleVidAnalysis", "视频解析"))
        self.lab_hint_vid_upload.setText(_translate("WgtSingleVidAnalysis", "上传视频"))
        self.lab_hint_vid_name.setText(_translate("WgtSingleVidAnalysis", "视频名称："))
        self.lab_hint_engineer.setText(_translate("WgtSingleVidAnalysis", "工程师"))
        self.lab_hint_cam_outer_radius.setText(_translate("WgtSingleVidAnalysis", "摄像工具外径/mm"))
        self.lab_hint_well_inner_radius.setText(_translate("WgtSingleVidAnalysis", "井筒内径"))
        self.lab_hint_vid_gen_place.setText(_translate("WgtSingleVidAnalysis", "视频生成地点"))
        self.lab_hint_well_name.setText(_translate("WgtSingleVidAnalysis", "井号名称"))
        self.lab_hint_vid_gen_time.setText(_translate("WgtSingleVidAnalysis", "视频生成时间"))
        self.edt_well_name.setHtml(_translate("WgtSingleVidAnalysis", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'宋体\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.edt_vid_gen_time.setHtml(_translate("WgtSingleVidAnalysis", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'宋体\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.edt_vid_gen_time.setPlaceholderText(_translate("WgtSingleVidAnalysis", "日期xxxx-xx-xx"))
        self.edt_vid_gen_place.setHtml(_translate("WgtSingleVidAnalysis", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'宋体\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.edt_well_inner_radius.setHtml(_translate("WgtSingleVidAnalysis", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'宋体\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.edt_cam_outer_radius.setHtml(_translate("WgtSingleVidAnalysis", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'宋体\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.edt_engineer.setHtml(_translate("WgtSingleVidAnalysis", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'宋体\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.lab_hint_choose_vid.setText(_translate("WgtSingleVidAnalysis", "点击[选择文件]，或拖拽文件到此区域"))
        self.btn_choose_vid.setText(_translate("WgtSingleVidAnalysis", "选择文件"))
        self.lab_hint_vid_format.setText(_translate("WgtSingleVidAnalysis", "支持：avi、mkv、mov、mp4格式"))
        self.lab_vid_cur_length.setText(_translate("WgtSingleVidAnalysis", "00:00:00"))
        self.lab_vid_total_length.setText(_translate("WgtSingleVidAnalysis", "/00:00:00"))
        self.btn_add_hole.setText(_translate("WgtSingleVidAnalysis", "添加孔洞"))
        self.lab_hint_hole_recog.setText(_translate("WgtSingleVidAnalysis", "孔洞识别"))
        self.lab_hint_start_resolve.setText(_translate("WgtSingleVidAnalysis", "请上传视频，点击[开始解析]"))
        self.btn_resolve.setText(_translate("WgtSingleVidAnalysis", "开始解析"))
        self.btn_gen_report.setText(_translate("WgtSingleVidAnalysis", "生成报告"))
import picture_rc
