#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : startup
# @Author  : cgpengda
# @Email   : cgpengda@gmail.com

""""
import sys
path = r'C:\Users\pengda\OneDrive'
if not path in sys.path:
    sys.path.append(path)

from deformer_weight_manager import startup
reload(startup)
startup.main()
"""

from .ui import gui
from maya import cmds

reload(gui)


def main():
    if cmds.window('deformer_manager_window', exists=True):
        cmds.deleteUI('deformer_manager_window', window=True)
    ui = gui.MainWindow()
    ui.show()


if __name__ == "__main__":
    main()
