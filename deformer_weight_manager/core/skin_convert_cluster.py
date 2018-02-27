import maya.cmds as cmds 
import maya.OpenMaya as om
import maya.OpenMayaAnim as oma

selection_joint_list = cmds.ls(selection=True)

for joint_object in selection_joint_list:
    mesh_object = 'pCylinderShape1'
    skin_object = 'skinCluster1'
    #joint_object = 'joint1'

    # input object to dag path
    mesh_selection_list = om.MSelectionList()
    mesh_selection_list.add(mesh_object)
    mesh_dag_path = om.MDagPath()
    mesh_selection_list.getDagPath(0, mesh_dag_path)

    joint_selection_list = om.MSelectionList()
    joint_selection_list.add(joint_object)
    joint_dag_path = om.MDagPath()
    joint_selection_list.getDagPath(0, joint_dag_path)

    skin_selection_list = om.MSelectionList()
    skin_mobject = om.MObject()
    om.MGlobal.getSelectionListByName(skin_object, skin_selection_list)
    skin_selection_list.getDependNode(0, skin_mobject)
    skin_mfn = oma.MFnSkinCluster(skin_mobject)

    # get joint influcenced points and weight values
    components = om.MSelectionList()
    weights    = om.MDoubleArray()
    skin_mfn.getPointsAffectedByInfluence(joint_dag_path, components, weights)

    # create cluster
    components_list = list()
    components.getSelectionStrings(components_list)
    cluster_node = cmds.cluster(components_list)

    cluster_selection_list = om.MSelectionList()
    om.MGlobal.getSelectionListByName(cluster_node[0], cluster_selection_list)
    cluster_mobject = om.MObject()
    cluster_selection_list.getDependNode(0, cluster_mobject)
    cluster_mfn = oma.MFnWeightGeometryFilter(cluster_mobject)

    # get geometry's type to cluster weights type
    geo_dag_path = om.MDagPath()
    geo_comp_obj = om.MObject()
    components.getDagPath(0, geo_dag_path, geo_comp_obj)

    # convert skinweights type to cluster weights type
    cluster_weights_array = om.MFloatArray()
    for index in weights:
        cluster_weights_array.append(index)

    # set weights
    cluster_mfn.setWeight(geo_dag_path, geo_comp_obj, cluster_weights_array)

    # change the cluster position
    chuster_pos = cmds.xform(joint_object, query=1, worldSpace=1, pivots=1)
    cluster_shape = cmds.listRelatives(cluster_node[1], children=True, shapes=True)[0]

    cmds.setAttr("%s.origin" % cluster_shape, chuster_pos[0], chuster_pos[1], chuster_pos[2])
    cmds.move(chuster_pos[0], chuster_pos[1], chuster_pos[2], "%s.scalePivot" % cluster_node[1],
              "%s.rotatePivot" % cluster_node[1])

print '\n# Successfully created new cluster!'