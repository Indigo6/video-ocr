import base64
import requests


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