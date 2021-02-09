import copy
import shutil
import time
import os

import cv2 as cv
import numpy as np
from lib.utils import fmt_time


def color_seg(img, color, srt_prob_thres=1):
    if color == "yellow":
        img_hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
        lower_hsv = np.array([26, 130, 46])  # 设定黄色下限, hue/saturation/value
        upper_hsv = np.array([34, 255, 255])  # 设定黄色上限
        mask = cv.inRange(img_hsv, lowerb=lower_hsv, upperb=upper_hsv)
        # 依据设定的上下限对目标图像进行二值化转换
        dst = cv.bitwise_and(img, img, mask=mask)
        # 将二值化图像与原图进行“与”操作；实际是提取前两个frame 的“与”结果，然后输出mask 为1的部分
        # dst = 255 * mask
        #
        # lower_hsv_blue = np.array([100, 100, 46])
        # upper_hsv_blue = np.array([124, 255, 255])
        # mask = cv.inRange(img_hsv, lowerb=lower_hsv_blue, upperb=upper_hsv_blue)
        # dst_blue = cv.bitwise_and(img, img, mask=mask)
        # lower_hsv_loose = np.array([26, 130, 46])
        # upper_hsv_loose = np.array([50, 255, 255])  # 设定黄色上限
        # mask = cv.inRange(img_hsv, lowerb=lower_hsv_loose, upperb=upper_hsv)
        # dst_loose = cv.bitwise_and(img, img, mask=mask)
        # dst_loose = cv.bitwise_or(dst_blue, dst_loose)
    elif color == "white":
        thresh = 220
        lower_rgb = np.array([thresh, thresh, thresh])
        upper_rgb = np.array([255, 255, 255])
        mask = cv.inRange(img, lowerb=lower_rgb, upperb=upper_rgb)
        dst = cv.bitwise_and(img, img, mask=mask)
        # dst = 255 * mask
        # dst_loose = copy.deepcopy(dst)
    else:
        raise ValueError("Only support yellow or white subtitle extract.")
    # srt_prob = (dst.astype(np.float32)**2).sum() / dst.size
    srt_prob = (dst**2).sum() / dst.size
    srt_yes = False
    if srt_prob > srt_prob_thres:
        srt_yes = True
    return dst, srt_yes


def if_srt_frame(img, color, srt_prob_thres=1, seg_method='color'):
    frame_segged, has_srt = color_seg(img, color, srt_prob_thres)
    if has_srt:
        imgray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        thresh = 200
        ret, binary = cv.threshold(imgray, thresh, 255, cv.THRESH_BINARY)  # 输入灰度图，输出二值图
        srt_prob = (binary**2).sum() / binary.size
        if srt_prob > 0.3:
            has_srt = False
    return frame_segged, has_srt


# 差异值哈希算法
def dhash(image):
    # 将图片转化为8*8
    image = cv.resize(image, (9, 8), interpolation=cv.INTER_CUBIC)
    # 将图片转化为灰度图
    if len(image.shape) == 3:
        gray = cv.cvtColor(image, cv.COLOR_RGB2GRAY)
    else:
        gray = image
    dhash_str = ''
    for i in range(8):
        for j in range(8):
            if gray[i, j] > gray[i, j + 1]:
                dhash_str = dhash_str + '1'
            else:
                dhash_str = dhash_str + '0'
    result = ''
    for i in range(0, 64, 4):
        result += ''.join('%x' % int(dhash_str[i: i + 4], 2))
    # print("dhash值",result)
    return result


# 计算两个哈希值之间的差异
def camp_hash(hash1, hash2):
    n = 0
    # hash长度不同返回-1,此时不能比较
    if len(hash1) != len(hash2):
        return -1
    # 如果hash长度相同遍历长度
    for i in range(len(hash1)):
        if hash1[i] != hash2[i]:
            n = n + 1
    return n


def hash_compare(img1, img2):
    hash1 = dhash(img1)
    hash2 = dhash(img2)
    return camp_hash(hash1, hash2)


def if_srt_changed(last_img, now_img):
    srt_changed = False
    srt_change_prob = hash_compare(last_img, now_img)
    if srt_change_prob > change_prob_thres:
        res = cv.absdiff(last_img, now_img)
        mean_res = res.sum() / res.size
        if mean_res > 10:
            srt_changed = True
    return srt_changed


def get_frames(video_path, srt_color, box, srt_prob_thres=1, change_prob_thres=1):

    _, video_name = os.path.split(video_path)
    frame_dir = 'frame/'+video_name+'/'
    if os.path.exists(frame_dir):
        shutil.rmtree(frame_dir)
    os.mkdir(frame_dir)

    video = cv.VideoCapture(video_path)
    frames_num = video.get(7)
    fps = video.get(5)

    fc = 0
    srt_count = 0
    fc_start = 0
    in_srt = False
    last_srt_frame = None
    last_srt_seg_frame = None
    time_start = time.time()
    while True:
        ret, frame = video.read()
        if not ret:
            break
        frame_shape = frame.shape
        resized_frame = cv.resize(frame, (int(640/frame_shape[0]*frame_shape[1]), 640))
        clipped_frame = resized_frame[box[0][0]:box[0][1], box[1][0]:box[1][1]]
        fc += 1

        frame_segged, has_srt = if_srt_frame(clipped_frame, srt_color, srt_prob_thres)
        if fc > (fps * vis_start):
            if debug:
                cv.imshow('resized', resized_frame)
                cv.waitKey(0)
                cv.imshow('clipped', clipped_frame)
                cv.waitKey(0)
                cv.imshow('segged', frame_segged)
                cv.waitKey(0)
        if has_srt:
            if not in_srt:
                in_srt = True
                fc_start = fc
                last_srt_frame = copy.deepcopy(clipped_frame)
                last_srt_seg_frame = copy.deepcopy(frame_segged)
            else:
                if if_srt_changed(last_srt_seg_frame, frame_segged):
                    srt_count += 1
                    cv.imwrite("{}/f{}_l{}.jpg".format(frame_dir, fc_start, fc-fc_start),
                               last_srt_frame)
                    if output_segged_frame:
                        cv.imwrite("{}/f{}_l{}_segged.jpg".format(frame_dir, fc_start, fc-fc_start),
                                   last_srt_seg_frame)
                    fc_start = fc
                    last_srt_frame = copy.deepcopy(clipped_frame)
                    last_srt_seg_frame = copy.deepcopy(frame_segged)
        else:
            if in_srt:
                in_srt = False
                cv.imwrite("{}/f{}_l{}.jpg".format(frame_dir, fc_start, fc-fc_start), last_srt_frame)
                if output_segged_frame:
                    cv.imwrite("{}/f{}_l{}_segged.jpg".format(frame_dir, fc_start, fc-fc_start),
                               last_srt_seg_frame)
                srt_count += 1
                fc_start = 0
        
        elapsed = time.time() - time_start
        eta = (frames_num - fc) * elapsed / fc if fc > 0 else 0
        print('[%d/%d] Elapsed: %s, ETA: %s' % (fc, frames_num,
                                                fmt_time(elapsed),
                                                fmt_time(eta)))
    video.release()


if __name__ == '__main__':  
    # test_format()
    # 视频所在文件夹路径
    video_path = "input/ABP-488_clip.mp4"

    debug = False
    output_segged_frame = True

    vis_start = 18
    clip_box = [[480, None], [200, 836]]

    srt_color = "white"
    srt_prob_thres = 1
    change_prob_thres = 5

    if video_path.endswith(('.mp4', '.mkv', '.avi', '.rmvb')):
        get_frames(video_path, srt_color, clip_box, 
                   srt_prob_thres, change_prob_thres)
    else:
        raise ValueError("Not a video file:{}".format(video_path))