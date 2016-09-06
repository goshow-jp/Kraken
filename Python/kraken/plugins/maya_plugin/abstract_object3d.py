"""Kraken Maya - Maya Builder module.

Classes:
Builder -- Component representation.

"""

# import json
import logging

from kraken.log import getLogger
from kraken.core.objects.object_3d import Object3D

import pymel.core as pm


logger = getLogger('kraken')
logger.setLevel(logging.INFO)


class AbstractSkeleton(Object3D):

    def __init__(self, kSceneItem, buildName, canvasNode):
        super(AbstractSkeleton, self).__init__(buildName, None)

        self.canvasNode = canvasNode
        self._boneCount = 0

        buildName = '{}Skeleton'.format(buildName)

        pm.FabricCanvasSetExtDeps(mayaNode=canvasNode,
                                  execPath="",
                                  extDep="Characters")

        initializeSkeletonNode = pm.FabricCanvasAddGraph(mayaNode=canvasNode,
                                                         execPath="",
                                                         xPos="0",
                                                         yPos="100",
                                                         title="initializeSkeleton")

        outputPort = pm.FabricCanvasAddPort(mayaNode=canvasNode,
                                            execPath=initializeSkeletonNode,
                                            desiredPortName="skeleton",
                                            portType="Out",
                                            typeSpec="Skeleton",
                                            connectToPortPath="")

        cacheNode = pm.FabricCanvasInstPreset(mayaNode=canvasNode,
                                              execPath="initializeSkeleton",
                                              presetPath="Fabric.Core.Data.Cache",
                                              xPos="100",
                                              yPos="20")

        pm.FabricCanvasConnect(mayaNode=canvasNode,
                               execPath="initializeSkeleton",
                               srcPortPath="{}.value".format(cacheNode),
                               dstPortPath="{}".format(outputPort))

        skeletonNode = pm.FabricCanvasInstPreset(mayaNode=canvasNode,
                                                 execPath="initializeSkeleton",
                                                 presetPath="Fabric.Exts.Characters.Skeleton.Skeleton",
                                                 xPos="-120",
                                                 yPos="100")

        rootBone = pm.FabricCanvasInstPreset(mayaNode=canvasNode,
                                             execPath="initializeSkeleton",
                                             presetPath="Fabric.Exts.Characters.Bone.ComposeBone",
                                             xPos="-60",
                                             yPos="100")

        pm.FabricCanvasSetPortDefaultValue(mayaNode=canvasNode,
                                           execPath="initializeSkeleton",
                                           portPath="{}.name".format(rootBone),
                                           type="String",
                                           value="\"root\"")

        addBone = pm.FabricCanvasInstPreset(mayaNode=canvasNode,
                                            execPath="initializeSkeleton",
                                            presetPath="Fabric.Exts.Characters.Skeleton.AddBone",
                                            xPos="0",
                                            yPos="100")

        pm.FabricCanvasConnect(mayaNode=canvasNode,
                               execPath="initializeSkeleton",
                               srcPortPath="{}.result".format(skeletonNode),
                               dstPortPath="{}.this".format(addBone))

        pm.FabricCanvasConnect(mayaNode=canvasNode,
                               execPath="initializeSkeleton",
                               srcPortPath="{}.result".format(rootBone),
                               dstPortPath="{}.bone".format(addBone))

        pm.FabricCanvasConnect(mayaNode=canvasNode,
                               execPath="initializeSkeleton",
                               srcPortPath="{}.this".format(addBone),
                               dstPortPath="{}.value".format(cacheNode))

        self.setLastBoneNode(addBone)
        self.skeletonDestNode = cacheNode

    def getNode(self):
        return self.canvasNode

    def setLastBoneNode(self, node):
        self.lastBoneNode = node

    def addBone(self, abstractBone):

        # composeBone node
        boneNode = pm.FabricCanvasInstPreset(mayaNode=self.canvasNode,
                                             execPath="initializeSkeleton",
                                             presetPath="Fabric.Exts.Characters.Bone.ComposeBone",
                                             xPos="-60",
                                             yPos="100")

        pm.FabricCanvasSetPortDefaultValue(mayaNode=self.canvasNode,
                                           execPath="initializeSkeleton",
                                           portPath="{}.name".format(boneNode),
                                           type="String",
                                           value="\"{}\"".format(abstractBone.buildName))

        pm.FabricCanvasSetPortDefaultValue(mayaNode=self.canvasNode,
                                           execPath="initializeSkeleton",
                                           portPath="{}.referencePose".format(boneNode),
                                           type="Xfo",
                                           value='{}'.format(abstractBone.getXfoAsJson()))

        pm.FabricCanvasSetPortDefaultValue(mayaNode=self.canvasNode,
                                           execPath="initializeSkeleton",
                                           portPath="{}.radius".format(boneNode),
                                           type="Float32",
                                           value='{}'.format(0.1))

        # addBone node, appending to skeleton
        addBone = pm.FabricCanvasInstPreset(mayaNode=self.canvasNode,
                                            execPath="initializeSkeleton",
                                            presetPath="Fabric.Exts.Characters.Skeleton.AddBone",
                                            xPos="0",
                                            yPos="100")

        pm.FabricCanvasConnect(mayaNode=self.canvasNode,
                               execPath="initializeSkeleton",
                               srcPortPath="{}.this".format(self.lastBoneNode),
                               dstPortPath="{}.this".format(addBone))

        pm.FabricCanvasConnect(mayaNode=self.canvasNode,
                               execPath="initializeSkeleton",
                               srcPortPath="{}.result".format(boneNode),
                               dstPortPath="{}.bone".format(addBone))

        pm.FabricCanvasConnect(mayaNode=self.canvasNode,
                               execPath="initializeSkeleton",
                               srcPortPath="{}.this".format(addBone),
                               dstPortPath="{}.value".format(self.skeletonDestNode))

        abstractBone.setBoneNode(boneNode)
        abstractBone.setAddBoneNode(addBone)
        self.setLastBoneNode(addBone)


class AbstractBone(Object3D):

    def __init__(self, kSceneItem, buildName, skeleton):
        super(AbstractBone, self).__init__(buildName, skeleton)

        self.canvasNode = skeleton.getNode()
        self.buildName = buildName


        self.xfo = kSceneItem.xfo

        skeleton.addBone(self)

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
