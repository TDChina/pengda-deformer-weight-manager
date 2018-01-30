#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : gui
# @Author  : cgpengda
# @Email   : cgpengda@gmail.com


from maya import cmds
from maya import OpenMaya
from maya import OpenMayaUI
from .proc import utils
from .resource import manager_qt

reload(utils)
reload(manager_qt)

try:
    from PySide2.QtCore import *
    from PySide2.QtGui import *
    from PySide2.QtWidgets import *
    from shiboken2 import wrapInstance
except ImportError:
    from PySide.QtCore import *
    from PySide.QtGui import *
    from shiboken import wrapInstance


def get_maya_window():
    # noinspection PyArgumentList
    maya_window = OpenMayaUI.MQtUtil.mainWindow()
    return wrapInstance(long(maya_window), QWidget)


class MainWindow(QMainWindow, manager_qt.Ui_deformer_manager_window):
    def __init__(self, parent=get_maya_window()):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)

        self.set_icon()
        self.connect_cmd()

    def set_icon(self):
        self.soft_radio.setIcon(utils.get_icon('softMod'))
        self.blend_radio.setIcon(utils.get_icon('blendShape'))
        self.wire_radio.setIcon(utils.get_icon('wire'))
        self.lattice_radio.setIcon(utils.get_icon('lattice'))
        self.cluster_radio.setIcon(utils.get_icon('cluster'))
        self.skin_radio.setIcon(utils.get_icon('skinCluster'))
        self.to_cluster_radio.setIcon(utils.get_icon('cluster'))
        self.to_skin_radio.setIcon(utils.get_icon('skinCluster'))
        self.source_button.setIcon(utils.get_icon('load'))
        self.target_button.setIcon(utils.get_icon('load'))
        self.convert_to_button.setIcon(utils.get_icon('convert_to'))
        self.copy_to_button.setIcon(utils.get_icon('copy_to'))
        self.clear_button.setIcon(utils.get_icon('clear'))
        self.combine_button.setIcon(utils.get_icon('combine'))
        self.copy_button.setIcon(utils.get_icon('copy'))
        self.mirror_button.setIcon(utils.get_icon('mirror'))
        self.export_button.setIcon(utils.get_icon('export'))
        self.import_button.setIcon(utils.get_icon('import'))

    def connect_cmd(self):
        self.source_button.clicked.connect(lambda: self.load_object_cmd('source'))
        self.target_button.clicked.connect(lambda: self.load_object_cmd('target'))
        self.convert_to_button.clicked.connect(self.convert_cmd)

    def load_object_cmd(self, load_type):
        sel_obj_list = cmds.ls(selection=True)
        if sel_obj_list:
            if load_type == 'source':
                self.source_line.setText(sel_obj_list[0])
                OpenMaya.MGlobal.displayInfo('Load source mesh : %s' % sel_obj_list[0])
            elif load_type == 'target':
                self.target_line.setText(sel_obj_list[0])
                OpenMaya.MGlobal.displayInfo('Load target mesh : %s' % sel_obj_list[0])
        else:
            OpenMaya.MGlobal.displayError('Please select the object.')

    def convert_cmd(self):
        from_type_dict = {"Soft Selection": "softMod", "Blend Shape": "blendShape", "Wire": "wire",
                          "Lattice": "lattice", "Cluster": "cluster", "Skin Cluster": "skin"}
        self.soft_radio.isChecked()
        self.blend_radio.isChecked()
        self.wire_radio.isChecked()



