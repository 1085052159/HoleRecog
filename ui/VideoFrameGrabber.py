# !/usr/bin/env python
# _*_ coding: utf-8 _*_
"""=============================
@ Author   : mycler
@ Time     : 2023-08-12 00:39
@ Desc说明  : 
@ FileName : VideoFrameGrabber.py
@ SoftWare : PyCharm集成开发环境
@ 项目名称   : T_0811
@ Mail     : 543559110@qq.com
@ Phone    : 17728923831
@ Version  : python3.8.10 64bit
=============================="""
# QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
# QMessageBox.question(self, 'Message', "<h3><font color='red'>文件路径不正确或参数为空</font color='red'></h3>", QMessageBox.Yes)
# style_file = './style.qss'
# style_sheet = QSSLoader.read_qss_file(style_file)
# window.setStyleSheet(style_sheet)
# from selenium.webdriver.chrome.options import Options
# option = webdriver.ChromeOptions() 
# option.add_experimental_option('useAutomationExtension', False) 
# option.add_experimental_option('excludeSwitches', ['enable-automation']) 
# driver = webdriver.Chrome(chrome_options=option) 
# driver.get("打开测试网页")
# self.setAttribute(Qt.WA_TranslucentBackground)    # 隐藏背景
# self.setWindowFlags(Qt.FramelessWindowHint)    # 无边框
# self.setAttribute(Qt.WA_StyledBackground)    # 激活背景
# self.setAttribute(Qt.WA_StyledBackground, True)     # 激活背景
# 引用By类要先导入 查找   (.*?):(.*),   替换  "$1":"$2",
# from selenium.webdriver.common.by import By
# response.encoding = response.apparent_encoding    # 自动转编码
# headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"}
# 如果您有一个包含多个字符串的列表，您可以将其合并成一个字符串，每个字符串之间用换行符分隔。以下是使用Python编程语言的示例代码：
# 
# python
# my_list = ["Hello", "world", "OpenAI"]
# 
# # 使用换行符 ("\n") 合并列表中的字符串
# result = "\n".join(my_list)
# 
# print(result)
# 输出：
# 
# Hello
# world
# OpenAI
# 在上述示例中，我们使用了join()方法来合并字符串列表，并使用换行符("\n")作为分隔符，将列表中的字符串连接起来形成一个字符串。

class VideoFrameGrabber:
    # def __init__(self, parent=None, *args, **kwargs):
    #     super(VideoFrameGrabber, self).__init__(parent, *args, **kwargs)
    #     self.setupUi(self)
    def __init__(self, ui, mainWnd):
        self.ui = ui
        self.ui = mainWnd

    def wgt_vid_display(self):
        """wgt_vid_display"""
        print('wgt_vid_display')


    def __delattr__(self, name: str) -> None:
        super().__delattr__(name)

def single_hole_update():
    """single_hole_update"""
    print('single_hole_update')

