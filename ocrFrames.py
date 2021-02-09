import copy
import shutil
import sys
import time
import os
import requests

import cv2 as cv
import numpy as np

from PIL import Image
from utils import fmt_time, ocr_baidu, get_access_token





def ocr_paddle(img):
    from paddleocr import PaddleOCR, draw_ocr
    # Paddleocr目前支持中英文、英文、法语、德语、韩语、日语，可以通过修改lang参数进行切换
    # 参数依次为`ch`, `en`, `french`, `german`, `korean`, `japan`。
    ocr = PaddleOCR(use_angle_cls=True, lang="ch")  # need to run only once to download and load model into memory
    img_path = 'PaddleOCR/doc/imgs/11.jpg'
    result = ocr.ocr(img_path, cls=True)
    for line in result:
        print(line)

    # 显示结果
    from PIL import Image
    image = Image.open(img_path).convert('RGB')
    boxes = [line[0] for line in result]
    txts = [line[1][0] for line in result]
    scores = [line[1][1] for line in result]
    im_show = draw_ocr(image, boxes, txts, scores, font_path='/path/to/PaddleOCR/doc/simfang.ttf')
    im_show = Image.fromarray(im_show)
    im_show.save('result.jpg')


def frame_ocr(img, img_segged, method, lang="chi_sim", token=None):
    # img_segged_bin = cv.imencode(".jpg", img_segged)[1].tobytes()
    img_bin = cv.imencode(".jpg", img)[1].tobytes()
    if method == "local":
        words = ocr_tesseract(img_segged, lang)
    elif method == "online":
        # words = ocr_baidu(img_segged_bin, token)
        words = ocr_baidu(img_bin, token)
        time.sleep(1)
    return words


def write_srt(txt, fc_start, fc_end, srt_count, content, fps):
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


if __name__ == '__main__':
    # test_format()
    # 视频所在文件夹路径
    clip_box = [[720, None], [480, 1256]]
    debug = True
    vis_start = 18
    language = "chi_tra"
    output_type = "txt"
    srt_color = "white"
    srt_prob_thres = 1
    change_prob_thres = 5
    video_path = "input/ABP-488_clip.mp4"
    # ocr API：本地的EasyOCR 还是 在线的百度
    # ocr_method = "local"
    ocr_method = "online"

    if video_path.endswith(('.mp4', '.mkv', '.avi', '.rmvb')):
        if ocr_method == "online":
            # 百度 API 的 API key 和 Secret key
            access_token = get_access_token('baidu_keys.txt')
            if access_token is None:
                print("Get token error!")
                sys.exit()
            else:
                get_frames(video_path, srt_color, ocr_method, output_type,
                           language, clip_box, srt_prob_thres, change_prob_thres,
                           access_token)
        else:
            get_frames(video_path, srt_color, ocr_method, output_type,
                       language, clip_box, srt_prob_thres, change_prob_thres)
    else:
        raise ValueError("Not a video file:{}".format(video_path))

