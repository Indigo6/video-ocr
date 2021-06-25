# VIDEO_OCR

基于 paddle_ocr/easy_ocr(本地) 和 百度AI平台(在线) 实现的视频硬嵌入字幕提取

## 依赖

+ python 依赖:  通过  `pip install -r requirements.txt` 命令安装

+ 百度 API：
  + 百度 API 在以下界面申请使用: [通用文字识别能力](https://ai.baidu.com/tech/ocr/general)
  
  + 申请之后，在此目录下新建 `baidu_keys.txt` 文本文档，把 `app_id` 、 `client_id`、 `client_secret`  分成两行存入该文本文档即可。
  
  + 详见 [HTTP-SDK文档](https://cloud.baidu.com/doc/OCR/s/wkibizyjk)
  
    > 常量`APP_ID`在百度智能云控制台中创建，常量`API_KEY`与`SECRET_KEY`是在创建完毕应用后，系统分配给用户的，均为字符串，用于标识用户，为访问做签名验证，可在AI服务控制台中的**应用列表**中查看。
    >
    > **注意**：如您以前是百度智能云的老用户，其中`API_KEY`对应百度智能云的“Access Key ID”，`SECRET_KEY`对应百度智能云的“Access Key Secret”。

## 用法

1. 打开 config/demo.yaml， 修改以下参数以适配自己的视频
    ```python
    OCR_METHOD: "paddle"            # ocr方法：paddle/easy/online
    LANG:                           # 字幕语言，TODO: 自动转成各种OCR需要的缩写
      - "ch_sim"
      - "en"
    VIDEO: "demo/demo.mp4"          # 输入视频（硬嵌入字幕视频）路径
    BOX:                            # 字幕在画面中的大致位置
      - 540                           # 上边界
      - None                          # 下边界
      - 100                           # 左边界
      - 1000                          # 右边界
    VIS: false                      # 是否可视化图片腐蚀结果
    OUT: "output/demo.srt"          # 提取结果字幕输出路径
    
    SPLIT:                          # 时间轴生成
      METHOD: "vision"                # vision/audio 使用视觉还是音频来生成时间轴
      VISION:                         # 使用视觉生成时间轴
        COLOR: "white"                  # 字幕颜色
        SRT_THRES: 1.0                  #
        CHANGE_THRES: 5.0               #
        OUT_IMG: true                   # 是否保存字幕关键帧
        OUT_SEG: false                  # 是否保存腐蚀后的字幕关键帧
      AUDIO:                         # 使用音频生成时间轴
        MIN: 0.0                        # 人声最低音量
        MAX: 0.0                        # 人声最高音量
    ```

## TODO
- [x] 改变视频时间轴方式，改为生成时间轴，而不是保存图片，这样和音频可以共用ocr环节
- [x] 百度 API 更新
- [ ] 通过音频生成时间轴
- [ ] 自动转成各种OCR需要的缩写
