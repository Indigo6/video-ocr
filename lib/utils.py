import argparse
import base64
import requests
import sys
import time

import cv2 as cv

from pysubs2 import SSAFile


class OcrReader:
    def __init__(self, cfg):
        self.cfg = cfg
        self.method = cfg.OCR_METHOD
        if cfg.OCR_METHOD == "easy":
            import easyocr
            self.model = easyocr.Reader(cfg.LANG)
        elif cfg.OCR_METHOD == "paddle":
            from paddleocr import PaddleOCR
            self.model = PaddleOCR(use_angle_cls=True, lang="ch")
        elif cfg.OCR_METHOD == "online":
            # 百度 API 的 API key 和 Secret key
            self.access_token = get_access_token('baidu_keys.txt')

            if self.access_token is None:
                print("Get token error!")
                sys.exit()

    def ocr(self, img):
        content = []
        if self.cfg.OCR_METHOD == "easy":
            result = self.model.readtext(img)
            for roi in result:
                content.append(roi[1])
        elif self.cfg.OCR_METHOD == "paddle":
            result = self.model.ocr(img)
            for roi in result:
                content.append(roi[1][0])
        elif self.cfg.OCR_METHOD == "online":
            result = ocr_baidu_http(img, self.access_token)
            for item in result:
                content.append(item['words'])
        return content


def ocr_with_timeline(cfg, ocr_reader, ass_path):
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
            subs[i].text = result[0]
            # TODO: 双语字幕
            i += 1

        count += 1
        if (count % 1) == 0 or count == total:
            elapsed = time.time() - start
            eta = (total - count) / count * elapsed
            print("[{}/{}], Elapsed: {}, ETA: {}".format(count, total, fmt_time(elapsed), fmt_time(eta)))
            subs.save(cfg.OUT, format_=cfg.OUT.split('.')[-1])


def parse_args():
    parser = argparse.ArgumentParser(description='Train keypoints network')
    # general
    parser.add_argument('--cfg',
                        default='config/demo.yaml',
                        help='experiment configure file name',
                        type=str)
    args = parser.parse_args()
    return args


# 用于对输出任务进度中的时间进行格式化
def fmt_time(dtime):
    if dtime <= 0:
        return '0:00.000'
    elif dtime < 60:
        return '0:%02d.%03d' % (int(dtime), int(dtime * 1000) % 1000)
    elif dtime < 3600:
        return '%d:%02d.%03d' % (int(dtime / 60), int(dtime) % 60, int(dtime * 1000) % 1000)
    else:
        return '%d:%02d:%02d.%03d' % (int(dtime / 3600), int((dtime % 3600) / 60), int(dtime) % 60,
                                      int(dtime * 1000) % 1000)


def is_contain_chinese(check_str):
    """
    判断字符串中是否包含中文
    :param check_str: {str} 需要检测的字符串
    :return: {bool} 包含返回True， 不包含返回False
    """
    for ch in check_str:
        if u'\u4e00' <= ch <= u'\u9fff':
            return True
    return False


def simplify_ass(cfg):
    # subs = SSAFile.load('S03E09.ass', encoding="utf-16-le")
    subs = SSAFile.load(cfg.OUT)

    last_txt = None
    last_index = 0

    i = 0
    length = len(subs)
    while i < length:
        line = subs[i]
        if not is_contain_chinese(line.text):
            subs.__delitem__(i)
            length -= 1
        elif line.text == last_txt:
            subs[last_index].end = line.end
            subs.__delitem__(i)
            length -= 1
        else:
            last_index = i
            last_txt = line.text
            i += 1
    subs.save(cfg.OUT)


def get_access_token(key_file_path):
    access_token = None
    with open(key_file_path, mode='r') as f:
        app_id = f.readline().strip()
        client_id = f.readline().strip()
        client_secret = f.readline().strip()
        # client_id 为官网获取的AK， client_secret 为官网获取的SK
        host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&' \
               + 'client_id={}&client_secret={}'.format(client_id, client_secret)
        response = requests.get(host)
        if response:
            access_token = response.json()["access_token"]
            print(access_token)
    return access_token


def ocr_baidu_http(image, ocr_token):
    image = cv.imencode(".jpg", image)[1].tobytes()
    img = base64.b64encode(image)
    request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic"
    # request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic"
    params = {"image": img}
    request_url = request_url + "?access_token=" + ocr_token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    ocr_response = requests.post(request_url, data=params, headers=headers)
    if ocr_response:
        words = ocr_response.json()['words_result']
        return words
    else:
        return ""


def get_baidu_client(key_file_path):
    from aip import AipOcr
    with open(key_file_path, mode='r') as f:
        app_id = f.readline().strip()
        client_id = f.readline().strip()
        client_secret = f.readline().strip()

    client = AipOcr(app_id, client_id, client_secret)
    return client


def ocr_baidu_aip(image, client):
    image = cv.imencode(".jpg", image)[1].tobytes()
    """ 如果有可选参数 """
    options = {"language_type": "CHN_ENG",
               "detect_direction": "true",
               "detect_language": "true",
               "probability": "true"}

    """ 带参数调用通用文字识别, 图片参数为本地图片 """
    result = client.basicGeneral(image, options)
    return result

