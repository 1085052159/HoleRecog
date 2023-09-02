import sys
import uuid

import PyQt5
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import Qt, QObject, QUrl, QRect, pyqtSignal, QPoint
from PyQt5.QtGui import QPainter, QImage
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow, QGridLayout, QToolBar, QAction
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent, QAbstractVideoBuffer, \
    QVideoFrame, QVideoSurfaceFormat, QAbstractVideoSurface
from PyQt5.QtMultimediaWidgets import QVideoWidget


class MyVideoSurface(QAbstractVideoSurface):

    frameAvailable = pyqtSignal(QImage)  # 截图完成信号

    def __init__(self, parent=None):
        super(QAbstractVideoSurface, self).__init__(parent)

    def supportedPixelFormats(self, type=None):
        support_format = [
            QVideoFrame.Format_ARGB32,
            QVideoFrame.Format_ARGB32_Premultiplied,
            QVideoFrame.Format_ARGB8565_Premultiplied,
            QVideoFrame.Format_AYUV444,
            QVideoFrame.Format_AYUV444_Premultiplied,
            QVideoFrame.Format_BGR24,
            QVideoFrame.Format_BGR32,
            QVideoFrame.Format_BGR555,
            QVideoFrame.Format_BGR565,
            QVideoFrame.Format_BGRA32,
            QVideoFrame.Format_BGRA32_Premultiplied,
            QVideoFrame.Format_BGRA5658_Premultiplied,
            QVideoFrame.Format_CameraRaw,
            QVideoFrame.Format_IMC1,
            QVideoFrame.Format_IMC2,
            QVideoFrame.Format_IMC3,
            QVideoFrame.Format_IMC4,
            QVideoFrame.Format_Jpeg,
            QVideoFrame.Format_NV12,
            QVideoFrame.Format_NV21,
            QVideoFrame.Format_RGB24,
            QVideoFrame.Format_RGB32,
            QVideoFrame.Format_RGB555,
            QVideoFrame.Format_RGB565,
            QVideoFrame.Format_User,
            QVideoFrame.Format_UYVY,
            QVideoFrame.Format_Y16,
            QVideoFrame.Format_Y8 ,
            QVideoFrame.Format_YUV420P,
            QVideoFrame.Format_YUV444,
            QVideoFrame.Format_YUYV,
            QVideoFrame.Format_YV12,
        ]
        return support_format

    def present(self, frame: 'QVideoFrame'):
        if frame.isValid():
            cloneFrame = QVideoFrame(frame)
            cloneFrame.map(QAbstractVideoBuffer.ReadOnly)
            image = QImage(cloneFrame.bits(), cloneFrame.width(), cloneFrame.height(),
                           QVideoFrame.imageFormatFromPixelFormat(cloneFrame.pixelFormat()))
            self.frameAvailable.emit(image)  # this is very important
            cloneFrame.unmap()

        if self.surfaceFormat().pixelFormat() != frame.pixelFormat() or \
                self.surfaceFormat().frameSize() != frame.size():
            self.setError(QAbstractVideoSurface.IncorrectFormatError)
            self.stop()

            return False
        else:
            return True