
# ------------------------------------------------------------------------------
# Copyright (c) Microsoft
# Licensed under the MIT License.
# Written by Bin Xiao (Bin.Xiao@microsoft.com)
# ------------------------------------------------------------------------------

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from yacs.config import CfgNode as CN


_C = CN()

_C.OCR_METHOD = "easy"
_C.LANG = ["ch_tra", "en"]
_C.VIDEO = "input/demo.mp4"
_C.OUT = "output/demo.srt"
_C.BOX = [480, None, 200, 836]
_C.VIS = False

_C.SPLIT = CN()
_C.SPLIT.METHOD = "vision"

_C.SPLIT.VISION = CN()
_C.SPLIT.VISION.COLOR = 'white'
_C.SPLIT.VISION.SRT_THRES = 1.0
_C.SPLIT.VISION.CHANGE_THRES = 5.0
_C.SPLIT.VISION.OUT_IMG = False
_C.SPLIT.VISION.OUT_SEG = False

_C.SPLIT.AUDIO = CN()
_C.SPLIT.AUDIO.MIN = 1.0
_C.SPLIT.AUDIO.MAX = 1.0


def update_config(cfg, args):
    cfg.defrost()
    cfg.merge_from_file(args.cfg)
    for i, border in enumerate(cfg.BOX):
        if border == "None":
            cfg.BOX[i] = None
    _, path = _C.VIDEO.split('/')
    name, _ = path.split('.')
    # _C.OUT = "output/" + name + ".ass"
    cfg.freeze()


if __name__ == '__main__':
    import sys
    with open(sys.argv[1], 'w') as f:
        print(_C, file=f)

