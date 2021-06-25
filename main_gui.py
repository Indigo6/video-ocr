import sys

import cv2 as cv

from PyQt5.QtWidgets import (QApplication, QFileDialog, QGraphicsScene,
                             QMainWindow)

from gui import *
from lib.core.split import split_vision
from lib.utils import get_image_view, ocr_with_timeline


class MyWindow(QMainWindow, Ui_VideoOCR):
    # 初始化
    def __init__(self, parent=None):
        super(MyWindow, self).__init__(parent)
        self.setupUi(self)

        # 注册监听
        # 打开文件的项
        self.openFile.triggered.connect(self.open_file)
        self.videoBar.sliderMoved.connect(self.video_bar)

        # 生成时间轴的项
        # self.testButton.clicked.connect(self.test_seg)

        # 生成字幕的项
        self.genSub.clicked.connect(self.gen_sub)
        self.saveFrames.isTristate()

        # 初始化实例变量
        self.video_path = None
        self.video = None
        self.video_total_frame = 0
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

        self.video_total_frame = self.video.get(7)

        # 缩放图像为适应窗口的大小
        # 获得缩放比例
        scene = get_image_view(self.videoView, frame)
        self.videoView.setScene(scene)
        self.hasOpen = True

    def video_bar(self):
        """
            通过 slider 所处位置确定
        """
        if not self.hasOpen:
            return
        bar_min = self.videoBar.minimum()
        bar_max = self.videoBar.maximum()
        bar_pos = self.videoBar.value()
        bar_ratio = (bar_pos - bar_min) / (bar_max - bar_min)
        self.frame_idx = int(self.video_total_frame * bar_ratio)
        self.video.set(cv.CAP_PROP_POS_FRAMES, self.frame_idx)  # 设置要获取的帧号
        _, frame = self.video.read()
        scene = get_image_view(self.videoView, frame)
        self.videoView.setScene(scene)

    def test_seg(self):
        save_frames = self.saveFrames.isTristate()
        print(self.video_path, "todo")

    def gen_sub(self):
        ocr_with_timeline(self.video)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWin = MyWindow()
    myWin.show()
    sys.exit(app.exec_())
