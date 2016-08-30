"""Kraken Canvas - Canvas Graph Manager module.

Classes:
GraphManager -- Node management.

"""

from kraken.core.kraken_system import ks
from kraken.plugins.canvas_plugin.graph_manager import GraphManager
import FabricEngine.Core as core

import maya.mel as mel
# import maya.cmds as cmds


class MayaGraphManager(GraphManager):

    """Manager object for taking care of all low level Canvas tasks"""

    __dfgHost = None
    __dfgBinding = None
    __dfgArgs = None
    __dfgExec = None
    __dfgNodes = None
    __dfgNodeAndPortMap = None
    __dfgConnections = None
    __dfgGroups = None
    __dfgGroupNames = None
    __dfgCurrentGroup = None

    def __init__(self, nodeName):
        super(GraphManager, self).__init__()

        ctxtId = mel.eval('FabricCanvasGetContextID;')
        bindId = mel.eval('FabricCanvasGetBindingID -node "{}";'.format(nodeName))
        client = core.createClient({'contextID': ctxtId})

        # client = ks.getCoreClient()
        ks.loadExtension('KrakenForCanvas')

        host = client.DFG.host
        dfgbinding = host.getBindingForID(bindId)
        dfgexec = dfgbinding.getExec()

        self.__dfgHost = client.getDFGHost()
        # self.__dfgBinding = self.__dfgHost.createBindingToNewGraph()
        # self.__dfgExec = self.__dfgBinding.getExec()
        self.__dfgBinding = dfgbinding
        self.__dfgExec = dfgexec
        self.__dfgArgs = {}
        self.__dfgNodes = {}
        self.__dfgNodeAndPortMap = {}
        self.__dfgConnections = {}
        self.__dfgGroups = {}
        self.__dfgGroupNames = []
        self.__dfgCurrentGroup = None
