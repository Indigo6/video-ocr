import argparse
import base64
import easyocr
import os
import re
import requests
import sys
import time

import cv2 as cv

from paddleocr import PaddleOCR
from pysubs2 import SSAFile
from PyQt5.Qt import QPixmap
from PyQt5.QtWidgets import QGraphicsScene, QMessageBox, QGraphicsView
from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtGui import QPen, QImage
from qimage2ndarray import array2qimage


class OcrReader:
    def __init__(self, ocr_method, lang):
        self.method = ocr_method
        if self.method == "easy":
            self.model = easyocr.Reader(lang)
        elif self.method == "paddle":
            self.model = PaddleOCR(use_angle_cls=False, lang="ch")
        elif self.method == "online":
            # 百度 API 的 API key 和 Secret key
            self.access_token = get_access_token('baidu_keys.txt')

            if self.access_token is None:
                print("Get token error!")
                sys.exit()

    def ocr(self, img):
        content = []
        if self.method == "easy":
            result = self.model.readtext(img)
            for roi in result:
                content.append(roi[1])
        elif self.method == "paddle":
            result = self.model.ocr(img)
            for roi in result:
                content.append(roi[1][0])
        elif self.method == "online":
            result = ocr_baidu_http(img, self.access_token)
            for item in result:
                content.append(item['words'])
        return content


class MyGraphicsView(QGraphicsView):
    def __init__(self, central_widget):
        super().__init__(central_widget)
        self.widget = central_widget
        self.start = [0, 0]
        self.end = [0, 0]
        self.my_scene = QGraphicsScene()
        self.rect = QRectF()
        self.old_rect_item = None
        self.old_img_item = None
        self.drawing = False

    def mousePressEvent(self, event):
        self.start = [event.x(), event.y()]
        self.drawing = True

    def mouseMoveEvent(self, event):
        if not self.drawing:
            return
        self.end = [event.x(), event.y()]

        temp_start = [min(self.start[0], self.end[0]), min(self.start[1], self.end[1])]
        temp_end = [max(self.start[0], self.end[0]), max(self.start[1], self.end[1])]

        if self.old_rect_item:
            self.my_scene.removeItem(self.old_rect_item)

        self.rect.setRect(temp_start[0], temp_start[1], temp_end[0] - temp_start[0], temp_end[1] - temp_start[1])
        self.old_rect_item = self.my_scene.addRect(self.rect, QPen(Qt.red, 3, Qt.SolidLine))
        self.setScene(self.my_scene)

    # 释放鼠标
    def mouseReleaseEvent(self, event):
        print('start:[{}, {}]'.format(self.start[0], self.start[1]))
        print('end:[{}, {}]'.format(self.end[0], self.end[1]))
        print(self.rect.getRect())
        
        self.drawing = False


def ocr_with_timeline(video, video_path, box, ocr_reader, lang, main_window, progress_bar):
    fps = video.get(5)

    _, video_name = os.path.split(video_path)
    video_name = video_name.split('.')[0]
    frame_dir = 'frame/'+video_name+'/'

    subs = SSAFile.load(frame_dir+'/split_vision.ass')

    prefix = video_path[:-len(video_path.split('.')[-1])]

    total = len(subs)
    start = time.time()
    count = 0

    re_chinese = re.compile(u"[\u4e00-\u9fa5]+")
    re_ascii = re.compile(r'\w+', re.ASCII)

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
        clipped_frame = frame[box[0][0]:box[0][1], box[1][0]:box[1][1]]

        result = ocr_reader.ocr(clipped_frame)
        print(result)
        if len(result) == 0:
            subs.__delitem__(i)
            length -= 1
        else:
            # subs[i].text = result[0]
            if len(lang) == 2:
                split = list(map(lambda x: len(x), [re.findall(re_chinese,result[i]) for i in range(len(result))]))
                eng_str = []
                ch_str = []
                iseng = 1
                for str_ind in reversed(range(len(result))):
                    iseng += split[str_ind]
                    if iseng == 1:
                        eng_str.append(result[str_ind])
                    else:
                        ch_str.append(result[str_ind])
                eng_str = ' '.join(reversed(eng_str))
                ch_str = ''.join(reversed(ch_str))
                subs[i].text = re.findall(re_chinese, ch_str)[0]
                subs[i+1].text = ' '.join(re.findall(re_ascii, eng_str))
            else:
                subtitle = ''.join(result)
                subs[i].text = re.findall(re_chinese, subtitle)[0]

            i += len(lang)

        count += len(lang)
        progress_bar.setValue(int(count / total * 100) + 1)
        if (count % 1) == 0 or count == total:
            elapsed = time.time() - start
            eta = (total - count) / count * elapsed
            print("[{}/{}], Elapsed: {}, ETA: {}".format(count, total, fmt_time(elapsed), fmt_time(eta)))
            subs.save(prefix+'ass', format_='ass')

    progress_bar.setValue(100)
    QMessageBox.information(main_window, "提示", "字幕生成成功！", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
    progress_bar.setValue(0)


def parse_args():
    parser = argparse.ArgumentParser(description='Video OCR')
    # general
    parser.add_argument('--cfg',
                        default='config/demo.yaml',
                        help='experiment configure file name',
                        type=str)
    args = parser.parse_args()
    return args


def check_dir():
    if not os.path.exists('frame'):
        os.mkdir('frame')


def get_empty_sub():
    text = '''
               1
               00:00:00,000 --> 00:00:05,000
               An example SubRip file.
           '''
    subs = SSAFile.from_string(text)
    subs.__delitem__(0)
    return subs


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
        _ = f.readline().strip()
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


# def get_baidu_client(key_file_path):
#     from aip import AipOcr
#     with open(key_file_path, mode='r') as f:
#         app_id = f.readline().strip()
#         client_id = f.readline().strip()
#         client_secret = f.readline().strip()
#
#     client = AipOcr(app_id, client_id, client_secret)
#     return client


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


def cv_to_qt(img):
    """
    将用 opencv 读入的图像转换成qt可以读取的图像
    ========== =====================
    序号       支持类型
    ========== =================
             1 灰度图 Gray
             2 三通道的图 BGR顺序
             3 四通道的图 BGRA顺序
    ========= ===================
    """
    if len(img.shape) == 2:
        # 读入灰度图的时候
        image = array2qimage(img)
    elif len(img.shape) == 3:
        # 读入RGB或RGBA的时候
        if img.shape[2] == 3:
            # 转换为RGB排列
            rgb_img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
            # rgb_img.shape[1]*rgb_img.shape[2]这一句时用来解决扭曲的问题
            # 详情参考 https://blog.csdn.net/owen7500/article/details/50905659 这篇博客
            image = QImage(rgb_img, rgb_img.shape[1], rgb_img.shape[0],
                           rgb_img.shape[1] * rgb_img.shape[2], QImage.Format_RGB888)
        elif img.shape[2] == 4:
            # 读入为RGBA的时候
            rgba_img = cv.cvtColor(img, cv.COLOR_BGRA2RGBA)
            image = array2qimage(rgba_img)
    return image


def get_image_view(scene, img_view, image):
    width = scene.width()
    height = scene.height()
    row, col = image.shape[1], image.shape[0]
    a = float(width / row)
    b = float(height / col)
    if a < b:
        scale = a
    else:
        scale = b
    dim = (int(row * scale), int(col * scale))
    # 缩放图像
    resized_frame = cv.resize(image, dim)
    # 将OpenCV格式储存的图片转换为QT可处理的图片类型
    show_img = cv_to_qt(resized_frame)

    # 将图片放入图片显示窗口
    img_item = scene.addPixmap(QPixmap.fromImage(show_img))

    width = img_item.boundingRect().getRect()[2]
    height = img_item.boundingRect().getRect()[3]
    scene_width = img_view.my_scene.width()
    scene_height = img_view.my_scene.height()

    img_item.setX((scene_width - width) / 2)
    img_item.setY((scene_height - height) / 2)
    return img_item
