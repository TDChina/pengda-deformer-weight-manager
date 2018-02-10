import maya.cmds as cmds
import maya.OpenMaya as om


# Get wire node
sel_object = cmds.ls(selection=True)[0]
sel_object_shape = cmds.listRelatives(sel_object, children=True, shapes=True)[0]
wire_node = cmds.listConnections(sel_object_shape, type='wire')[0]
crv_shape = cmds.listConnections(wire_node,sh=1,t='nurbsCurve')[1]
crv = cmds.listRelatives(crv_shape, parent=True)[0]

curve_spans = cmds.getAttr('%s.spans' % crv_shape)
curve_degree = cmds.getAttr('%s.degree' % crv_shape)
vertx_count = curve_spans + curve_degree

# Create joint
wire_jnt_grp = cmds.group(empty=True, name='%s_wire_jnt_grp' % sel_object)
root_jnt = cmds.joint(name='%s_wire_root_jnt' % sel_object)

cmds.select(clear=True)
for index in range(vertx_count):
    cv = '%s.cv[%d]' % (crv, index)
    pos = cmds.pointPosition(cv)
    jnt = cmds.joint(position=pos, name='%s_wire_%02d_jnt' % (sel_object, index+1))
    cmds.parent(jnt, wire_jnt_grp)
    cmds.select(clear=True)

# Make skin 
cmds.select('*wire_*_jnt')
jnt_list = cmds.ls(selection=True)

cmds.skinCluster(jnt_list, sel_object, toSelectedBones=True, bindMethod=1, skinMethod=0, normalizeWeights=1, weightDistribution=0, 
                 maximumInfluences=3, 
                 dropoffRate=4.0)
