import sys
import time

import cv2 as cv
from pysubs2 import SSAFile
from utils import fmt_time, ocr_baidu, get_access_token


if __name__ == "__main__":
    ass_path = "input/ABP-488.ass"

    # subs = SSAFile.load('S03E09.ass', encoding="utf-16-le")
    subs = SSAFile.load(ass_path)
    for line in subs:
        print(fmt_time(line.start/1000), fmt_time(line.end/1000))