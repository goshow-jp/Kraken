"""Kraken Canvas - Canvas Graph Manager module.

Classes:
GraphManager -- Node management.

"""

from kraken.core.kraken_system import ks
from kraken.plugins.canvas_plugin.graph_manager import GraphManager
import FabricEngine.Core as core

import maya.mel as mel
import pymel.core as pm
# import maya.cmds as cmds


class MayaGraphManager(GraphManager):

    """Manager object for taking care of all low level Canvas tasks"""

    __nodeName = None

    def __init__(self, nodeName):
        super(MayaGraphManager, self).__init__()

        self.canvasNode = pm.createNode('canvasNode', name=nodeName)
        # mel.eval('setAttr "{}.nodeState" 1;'.format(nodeName))
        ctxtId = mel.eval('FabricCanvasGetContextID;')
        bindId = mel.eval('FabricCanvasGetBindingID -node "{}";'.format(self.canvasNode))
        client = core.createClient({'contextID': ctxtId, 'guarded': True})

        # client = ks.getCoreClient()
        ks.loadExtension('KrakenForCanvas')

        host = client.DFG.host
        dfgbinding = host.getBindingForID(bindId)
        dfgexec = dfgbinding.getExec()

        self._GraphManager__dfgHost = client.getDFGHost()
        self._GraphManager__dfgBinding = dfgbinding
        self._GraphManager__dfgExec = dfgexec
        self.__nodeName = self.canvasNode
        self.__name__ = "MayaGraphManager"
        self.dfgBinding = dfgbinding

    @property
    def nodeName(self):
        return self.__nodeName

    def getCanvasNode(self):
        return self.canvasNode

    def __addNodeToGroup(self, node):
        if(not self._GraphManager__dfgCurrentGroup):
            return
        self._GraphManager__dfgGroups[self._GraphManager__dfgCurrentGroup].append(node)

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
