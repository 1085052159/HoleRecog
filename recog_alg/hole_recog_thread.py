import sys
from PyQt5.QtCore import pyqtSignal, QThread
from PyQt5.QtWidgets import QWidget, QListWidget, QPushButton, QGridLayout, QApplication, QMessageBox
from recog_alg.hole_recog_pipeline import hole_recog


class InferThread(QThread):
    infer_finished = pyqtSignal(dict)

    def __init__(self, parent=None):
        super(InferThread, self).__init__(parent)

    def set_params(self, vid_path, batch_size=128, device="cuda", save_path="./hole_recog", show_temp=False):
        self.vid_path = vid_path
        self.batch_size = batch_size
        self.device = device
        self.save_path = save_path
        self.show_temp = show_temp

    def run(self):
        hole_infos = hole_recog(self.vid_path, self.batch_size, self.device, self.save_path, self.show_temp)
        self.infer_finished.emit(hole_infos)


class MainWidget(QWidget):
    def __init__(self, parent=None):
        super(MainWidget, self).__init__(parent)
        # 设置标题
        self.setWindowTitle('QThread多线程例子')

        # 实例化列表控件与按钮控件
        self.listFile = QListWidget()
        self.btnStart = QPushButton('开始')

        # 把控件放置在栅格布局中
        layout = QGridLayout(self)
        layout.addWidget(self.listFile, 0, 0, 1, 2)
        layout.addWidget(self.btnStart, 1, 1)

        # 信号与槽函数的连接
        self.btnStart.clicked.connect(self.slotStart)

    def set_thread(self, thread):
        self.thread = thread
        self.thread.infer_finished.connect(self.slotAdd)


    def slotAdd(self, hole_infos):
        if hole_infos is None:
            print("hole_infos is None")
            return
        print("hole_infos: ", hole_infos.keys())
        self.listFile.addItem("finished")
        self.btnStart.setEnabled(True)

    def slotStart(self):
        # 开始按钮不可点击，线程开始
        self.btnStart.setEnabled(False)
        QMessageBox(QMessageBox.Warning, "警告", "正在推理中").exec_()
        self.thread.start()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = MainWidget()
    # 实例化多线程对象
    thread = InferThread()
    thread.set_params("video011.avi")
    demo.set_thread(thread)
    demo.show()
    sys.exit(app.exec_())
