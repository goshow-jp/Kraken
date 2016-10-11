"""Kraken Canvas - Canvas Graph Manager module.

Classes:
GraphManager -- Node management.

"""

import json
from collections import defaultdict

from kraken.core.kraken_system import ks
# import FabricEngine.Core as core
import FabricEngine.CAPI


class GraphManager(object):
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

    def __init__(self):
        super(GraphManager, self).__init__()

        client = ks.getCoreClient()
        ks.loadExtension('KrakenForCanvas')

        self.__dfgHost = client.getDFGHost()
        self.__dfgBinding = self.__dfgHost.createBindingToNewGraph()
        self.__dfgExec = self.__dfgBinding.getExec()
        self.__dfgArgs = defaultdict(dict)
        self.__dfgNodes = defaultdict(dict)
        self.__dfgNodeAndPortMap = defaultdict(dict)
        self.__dfgConnections = defaultdict(dict)
        self.__dfgGroups = {}
        self.__dfgGroupNames = []
        self.__dfgCurrentGroup = None

    def dfgExecSetter(func):
        def wrapper(*args, **kwargs):

            for a in args:
                if type(a) == FabricEngine.CAPI.DFGExec:
                    f = True
                    break
            else:
                f = False

            if not f and not kwargs.get("dfgExec", None):
                kwargs["dfgExec"] = args[0].__dfgExec

            return func(*args, **kwargs)
        return wrapper

    # ===============
    # Canvas Methods
    # ===============
    @dfgExecSetter
    def setTitle(self, title, dfgExec=None):
        dfgExec.setTitle(title)

    @dfgExecSetter
    def getUniqueTitle(self, path, title, dfgExec=None):
        titleSuffix = 1
        uniqueTitle = title
        lookup = '%s|%s' % (path, uniqueTitle)
        while lookup in self.__dfgNodes[dfgExec]:
            titleSuffix = titleSuffix + 1
            uniqueTitle = '%s_%d' % (title, titleSuffix)
            lookup = '%s|%s' % (path, uniqueTitle)

        return uniqueTitle

    @dfgExecSetter
    def addExtDep(self, extDep, dfgExec=None):
        dfgExec.addExtDep(extDep)

    @dfgExecSetter
    def hasNode(self, path, title=None, dfgExec=None):
        lookup = path
        if title is not None:
            lookup = "%s|%s" % (path, title)

        return lookup in self.__dfgNodes[dfgExec]

    @dfgExecSetter
    def hasNodeSI(self, kSceneItem, title=None, dfgExec=None):
        return self.hasNode(kSceneItem.getPath(), title=title, dfgExec=dfgExec)

    @dfgExecSetter
    def getNode(self, path, title=None, dfgExec=None):
        lookup = path
        if title is not None:
            lookup = "%s|%s" % (path, title)

        return self.__dfgNodes[dfgExec].get(lookup, None)

    @dfgExecSetter
    def getNodesUnderPath(self, path, title=None, dfgExec=None):
        lookup = path
        if title is not None:
            lookup = "%s|%s" % (path, title)

        res = []
        for n in self.__dfgNodes[dfgExec]:
            if n.startswith(lookup):
                res.append(n)
        return res

    @dfgExecSetter
    def getNodeSI(self, kSceneItem, title=None, dfgExec=None):
        return self.getNode(kSceneItem.getPath(), title=title, dfgExec=dfgExec)

    @dfgExecSetter
    def getNodeAndPort(self, path, asInput=True, dfgExec=None):
        if path not in self.__dfgNodeAndPortMap[dfgExec]:
            return None

        nodeAndPort = self.__dfgNodeAndPortMap[dfgExec][path]
        if asInput:
            return nodeAndPort[0]

        return nodeAndPort[1]

    @dfgExecSetter
    def getNodeAndPortSI(self, kSceneItem, asInput=True, dfgExec=None):
        return self.getNodeAndPort(kSceneItem.getPath(), asInput=asInput, dfgExec=dfgExec)

    @dfgExecSetter
    def setNodeAndPort(self, path, node, port, asInput=False, dfgExec=None):
        nodeAndPort = self.__dfgNodeAndPortMap[dfgExec].get(path, [(node, port), (node, port)])

        if asInput:
            nodeAndPort[0] = (node, port)
        else:
            nodeAndPort[1] = (node, port)

        self.__dfgNodeAndPortMap[dfgExec][path] = nodeAndPort

    def setNodeAndPortSI(self, kSceneItem, node, port, asInput=False):
        self.setNodeAndPort(kSceneItem.getPath(), node, port, asInput=asInput)

    def getExec(self):
        return self.__dfgExec

    def getSubExec(self, node):
        return self.__dfgExec.getSubExec(node)

    @dfgExecSetter
    def hasArgument(self, name, dfgExec=None):
        return name in self.__dfgArgs[dfgExec]

    @dfgExecSetter
    def getOrCreateArgument(self, name, dataType=None, defaultValue=None, portType="In", dfgExec=None):
        if name in self.__dfgArgs[dfgExec]:
            return self.__dfgArgs[dfgExec][name]

        client = ks.getCoreClient()
        dfgPortType = client.DFG.PortTypes.In
        if portType.lower() == 'out':
            dfgPortType = client.DFG.PortTypes.Out
        elif portType.lower() == 'io':
            dfgPortType = client.DFG.PortTypes.IO

        self.__dfgArgs[dfgExec][name] = dfgExec.addExecPort(name, dfgPortType)
        if dataType:
            self.__dfgBinding.setArgValue(self.__dfgArgs[dfgExec][name], ks.rtVal(dataType, defaultValue))

        return self.__dfgArgs[dfgExec][name]

    @dfgExecSetter
    def removeArgument(self, name, dfgExec=None):
        if name not in self.__dfgArgs[dfgExec]:
            return False

        dfgExec.removeExecPort(self.__dfgArgs[dfgExec][name])
        del self.__dfgArgs[dfgExec][name]

        return True

    @dfgExecSetter
    def createNodeFromPreset(self, path, preset, title=None, dfgExec=None, **metaData):
        lookup = path
        if title is not None:
            lookup = "%s|%s" % (path, title)

        if lookup in self.__dfgNodes[dfgExec]:
            raise Exception("Node for %s already exists." % lookup)

        node = dfgExec.addInstFromPreset(preset)
        self.__dfgNodes[dfgExec][lookup] = node
        self.setNodeMetaDataFromDict(lookup, metaData, dfgExec=dfgExec)
        self.__addNodeToGroup(node)

        return node

    @dfgExecSetter
    def createNodeFromPresetSI(self, kSceneItem, preset, title=None, dfgExec=None, **metaData):
        node = self.createNodeFromPreset(kSceneItem.getPath(), preset, title=title, dfgExec=dfgExec, **metaData)
        self.setNodeMetaDataSI(kSceneItem, 'uiComment', kSceneItem.getPath(), title=title, dfgExec=dfgExec)

        return node

    @dfgExecSetter
    def createFunctionNode(self, path, title, dfgExec=None, **metaData):
        lookup = path
        if title is not None:
            lookup = "%s|%s" % (path, title)

        if lookup in self.__dfgNodes[dfgExec]:
            raise Exception("Node for %s already exists." % lookup)

        node = dfgExec.addInstWithNewFunc(title)
        self.__dfgNodes[dfgExec][lookup] = node
        self.setNodeMetaDataFromDict(lookup, metaData, dfgExec)
        self.__addNodeToGroup(node)

        return node

    @dfgExecSetter
    def createFunctionNodeSI(self, kSceneItem, title, dfgExec=None, **metaData):
        return self.createFunctionNode(kSceneItem.getPath(), title, dfgExec=dfgExec, **metaData)

    @dfgExecSetter
    def createGraphNode(self, path, title, dfgExec=None, **metaData):
        lookup = path
        if title is not None:
            lookup = "%s|%s" % (path, title)

        if lookup in self.__dfgNodes[dfgExec]:
            raise Exception("Node for %s already exists." % lookup)

        node = dfgExec.addInstWithNewGraph(str(title))
        self.__dfgNodes[dfgExec][lookup] = node
        self.setNodeMetaDataFromDict(lookup, metaData)
        self.__addNodeToGroup(node)

        return node

    @dfgExecSetter
    def createGraphNodeSI(self, kSceneItem, title, dfgExec=None, **metaData):
        return self.createGraphNode(kSceneItem.getPath(), title, dfgExec=dfgExec, **metaData)

    @dfgExecSetter
    def createVariableNode(self, path, title, dataType, extension="", dfgExec=None, **metaData):
        lookup = path
        if title is not None:
            lookup = "%s|%s" % (path, title)

        if lookup in self.__dfgNodes[dfgExec]:
            raise Exception("Node for %s already exists." % lookup)

        node = dfgExec.addVar(title, dataType, extension)
        self.__dfgNodes[dfgExec][lookup] = node
        self.setNodeMetaDataFromDict(lookup, metaData, dfgExec)
        self.__addNodeToGroup(node)

        return node

    @dfgExecSetter
    def createVariableNodeSI(self, kSceneItem, title, dataType, extension="", dfgExec=None, **metaData):
        return self.createVariableNode(kSceneItem.getPath(), title, dataType, extension=extension, dfgExec=dfgExec, **metaData)

    @dfgExecSetter
    def removeNode(self, path, title=None, dfgExec=None):
        lookup = path
        if title is not None:
            lookup = "%s|%s" % (path, title)

        if lookup not in self.__dfgNodes[dfgExec]:
            raise Exception("Node for %s does not exist." % lookup)

        node = self.__dfgNodes[dfgExec][lookup]
        dfgExec.removeNode(node)
        del self.__dfgNodes[dfgExec][lookup]

        # clean up groups
        for group in self.__dfgGroups:
            for i in range(len(self.__dfgGroups[group])):
                if self.__dfgGroups[group][i] == node:
                    del self.__dfgGroups[group][i]
                    break

        # clean up connections
        if node in self.__dfgConnections[dfgExec]:
            del self.__dfgConnections[dfgExec][node]
        for nodeName in self.__dfgConnections[dfgExec]:
            ports = self.__dfgConnections[dfgExec][nodeName]
            for portName in ports:
                connections = ports[portName]
                newConnections = []
                for c in connections:
                    if c[0] == node:
                        continue

                    newConnections += [c]
                self.__dfgConnections[dfgExec][nodeName][portName] = newConnections

        return True

    @dfgExecSetter
    def removeNodeSI(self, kSceneItem, title=None, dfgExec=None):
        return self.removeNode(kSceneItem.getPath(), title=title, dfgExec=dfgExec)

    @dfgExecSetter
    def connectNodes(self, nodeA, portA, nodeB, portB, dfgExec=None):
        self.removeConnection(nodeB, portB, dfgExec)

        typeA = self.getNodePortResolvedType(nodeA, portA, dfgExec)
        typeB = self.getNodePortResolvedType(nodeB, portB, dfgExec)

        if typeA != typeB and typeA is not None and typeB is not None:
            if typeA == 'Xfo' and typeB == 'Mat44':
                preset = "Fabric.Exts.Math.Xfo.ToMat44"
                title = self.getUniqueTitle(nodeA, 'Convert', dfgExec)
                convertNode = self.createNodeFromPreset(nodeA, preset, title=title, dfgExec=dfgExec)
                self.connectNodes(nodeA, portA, convertNode, "this", dfgExec)
                nodeA = convertNode
                portA = "result"
            elif typeA == 'Mat44' and typeB == 'Xfo':
                preset = "Fabric.Exts.Math.Xfo.SetFromMat44"
                title = self.getUniqueTitle(nodeA, 'Convert', dfgExec)
                convertNode = self.createNodeFromPreset(nodeA, preset, title=title, dfgExec=dfgExec)
                self.connectNodes(nodeA, portA, convertNode, "m", dfgExec)
                nodeA = convertNode
                portA = "this"
            elif typeA == 'Execute' or typeB == 'Execute':
                pass
            else:
                raise Exception('Cannot connect - incompatible type specs %s and %s.' % (typeA, typeB))

        dfgExec.connectTo(nodeA + '.' + portA, nodeB + '.' + portB)

        if nodeA not in self.__dfgConnections[dfgExec]:
            self.__dfgConnections[dfgExec][nodeA] = {}

        if portA not in self.__dfgConnections[dfgExec][nodeA]:
            self.__dfgConnections[dfgExec][nodeA][portA] = []

        self.__dfgConnections[dfgExec][nodeA][portA].append((nodeB, portB))

        return True

    @dfgExecSetter
    def connectArg(self, argA, argB, argC, dfgExec=None):

        if argA in self.__dfgArgs[dfgExec]:
            dfgExec.connectTo(argA, argB + '.' + argC)
            return True

        elif argC in self.__dfgArgs[dfgExec]:
            dfgExec.connectTo(argA + '.' + argB, argC)
            return True

        return False

    @dfgExecSetter
    def replaceConnections(self, oldNode, oldPort, newNode, newPort, dfgExec=None):
        prevConnections = []
        prevConnections = self.getConnections(oldNode, oldPort, dfgExec)
        for c in prevConnections:
            if c[0] == newNode:
                continue
            self.removeConnection(c[0], c[1], dfgExec)
            self.connectNodes(newNode, newPort, c[0], c[1], dfgExec)

    @dfgExecSetter
    def removeConnection(self, node, port, dfgExec=None):
        result = False
        for nodeName in self.__dfgConnections[dfgExec]:
            ports = self.__dfgConnections[dfgExec][nodeName]
            for portName in ports:
                connections = ports[portName]
                newConnections = []
                for i in range(len(connections)):
                    if '.'.join(connections[i]) == node + '.' + port:
                        dfgExec.disconnectFrom(nodeName + '.' + portName, node + '.' + port)
                        result = True
                        break
                    else:
                        newConnections += [connections[i]]
                self.__dfgConnections[dfgExec][nodeName][portName] = newConnections
                if result:
                    return result

        return result

    @dfgExecSetter
    def getConnections(self, node, port, targets=True, dfgExec=None):
        result = []
        for nodeName in self.__dfgConnections[dfgExec]:
            ports = self.__dfgConnections[dfgExec][nodeName]
            for portName in ports:
                connections = ports[portName]
                if targets:
                    if node + '.' + port == nodeName + '.' + portName:
                        result += connections
                    else:
                        continue
                else:
                    for c in connections:
                        if '.'.join(c) == node + '.' + port:
                            result += [(nodeName, portName)]

        return result

    @dfgExecSetter
    def getNodeMetaData(self, path, key, defaultValue=None, title=None, dfgExec=None):
        lookup = path
        if title is not None:
            lookup = "%s|%s" % (path, title)

        if lookup not in self.__dfgNodes[dfgExec]:
            return defaultValue
        node = self.__dfgNodes[dfgExec][lookup]

        return dfgExec.getNodeMetadata(node, key)

    @dfgExecSetter
    def getNodeMetaDataSI(self, kSceneItem, key, defaultValue=None, title=None, dfgExec=None):
        return self.getNodeMetaData(kSceneItem.getPath(), key, defaultValue=defaultValue, title=title, dfgExec=dfgExec)

    @dfgExecSetter
    def setNodeMetaData(self, path, key, value, title=None, dfgExec=None):
        lookup = path
        node = path
        if title is not None:
            lookup = "%s|%s" % (path, title)
        if lookup in self.__dfgNodes[dfgExec]:
            node = self.__dfgNodes[dfgExec][lookup]
        dfgExec.setNodeMetadata(node, key, str(value))
        if key == 'uiComment':
            dfgExec.setNodeMetadata(node, 'uiCommentExpanded', 'true')

        return True

    @dfgExecSetter
    def setNodeMetaDataSI(self, kSceneItem, key, value, title=None, dfgExec=None):
        return self.setNodeMetaData(kSceneItem.getPath(), key, value, title=title, dfgExec=dfgExec)

    @dfgExecSetter
    def setNodeMetaDataFromDict(self, node, metaData, dfgExec=None):
        for key, value in metaData:
            self.setNodeMetaData(node, key, value, dfgExec=dfgExec)

    @dfgExecSetter
    def computeCurrentPortValue(self, node, port, dfgExec=None):

        if dfgExec != self.getExec():
            tempPort = self.getOrCreateArgument("temp", portType="Out", dfgExec=dfgExec)
            self.connectArg(node, port, tempPort, dfgExec)

            rootTempPort = self.getOrCreateArgument("temp", portType="Out")
            p = dfgExec.getExecPath()
            self.connectArg(p, "temp", rootTempPort, dfgExec=self.__dfgExec)

        else:
            tempPort = self.getOrCreateArgument("temp", portType="Out")
            self.connectArg(node, port, tempPort, dfgExec)

        errors = json.loads(self.__dfgBinding.getErrors(True))
        if errors and len(errors) > 0:
            raise Exception(str(errors))

        self.__dfgBinding.execute()

        value = self.__dfgBinding.getArgValue(tempPort)

        if dfgExec != self.getExec():
            self.removeArgument(rootTempPort, dfgExec)

        self.removeArgument(tempPort, dfgExec)

        return value

    @dfgExecSetter
    def computeCurrentPortValueSI(self, kSceneItem, dfgExec=None):
        nodeAndPort = self.getNodeAndPortSI(kSceneItem, asInput=True)
        if not nodeAndPort:
            return None
        (node, port) = nodeAndPort

        return self.computeCurrentPortValue(node, port, dfgExec)

    @dfgExecSetter
    def setPortDefaultValue(self, node, port, value, dfgExec=None):
        portPath = "%s.%s" % (node, port)

        subExec = dfgExec.getSubExec(node)
        dataType = subExec.getExecPortTypeSpec(port)

        rtVal = value
        if str(type(rtVal)) != '<type \'PyRTValObject\'>':
            rtVal = ks.rtVal(dataType, value)

        dfgExec.setPortDefaultValue(portPath, rtVal)

        return True

    @dfgExecSetter
    def getNodePortResolvedType(self, node, port, dfgExec=None):
        result = dfgExec.getNodePortResolvedType(node + '.' + port)
        return result

    def getCurrentGroup(self):
        return self.__dfgCurrentGroup

    def getAllGroupNames(self):
        return self.__dfgGroupNames + []

    def getNodesInGroup(self, group):
        return self.__dfgGroups.get(group, []) + []

    def setCurrentGroup(self, group):

        if group is None:
            self.__dfgCurrentGroup = None
            return None

        if group not in self.__dfgGroups:
            self.__dfgGroups[group] = []
            self.__dfgGroupNames.append(group)

        if group != self.__dfgCurrentGroup:
            self.__dfgCurrentGroup = group

        return self.__dfgGroups[self.__dfgCurrentGroup]

    def __addNodeToGroup(self, node):
        if(not self.__dfgCurrentGroup):
            return
        self.__dfgGroups[self.__dfgCurrentGroup].append(node)

    @dfgExecSetter
    def changeGroup(self, path, group, dfgExec=None):
        if group not in self.__dfgGroups:
            self.__dfgGroups[group] = []
            self.__dfgGroupNames.append(group)

        nodes = self.getNodesUnderPath(path, dfgExec=dfgExec)

        def _inner(n):
            for gn, gv in self.__dfgGroups.iteritems():
                for g in gv:
                    if n.startswith(g):
                        gv.remove(g)
                        yield g

        for n in nodes:
            for g in _inner(n):
                self.__dfgGroups[group].append(g)

    @dfgExecSetter
    def getAllNodeNames(self, dfgExec=None):
        return self.__dfgNodes[dfgExec].values()

    @dfgExecSetter
    def getNodeConnections(self, nodeName, dfgExec=None):
        keys = {}
        result = []
        node = self.__dfgConnections[dfgExec].get(nodeName, {})
        for portName in node:
            port = node[portName]
            for (otherNode, otherPort) in port:
                key = '%s - %s' % (nodeName, otherNode)
                if key in keys:
                    continue
                keys[key] = True
                result += [otherNode]

        return result

    @dfgExecSetter
    def getAllNodeConnections(self, dfgExec=None):
        keys = {}
        result = {}
        for nodeName in self.__dfgConnections[dfgExec]:
            node = self.__dfgConnections[dfgExec][nodeName]
            for portName in node:
                port = node[portName]
                for (otherNode, otherPort) in port:
                    key = '%s - %s' % (nodeName, otherNode)
                    if key in keys:
                        continue
                    keys[key] = True
                    if nodeName not in result:
                        result[nodeName] = []
                    result[nodeName] += [otherNode]

        return result

    @dfgExecSetter
    def getNumPorts(self, node, dfgExec=None):
        nodeType = dfgExec.getNodeType(node)
        if nodeType == 3:  # var
            return 1
        elif nodeType == 0:  # inst
            subExec = dfgExec.getSubExec(node)
            return subExec.getExecPortCount()

        return 0

    @dfgExecSetter
    def hasInputConnections(self, node, dfgExec=None):
        for nodeName in self.__dfgConnections[dfgExec]:
            ports = self.__dfgConnections[dfgExec][nodeName]
            for portName in ports:
                connections = ports[portName]
                for c in connections:
                    if c[0] == node:
                        return True

        return False

    @dfgExecSetter
    def hasOutputConnections(self, node, dfgExec=None):
        ports = self.__dfgConnections[dfgExec].get(node, {})
        for port in ports:
            if len(ports) > 0:
                return True

        return False

    @dfgExecSetter
    def getPortIndex(self, node, port, dfgExec=None):
        nodeType = dfgExec.getNodeType(node)
        if nodeType == 3:  # var
            return 0
        elif nodeType == 0:  # inst
            subExec = dfgExec.getSubExec(node)
            for i in range(subExec.getExecPortCount()):
                portName = subExec.getExecPortName(i)
                if portName == port:
                    return i

        return 0

    @dfgExecSetter
    def getMinConnectionPortIndex(self, sourceNode, targetNode, dfgExec=None):
        minIndex = 10000
        node = self.__dfgConnections[dfgExec].get(sourceNode, {})
        for portName in node:
            port = node[portName]
            for (otherNode, otherPort) in port:
                if not otherNode == targetNode:
                    continue
                index = self.getPortIndex(otherNode, otherPort, dfgExec)
                if index < minIndex:
                    minIndex = index

        if minIndex == 10000:
            return 0

        return minIndex

    @dfgExecSetter
    def getAllNodePortIndices(self, dfgExec=None):
        result = {}
        nodes = self.getAllNodeNames()
        for n in nodes:
            result[n] = {}
            nodeType = dfgExec.getNodeType(n)
            if nodeType == 3:  # var
                result[n]['value'] = 0
            elif nodeType == 0:  # inst
                subExec = dfgExec.getSubExec(n)
                for i in range(subExec.getExecPortCount()):
                    port = subExec.getExecPortName(i)
                    result[n][port] = i

        return result

    def getAllInputConnections(self):
        nodes = self.getAllNodeNames()
        connections = {}
        for n in nodes:
            connections[n] = []

    @dfgExecSetter
    def implodeNodesByGroup(self, dfgExec=None):
        for group in self.__dfgGroupNames:
            nodes = self.__dfgGroups[group]

            implodedName = dfgExec.implodeNodes(group, nodes)

            # todo
            # # rename the ports based on their source metadata
            # subExec = self.__dfgTopLevelGraph.getSubExec(implodedName)
            # for i in range(subExec.getExecPortCount()):
            #     if subExec.getExecPortType(i) == client.DFG.PortTypes.In:
            #         continue
            #     arg = subExec.getExecPortName(i)
            #     shouldBreak = False
            #     for j in range(subExec.getNodeCount()):
            #         if shouldBreak:
            #             break
            #         node = subExec.getNodeName(j)
            #         if subExec.getNodeType(node) > 1:
            #             continue
            #         nodeExec = subExec.getSubExec(node)
            #         for k in range(nodeExec.getExecPortCount()):
            #             port = nodeExec.getExecPortName(k)
            #             if subExec.isConnectedTo(node+'.'+port, arg):
            #                 metaData = subExec.getNodeMetadata(node, 'uiComment')
            #                 if not metaData:
            #                     continue
            #                 name = metaData.rpartition('.')[2]
            #                 subExec.renameExecPort(arg, name)
            #                 shouldBreak = True
            #                 break

    @dfgExecSetter
    def removeUnpluggedPort(self, dfgExec=None):
        c = dfgExec.getExecPortCount()

        for i in range(c):
            name = dfgExec.getExecPortName(i)
            hasDst = dfgExec.hasDstPorts(name)
            isInput = dfgExec.getPortType(name) is 2

            if isInput and not hasDst:
                # this may destroy the counter 'c', so restart this process
                dfgExec.removePort(name)
                self.removeUnpluggedPort(dfgExec=dfgExec)
                break

    def saveToFile(self, filePath):
        content = self.__dfgBinding.exportJSON()
        open(filePath, "w").write(content)
        print 'Canvas Builder: Saved file ' + str(filePath)
