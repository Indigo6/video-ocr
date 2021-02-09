# PDF_OCR2DOC

基于 Tesseract(本地) 和 百度AI平台(在线) 实现的 pdf 文本识别，并经过格式处理输出到 docx 中

## 依赖

+ Tesseract: [官方指南](https://github.com/tesseract-ocr/tesseract/wiki#windows)

  + 前往  [Tesseract at UB Mannheim](https://github.com/UB-Mannheim/tesseract/wiki)  下载安装包安装

  + 添加环境变量

    >  To access tesseract-OCR from any location you may have to add the directory where the tesseract-OCR binaries are located to the Path variables, probably `C:\Program Files\Tesseract-OCR`. 

  + 在 cmd 中尝试运行 

    ```shell
    命令：
    tesseract -v
    输出如下，即代表成功：
    tesseract v5.0.0-alpha.20191030
     leptonica-1.78.0
      libgif 5.1.4 : libjpeg 8d (libjpeg-turbo 1.5.3) : libpng 1.6.34 : libtiff 4.0.9 : zlib 1.2.11 : libwebp 0.6.1 : libopenjp2 2.3.0
     Found AVX2
     Found AVX
     Found FMA
     Found SSE
     Found libarchive 3.3.2 zlib/1.2.11 liblzma/5.2.3 bz2lib/1.0.6 liblz4/1.7.5
    ```

+ python 依赖:  试试通过  `pip install -r requirements.txt` 命令安装

  +  遇到 `ImportError: cannot import name 'etree'` 错误，重装 `lxml` 即可解决

## 用法

打开 main.py， 修改以下参数以适配自己的扫描版 pdf

```python
    # pdf所在文件夹路径
    dir_path = "./"
    # 获取 pdf 中 image 的方法：每一页 还是 正则式检查每一个对象
    image_method = "页面"
    # pdf 中每一行的文字个数，我取的是非段结尾行的文字个数(如36\37\38)的最小值
    words_per_line = 36
    # ocr API：本地的Tesseract 还是 在线的百度
    # ocr_method = "local"
    ocr_method = "online"
    # 百度 API 的 API key 和 Secret key
    client_id = ""
    client_secret = ""
    with open('baidu_keys.txt', mode='r') as f:
        client_id = f.readline().strip()
        client_secret = f.readline().strip()
```

其中百度 API 在以下界面申请使用: [通用文字识别能力](https://ai.baidu.com/tech/ocr/general)

申请之后，在此目录下新建 `baidu_keys.txt` 文本文档，把 `client_id`、 `client_secret`  分成两行存入该文本文档即可。