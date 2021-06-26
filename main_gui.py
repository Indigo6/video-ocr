import sys

import cv2 as cv
import numpy as np

from PyQt5.QtWidgets import (QApplication, QFileDialog, QMessageBox,
                             QMainWindow)

from gui import *
from lib.core.split import split_vision
from lib.utils import get_image_view, ocr_with_timeline, OcrReader


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
        self.testButton.clicked.connect(self.test_seg)
        self.genTime.clicked.connect(self.gen_time)

        # 生成字幕的项
        self.genSub.clicked.connect(self.gen_sub)

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
        print(self.video_path, "todo")
        box = [[410, None], [100, 800]]

    def gen_time(self):
        save_frames = self.saveFrames.isChecked()
        seg_method = self.segMethod.itemText(self.segMethod.currentIndex())
        upper_value = self.maxValue.text()
        lower_value = self.minValue.text()
        upper_values = np.array([int(i) for i in upper_value.split(',')])
        lower_values = np.array([int(i) for i in lower_value.split(',')])

        srt_prob_thres = float(self.srtThres.text())
        change_prob_thres = float(self.chgThres.text())

        # lang = 'ch_sim'
        lang_box_text = self.langBox.itemText(self.langBox.currentIndex())
        lang = [lang_box_text] if lang_box_text != "dual" else ['ch_sim', 'en']

        # TODO: 如何获得 box 数据
        box = [[410, None], [100, 800]]

        split_vision(self.video, self.video_path, upper_values, lower_values, seg_method,
                     box, lang, srt_prob_thres, change_prob_thres, save_frames)
        QMessageBox.information(self, "提示", "时间轴生成成功！", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)

    def gen_sub(self):
        box = [[410, None], [100, 800]]
        ocr_method = self.ocrMethod.itemText(self.ocrMethod.currentIndex())
        # lang = ['ch_sim']
        lang_box_text = self.langBox.itemText(self.langBox.currentIndex())
        lang = [lang_box_text] if lang_box_text != "dual" else ['ch_sim', 'en']
        # TODO: 自动转成各种OCR需要的缩写
        ocr_reader = OcrReader(ocr_method, lang)
        ass_path = "demo/split_vision.ass"
        ocr_with_timeline(self.video, box, ocr_reader, ass_path, lang)
        QMessageBox.information(self, "提示", "字幕生成成功！", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWin = MyWindow()
    myWin.show()
    sys.exit(app.exec_())
