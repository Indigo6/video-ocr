import threading
from lib.core.split import split_vision
from .utils import ocr_with_timeline


class TimelineThread(threading.Thread):
    def __init__(self, video, video_path, upper_value, lower_value, seg_method, box, main_window, progress_bar,
                 lang="ch_sim", srt_prob_thres=1, change_prob_thres=1, output_frame=False):
        threading.Thread.__init__(self)
        self.video = video
        self.video_path = video_path
        self.upper_values = upper_value
        self.lower_values = lower_value
        self.seg_method = seg_method
        self.box = box
        self.main_window = main_window
        self.progress_bar = progress_bar
        self.lang = lang
        self.srt_prob_thres = srt_prob_thres
        self.change_prob_thres = change_prob_thres
        self.output_frame = output_frame

    def run(self):
        split_vision(self.video, self.video_path, self.upper_values, self.lower_values, self.seg_method, self.box,
                     self.main_window, self.progress_bar, self.lang, self.srt_prob_thres, self.change_prob_thres,
                     self.output_frame)


class GenSubThread(threading.Thread):
    def __init__(self, video, video_path, box, ocr_reader, lang, main_window, progress_bar):
        threading.Thread.__init__(self)
        self.video = video
        self.video_path = video_path
        self.box = box
        self.ocr_reader = ocr_reader
        self.lang = lang
        self.main_window = main_window
        self.progress_bar = progress_bar

    def run(self):
        ocr_with_timeline(self.video, self.video_path, self.box, self.ocr_reader,
                          self.lang, self.main_window, self.progress_bar)
