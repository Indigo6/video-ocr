import sys

import cv2 as cv
import numpy as np

from PyQt5.QtWidgets import (QApplication, QFileDialog, QColorDialog,
                             QMainWindow)

from gui import *
from lib.utils import get_image_view, OcrReader, check_dir
from lib.threads import TimelineThread, GenSubThread
from lib.core.split import if_srt_frame


class MyWindow(QMainWindow, Ui_VideoOCR):
    # 初始化
    def __init__(self, parent=None):
        super(MyWindow, self).__init__(parent)
        self.setupUi(self)

        # 注册监听
        # 打开文件的项
        self.openFile.triggered.connect(self.open_file)
        self.videoBar.sliderMoved.connect(self.video_bar)

        # 参数配置项
        self.colorButton1.clicked.connect(self.upper_color)
        self.colorButton2.clicked.connect(self.lower_color)

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
        self.frame = None
        self.hasOpen = False

        check_dir()

    def open_file(self):
        """
        打开视频，并显示第一帧
        """
        video_name, video_type = QFileDialog.getOpenFileName(self, "打开视频", "", "*.mp4;;*.mkv;;*.avi;;*.rmvb")
        if not video_name:
            return
        if not video_type not in ['.mp4', '.mkv', '.avi', '.rmvb']:
            raise ValueError("Not a video file:{}".format(video_name))
        print(video_name, video_type)

        self.video_path = video_name
        self.video = cv.VideoCapture(video_name)

        ret, self.frame = self.video.read()
        if not ret:
            raise ValueError("An empty video:{}".format(video_name))

        self.video_total_frame = self.video.get(7)

        # 缩放图像为适应窗口的大小
        # 获得缩放比例
        scene = get_image_view(self.videoView, self.frame)
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
        _, self.frame = self.video.read()
        scene = get_image_view(self.videoView, self.frame)
        self.videoView.setScene(scene)

    def upper_color(self):
        col = QColorDialog.getColor()
        if col.isValid():
            color_type = self.segMethod.itemText(self.segMethod.currentIndex())
            if color_type == "RGB":
                upper_str = '{},{},{}'.format(col.red(), col.green(), col.blue())
                # 将选择的颜色输出在输入框.
                self.maxValue.setText(upper_str)
            else:
                upper_str = '{},{},{}'.format(col.hue(), col.saturation(), col.value())
                # 将选择的颜色输出在输入框.
                self.maxValue.setText(upper_str)

    def lower_color(self):
        col = QColorDialog.getColor()
        if col.isValid():
            color_type = self.segMethod.itemText(self.segMethod.currentIndex())
            if color_type == "RGB":
                lower_str = '{},{},{}'.format(col.red(), col.green(), col.blue())
                # 将选择的颜色输出在输入框.
                self.minValue.setText(lower_str)
            else:
                lower_str = '{},{},{}'.format(col.hue(), col.saturation(), col.value())
                # 将选择的颜色输出在输入框.
                self.minValue.setText(lower_str)

    def test_seg(self):
        if not self.hasOpen:
            return
        # TODO: 如何获得 box 数据
        box = [[410, None], [100, 800]]

        srt_prob_thres = float(self.srtThres.text())
        seg_method = self.segMethod.itemText(self.segMethod.currentIndex())
        upper_value = self.maxValue.text()
        lower_value = self.minValue.text()
        upper_values = np.array([int(i) for i in upper_value.split(',')])
        lower_values = np.array([int(i) for i in lower_value.split(',')])

        clipped_frame = self.frame[box[0][0]:box[0][1], box[1][0]:box[1][1]]
        frame_seg, has_srt = if_srt_frame(clipped_frame, upper_values, lower_values, seg_method, srt_prob_thres)
        # 缩放图像为适应窗口的大小
        # 获得缩放比例
        scene = get_image_view(self.clipView, frame_seg)
        self.clipView.setScene(scene)
        if has_srt:
            self.isSrt.setText('检测结果: 该帧包含字幕')
        else:
            self.isSrt.setText('检测结果: 该帧不包含字幕')

    def gen_time(self):
        if not self.hasOpen:
            return
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

        # split_vision(self.video, self.video_path, upper_values, lower_values, seg_method, box,
        #              self.progressBar, lang, srt_prob_thres, change_prob_thres, save_frames)
        split_thread = TimelineThread(self.video, self.video_path, upper_values, lower_values, seg_method, box,
                                      self, self.progressBar, lang, srt_prob_thres, change_prob_thres, save_frames)
        split_thread.run()

    def gen_sub(self):
        if not self.hasOpen:
            return
        box = [[410, None], [160, 760]]
        ocr_method = self.ocrMethod.itemText(self.ocrMethod.currentIndex())
        # lang = ['ch_sim']
        lang_box_text = self.langBox.itemText(self.langBox.currentIndex())
        lang = [lang_box_text] if lang_box_text != "dual" else ['ch_sim', 'en']
        # TODO: 自动转成各种OCR需要的缩写
        ocr_reader = OcrReader(ocr_method, lang)
        ass_path = "output/split_vision.ass"
        # ocr_with_timeline(self.video, box, ocr_reader, ass_path, lang, self.progressBar)
        gen_sub_thread = GenSubThread(self.video, box, ocr_reader, ass_path, lang, self, self.progressBar)
        gen_sub_thread.run()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWin = MyWindow()
    myWin.show()
    sys.exit(app.exec_())
