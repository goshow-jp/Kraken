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

        self.buildBase(kOperator, buildName, rigGraph)
        if self.isKLBased:
            self.buildKLBasedBase(kOperator, buildName)
        else:
            self.buildPresetBasedBase(kOperator, buildName)

        self.buildPorts(kOperator, buildName)
        self.setOperatorCode(kOperator, buildName)

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

    def buildPorts(self, kOperator, buildName):
        for i in xrange(self.getPortCount(kOperator)):
            self.forEachPort(kOperator, buildName, i)

    def forEachPort(self, kOperator, buildName, index):

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
                    connectionTargets[index]['dccSceneItem'])
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

    def _connectInput(self, kOperator, buildName, portName, portConnectionType, portDataType, tgt, opObject, dccSceneItem):

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
            message = ("Operator '" + self.solverSolveNodeName +
                       "' port '" + portName + "' not connected."
                       "' dccSceneItem type '" + str(type(dccSceneItem)) + "' not supported.")
            logger.warning(message)
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
                    connectionTargets[index]['dccSceneItem'])
        else:
            if connectionTargets['opObject'] is not None:
                self._connectOutput(
                    buildName,
                    portName,
                    portConnectionType,
                    portDataType,
                    str(self.canvasNode + "." + portName),
                    connectionTargets['opObject'],
                    connectionTargets['dccSceneItem'])

    def _connectOutput(self, buildName, portName, portConnectionType, portDataType, src, opObject, dccSceneItem):

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
            message = ("Operator '" + self.solverSolveNodeName +
                       "' port '" + portName + "' not connected."
                       "' dccSceneItem type '" + str(type(dccSceneItem)) + "' not supported.")
            logger.warning(message)
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

