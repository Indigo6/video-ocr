import os

import cv2 as cv

from lib.utils import OcrReader, ocr_with_timeline
from .split import split_vision


def write_srt(txt, fc_start, fc_end, srt_count, content, fps):
    # txt: file handler
    def fc2time(fc):
        ftime = fc / fps
        if ftime <= 0:
            return '0:00,000'
        elif ftime < 1:
            return '00:00:00,%03d' % (ftime * 1000)
        elif ftime < 60:
            return '00:00:%02d,%03d' % (int(ftime), int(ftime * 1000) % 1000)
        elif ftime < 3600:
            return '00:%02d:%02d,%03d' % (int(ftime / 60), int(ftime) % 60, int(ftime * 1000) % 1000)
        else:
            return '%02d:%02d:%02d,%03d' % (int(ftime / 3600), int((ftime % 3600) / 60),
                                            int(ftime) % 60, int(ftime * 1000) % 1000)

    txt.write("{}\n".format(srt_count))
    txt.write("{} --> {}\n".format(fc2time(fc_start), fc2time(fc_end)))
    txt.write("{}\n".format(content))
    print("{}\n".format(srt_count))
    print("{} --> {}\n".format(fc2time(fc_start), fc2time(fc_end)))
    print("{}\n".format(content))


def ocr_and_write(cfg, ocr_reader, fps):
    video_path = cfg.VIDEO
    _, video_name = os.path.split(video_path)
    video_name = video_name.split('.')[0]
    frame_dir = 'frame/' + video_name + '/'

    # TODO: 读取 frame 文件夹下提取的所有图片进行识别，
    #  并根据文件名标示的时间轴写入字幕文件
    #  use write_srt()
    print("To be done.")


def video_ocr_vision(cfg):
    srt_color = cfg.SPLIT.VISION.COLOR
    clip_box = cfg.BOX
    srt_prob_thres = cfg.SPLIT.VISION.SRT_THRES
    change_prob_thres = cfg.SPLIT.VISION.CHANGE_THRES

    # split_vision(cfg, srt_color, clip_box, srt_prob_thres, change_prob_thres)

    ocr_reader = OcrReader(cfg)
    ocr_with_timeline(cfg, ocr_reader, 'demo/split_vision.ass')



