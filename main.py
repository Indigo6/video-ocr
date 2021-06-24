from lib.utils import parse_args
from lib.config import cfg, update_config
from lib.core.vision import video_ocr_vision
from lib.core.audio import video_ocr_audio


if __name__ == "__main__":
    args = parse_args()
    update_config(cfg, args)

    video_path = cfg.VIDEO
    if not cfg.VIDEO.endswith(('.mp4', '.mkv', '.avi', '.rmvb')):
        raise ValueError("Not a video file:{}".format(cfg.VIDEO))

    if cfg.SPLIT.METHOD == 'vision':
        video_ocr_vision(cfg)
    else:
        video_ocr_audio(cfg)
