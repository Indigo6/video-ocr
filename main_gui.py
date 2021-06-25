import sys

import cv2 as cv

from PyQt5.Qt import QPixmap
from PyQt5.QtWidgets import (QApplication, QFileDialog, QGraphicsScene,
                             QMainWindow)

from gui import *
from lib.core.split import split_vision
from lib.utils import cv_to_qt


class MyWindow(QMainWindow, Ui_MainWindow):
    # 初始化
    def __init__(self, parent=None):
        super(MyWindow, self).__init__(parent)
        self.setupUi(self)

        # 注册监听
        # 打开文件的项
        self.openFile.triggered.connect(self.open_file)
        self.videoBar.actionTriggered(0).connect(self.video_bar())

        # 生成时间轴的项
        self.testButton.triggered.connect(self.test_seg)

        # 初始化实例变量
        self.video_path = None
        self.video = None
        self.frame_idx = 0
        self.hasOpen = False

    def open_file(self):
        """
        打开视频，并显示第一帧
        """
        video_name, video_type = QFileDialog.getOpenFileName(self, "打开视频", "", "*.mp4;;*.mkv;;*.avi;;*.rmvb")
        if not video_type not in ['.mp4', '.mkv', '.avi', '.rmvb']:
            raise ValueError("Not a video file:{}".format(video_name))
        print(video_name, video_type)

        self.video_path = video_name
        self.video = cv.VideoCapture(video_name)

        ret, frame = self.video.read()
        if not ret:
            raise ValueError("An empty video:{}".format(video_name))

        # 缩放图像为适应窗口的大小
        # 获得缩放比例
        width = self.videoView.width()
        height = self.videoView.height()
        row, col = frame.shape[1], frame.shape[0]
        a = float((width - 10) / row)
        b = float((height - 5) / col)
        if a < b:
            scale = a
        else:
            scale = b
        dim = (int(row * scale), int(col * scale))
        # 缩放图像
        resized_frame = cv.resize(frame, dim)
        # 将OpenCV格式储存的图片转换为QT可处理的图片类型
        show_img = cv_to_qt(resized_frame)

        # 将图片放入图片显示窗口
        scene = QGraphicsScene()
        scene.addPixmap(QPixmap.fromImage(show_img))
        self.videoView.setScene(scene)
        self.hasOpen = True

    def test_seg(self):
        print(self.video_path, "todo")

    def video_bar(self):
        print(self.video_path, "todo")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWin = MyWindow()
    myWin.show()
    sys.exit(app.exec_())
