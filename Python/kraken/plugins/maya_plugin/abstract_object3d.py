"""Kraken Maya - Maya Builder module.

Classes:
Builder -- Component representation.

"""

# import json
import logging

from kraken.log import getLogger
# from kraken.core.kraken_system import ks
from kraken.core.objects.object_3d import Object3D

import pymel.core as pm


logger = getLogger('kraken')
logger.setLevel(logging.INFO)


class AbstractSkeleton(Object3D):

    def __init__(self, buildName, rigGraph):
        super(AbstractSkeleton, self).__init__(buildName, None)

        self.rigGraph = rigGraph
        canvasNode = self.rigGraph.nodeName

        self.canvasNode = canvasNode
        self._boneCount = 0

        buildName = '{}Skeleton'.format(buildName)

        pm.FabricCanvasSetExtDeps(mayaNode=canvasNode,
                                  execPath="",
                                  extDep="Characters")

        pm.FabricCanvasSetExtDeps(mayaNode=canvasNode,
                                  execPath="",
                                  extDep="Kraken.KrakenForCanvas")

        initializeSkeletonNode = pm.FabricCanvasAddGraph(mayaNode=canvasNode,
                                                         execPath="",
                                                         xPos="0",
                                                         yPos="100",
                                                         title="initializeSkeleton")

        self.containerNodeName = initializeSkeletonNode
        self.containerNodeExec = self.rigGraph.getSubExec(self.containerNodeName)
        self.rigGraph.addExtDep("KrakenForCanvas", dfgExec=self.containerNodeExec)

        path = self.containerNodeName + "emptyTransformArray"
        emptyTransformArray = self.rigGraph.createNodeFromPreset(path,
                                                                 "Fabric.Core.Array.EmptyArray",
                                                                 dfgExec=self.containerNodeExec)

        addBone = self.rigGraph.createNodeFromPreset(buildName + "push",
                                                     "Fabric.Core.Array.Push",
                                                     dfgExec=self.containerNodeExec)

        self.rigGraph.connectNodes(emptyTransformArray, "output", addBone, "array", dfgExec=self.containerNodeExec)

        path = self.containerNodeName + "skeletonVariable"
        self.variableNode = self.rigGraph.createVariableNode(path,
                                                             "transforms",
                                                             "KrakenTransform[]",
                                                             extension="KrakenForCanvas",
                                                             dfgExec=self.containerNodeExec)

        self.rigGraph.connectNodes(addBone, "array", self.variableNode, "value", dfgExec=self.containerNodeExec)

        self.setLastBoneNode(addBone)
        # self.skeletonDestNode = cacheNode

    def getNode(self):
        return self.canvasNode

    def setLastBoneNode(self, node):
        self.lastBoneNode = node

    def addBone(self, abstractBone):

        def _setPortVal(node, key, val):
            self.rigGraph.setPortDefaultValue(node, key, val, dfgExec=self.containerNodeExec)

        # composeBone node
        boneNode = self.rigGraph.createNodeFromPresetSI(abstractBone,
                                                        "Kraken.KrakenForCanvas.Constructors.KrakenTransform",
                                                        abstractBone.buildName,
                                                        dfgExec=self.containerNodeExec)

        _setPortVal(boneNode, "name", abstractBone.buildName)
        _setPortVal(boneNode, "buildName", abstractBone.buildName)
        _setPortVal(boneNode, "path", abstractBone.getPath())

        addBone = self.rigGraph.createNodeFromPreset(abstractBone.buildName + "push",
                                                     "Fabric.Core.Array.Push",
                                                     dfgExec=self.containerNodeExec)

        self.rigGraph.connectNodes(boneNode, "result", addBone, "element", dfgExec=self.containerNodeExec)
        self.rigGraph.connectNodes(self.lastBoneNode, "array", addBone, "array", dfgExec=self.containerNodeExec)
        self.rigGraph.connectNodes(addBone, "array", self.variableNode, "value", dfgExec=self.containerNodeExec)

        '''
        pm.FabricCanvasSetPortDefaultValue(mayaNode=self.canvasNode,
                                           execPath="initializeSkeleton",
                                           portPath="{}.referencePose".format(boneNode),
                                           type="Xfo",
                                           value='{}'.format(abstractBone.getXfoAsJson()))

        '''

        abstractBone.setBoneNode(boneNode)
        abstractBone.setAddBoneNode(addBone)
        abstractBone.setBoneIndex(self._boneCount)
        self.setLastBoneNode(addBone)
        self._boneCount += 1


class AbstractBone(Object3D):

    def __init__(self, kSceneItem, buildName, skeleton):
        super(AbstractBone, self).__init__(buildName, skeleton)

        self.canvasNode = skeleton.getNode()
        self.buildName = buildName

        self.xfo = kSceneItem.xfo
        self._index = -1

        skeleton.addBone(self)

    def setBoneIndex(self, id):
        self._index = id

    def getBoneIndex(self):
        return self._index

    @property
    def id(self):
        return self._index

    ###################################
    # implement Maya object's behaviour
    ###################################

    def setTransform(self, kObject):
        self.setReferencePose(self.__xfo)

    def lockParameters(self, kObject):
        pass

    def setVisibility(self, kObject):
        pass

    def setObjectColor(self, kObject):
        pass

    def setRotation(self, quat, space):
        pass

    def setRotationOrder(self, axis,  flag):
        pass

    def setScale(self, vec):
        pass

    def setTranslation(self, vec, space):
        pass

    def exists(self):
        pass

    def getShape(self):
        return None

    ##################
    #
    ##################
    def setBoneNode(self, node):
        self.boneNode = node

    def setAddBoneNode(self, node):
        self.addBoneNode = node

    def setReferencePose(self, xfo):

        pm.FabricCanvasSetPortDefaultValue(
            mayaNode=self.canvasNode,
            execPath="initializeSkeleton",
            portPath="{}.referencePose".format(self.boneNode),
            type="Xfo",
            value='{}'.format(self.getXfoAsJson()))

    def getXfoAsJson(self):
        qat = self.xfo.ori
        ori = self.xfo.ori.v
        pos = self.xfo.tr
        scl = self.xfo.sc

        json = r"""{{
                "ori" : {{
                    "v" : {{
                        "x" : {},
                        "y" : {},
                        "z" : {}
                    }},
                    "w" : {}
                }},
                "tr" : {{
                    "x" : {},
                    "y" : {},
                    "z" : {}
                }},
                "sc" : {{
                    "x" : {},
                    "y" : {},
                    "z" : {}
                }}
            }}""".format(ori.x, ori.y, ori.z, qat.w,
                         pos.x, pos.y, pos.z,
                         scl.x, scl.y, scl.z)

        return json
