import argparse
import sys
import time

import cv2 as cv

from pysubs2 import SSAFile
from lib.utils import fmt_time, simplify_ass, OcrReader


def ocr_with_timeline(cfg, ocr_reader):
    ass_path = cfg.SPLIT.AUDIO.ASS_PATH
    box = [cfg.BOX[:2], cfg.BOX[2:]]

    video = cv.VideoCapture(cfg.VIDEO)
    fps = video.get(5)  # 设置要获取的帧号
    ret, test_frame = video.read()
    if not ret:
        print("Open Video Error!")
        sys.exit()
    frame_shape = test_frame.shape

    # subs = SSAFile.load('S03E09.ass', encoding="utf-16-le")
    subs = SSAFile.load(ass_path)

    total = len(subs)
    start = time.time()
    count = 0

    i = 0
    length = len(subs)
    while i < length:
        line = subs[i]
        srt_start = line.start / 1000
        srt_end = line.end / 1000
        # print(fmt_time(srt_start), fmt_time(srt_end))
        srt_mid = (srt_start + srt_end) / 2
        frame_id = int(srt_mid * fps)

        video.set(cv.CAP_PROP_POS_FRAMES, frame_id)  # 设置要获取的帧号
        _, frame = video.read()
        resized_frame = cv.resize(frame, (int(640 / frame_shape[0] * frame_shape[1]), 640))
        clipped_frame = resized_frame[box[0][0]:box[0][1], box[1][0]:box[1][1]]

        if cfg.VIS:
            cv.imshow("ocr_img", clipped_frame)
            cv.waitKey(7000)

        result = ocr_reader.ocr(clipped_frame)

        if len(result) == 0:
            subs.__delitem__(i)
            length -= 1
        else:
            subs[i].text = result[0][1]
            i += 1

        count += 1
        if (count % 100) == 0 or count == total:
            elapsed = time.time() - start
            eta = (total - count) / count * elapsed
            print("[{}/{}], Elapsed: {}, ETA: {}".format(count, total, fmt_time(elapsed), fmt_time(eta)))
            subs.save(cfg.OUT)


def video_ocr_audio(cfg):
    reader = OcrReader(cfg)
    # TODO: timeline generation
    ocr_with_timeline(cfg, reader)
    simplify_ass(cfg)

