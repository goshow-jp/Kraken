"""Kraken Maya - Maya Builder module.

Classes:
Builder -- Component representation.

"""

import logging

from kraken.log import getLogger

from kraken.core.kraken_system import ks
from kraken.core.configs.config import Config

from kraken.core.maths import Vec2, Vec3, Xfo, Mat44
# from kraken.core.maths import Vec2, Vec3, Xfo, Mat44, Math_radToDeg, RotationOrder

# from kraken.core.builder import Builder
from kraken.core.objects.object_3d import Object3D
from kraken.core.objects.attributes.attribute import Attribute

# from kraken.plugins.maya_plugin.graph_manager import MayaGraphManager
from kraken.plugins.maya_plugin.abstract_object3d import AbstractBone  # , AbstractSkeleton

import pymel.core as pm
# import pymel.core.datatypes as dt
# import maya.cmds as cmds


logger = getLogger('kraken')
logger.setLevel(logging.INFO)


class CanvasOperator(object):

    graphNodeName = ''

    def __init__(self, builder, kOperator, buildName, rigGraph, isKLBased=False):
        self.builder = builder
        self.isKLBased = isKLBased
        self.rigGraph = rigGraph
        self.rigGraph.setCurrentGroup(None)
        self.inputControls = []
        self.outputControls = []
        self.buildName = buildName

        self.buildBase(kOperator, buildName, rigGraph)
        if self.isKLBased:
            self.buildKLBasedBase(kOperator, buildName)
        else:
            self.buildPresetBasedBase(kOperator, buildName)

        self.buildPorts(kOperator, buildName)
        self.setOperatorCode(kOperator, buildName)
        self.buildCache(kOperator, buildName)

        try:
            self.selectKrakenTransformNodeName
        except AttributeError:
            self.rigGraph.getExec().connectTo("{}.exec".format(self.containerNodeName), ".exec")

        try:
            # self.ifCachedUpdate
            self.rigGraph.getExec().connectTo("{}.exec2".format(self.containerNodeName), ".exec")
        except AttributeError:
            pass

    def buildBase(self, kOperator, buildName, rigGraph):
        self.client = ks.getCoreClient()
        # Create Canvas Operator
        # canvasNode = pm.createNode('canvasNode', name=buildName)
        # self._registerSceneItemPair(kOperator, pm.PyNode(canvasNode))
        self.canvasNode = self.rigGraph.nodeName
        self.rigGraph.setCurrentGroup("Solvers")
        self.containerNodeName = self.rigGraph.createGraphNodeSI(kOperator, buildName)
        self.rigGraph.setCurrentGroup(None)
        self.containerExec = self.rigGraph.getSubExec(self.containerNodeName)

        self.config = Config.getInstance()
        self.nameTemplate = self.config.getNameTemplate()
        typeTokens = self.nameTemplate['types']
        opTypeToken = typeTokens.get(type(kOperator).__name__, 'op')

        self.solverNodeName = '_'.join([kOperator.getName(), opTypeToken])
        self.solverSolveNodeName = '_'.join([kOperator.getName(), 'solve', opTypeToken])

        self.rigGraph.addExtDep('Kraken', dfgExec=self.containerExec)
        self.rigGraph.addExtDep(kOperator.getExtension(), dfgExec=self.containerExec)

    def buildKLBasedBase(self, kOperator, buildName):

        solverTypeName = kOperator.getSolverTypeName()

        # Create Solver Function Node
        dfgEntry = "dfgEntry {\n  solver = " + solverTypeName + "();\n}"
        solverNodeCode = "{}\n\n{}".format('require ' + kOperator.getExtension() + ';', dfgEntry)

        tmpPath = "{}|{}|{}".format(kOperator.getPath(), buildName, self.solverNodeName)
        self.rigGraph.createFunctionNode(tmpPath, self.solverNodeName, dfgExec=self.containerExec)
        solverExec = self.rigGraph.getSubExec("{}.{}".format(self.containerNodeName, self.solverNodeName))
        solverExec.setCode(solverNodeCode)
        solverExec.addExecPort("solver", self.client.DFG.PortTypes.Out, solverTypeName)

        # Create Solver Variable node and connect it.
        tmpPath = "{}|{}|{}|{}".format(kOperator.getPath(), buildName, self.solverNodeName, "solverVar")

        tmpTitle = "solverVar"
        solverVarName = self.rigGraph.createVariableNode(
            tmpPath, tmpTitle, solverTypeName, extension=kOperator.getExtension(), dfgExec=self.containerExec)

        self.rigGraph.connectNodes(
            self.solverNodeName, "solver", solverVarName, "value", dfgExec=self.containerExec)

        # Crate Solver "Solve" Function Node
        tmpPath = "{}|{}|{}".format(kOperator.getPath(), buildName, self.solverSolveNodeName)
        self.rigGraph.createFunctionNode(tmpPath, self.solverSolveNodeName, dfgExec=self.containerExec)
        solverSolveExec = self.rigGraph.getSubExec("{}.{}".format(self.containerNodeName, self.solverSolveNodeName))
        solverSolveExec.setCode("dfgEntry {}")
        solverSolveExec.addExecPort("solver", self.client.DFG.PortTypes.IO, solverTypeName)

        self.rigGraph.connectNodes(
            solverVarName, "value", self.solverSolveNodeName, "solver", dfgExec=self.containerExec)
        self.rigGraph.connectNodes(
            self.solverSolveNodeName, "solver", "", "exec", dfgExec=self.containerExec)

    def buildPresetBasedBase(self, kOperator, buildName):

        tmpPath = "{}|{}".format(self.containerNodeName, kOperator.getPresetPath())
        self.graphNodeName = self.rigGraph.createNodeFromPreset(
            tmpPath, kOperator.getPresetPath(), self.solverNodeName, dfgExec=self.containerExec)

    def getPortCount(self, kOperator):
        if self.isKLBased is True:
            portCount = len(kOperator.getSolverArgs())

        else:
            host = ks.getCoreClient().DFG.host
            self.opBinding = host.createBindingToPreset(kOperator.getPresetPath())
            self.node = self.opBinding.getExec()

            self.portTypeMap = {
                0: 'In',
                1: 'IO',
                2: 'Out'
            }
            portCount = self.node.getExecPortCount()

        return portCount

    def validatePortValue(self, kOperator, rtVal, portName, portDataType):
        """Validate port value type when passing built in Python types.

        Args:
            rtVal (RTVal): rtValue object.
            portName (str): Name of the argument being validated.
            portDataType (str): Type of the argument being validated.

        """

        # Validate types when passing a built in Python type
        if type(rtVal) in (bool, str, int, float):
            if portDataType in ('Scalar', 'Float32', 'UInt32'):
                if type(rtVal) not in (float, int):
                    raise TypeError(kOperator.getName() + ".evaluate(): Invalid Argument Value: " + str(rtVal) + " (" + type(rtVal).__name__ + "), for Argument: " + portName + " (" + portDataType + ")")

            elif portDataType == 'Boolean':
                if type(rtVal) != bool and not (type(rtVal) == int and (rtVal == 0 or rtVal == 1)):
                    raise TypeError(kOperator.getName() + ".evaluate(): Invalid Argument Value: " + str(rtVal) + " (" + type(rtVal).__name__ + "), for Argument: " + portName + " (" + portDataType + ")")

            elif portDataType == 'String':
                if type(rtVal) != str:
                    raise TypeError(kOperator.getName() + ".evaluate(): Invalid Argument Value: " + str(rtVal) + " (" + type(rtVal).__name__ + "), for Argument: " + portName + " (" + portDataType + ")")

    def buildCache(self, kOperator, buildName):
        if self.inputControls:
            self.buildInputCache(kOperator, buildName)
        if self.outputControls:
            self.buildOutputCache(kOperator, buildName)
        if self.inputControls and self.outputControls:
            self.connectCache(kOperator, buildName)

    def buildInputCache(self, kOperator, buildName):
        cache_preset_path = "Kraken.KrakenForCanvas.KrakenInputCache"
        tmpPath = "{}|{}".format(self.containerNodeName, "KrakenInputCache")
        inputArrayNodeNameIn = "ComposeKrakenInputArray"
        inputArrayNodeNameOut = "DecomposeKrakenInputArray"
        self.inputCacheNodeName = self.rigGraph.createNodeFromPreset(
            tmpPath, cache_preset_path, self.solverNodeName, dfgExec=self.containerExec)

        # detect if array builder is needed
        for i, input in enumerate(self.inputControls):
            if isinstance(input[1], list) and len(self.inputControls) == 1:
                needArrayBuilder = False
                self.rigGraph.connectNodes("", input[0], self.inputCacheNodeName, "input", dfgExec=self.containerExec)
                self.rigGraph.connectNodes(self.inputCacheNodeName, "result", self.solverSolveNodeName, input[0], dfgExec=self.containerExec)
                break
        else:
            needArrayBuilder = True

        if not needArrayBuilder:
            return

        # build inputs array
        tmpPath = "{}|{}".format(self.containerNodeName, inputArrayNodeNameIn)
        self.rigGraph.createFunctionNode(tmpPath, inputArrayNodeNameIn, dfgExec=self.containerExec)
        composeInputArray = self.rigGraph.getSubExec("{}.{}".format(self.containerNodeName, inputArrayNodeNameIn))
        composeInputArray.addExecPort("result", self.client.DFG.PortTypes.Out, "Mat44[]")

        tmpPath = "{}|{}".format(self.containerNodeName, inputArrayNodeNameOut)
        self.rigGraph.createFunctionNode(tmpPath, inputArrayNodeNameOut, dfgExec=self.containerExec)
        decomposeInputArray = self.rigGraph.getSubExec("{}.{}".format(self.containerNodeName, inputArrayNodeNameOut))
        decomposeInputArray.addExecPort("result", self.client.DFG.PortTypes.In, "Mat44[]")

        compCode = "  result.resize( {} );\n".format(len(self.inputControls))
        decompCode = ""
        for i, input in enumerate(self.inputControls):
            if isinstance(input[1], list):
                for x in input[1]:
                    composeInputArray.addExecPort(x['opObject'].getName(), self.client.DFG.PortTypes.In, "Mat44")
                    decomposeInputArray.addExecPort(x['opObject'].getName(), self.client.DFG.PortTypes.Out, "Mat44")
            else:
                composeInputArray.addExecPort(input[0], self.client.DFG.PortTypes.In, "Mat44")
                decomposeInputArray.addExecPort(input[0], self.client.DFG.PortTypes.Out, "Mat44")

                compCode += "  result[ {} ] = {};\n".format(i, input[0])
                decompCode += "  {} = result[ {} ];\n".format(input[0], i)

                self.rigGraph.connectNodes("", input[0], inputArrayNodeNameIn, input[0], dfgExec=self.containerExec)
                self.rigGraph.connectNodes(inputArrayNodeNameOut, input[0], self.solverSolveNodeName, input[0], dfgExec=self.containerExec)

        compInputArrayCode = "dfgEntry {{\n{}\n}}".format(compCode)
        decompInputArrayCode = "dfgEntry {{\n{}\n}}".format(decompCode)
        composeInputArray.setCode(compInputArrayCode)
        decomposeInputArray.setCode(decompInputArrayCode)

        self.rigGraph.connectNodes(
            inputArrayNodeNameIn, "result", self.inputCacheNodeName, "input", dfgExec=self.containerExec)
        self.rigGraph.connectNodes(
            self.inputCacheNodeName, "result", inputArrayNodeNameOut, "result", dfgExec=self.containerExec)

    def buildOutputCache(self, kOperator, buildName):
        cache_preset_path = "Kraken.KrakenForCanvas.KrakenOutputCache"
        tmpPath = "{}|{}".format(self.containerNodeName, "KrakenOutputCache")
        outputArrayNodeNameIn = "ComposeKrakenOutputArray"
        outputArrayNodeNameOut = "DecomposeKrakenOutputArray"

        self.outputCacheNodeName = self.rigGraph.createNodeFromPreset(
            tmpPath, cache_preset_path, self.solverNodeName, dfgExec=self.containerExec)

        # detect if array builder is needed
        for i, output in enumerate(self.outputControls):
            if isinstance(output[1], list) and len(self.outputControls) == 1:
                needArrayBuilder = False
                self.rigGraph.connectNodes(self.solverSolveNodeName, output[0], self.outputCacheNodeName, "output", dfgExec=self.containerExec)
                self.rigGraph.connectNodes(self.outputCacheNodeName, "result", "", output[0], dfgExec=self.containerExec)
                break
        else:
            needArrayBuilder = True

        if not needArrayBuilder:
            return

        # build output array
        tmpPath = "{}|{}".format(self.containerNodeName, outputArrayNodeNameIn)
        self.rigGraph.createFunctionNode(tmpPath, outputArrayNodeNameIn, dfgExec=self.containerExec)
        composeOutputArray = self.rigGraph.getSubExec("{}.{}".format(self.containerNodeName, outputArrayNodeNameIn))
        composeOutputArray.addExecPort("result", self.client.DFG.PortTypes.Out, "Mat44[]")

        tmpPath = "{}|{}".format(self.containerNodeName, outputArrayNodeNameOut)
        self.rigGraph.createFunctionNode(tmpPath, outputArrayNodeNameOut, dfgExec=self.containerExec)
        decomposeOutputArray = self.rigGraph.getSubExec("{}.{}".format(self.containerNodeName, outputArrayNodeNameOut))
        decomposeOutputArray.addExecPort("result", self.client.DFG.PortTypes.In, "Mat44[]")

        compCode = "  result.resize( {} );\n".format(len(self.outputControls))
        decompCode = ""
        for i, output in enumerate(self.outputControls):
            if isinstance(output[1], list):
                pn = composeOutputArray.addExecPort(output[0], self.client.DFG.PortTypes.In, "Mat44")
                po = decomposeOutputArray.addExecPort(output[0], self.client.DFG.PortTypes.Out, "Mat44")

            else:
                pn = composeOutputArray.addExecPort(output[0], self.client.DFG.PortTypes.In, "Mat44")
                po = decomposeOutputArray.addExecPort(output[0], self.client.DFG.PortTypes.Out, "Mat44")

                compCode += "  result[ {} ] = {};\n".format(i, pn)
                decompCode += "  {} = result[ {} ];\n".format(po, i)

                self.rigGraph.connectNodes(self.solverSolveNodeName, output[0], outputArrayNodeNameIn, pn, dfgExec=self.containerExec)
                self.rigGraph.connectNodes(outputArrayNodeNameOut, po, "", output[0], dfgExec=self.containerExec)

        compOutputArrayCode = "dfgEntry {{\n{}\n}}".format(compCode)
        decompOutputArrayCode = "dfgEntry {{\n{}\n}}".format(decompCode)
        composeOutputArray.setCode(compOutputArrayCode)
        decomposeOutputArray.setCode(decompOutputArrayCode)

        self.rigGraph.connectNodes(
            outputArrayNodeNameIn, "result", self.outputCacheNodeName, "output", dfgExec=self.containerExec)
        self.rigGraph.connectNodes(
            self.outputCacheNodeName, "result", outputArrayNodeNameOut, "result", dfgExec=self.containerExec)

    def connectCache(self, kOperator, buildName):
        self.rigGraph.connectNodes(
            self.inputCacheNodeName, "isCached", self.outputCacheNodeName, "isCached", dfgExec=self.containerExec)

        self.rigGraph.connectNodes(
            self.inputCacheNodeName, "exec", self.outputCacheNodeName, "exec", dfgExec=self.containerExec)

        # FIXME: achieving overlapping connection on exec, can not use GraphManager.connectNodes()
        self.containerExec.connectTo("{}.exec".format(self.outputCacheNodeName), ".exec")

        try:
            # FIXME: cause crash while build
            self.rigGraph.connectNodes(
                self.selectKrakenTransformNodeName, "result", self.inputCacheNodeName, "input", dfgExec=self.containerExec)
            pass
        except AttributeError:
            pass

        try:
            self.rigGraph.connectNodes(
                self.outputCacheNodeName, "isCached", self.ifCachedUpdate, "cond", dfgExec=self.containerExec)
        except AttributeError:
            pass

        try:
            self.rigGraph.connectNodes(
                self.mergeUpdateExec, "result", self.outputCacheNodeName, "if_false", dfgExec=self.containerExec)
        except AttributeError:
            pass

    def buildPorts(self, kOperator, buildName):
        self.outExec2ndPort = pm.FabricCanvasAddPort(mayaNode=self.canvasNode,
                                                     execPath=self.containerNodeName,
                                                     desiredPortName="exec2",
                                                     portType="Out",
                                                     typeSpec="Execute",
                                                     connectToPortPath="")

        for i in xrange(self.getPortCount(kOperator)):
            self._forEachPort(kOperator, buildName, i)

    def _forEachPort(self, kOperator, buildName, index):

        portName, portConnectionType, portDataType = self.getPortInformation(kOperator, index)

        # add port
        self.addPort(portConnectionType, kOperator, portName, portDataType)

        # portType dependent process
        if portDataType == 'EvalContext':
            return
        elif portDataType == 'Execute':
            return
        elif portDataType == 'DrawingHandle':
            return
        elif portDataType == 'InlineDebugShape':
            return
        elif portDataType == 'Execute' and portName == 'exec':
            return

        # special port
        if portName == 'time':
            pm.expression(o=self.canvasNode + '.time', s=self.canvasNode + '.time = time;')
            return
        if portName == 'frame':
            pm.expression(o=self.canvasNode + '.frame', s=self.canvasNode + '.frame = frame;')
            return

        # Get the port's input from the DCC
        connectionTargets = self.getConnectionTargets(kOperator, portName, portConnectionType, portDataType)
        # Add the Canvas Port for each port.
        if portConnectionType == 'In':
            self.makeConnectInput(kOperator, buildName, portName, portConnectionType, portDataType, connectionTargets)

        elif portConnectionType in ['IO', 'Out']:
            self.makeConnectOutput(buildName, portName, portConnectionType, portDataType, connectionTargets)

    def setOperatorCode(self, kOperator, buildName):
        if self.isKLBased is True:
            opSourceCode = kOperator.generateSourceCode()
            pm.FabricCanvasSetCode(mayaNode=self.canvasNode,
                                   execPath="{}.{}".format(self.containerNodeName, self.solverSolveNodeName),
                                   code=opSourceCode)

    def getPortInformation(self, kOperator, portIndex):
        if self.isKLBased is True:
            args = kOperator.getSolverArgs()
            arg = args[portIndex]
            portName = arg.name.getSimpleType()
            portConnectionType = arg.connectionType.getSimpleType()
            portDataType = arg.dataType.getSimpleType()

        else:
            portName = self.node.getExecPortName(portIndex)
            portConnectionType = self.portTypeMap[self.node.getExecPortType(portIndex)]
            rtVal = self.opBinding.getArgValue(portName)
            portDataType = rtVal.getTypeName().getSimpleType()

        return portName, portConnectionType, portDataType

    def addPort(self, portConnectionType, kOperator, portName, portDataType):
        if portConnectionType == 'In':
            self.addPortForTypeIn(kOperator, portName, portDataType)

        elif portConnectionType in ['IO', 'Out']:
            self.addPortForTypeOut(kOperator, portName, portDataType)

        else:
            raise Exception("Invalid connection type:" + portConnectionType)

    def getConnectionTargets(self, kOperator, portName, portConnectionType, portDataType):
        if portConnectionType == 'In':
            connectedObjects = kOperator.getInput(portName)
        elif portConnectionType in ['IO', 'Out']:
            connectedObjects = kOperator.getOutput(portName)

        if portDataType.endswith('[]'):
            connectionTargets = self.prepareConnectionArrayPort(connectedObjects)

        else:
            if connectedObjects is None:
                if self.isKLBased:
                    opType = kOperator.getExtension() + ":" + kOperator.getSolverTypeName()
                else:
                    opType = kOperator.getPresetPath()

                logger.warning("Operator '" + self.solverSolveNodeName +
                               "' of type '" + opType +
                               "' port '" + portName + "' not connected.")

            connectionTargets = self.prepareConnection(connectedObjects)

        return connectionTargets

    def addPortForTypeIn(self, kOperator, portName, portDataType):
        if self.isKLBased is True:
            pm.FabricCanvasAddPort(mayaNode=self.canvasNode,
                                   execPath=self.containerNodeName,
                                   desiredPortName=portName,
                                   portType="In",
                                   typeSpec=portDataType,
                                   connectToPortPath="")

            pm.FabricCanvasAddPort(mayaNode=self.canvasNode,
                                   execPath="{}.{}".format(self.containerNodeName, self.solverSolveNodeName),
                                   desiredPortName=portName,
                                   portType="In",
                                   typeSpec=portDataType,
                                   connectToPortPath="")

            pm.FabricCanvasConnect(mayaNode=self.canvasNode,
                                   execPath=self.containerNodeName,
                                   srcPortPath=portName,
                                   dstPortPath=self.solverSolveNodeName + "." + portName)

        else:
            if portDataType != 'Execute':
                pm.FabricCanvasAddPort(
                    mayaNode=self.canvasNode,
                    execPath=self.containerNodeName,
                    desiredPortName=portName,
                    portType="In",
                    typeSpec=portDataType,
                    connectToPortPath="")

            pm.FabricCanvasConnect(
                mayaNode=self.canvasNode,
                execPath=self.containerNodeName,
                srcPortPath=portName,
                dstPortPath=self.graphNodeName + "." + portName)

    def addPortForTypeOut(self, kOperator, portName, portDataType):

            if portDataType in ('Execute', 'InlineInstance', 'DrawingHandle'):
                # Don't expose invalid Maya data type InlineInstance, instead connect to exec port
                dstPortPath = "exec"
            else:
                dstPortPath = portName

            if self.isKLBased is True:
                srcPortNode = self.solverSolveNodeName
                pm.FabricCanvasAddPort(
                    mayaNode=self.canvasNode,
                    execPath="{}.{}".format(self.containerNodeName, self.solverSolveNodeName),
                    desiredPortName=portName,
                    portType="Out",
                    typeSpec=portDataType,
                    connectToPortPath="")
            else:
                srcPortNode = self.graphNodeName

            if portDataType not in ('Execute', 'InlineInstance', 'DrawingHandle'):
                pm.FabricCanvasAddPort(
                    mayaNode=self.canvasNode,
                    execPath=self.containerNodeName,
                    desiredPortName=portName,
                    portType="Out",
                    typeSpec=portDataType,
                    connectToPortPath="")

            pm.FabricCanvasConnect(
                mayaNode=self.canvasNode,
                execPath=self.containerNodeName,
                srcPortPath=srcPortNode + "." + portName,
                dstPortPath=dstPortPath)

    def prepareConnectionArrayPort(self, connectedObjects):
        # In CanvasMaya, output arrays are not resized by the system
        # prior to calling into Canvas, so we explicily resize the
        # arrays in the generated operator stub code.
        if connectedObjects is None:
            connectedObjects = []

        connectionTargets = []
        for index in xrange(len(connectedObjects)):
            opObject = connectedObjects[index]
            dccSceneItem = self.builder.getDCCSceneItem(opObject)

            if hasattr(opObject, "getName"):
                # Handle output connections to visibility attributes.
                if opObject.getName() == 'visibility' and opObject.getParent().getName() == 'implicitAttrGrp':
                    dccItem = self.builder.getDCCSceneItem(opObject.getParent().getParent())
                    dccSceneItem = dccItem.attr('visibility')
                elif opObject.getName() == 'shapeVisibility' and opObject.getParent().getName() == 'implicitAttrGrp':
                    dccItem = self.builder.getDCCSceneItem(opObject.getParent().getParent())
                    shape = dccItem.getShape()
                    dccSceneItem = shape.attr('visibility')

            connectionTargets.append(
                {
                    'opObject': opObject,
                    'dccSceneItem': dccSceneItem
                })

        return connectionTargets

    def prepareConnection(self, connectedObjects):
        opObject = connectedObjects
        dccSceneItem = self.builder.getDCCSceneItem(opObject)
        if hasattr(opObject, "getName"):
            # Handle output connections to visibility attributes.
            if opObject.getName() == 'visibility' and opObject.getParent().getName() == 'implicitAttrGrp':
                dccItem = self.builder.getDCCSceneItem(opObject.getParent().getParent())
                dccSceneItem = dccItem.attr('visibility')
            elif opObject.getName() == 'shapeVisibility' and opObject.getParent().getName() == 'implicitAttrGrp':
                dccItem = self.builder.getDCCSceneItem(opObject.getParent().getParent())
                shape = dccItem.getShape()
                dccSceneItem = shape.attr('visibility')

        connectionTargets = {
            'opObject': opObject,
            'dccSceneItem': dccSceneItem
        }

        return connectionTargets

    def makeConnectInput(self, kOperator, buildName, portName, portConnectionType, portDataType, connectionTargets):

        if portDataType.endswith('[]'):
            for index in xrange(len(connectionTargets)):
                self._connectInput(
                    kOperator,
                    buildName,
                    portName,
                    portConnectionType,
                    portDataType,
                    self.canvasNode + "." + portName + '[' + str(index) + ']',
                    connectionTargets[index]['opObject'],
                    connectionTargets[index]['dccSceneItem'],
                    index)
        else:
            self._connectInput(
                kOperator,
                buildName,
                portName,
                portConnectionType,
                portDataType,
                self.canvasNode + "." + portName,
                connectionTargets['opObject'],
                connectionTargets['dccSceneItem'])

        if "Mat44" in portDataType:
            self.inputControls.append([portName, connectionTargets])

    def _connectInput(self, kOperator, buildName, portName, portConnectionType, portDataType, tgt, opObject, dccSceneItem, index=-1):

        desiredPortName = "{}_{}".format(buildName, portName)
        realPortName = pm.FabricCanvasAddPort(mayaNode=self.canvasNode,
                                              execPath="",
                                              desiredPortName=desiredPortName,
                                              portType=portConnectionType,
                                              typeSpec=portDataType,
                                              connectToPortPath="")

        # array nodes, skip
        if realPortName != desiredPortName:
            pm.FabricCanvasRemovePort(mayaNode=self.canvasNode,
                                      execPath="",
                                      portName=realPortName)
            realPortName = desiredPortName

        else:
            pm.FabricCanvasConnect(mayaNode=self.canvasNode,
                                   execPath="",
                                   srcPortPath=realPortName,
                                   dstPortPath="{}.{}".format(self.containerNodeName, portName))

        tgt = "{}.{}".format(self.canvasNode, "{}_{}".format(buildName, tgt.split(".")[-1]))

        if type(dccSceneItem) == AbstractBone:
            self.selectKrakenTransformSkeleton(index, portName, dccSceneItem)
            return

        if isinstance(opObject, Attribute):
            pm.connectAttr(dccSceneItem, tgt)
        elif isinstance(opObject, Object3D):
            pm.connectAttr(dccSceneItem.attr('worldMatrix'), tgt)
        elif isinstance(opObject, Xfo):
            self.setMat44Attr(tgt.partition(".")[0], tgt.partition(".")[2], opObject.toMat44())
        elif isinstance(opObject, Mat44):
            self.setMat44Attr(tgt.partition(".")[0], tgt.partition(".")[2], opObject)
        elif isinstance(opObject, Vec2):
            pm.setAttr(tgt, opObject.x, opObject.y, type="double2")
        elif isinstance(opObject, Vec3):
            pm.setAttr(tgt, opObject.x, opObject.y, opObject.z, type="double3")
        else:
            self.validatePortValue(kOperator, opObject, portName, portDataType)

            pm.setAttr(tgt, opObject)

    def makeConnectOutput(self, buildName, portName, portConnectionType, portDataType, connectionTargets):

        if portDataType.endswith('[]'):
            for index in xrange(len(connectionTargets)):
                self._connectOutput(
                    buildName,
                    portName,
                    portConnectionType,
                    portDataType,
                    str(self.canvasNode + "." + portName) + '[' + str(index) + ']',
                    connectionTargets[index]['opObject'],
                    connectionTargets[index]['dccSceneItem'],
                    index)
        else:
            if connectionTargets['opObject'] is not None:
                self._connectOutput(
                    buildName,
                    portName,
                    portConnectionType,
                    portDataType,
                    str(self.canvasNode + "." + portName),
                    connectionTargets['opObject'],
                    connectionTargets['dccSceneItem'],
                    -1)

        if "Mat44" in portDataType:
            self.outputControls.append([portName, connectionTargets])

    def _connectOutput(self, buildName, portName, portConnectionType, portDataType, src, opObject, dccSceneItem, index=-1):

        desiredPortName = "{}_{}".format(buildName, portName)
        realPortName = pm.FabricCanvasAddPort(mayaNode=self.canvasNode,
                                              execPath="",
                                              desiredPortName=desiredPortName,
                                              portType=portConnectionType,
                                              typeSpec=portDataType,
                                              connectToPortPath="")

        # array nodes, skip
        if realPortName != desiredPortName:
            pm.FabricCanvasRemovePort(mayaNode=self.canvasNode,
                                      execPath="",
                                      portName=realPortName)
            realPortName = desiredPortName

        else:
            pm.FabricCanvasConnect(mayaNode=self.canvasNode,
                                   execPath="",
                                   srcPortPath="{}.{}".format(self.containerNodeName, portName),
                                   dstPortPath=realPortName)

        src = "{}.{}".format(self.canvasNode, "{}_{}".format(buildName, src.split(".")[-1]))

        if type(dccSceneItem) == AbstractBone:
            self.updateKrakenTransformSkeleton(index, portName, dccSceneItem)
            return

        if isinstance(opObject, Attribute):
            pm.connectAttr(src, dccSceneItem)
        elif isinstance(opObject, Object3D):
            decomposeNode = pm.createNode('decomposeMatrix')
            pm.connectAttr(src,
                           decomposeNode.attr("inputMatrix"),
                           force=True)

            decomposeNode.attr("outputRotate").connect(dccSceneItem.attr("rotate"))
            decomposeNode.attr("outputScale").connect(dccSceneItem.attr("scale"))
            decomposeNode.attr("outputTranslate").connect(dccSceneItem.attr("translate"))

        elif isinstance(opObject, Xfo):
            raise NotImplementedError("Kraken Canvas Operator cannot set object [%s] outputs with Xfo outputs types directly!")
        elif isinstance(opObject, Mat44):
            raise NotImplementedError("Kraken Canvas Operator cannot set object [%s] outputs with Mat44 types directly!")
        else:
            raise NotImplementedError("Kraken Canvas Operator cannot set object [%s] outputs with Python built-in types [%s] directly!" % (src, opObject.__class__.__name__))

    def selectKrakenTransformSkeleton(self, index, inputPort, bone):
        select_preset_path = "Kraken.KrakenAnimation.SelectKrakenTransform"
        tmpPath = "{}|{}".format(self.containerNodeName, "SelectKrakenTransform")

        try:
            rtVal = self.containerExec.getPortDefaultValue("{}.indice".format(self.selectKrakenTransformNodeName), "UInt32[]")
            size = len(rtVal)
            rtVal.resize(size + 1)
            rtVal[size] = bone.id
            self.containerExec.setPortDefaultValue("{}.indice".format(self.selectKrakenTransformNodeName), rtVal, False)

        except AttributeError:
            self.selectKrakenTransformNodeName = self.rigGraph.createNodeFromPreset(
                tmpPath, select_preset_path, self.solverNodeName, dfgExec=self.containerExec)
            rtVal = self.client.RT.types.UInt32.createArray([bone.id])
            self.containerExec.setPortDefaultValue("{}.indice".format(self.selectKrakenTransformNodeName), rtVal, False)

    def updateKrakenTransformSkeleton(self, index, inputPort, bone):
        update_preset_path = "Kraken.KrakenAnimation.UpdateKrakenTransform"

        tmpPath = "{}|{}|{}".format(self.containerNodeName, "UpdateKrakenTransform", bone.shortName)
        update = self.rigGraph.createNodeFromPreset(
            tmpPath, update_preset_path, self.solverNodeName, dfgExec=self.containerExec)

        tmpPath = "{}|{}".format(self.containerNodeName, "UpdateKrakenTransform")
        self.ifCachedUpdate = self.rigGraph.getNode(tmpPath, title="If", dfgExec=self.containerExec)
        if not self.ifCachedUpdate:
            self.ifCachedUpdate = self.rigGraph.createNodeFromPreset(
                tmpPath, "Fabric.Core.Control.If", "If", dfgExec=self.containerExec)

            self.containerExec.connectTo("{}.result".format(self.ifCachedUpdate), ".{}".format(self.outExec2ndPort))

            tmpPath = "{}|{}".format(self.containerNodeName, "UpdateKrakenTransform")
            self.mergeUpdateExec = self.rigGraph.createNodeFromPreset(
                tmpPath, "Fabric.Exts.FabricInterfaces.Execute.Merge", "Merge", dfgExec=self.containerExec)
            self.rigGraph.connectNodes(
                self.mergeUpdateExec, "result", self.ifCachedUpdate, "if_false", dfgExec=self.containerExec)

        def _searchGetterIndex(id):
            tmpPath = "{}|{}".format(self.containerNodeName, "UpdateKrakenTransform")
            get = self.rigGraph.getNode(tmpPath, title="get{}".format(str(id)), dfgExec=self.containerExec)
            if get is not None:
                return _searchGetterIndex(id + 1)
            else:
                return id

        if index is not -1:
            tmpPath = "{}|{}".format(self.containerNodeName, "UpdateKrakenTransform")
            index = _searchGetterIndex(index)
            get = self.rigGraph.createNodeFromPreset(
                tmpPath, "Fabric.Core.Array.Get", "get{}".format(str(index)), dfgExec=self.containerExec)

            rtVal = ks.rtVal("UInt32", index)
            self.containerExec.setPortDefaultValue("{}.index".format(get), rtVal, False)

            self.rigGraph.connectNodes(
                self.solverSolveNodeName, inputPort, get, "array", dfgExec=self.containerExec)

            self.rigGraph.connectNodes(
                get, "element", update, "element", dfgExec=self.containerExec)

        else:
            self.rigGraph.connectNodes(
                self.solverSolveNodeName, inputPort, update, "element", dfgExec=self.containerExec)

        rtVal = ks.rtVal("UInt32", bone.id)
        self.containerExec.setPortDefaultValue("{}.index".format(update), rtVal, False)

        # FIXME: achieving overlapping connection on exec, can not use GraphManager.connectNodes()
        self.containerExec.connectTo("{}.exec".format(update), "{}.this".format(self.mergeUpdateExec))
