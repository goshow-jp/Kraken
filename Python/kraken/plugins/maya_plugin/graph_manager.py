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
        # self.__dfgBinding = self.__dfgHost.createBindingToNewGraph()
        # self.__dfgExec = self.__dfgBinding.getExec()
        self._GraphManager__dfgBinding = dfgbinding
        self._GraphManager__dfgExec = dfgexec
        self._GraphManager__dfgArgs = {}
        self._GraphManager__dfgNodes = {}
        self._GraphManager__dfgNodeAndPortMap = {}
        self._GraphManager__dfgConnections = {}
        self._GraphManager__dfgGroups = {}
        self._GraphManager__dfgGroupNames = []
        self._GraphManager__dfgCurrentGroup = None

        self.__nodeName = canvasNode

    @property
    def nodeName(self):
        return self.__nodeName

    def __addNodeToGroup(self, node):
        if(not self._GraphManager__dfgCurrentGroup):
            return
        self._GraphManager__dfgGroups[self._GraphManager__dfgCurrentGroup].append(node)

    def createGraphNode(self, path, title, **metaData):
        lookup = path
        if title is not None:
            lookup = "%s|%s" % (path, title)

        if lookup in self._GraphManager__dfgNodes:
            raise Exception("Node for %s already exists." % lookup)

        node = self._GraphManager__dfgExec.addInstWithNewGraph(str(title))
        self._GraphManager__dfgNodes[lookup] = node
        self.setNodeMetaDataFromDict(lookup, metaData)
        self._GraphManager__addNodeToGroup(node)

        return node

    def createGraphNodeSI(self, kSceneItem, title, **metaData):
        return self.createGraphNode(kSceneItem.getPath(), title, **metaData)
