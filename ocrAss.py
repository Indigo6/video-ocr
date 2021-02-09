import argparse
import sys
import time
import easyocr

import cv2 as cv

from pysubs2 import SSAFile
from lib.utils import fmt_time, simplify_ass
from lib.config import cfg, update_config


def ocr_with_timeline():
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

        result = reader.readtext(clipped_frame)

        if len(result) == 0:
            subs.__delitem__(i)
            length -= 1
        else:
            subs[i].text = result[0][1]
            i += 1

        count += 1
        if (count % 100) == 0:
            elapsed = time.time() - start
            eta = (total - count) / count * elapsed
            print("Line {}, Elapsed: {}, ETA: {}".format(count, fmt_time(elapsed), fmt_time(eta)))
            subs.save(ass_path)


def parse_args():
    parser = argparse.ArgumentParser(description='Train keypoints network')
    # general
    parser.add_argument('--cfg',
                        help='experiment configure file name',
                        required=True,
                        type=str,
                        default='')
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = parse_args()
    update_config(cfg, args)

    reader = easyocr.Reader(cfg.LANG)

    video_path = cfg.VIDEO
    ass_path = cfg.SUB
    box = [cfg.BOX[:2], cfg.BOX[2:]]

    video = cv.VideoCapture(video_path)
    fps = video.get(5)  # 设置要获取的帧号
    ret, test_frame = video.read()
    if not ret:
        print("Open Video Error!")
        sys.exit()
    frame_shape = test_frame.shape

    ocr_with_timeline()
    simplify_ass(ass_path)
