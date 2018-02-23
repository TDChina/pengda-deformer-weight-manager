#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : soft_convert_cluster.py
# @Author  : cgpengda
# @Email   : cgpengda@gmail.com


import maya.cmds as cmds
import maya.OpenMaya as om


def soft_convert_cluster():
    """
    softMode weight convert cluster
    """
    # Get selected point position
    selected_point = cmds.ls(selection=True, flatten=True)
    selected_point_pos = cmds.pointPosition(selected_point, world=True)

    # Get soft selection range
    components = om.MSelectionList()
    soft_selection = om.MRichSelection()
    om.MGlobal.getRichSelection(soft_selection)
    soft_selection.getSelection(components)

    # Get soft weight list
    weight_list = {}
    full_name = None
    short_name = None
    dag_path = om.MDagPath()
    component = om.MObject()
    vertex_iter = om.MItSelectionList(components, om.MFn.kMeshVertComponent)
    while not vertex_iter.isDone():
        vertex_iter.getDagPath(dag_path, component)
        dag_path.pop()
        full_name = dag_path.fullPathName()
        short_name = full_name.split("|")[-1]
        fn_components = om.MFnSingleIndexedComponent(component)
        for i in range(fn_components.elementCount()):
            weight_list.setdefault(fn_components.element(i), fn_components.weight(i).influence())
        vertex_iter.next()

    # Create cluster
    vertex_list = ["%s.vtx[%d]" % (full_name, vertex) for vertex in weight_list]
    new_cluster = cmds.cluster(vertex_list, n='%s_SoftToCluster' % short_name)

    # Set cluster weight
    for vertex, weight in weight_list.iteritems():
        cmds.setAttr('%s.weightList[0].w[%d]' % (new_cluster[0], vertex), weight)

    # Set cluster position
    new_cluster_shape = cmds.listRelatives(new_cluster, children=True, shapes=True)[0]
    cmds.setAttr("%s.origin" % new_cluster_shape, selected_point_pos[0], selected_point_pos[1], selected_point_pos[2])
    cmds.move(selected_point_pos[0], selected_point_pos[1], selected_point_pos[2], "%s.scalePivot" % new_cluster[1],
              "%s.rotatePivot" % new_cluster[1])


if __name__ == '__main__':
    soft_convert_cluster()
