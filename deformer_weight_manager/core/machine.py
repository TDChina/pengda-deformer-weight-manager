#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : machine
# @Author  : cgpengda
# @Email   : cgpengda@gmail.com


from maya import cmds
from ..ui.proc import utils

reload(utils)

try:
    from PySide2.QtCore import *
    from PySide2.QtGui import *
    from PySide2.QtWidgets import *
    from shiboken2 import wrapInstance
except ImportError:
    from PySide.QtCore import *
    from PySide.QtGui import *
    from shiboken import wrapInstance


class DeformerWeightMachine(object):
    def __init__(self):
        pass

    @staticmethod
    def load_object():
        sel_obj_list = cmds.ls(selection=True)
        print sel_obj_list
