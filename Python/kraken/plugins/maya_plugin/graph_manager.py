"""Kraken Canvas - Canvas Graph Manager module.

Classes:
GraphManager -- Node management.

"""

from collections import defaultdict

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

        canvasNode = pm.createNode('canvasNode', name=nodeName)
        ctxtId = mel.eval('FabricCanvasGetContextID;')
        bindId = mel.eval('FabricCanvasGetBindingID -node "{}";'.format(canvasNode))
        client = core.createClient({'contextID': ctxtId})

        # client = ks.getCoreClient()
        ks.loadExtension('KrakenForCanvas')

        host = client.DFG.host
        dfgbinding = host.getBindingForID(bindId)
        dfgexec = dfgbinding.getExec()

        self._GraphManager__dfgHost = client.getDFGHost()
        self._GraphManager__dfgBinding = dfgbinding
        self._GraphManager__dfgExec = dfgexec
        self.__nodeName = canvasNode
        self.dfgBinding = dfgbinding

    @property
    def nodeName(self):
        return self.__nodeName

    def __addNodeToGroup(self, node):
        if(not self._GraphManager__dfgCurrentGroup):
            return
        self._GraphManager__dfgGroups[self._GraphManager__dfgCurrentGroup].append(node)
