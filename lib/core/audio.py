import argparse
import sys
import time

import cv2 as cv

from pysubs2 import SSAFile
from lib.utils import fmt_time, simplify_ass, OcrReader, ocr_with_timeline


def video_ocr_audio(cfg):
    reader = OcrReader(cfg)
    # TODO: timeline generation
    ocr_with_timeline(cfg, reader)
    simplify_ass(cfg)

