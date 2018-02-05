import maya.api.OpenMaya as om
import maya.cmds as cmds

selectionList = cmds.ls(selection=True)

for deformObject in selectionList:
    meshObject = 'pCylinderShape1'
    #deformObject = 'cluster3Handle'

    # input object to dag path
    meshSelectionList = om.MSelectionList()
    meshSelectionList.add(meshObject)
    meshDagPath = meshSelectionList.getDagPath(0)

    deformSelectionList = om.MSelectionList()
    deformSelectionList.add(deformObject)
    deformDagPath = deformSelectionList.getDagPath(0)

    # get the vertex orig position
    mfnMesh = om.MFnMesh(meshDagPath)
    origPositionList = mfnMesh.getPoints(om.MSpace.kObject)

    # set the transform value to deformer
    mfnTransform = om.MFnTransform(deformDagPath)
    xyzMVector = om.MVector(0, 1, 0)
    mfnTransform.setTranslation(xyzMVector, om.MSpace.kTransform)

    deforPositionList = mfnMesh.getPoints(om.MSpace.kObject)

    zeroMVector = om.MVector(0, 0, 0)
    mfnTransform.setTranslation(zeroMVector, om.MSpace.kTransform)

    weightList = {}
    for index in range(len(origPositionList)):
        origMVector = om.MVector(origPositionList[index])
        deformMVector = om.MVector(deforPositionList[index])
        
        length = origMVector - deformMVector
        weight = length.length()
        weightList.setdefault(index, weight)

    # create new cluster
    new_cluster = cmds.cluster(meshObject, n='new_cluster')

    # set weight to vertex
    for vertex, weight in weightList.iteritems():
        cmds.setAttr('%s.weightList[0].w[%d]' % (new_cluster[0], vertex), weight)

    # change the cluster position
    chuster_pos = cmds.xform(deformObject, query=1, worldSpace=1, pivots=1)
    cluster_shape = cmds.listRelatives(new_cluster, children=True, shapes=True)[0]
    
    cmds.setAttr("%s.origin" % cluster_shape, chuster_pos[0], chuster_pos[1], chuster_pos[2])
    cmds.move(chuster_pos[0], chuster_pos[1], chuster_pos[2], "%s.scalePivot" % new_cluster[1],
              "%s.rotatePivot" % new_cluster[1])

print '\n# Successfully created new cluster!'


