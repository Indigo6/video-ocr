import time
import cv2 as cv
import numpy as np

from utils import fmt_time


def test_hsv():
    image_path = "ABP-504_clip_2.png"
    img = cv.imread(image_path)
    img_shape = img.shape
    img = cv.resize(img, (int(480/img_shape[0]*img_shape[1]), 480))
    img = img[400:None, :585]
    cv.imwrite('test1.jpg', img)
    img_hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    lower_hsv = np.array([26, 150, 46])         # 设定黄色下限, hue/saturation/value
    upper_hsv = np.array([34, 255, 255])        # 设定黄色上限
    mask = cv.inRange(img_hsv, lowerb=lower_hsv, upperb=upper_hsv)  # 依据设定的上下限对目标图像进行二值化转换
    dst = cv.bitwise_and(img, img, mask=mask)   # 将二值化图像与原图进行“与”操作；实际是提取前两个frame 的“与”结果，然后输出mask 为1的部分
    # 注意：括号中要写mask=xxx
    print((dst ** 2).sum() / dst.size * 100)
    cv.imwrite('test.jpg', dst)


def test_ocr():
    from paddleocr import PaddleOCR
    import easyocr
    reader = easyocr.Reader(['ch_tra', 'en'], gpu=False)  # need to run only once to load model into memory
    # Paddleocr 目前支持中英文、英文、法语、德语、韩语、日语，可以通过修改lang参数进行切换
    # 参数依次为`ch`, `en`, `french`, `german`, `korean`, `japan`。
    # need to run only once to download and load model into memory
    ocr = PaddleOCR(lang="ch")
    # ocr = PaddleOCR(lang="ch",
    #                 det_model_dir=r'C:\Users\Indigo6\.paddleocr\2.0\ch_ppocr_server_v2.0_det_infer',
    #                 rec_model_dir=r'C:\Users\Indigo6\.paddleocr\2.0\ch_ppocr_server_v2.0_rec_infer')
    # img_path = 'test1.jpg'
    img_path = 'f44.jpg'
    start = time.time()
    # result = ocr.ocr(img_path, rec=False)
    result = ocr.ocr(img_path)
    print('paddle cost time: ', fmt_time(time.time()-start))
    for line in result:
        print(line)

    start = time.time()
    result = reader.readtext(img_path)
    print('EasyOCR cost time: ', fmt_time(time.time()-start))
    for line in result:
        print(line)


def test_gray():
    image_path = "test3.jpg"
    img = cv.imread(image_path)
    imgray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    thresh = 210
    ret, binary = cv.threshold(imgray, thresh, 255, cv.THRESH_BINARY)  # 输入灰度图，输出二值图
    frame_segged = cv.bitwise_not(binary)  # 取反
    srt_prob = (binary**2).sum() / binary.size
    has_srt = False
    if srt_prob < 0.5:
        has_srt = True
    cv.imwrite("out_"+image_path, binary)


if __name__ == '__main__':
    # test_gray()
    test_ocr()

