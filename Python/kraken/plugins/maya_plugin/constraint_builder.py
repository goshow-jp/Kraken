"""Kraken Maya - Maya Builder module.

Classes:
Builder -- Component representation.

"""

import logging

import textwrap

from kraken.log import getLogger

from kraken.plugins.maya_plugin.abstract_object3d import AbstractBone  # , AbstractSkeleton
from kraken.plugins.maya_plugin.canvas_operator_builder import CanvasOperator

import pymel.core as pm


logger = getLogger('kraken')
logger.setLevel(logging.INFO)


class CanvasConstraint(CanvasOperator):

    graphNodeName = ''

    def __init__(self, builder, kConstraint, buildName, rigGraph):
        super(CanvasConstraint, self).__init__(builder, kConstraint, buildName, rigGraph, isKLBased=False)

    def initialize(self, kConstraint):
        self.inputControls = []
        self.outputControls = []
        self.cnsClass = kConstraint.__class__.__name__
        if self.cnsClass not in [
            'OrientationConstraint',
            'PoseConstraint',
            'PositionConstraint',
            'ScaleConstraint'
        ]:
            print("buildNodesFromConstraint: Unexpected class " + self.cnsClass)
            return False

        self.abstractOnly = False
        self.src = []
        self.dst = []
        self.kOpe = kConstraint

    def build(self, kConstraint, buildName):
        self.rigGraph.setCurrentGroup("Solvers")
        self.containerNodeName = self.rigGraph.createGraphNodeSI(kConstraint, buildName)
        self.rigGraph.setCurrentGroup(None)
        self.containerExec = self.rigGraph.getSubExec(self.containerNodeName)

        self.nameTemplate = self.config.getNameTemplate()
        # typeTokens = self.nameTemplate['types']
        # opTypeToken = typeTokens.get(type(kConstraint).__name__, 'cns')

        ##########################################################################################
        constrainers = kConstraint.getConstrainers()
        constrainee = kConstraint.getConstrainee()

        if len(constrainers) == 1:

            preset = "Kraken.KrakenForCanvas.Constraints.ComputeKraken%s" % self.cnsClass
            tmpPath = "{}".format(self.containerNodeName)
            self.cnsComputeNodeName = self.rigGraph.createNodeFromPreset(
                tmpPath, preset, title='compute', dfgExec=self.containerExec)
            self.solverNodeName = self.cnsComputeNodeName
            self.solverSolveNodeName = self.cnsComputeNodeName

            (nerNode, nerPort, tmp) = self.placeSelectBoneNode(constrainers[0], "{}|{}".format(self.containerNodeName, "constrainer"), skipIfDCCInput=False, ioType="in")
            (neeNode, neePort, tmp) = self.placeSelectBoneNode(constrainee, "{}|{}".format(self.containerNodeName, "constrainee"), skipIfDCCInput=True, ioType="out")

            self.conn(nerNode, nerPort, self.cnsComputeNodeName, 'constrainer')
            self.conn(neeNode, neePort, self.cnsComputeNodeName, 'constrainee')

            if kConstraint.getMaintainOffset():
                # offset = self.calculateOffset(constrainers[0], constrainee, nerNode, nerPort, neeNode, neePort)
                offset = kConstraint.computeOffset().toMat44().getRTVal()
                self.rigGraph.setPortDefaultValue(self.cnsComputeNodeName, "offset", offset, dfgExec=self.containerExec)

        else:
            # TODO:
            print "todo later", self.bulidName
            preset = "Kraken.KrakenForCanvas.Constraints.Kraken%s" % self.cnsClass
            constructNode = self.rigGraph.createNodeFromPresetSI(kConstraint, preset, title='constructor')
            lastNode = constructNode
            lastPort = "result"

            for constrainer in constrainers:
                preset = "Kraken.KrakenForCanvas.Constraints.AddConstrainer"
                title = 'addConstrainer_' + constrainer.getPath()
                addNode = self.rigGraph.createNodeFromPresetSI(kConstraint, preset, title=title)

                self.conn(lastNode, lastPort, addNode, 'this')

                (constrainerNode, constrainerPort) = self.rigGraph.getNodeAndPortSI(constrainer, asInput=False)
                self.conn(constrainerNode, constrainerPort, addNode, 'constrainer')

                lastNode = addNode
                lastPort = 'this'

        '''
            preset = "Kraken.KrakenForCanvas.Constraints.Compute"
            computeNode = self.rigGraph.createNodeFromPresetSI(kConstraint, preset, title='compute')
            self.conn(lastNode, lastPort, computeNode, 'this')
            self.conn(constraineeNode, constraineePort, computeNode, 'xfo')

            if kConstraint.getMaintainOffset():
                preset = "Kraken.KrakenForCanvas.KrakenForCanvas.Constraints.ComputeOffset"
                computeOffsetNode = self.rigGraph.createNodeFromPresetSI(kConstraint, preset, title='computeOffset')
                self.conn(lastNode, lastPort, computeOffsetNode, 'this')
                self.conn(constraineeNode, constraineePort, computeOffsetNode, 'constrainee')
                offset = self.rigGraph.computeCurrentPortValue(computeOffsetNode, 'result')
                self.rigGraph.removeNodeSI(kConstraint, title='computeOffset')
                self.rigGraph.setPortDefaultValue(constructNode, "offset", offset)
        '''

        neeBone = self.builder.getDCCSceneItem(constrainee)
        portName, i = self.placeUpdateBoneNode(constrainee, neeBone, "result")
        self.dst.append([portName, neeBone, "{}.{}".format(self.canvasNodeName, portName)])
        # self.setTransformPortSI(constrainee, computeNode, 'result')
        # self._registerSceneItemPair(kConstraint, self.rigGraph)

    def placeSelectBoneNode(self, obj, path, skipIfDCCInput=False, ioType="in"):
        ''' returns node name and port name. '''

        nodeName, portName, realPortName = [None, None, None]
        bone = self.builder.getDCCSceneItem(obj)

        if type(bone) == AbstractBone:
            if self.abstractOnly:
                nodeName, portName, realPortName = self.placeSelectAbstractBoneNode(bone, bone.name, path)
            elif "in" in ioType:
                nodeName, portName, realPortName = self.addInputTransform(bone, str(bone.name), path)
                canvasNode = self.rigGraph.getCanvasNode()
                self.builder.setMat44Attr(canvasNode, realPortName, obj.globalXfo.toMat44())
        else:
            if not skipIfDCCInput:
                nodeName, portName, realPortName = self.addInputTransform(bone, str(bone.name()), path)

        if "in" in ioType:
            self.src.append([bone, realPortName])
        return [nodeName, portName, realPortName]

    def addInputTransform(self, bone, name, path):
        realPortName = self.rigGraph.getExec().addExecPort(name, self.client.DFG.PortTypes.In, "Mat44")
        i = self.containerExec.addExecPort(name, self.client.DFG.PortTypes.In, "Mat44")
        self.rigGraph.connectNodes("", name, self.containerNodeName, i)

        # connectionTargets = self.prepareConnection(bone)
        self.prepareConnection(bone)
        tgt = "{}.{}".format(self.canvasNodeName, name)
        try:
            if type(bone) is not AbstractBone:
                pm.connectAttr(bone.attr('worldMatrix'), tgt)
        except RuntimeError as e:
            print e

        return ["", i, realPortName]

    def placeSelectAbstractBoneNode(self, bone, name, path):
        if isinstance(bone, list):
            if len(bone) == 1:
                array = False
                ids = [bone[0].id]
            else:
                array = True
                ids = [x.id for x in bone]
        else:
            array = False
            ids = [bone.id]

        # SelectKrakenTransform returns result[] = Mat44[]
        preset = "Kraken.KrakenAnimation.SelectKrakenTransform"
        title = "SelectKrakenTransform"
        sel = self.rigGraph.createNodeFromPreset(path, preset, title, dfgExec=self.containerExec)

        rtVal = self.client.RT.types.UInt32.createArray(ids)
        self.containerExec.setPortDefaultValue("{}.indice".format(sel), rtVal, False)

        # Mat44[] into Mat44
        if not array:
            convCode = textwrap.dedent("""
                dfgEntry{{
                  result = input[0];
                  // report( "{}:  " + result.translation() );
                }}
            """.format(self.buildName))

        else:
            convCode = textwrap.dedent("""
                dfgEntry{{
                  result = input[0];
                  // report( "{}:  " + result.translation() );
                }}
            """.format(self.buildName))

        toMat44 = self.rigGraph.createFunctionNode(path, "toMat44", dfgExec=self.containerExec)
        convExec = self.rigGraph.getSubExec("{}.{}".format(self.containerNodeName, toMat44))
        i = convExec.addExecPort("input", self.client.DFG.PortTypes.In, "Mat44[]")
        o = convExec.addExecPort("result", self.client.DFG.PortTypes.Out, "Mat44")
        convExec.setCode(convCode)

        self.rigGraph.connectNodes(sel, "result", toMat44, i, dfgExec=self.containerExec)
        return toMat44, o, ""

    def placeUpdateBoneNode(self, constrainee, bone, path):

        if type(bone) == AbstractBone:
            if self.abstractOnly:
                return self.placeUpdateAbstractBoneNode(constrainee, bone, path)
            else:
                return self.addOutputTransform(constrainee, bone.name, path)

        else:
            return self.addOutputTransform(constrainee, bone.name(), path)

    def placeUpdateAbstractBoneNode(self, nee, bone, path):
        preset = "Kraken.KrakenAnimation.UpdateKrakenTransform"
        update = self.addPreset(path, preset, title=bone.shortName)
        rtVal = self.client.RT.types.UInt32(bone.id)
        self.containerExec.setPortDefaultValue("{}.index".format(update), rtVal, False)

        self.conn(self.cnsComputeNodeName, "result", update, "element")
        # FIXME: achieving overlapping connection on exec, can not use GraphManager.connectNodes()
        self.containerExec.connectTo("{}.exec".format(update), ".exec")

        return ["", -1]

    def addOutputTransform(self, nee, boneName, path):
        i = self.containerExec.addExecPort(str(boneName), self.client.DFG.PortTypes.Out, "Mat44")
        try:
            self.conn(self.cnsComputeNodeName, "result", "", boneName)
        except Exception:
            pass

        # force evaluate before done connect
        # FIXME:
        self.rigGraph.computeCurrentPortValue(self.cnsComputeNodeName, 'result', dfgExec=self.containerExec)

        connTargets = self.prepareConnection(nee)
        portName = self.makeConnectOutput(self.buildName, boneName, "Out", "Mat44", connTargets)

        return [portName, i]

    def calculateOffset(self, nerBone, neeBone, nodeA, portA, nodeB, portB):
        tmpPath = "{}".format(self.containerNodeName)
        removeNodeALater = False
        removeNodeBLater = False

        if not nodeA:
            removeNodeALater = True
            nerMat44 = nerBone.globalXfo.toMat44()
            preset = "Fabric.Exts.Math.Mat44.ComposeMat44"
            nodeA = self.rigGraph.createNodeFromPreset(tmpPath, preset, "tempNerMat", dfgExec=self.containerExec)
            self.containerExec.setPortDefaultValue("{}.row0".format(nodeA), nerMat44.row0.getRTVal(), False)
            self.containerExec.setPortDefaultValue("{}.row1".format(nodeA), nerMat44.row1.getRTVal(), False)
            self.containerExec.setPortDefaultValue("{}.row2".format(nodeA), nerMat44.row2.getRTVal(), False)
            self.containerExec.setPortDefaultValue("{}.row3".format(nodeA), nerMat44.row3.getRTVal(), False)
            portA = "result"

        if not nodeB:
            removeNodeBLater = True
            neeMat44 = neeBone.globalXfo.toMat44()
            preset = "Fabric.Exts.Math.Mat44.ComposeMat44"
            nodeB = self.rigGraph.createNodeFromPreset(tmpPath, preset, "tempNeeMat", dfgExec=self.containerExec)
            self.containerExec.setPortDefaultValue("{}.row0".format(nodeB), neeMat44.row0.getRTVal(), False)
            self.containerExec.setPortDefaultValue("{}.row1".format(nodeB), neeMat44.row1.getRTVal(), False)
            self.containerExec.setPortDefaultValue("{}.row2".format(nodeB), neeMat44.row2.getRTVal(), False)
            self.containerExec.setPortDefaultValue("{}.row3".format(nodeB), neeMat44.row3.getRTVal(), False)
            portB = "result"

        preset = "Kraken.KrakenForCanvas.Constraints.Kraken%s" % self.cnsClass
        constructNode = self.rigGraph.createNodeFromPreset(tmpPath, preset, title='constructor', dfgExec=self.containerExec)

        # for resolving type
        tempMat = self.rigGraph.createVariableNode(tmpPath, "tempMat", "Mat44", dfgExec=self.containerExec)
        self.conn(tempMat, "value", constructNode, "offset")

        preset = "Kraken.KrakenForCanvas.Constraints.ComputeOffsetSimple"
        computeOffsetNode = self.rigGraph.createNodeFromPreset(
            tmpPath, preset, title='computeOffset', dfgExec=self.containerExec)

        self.conn(constructNode, 'result', computeOffsetNode, 'this')
        self.conn(nodeA, portA, computeOffsetNode, 'constrainer')
        self.conn(nodeB, portB, computeOffsetNode, 'constrainee')
        offset = self.rigGraph.computeCurrentPortValue(computeOffsetNode, 'result', dfgExec=self.containerExec)
        self.rigGraph.removeNode(tmpPath, title='computeOffset', dfgExec=self.containerExec)
        self.rigGraph.removeNode(tmpPath, title='constructor', dfgExec=self.containerExec)
        self.rigGraph.removeNode(tmpPath, title=tempMat, dfgExec=self.containerExec)
        if removeNodeALater:
            self.rigGraph.removeNode(tmpPath, title="tempNerMat", dfgExec=self.containerExec)
        if removeNodeBLater:
            self.rigGraph.removeNode(tmpPath, title="tempNeeMat", dfgExec=self.containerExec)
        self.rigGraph.removeArgument('temp')

        # print self.buildName, "offset: ", offset
        return offset

    def finalize(self):
        self.rigGraph.getExec().connectTo("{}.exec".format(self.containerNodeName), ".exec")
