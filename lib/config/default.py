
# ------------------------------------------------------------------------------
# Copyright (c) Microsoft
# Licensed under the MIT License.
# Written by Bin Xiao (Bin.Xiao@microsoft.com)
# ------------------------------------------------------------------------------

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os

from yacs.config import CfgNode as CN


_C = CN()

_C.LANG = ["ch_tra", "en"]
_C.VIDEO = "input/demo.mp4"
_C.SUB = "input/demo.ass"
_C.BOX = [480, None, 200, 836]
_C.LOSS = CN()
_C.LOSS.USE_OHKM = False
_C.LOSS.PLUS_M = False
_C.LOSS.TOPK = 8
_C.LOSS.USE_TARGET_WEIGHT = True
_C.LOSS.USE_DIFFERENT_JOINTS_WEIGHT = False


def update_config(cfg, args):
    cfg.defrost()
    cfg.merge_from_file(args.cfg)
    for i, border in enumerate(cfg.BOX):
        if border == "None":
            cfg.BOX[i] = None
    cfg.freeze()


if __name__ == '__main__':
    import sys
    with open(sys.argv[1], 'w') as f:
        print(_C, file=f)

