# VIDEO_OCR

基于 paddle_ocr/easy_ocr(本地) 和 百度AI平台(在线) 实现的视频硬嵌入字幕提取

## 依赖

+ python 依赖:  试试通过  `pip install -r requirements.txt` 命令安装

  +  遇到 `ImportError: cannot import name 'etree'` 错误，重装 `lxml` 即可解决

+ 百度 API：
  + 百度 API 在以下界面申请使用: [通用文字识别能力](https://ai.baidu.com/tech/ocr/general)
  + 申请之后，在此目录下新建 `baidu_keys.txt` 文本文档，把 `client_id`、 `client_secret`  分成两行存入该文本文档即可。

## 用法

打开 config/demo.yaml， 修改以下参数以适配自己的视频

```python
OCR_METHOD: "paddle"
LANG:
  - "ch_sim"
  - "en"
VIDEO: "demo/demo.mp4"
BOX:
  - 540
  - None
  - 100
  - 1000
VIS: false
OUT: "output/demo.srt"

SPLIT:
  METHOD: "vision"
  VISION:
    COLOR: "white"
    SRT_THRES: 1.0
    CHANGE_THRES: 5.0
    OUTPUT_SEG: False
  AUDIO:
    ASS_PATH: 'demo/demo.ass'
    MIN: 0.0
    MAX: 0.0
```

## TODO
- [ ] 通过音频生成时间轴
- [ ] 改变视频时间轴方式，改为生成时间轴，而不是保存图片，这样和音频可以共用ocr环节
- [ ] 百度 API 更新
