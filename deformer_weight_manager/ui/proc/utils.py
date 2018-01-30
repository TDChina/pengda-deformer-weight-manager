#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : utils
# @Author  : cgpengda
# @Email   : cgpengda@gmail.com

import os
try:
    from PySide2 import QtGui
except ImportError:
    from PySide import QtGui

ICON_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'resource/icon').replace('\\', '/')


def get_icon(image, suffix='png'):
    icon = QtGui.QIcon()
    icon.addPixmap(QtGui.QPixmap(os.path.join(ICON_PATH, '%s.%s' % (image, suffix))), QtGui.QIcon.Normal,
                   QtGui.QIcon.Off)
    print icon
    return icon


def get_pixmap(image, suffix='png'):
    pixmap = QtGui.QPixmap(os.path.join(ICON_PATH, '%s.%s' % (image, suffix)))
    return pixmap
