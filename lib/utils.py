import argparse
import base64
import requests
import sys

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
            self.access_token = get_access_token('../../baidu_keys.txt')
            if self.access_token is None:
                print("Get token error!")
                sys.exit()

    def ocr(self, img):
        if self.cfg.METHOD == "easy":
            result = self.model.readtext(img)
        elif self.cfg.METHOD == "paddle":
            result = self.model.ocr(img)
        elif self.cfg.METHOD == "online":
            ocr_baidu(img, self.access_token)
        return result


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


def ocr_baidu(image, ocr_token):
    img = base64.b64encode(image)
    request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic"
    # request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic"
    params = {"image": img}
    request_url = request_url + "?access_token=" + ocr_token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    ocr_response = requests.post(request_url, data=params, headers=headers)
    if ocr_response:
        words = ocr_response.json()['words_result']
        result = ""
        for item in words:
            result += item['words']
        return result
    else:
        return ""
