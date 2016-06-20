import math

from kraken.core.maths import Vec3, Quat, Euler, Math_degToRad
from kraken.core.maths.xfo import Xfo

from kraken.core.objects.components.base_example_component import BaseExampleComponent

from kraken.core.objects.attributes.attribute_group import AttributeGroup
from kraken.core.objects.attributes.scalar_attribute import ScalarAttribute
from kraken.core.objects.attributes.integer_attribute import IntegerAttribute
from kraken.core.objects.attributes.bool_attribute import BoolAttribute
from kraken.core.objects.attributes.string_attribute import StringAttribute

from kraken.core.objects.constraints.pose_constraint import PoseConstraint

from kraken.core.objects.component_group import ComponentGroup
from kraken.core.objects.components.component_output import ComponentOutput
from kraken.core.objects.components.component_input import ComponentInput
from kraken.core.objects.hierarchy_group import HierarchyGroup
from kraken.core.objects.locator import Locator
from kraken.core.objects.joint import Joint
from kraken.core.objects.ctrlSpace import CtrlSpace
from kraken.core.objects.layer import Layer
from kraken.core.objects.control import Control

from kraken.core.objects.operators.kl_operator import KLOperator

from kraken.core.profiler import Profiler
from kraken.helpers.utility_methods import logHierarchy

import kraken_components.gsw.gsw_icon as icon


class GswSpringStrandComponent(BaseExampleComponent):
    """Insect Leg Base"""

    def __init__(self, name='SpringStrandBase', parent=None):

        super(GswSpringStrandComponent, self).__init__(name, parent)

        # ===========
        # Declare IO
        # ===========
        # Declare Inputs Xfos
        self.rootInputTgt       = self.createInput('rootInput',    dataType='Xfo',   parent=self.inputHrcGrp).getTarget()
        #self.rootInputTgt       = self.createInput('rootInputs',    dataType='Xfo[]',   parent=self.inputHrcGrp).getTarget()
        #self.collisionObjects    = self.createInput('collisions',   dataType='Mesh[]',  parent=self.inputHrcGrp).getTarget()

        # Declare Output Xfos
        self.boneOutputs         = self.createOutput('boneOutputs',   dataType='Xfo[]')
        self.endXfoOutputs       = self.createOutput('endXfoOutputs', dataType='Xfo[]')

        # Declare Input Attrs
        self.drawDebugInputAttr  = self.createInput('drawDebug',    dataType='Boolean', value=False, parent=self.cmpInputAttrGrp).getTarget()
        self.rigScaleInputAttr   = self.createInput('rigScale',     dataType='Float',   value=1.0,   parent=self.cmpInputAttrGrp).getTarget()
        self.tipBoneLenInputAttr = self.createInput('tipBoneLen',   dataType='Float',   value=1.0,   parent=self.cmpInputAttrGrp).getTarget()

        # Declare Output Attrs

    def _getCtrlName(self, x, y):
        """ generate strand x - vertex y's name """
        
        return "Col{}Row{}".format(str(x + 1).zfill(2), str(y + 1).zfill(2))

    def _getIKName(self, x):
        """ generate strand x's IK controller name """
        
        return "IKCol{}".format(str(x + 1).zfill(2))

    def _getFKCtrlName(self, x, y):
        """ generate strand x - vertex y's name """

        return "FKCol{}Row{}".format(str(x + 1).zfill(2), str(y + 1).zfill(2))

    def _getFKBoneName(self, x, y):
        """ generate strand x - vertex y's name """

        return "bone-FKCol{}Row{}".format(str(x + 1).zfill(2), str(y + 1).zfill(2))

    def _getChainBaseName(self, x):

        return "ChainBaseCol{}".format(str(x + 1).zfill(2))

    def _getBoneName(self, x, y):
        """ generate strand x - vertex y's name """

        return "BoneCol{}Row{}".format(str(x + 1).zfill(2), str(y + 1).zfill(2))

    def _getEndName(self, x):
        """ generate strand x - vertex y's name """

        return "EndXfoCol{}".format(str(x + 1).zfill(2))


class GswSpringStrandComponentGuide(GswSpringStrandComponent):
    """SpringStrand Component Guide"""

    def __init__(self, name='SpringStrand', parent=None, data=None):

        Profiler.getInstance().push("Construct SpringStrand Guide Component:" + name)
        super(GswSpringStrandComponentGuide, self).__init__(name, parent)

        # =========================================================================================
        # Controls
        # =========================================================================================
        guideSettingsAttrGrp = AttributeGroup("GuideSettings", parent=self)
        self.numStrands      = IntegerAttribute('numStrands', value=3, minValue=1, maxValue=99, parent=guideSettingsAttrGrp)
        self.numJoints       = IntegerAttribute('numJoints',  value=3, minValue=2, maxValue=20, parent=guideSettingsAttrGrp)

        self.numStrands.setValueChangeCallback(self.updateNumStrand)
        self.numJoints.setValueChangeCallback(self.updateNumJoint)

        self.jointCtrls    = []
        self.strandOutputs = []

        if data is None:
            data = self._makeDafaultData()

        self.loadData(data)

        Profiler.getInstance().pop()

    # =============================================================================================
    # Data Methods
    # =============================================================================================
    def saveData(self):
        """Save the data for the component to be persisted.

        Return:
        The JSON data object

        """

        data = super(GswSpringStrandComponentGuide, self).saveData()

        jointPositions = []
        for i in xrange(len(self.jointCtrls)):
            jointPositions.append(self.jointCtrls[i].xfo.tr)

        data['jointPositions'] = jointPositions

        return data

    def loadData(self, data):
        """Load a saved guide representation from persisted data.

        Arguments:
        data -- object, The JSON data object.

        Return:
        True if successful.

        """

        super(GswSpringStrandComponentGuide, self).loadData(data)

        for i in xrange(len(data['jointPositions'])):
            self.jointCtrls[i].xfo.tr = data['jointPositions'][i]

        return True

    def getRigBuildData(self):
        """Returns the Guide data used by the Rig Component to define the layout of the final rig..

        Return:
        The JSON rig data object.

        """

        data = super(GswSpringStrandComponentGuide, self).getRigBuildData()
        numJoints   = self.numJoints.getValue()
        numStrands  = self.numStrands.getValue()
        data['strands'] = []

        def _each(i):
            boneXfos    = []
            boneLengths = []

            # Calculate forward vector
            rootId  = i * (numJoints + 1 )
            nextId  = rootId + 1
            tipId   = rootId + (numJoints + 1) - 1
            sub = lambda x, y: self.jointCtrls[x].xfo.tr.subtract(self.jointCtrls[y].xfo.tr).unit()

            toFirst = sub(rootId, nextId)
            toTip   = sub(rootId, tipId)
            forward = toTip.cross(toFirst).unit()

            # Calculate Xfos
            for j in xrange(numJoints):
                nextId = rootId + j + 1
                thisId = rootId + j

                boneVec = self.jointCtrls[nextId].xfo.tr.subtract(self.jointCtrls[thisId].xfo.tr)
                boneLengths.append(boneVec.length())
                bone1Normal = forward.cross(boneVec).unit()
                bone1ZAxis = boneVec.cross(bone1Normal).unit()

                xfo = Xfo()
                xfo.setFromVectors(boneVec.unit(), bone1Normal, bone1ZAxis, self.jointCtrls[thisId].xfo.tr)

                boneXfos.append(xfo)

            _push(i, boneXfos, boneLengths)

        def _push(i, boneXfos, boneLengths):
            strand = {}
            strand['boneXfos']    = boneXfos
            strand['endXfo']      = self.jointCtrls[(i + 1) * (numJoints + 1 ) - 1].xfo
            strand['boneLengths'] = boneLengths

            data['strands'].append(strand)

        for i in xrange(self.numStrands.getValue()):
            _each(i)

        return data

    # =============================================================================================
    # Callbacks
    # =============================================================================================
    def updateNumStrand(self, numStrands):
        """Load a saved guide representation from persisted data.

        Arguments:
        numStrands -- object, The number of strands inthe chain.

        Return:
        True if successful.

        """

        if numStrands == 0:
            raise IndexError("'numStrands' must be > 0")

        name = self._getCtrlName  # shortcut
        numJoints = self.numJoints.getValue()
        old = len(self.jointCtrls) // (numJoints + 1)
        if numStrands > old:
            # append new strand(s)
            for strandId in xrange(old, numStrands):
                for i in xrange(numJoints + 1):
                    # n = name(strandId, i)

                    newCtrl = Control(name(strandId, i), parent=self.ctrlCmpGrp, shape="sphere")
                    self.jointCtrls.append(newCtrl)

                    newOutput = ComponentOutput(name(strandId, i), parent=self.outputHrcGrp)
                    self.strandOutputs.append(newOutput)

        elif numStrands < old:
            numExtra = old - numStrands
            for s in xrange(numExtra):
                for i in xrange(numJoints + 1):
                    extraCtrl = self.jointCtrls.pop()
                    self.ctrlCmpGrp.removeChild(extraCtrl)

                    extraOutput = self.strandOutputs.pop()
                    self.outputHrcGrp.removeChild(extraOutput)

        # Reset the control positions based on new number of joints
        jointPositions = self.generateGuidePositions(numStrands, numJoints)
        for i in xrange(len(self.jointCtrls)):
            self.jointCtrls[i].xfo.tr = jointPositions[i]

        return True

    def updateNumJoint(self, numJoints):
        """Load a saved guide representation from persisted data.

        Arguments:
        numJoints -- object, The number of joints inthe chain.

        Return:
        True if successful.

        """

        if numJoints == 0:
            raise IndexError("'numJoints' must be > 0")

        name = self._getCtrlName  #shortcut
        numStrands = self.numStrands.getValue()
        old  = len(self.jointCtrls) // numStrands
        if numJoints + 1 > old:
            numAppended = 0
            for strandId in range(numStrands):
                for i in xrange(old, numJoints + 1):
                    n = name(strandId, i)
                    id = strandId * numJoints + i + numAppended

                    newCtrl = Control(n, parent=self.ctrlCmpGrp, shape="sphere")
                    self.jointCtrls.insert(id, newCtrl)

                    newOutput = ComponentOutput(n, parent=self.outputHrcGrp)
                    self.strandOutputs.insert(id, newOutput)

                    numAppended += 1

        elif numJoints + 1 < old:
            numExtraCtrls = old - (numJoints + 1)
            markToDelete = []  # prepare for destructive pop oppe
            for strandId in xrange(numStrands):
                for i in xrange(1, numExtraCtrls + 1):
                    markToDelete.append((strandId + 1) * old - i)
            markToDelete.sort()
            markToDelete.reverse()

            for id in markToDelete:
                extraCtrl = self.jointCtrls.pop(id)
                self.ctrlCmpGrp.removeChild(extraCtrl)

                extraOutput = self.strandOutputs.pop(id)
                self.outputHrcGrp.removeChild(extraOutput)

        # Reset the control positions based on new number of joints
        jointPositions = self.generateGuidePositions(numStrands, numJoints)
        for i, ctrl in enumerate(self.jointCtrls):
            ctrl.xfo.tr = jointPositions[i]

        return True

    def generateGuidePositions(self, numStrands, numJoints):
        """Generates the positions for the guide controls based on the number
        of joints.

        Args:
            numStrands (int): Number of strands.
            numJoints  (int): Number of joints on each strand to generate a transform for.

        Returns:
            list: Guide control positions.

        """

        halfPi = math.pi / 2.0
        step   = halfPi  / numJoints
        rotRad = math.pi * 2.0 / numStrands

        def rot(x, z, rad):
            """ rotate in x,z plane """

            return [(x * math.cos(rad) - z * math.sin(rad)),
                    (x * math.sin(rad) + z * math.cos(rad))]


        guidePositions = []
        for i in xrange(numStrands):
            for j in xrange(numJoints + 1):
                x = math.cos((j * step) + halfPi) * -10 + 1
                y = math.sin((j * step) + halfPi) * 10
                z = 0

                x, z = rot(x, z, rotRad * i)
                guidePositions.append(Vec3(x, y, z))

        return guidePositions

    def _getCtrlName(self, x, y):
        """ generate strand x - vertex y's name """
        
        return "col{}row{}".format(str(x + 1).zfill(2), str(y + 1).zfill(2))

    def _makeDafaultData(self):

        self.jointCtrls    = []
        self.strandOutputs = []

        numStrands         = self.numStrands.getValue()
        numJoints          = self.numJoints.getValue()
        jointPositions     = self.generateGuidePositions(numStrands, numJoints)

        gn = lambda x, y: self._getCtrlName(x, y)

        for i in xrange(numStrands):
            for j in xrange(numJoints):
                self.jointCtrls.append(Control(gn(i, j), parent=self.ctrlCmpGrp, shape="sphere"))
                self.strandOutputs.append(ComponentOutput(gn(i, j), parent=self.outputHrcGrp))

        self.boneOutputs.setTarget(self.strandOutputs)

        data = {
           "location":       "M",
           "jointPositions": jointPositions,
           "numJoints":      self.numJoints.getValue()
          }

        return data

    # ==============
    # Class Methods
    # ==============
    @classmethod
    def getComponentType(cls):
        """Enables introspection of the class prior to construction to determine if it is a guide component.

        Return:
        The true if this component is a guide component.

        """

        return 'Guide'

    @classmethod
    def getRigComponentClass(cls):
        """Returns the corresponding rig component class for this guide component class

        Return:
        The rig component class.

        """

        return GswSpringStrandComponentRig


class GswSpringStrandComponentRig(GswSpringStrandComponent):

    """Spring Strand Rig"""

    def __init__(self, name='SpringStrand', parent=None):

        Profiler.getInstance().push("Construct SpringStrand Rig Component:" + name)
        super(GswSpringStrandComponentRig, self).__init__(name, parent)

        # =========
        # Controls
        # =========

        # Chain Base
        self.chainBase = []
        self.chainBase.append(Locator('ChainBaseCol00', parent=self.ctrlCmpGrp))
        self.chainBase[0].setShapeVisibility(False)

        # FK
        self.fkCtrlSpaces = [[]]
        self.fkCtrls      = []

        # IK Control
        self.ikCtrlSpace = []
        self.ikCtrl      = []

        # Add first controller(must exists), others later on loadData()
        self.addFKCtrl(0)
        s, c = self.addIKCtrl(0)
        self.ikCtrlSpace.append(s)
        self.ikCtrl.append(c)

        # Add Component Params to IK control
        tentacleSettingsAttrGrp    = AttributeGroup("DisplayInfo_SpringStrandSetting", parent=self.ctrlCmpGrp)
        tentacledrawDebugInputAttr = BoolAttribute('drawDebug',          value=False, parent=tentacleSettingsAttrGrp)
        fkikInputAttr              = ScalarAttribute('ikblend',          value=0.0,   minValue=0.0,  maxValue=1.0,  parent=tentacleSettingsAttrGrp)
        waveLength_YInputAttr      = ScalarAttribute('waveLength_Y',     value=1.0,   minValue=0.0,  maxValue=5.0,  parent=tentacleSettingsAttrGrp)
        waveAmplitude_YInputAttr   = ScalarAttribute('waveAmplitude_Y',  value=0.0,   minValue=-3.0, maxValue=3.0,  parent=tentacleSettingsAttrGrp)
        waveFrequency_YInputAttr   = ScalarAttribute('waveFrequency_Y',  value=2.0,   minValue=0.0,  maxValue=10.0, parent=tentacleSettingsAttrGrp)
        waveLength_ZInputAttr      = ScalarAttribute('waveLength_Z',     value=2.329, minValue=0.0,  maxValue=5.0,  parent=tentacleSettingsAttrGrp)
        waveAmplitude_ZInputAttr   = ScalarAttribute('waveAmplitude_Z',  value=0.0,   minValue=-3.0, maxValue=3.0,  parent=tentacleSettingsAttrGrp)
        waveFrequency_ZInputAttr   = ScalarAttribute('waveFrequency_Z',  value=3.354, minValue=0.0,  maxValue=10.0, parent=tentacleSettingsAttrGrp)
        tipBiasInputAttr           = ScalarAttribute('tipBias',          value=1.0,   minValue=0.0,  maxValue=1.0,  parent=tentacleSettingsAttrGrp)

        springStrengthInputAttr    = ScalarAttribute('springStrength',   value=0.3,   minValue=0.0,  maxValue=1.0,  parent=tentacleSettingsAttrGrp)
        dampeningInputAttr         = ScalarAttribute('dampening',        value=0.03,  minValue=0.0,  maxValue=1.0,  parent=tentacleSettingsAttrGrp)
        simulationWeightInputAttr  = ScalarAttribute('simulationWeight', value=1.0,   minValue=0.0,  maxValue=1.0,  parent=tentacleSettingsAttrGrp)
        softLimitBoundsInputAttr   = ScalarAttribute('softLimitBounds',  value=5.0,   minValue=0.0,  maxValue=10.0, parent=tentacleSettingsAttrGrp)

        # Connect IO to controls
        self.drawDebugInputAttr.connect(tentacledrawDebugInputAttr)

        # ==========
        # Deformers
        # ==========
        deformersLayer = self.getOrCreateLayer('deformers')
        self.defCmpGrp = ComponentGroup(self.getName(), self, parent=deformersLayer)
        self.deformerJoints   = []
        self.boneOutputsTgt   = []
        self.endXfoOutputsTgt = []

        # =====================
        # Create Component I/O
        # =====================

        # Set IO Targets
        self.boneOutputs.setTarget(self.boneOutputsTgt)
        self.endXfoOutputs.setTarget(self.endXfoOutputsTgt)

        # ==============
        # Constrain I/O
        # ==============
        # Constraint inputs
        self.rootInputTgts = []

        chainBaseInputConstraint = PoseConstraint('_'.join([self.chainBase[0].getName(), 'To', self.rootInputTgt.getName()]))
        chainBaseInputConstraint.setMaintainOffset(True)
        chainBaseInputConstraint.addConstrainer(self.rootInputTgt)
        self.chainBase[0].addConstraint(chainBaseInputConstraint)

        # ========================================================================================
        # Add Splice Ops
        # ========================================================================================

        #######################################################################
        # Add solver Splice Op
        self.strandSolverKLOp = KLOperator('SpringStrandSolverKLOp', 'SpringStrandSolver', 'ParticleSystem')
        self.addOperator(self.strandSolverKLOp)
        setSolverInput  = lambda name, attr: self.strandSolverKLOp.setInput(name, attr)
        setSolverOutput = lambda name, attr: self.strandSolverKLOp.setOutput(name, attr)

        # # Add Att Inputs
        setSolverInput('drawDebug',    self.drawDebugInputAttr)
        setSolverInput('rigScale',     self.rigScaleInputAttr)
        setSolverInput('ikblend',      fkikInputAttr)
        setSolverInput('tipBoneLen',   self.tipBoneLenInputAttr)

        # Add Xfo Inputs
        setSolverInput('ikgoal',       self.ikCtrl)
        setSolverInput('fkcontrols',   self.fkCtrls)

        # Add Xfo Outputs
        setSolverOutput('pose',        self.boneOutputsTgt)
        setSolverOutput('strandEnd',   self.endXfoOutputsTgt)

        ######################################################################
        # Add Deformer Splice Op
        self.outputsToDeformersKLOp = KLOperator('SpringStrandDeformerKLOp', 'MultiPoseConstraintSolver', 'Kraken')
        self.addOperator(self.outputsToDeformersKLOp)
        setDeformerInput  = lambda name, attr: self.outputsToDeformersKLOp.setInput(name, attr)
        setDeformerOutput = lambda name, attr: self.outputsToDeformersKLOp.setOutput(name, attr)

        # Add Att Inputs
        setDeformerInput('drawDebug',     self.drawDebugInputAttr)
        setDeformerInput('rigScale',      self.rigScaleInputAttr)

        # Add Xfo Inputs
        setDeformerInput('constrainers',  self.boneOutputsTgt)

        # Add Xfo Outputs
        setDeformerOutput('constrainees', self.deformerJoints)

        self.strandSolverKLOp.evaluate()

        Profiler.getInstance().pop()

    def addFKCtrl(self, strandId):
        self.setNumControls(strandId, 2)

    def addIKCtrl(self, i):
        ikCtrlSpace = CtrlSpace(self._getIKName(i), parent=self.ctrlCmpGrp)
        ikCtrl      = Control(self._getIKName(i),   parent=ikCtrlSpace, shape="sphere")

        ikCtrl.scalePoints(Vec3(0.25, 0.25, 0.25))
        ikCtrl.lockScale(   x=True, y=True, z=True)
        ikCtrl.lockRotation(x=True, y=True, z=True)

        return ikCtrlSpace, ikCtrl

    def setRootInputs(self, strandId):
        name = self._getBoneName(strandId, 0)
        input = ComponentInput(name, parent=self.rootInputTgt)
        self.rootInputTgts.append(input)

        # FK
        cons = PoseConstraint('_'.join([self.fkCtrlSpaces[strandId][0].getName(), 'To', self.rootInputTgts[strandId].getName()]))
        cons.setMaintainOffset(True)
        cons.addConstrainer(self.rootInputTgts[strandId])
        self.fkCtrlSpaces[strandId][0].addConstraint(cons)

        # IK
        cons = PoseConstraint('_'.join([self.ikCtrlSpace[strandId].getName(), 'To', self.rootInputTgts[strandId].getName()]))
        cons.setMaintainOffset(True)
        cons.addConstrainer(self.rootInputTgts[strandId])
        self.ikCtrlSpace[strandId].addConstraint(cons)

    def setNumControls(self, strandId, numControls):
        """
            strandId: strand(row) number
            numControls: number of controls on a strand
        """

        # Add new control spaces and controls
        if strandId >= len(self.fkCtrlSpaces):
            self.fkCtrlSpaces.append([])

        for i in xrange(len(self.fkCtrlSpaces[strandId]), numControls):
            if i == 0:
                parent = self.ctrlCmpGrp
            else:
                parent = self.fkCtrls[(strandId * numControls) + i - 1]

            boneName = self._getFKBoneName(strandId, i)
            fkCtrlSpace = CtrlSpace(boneName, parent=parent)

            fkCtrl = Control(boneName, parent=fkCtrlSpace)
            fkCtrl.setCurveData(icon.cube_with_peek2)
            fkCtrl.alignOnXAxis()
            fkCtrl.lockScale(x=True, y=True, z=True)
            fkCtrl.lockTranslation(x=True, y=True, z=True)

            # bColor = 0.5 * ((i + 1.0) / numControls)
            # fkCtrl.setColor([1.0, 1.0, bColor])

            self.fkCtrlSpaces[strandId].append(fkCtrlSpace)
            self.fkCtrls.append(fkCtrl)

    def setNumDeformers(self, strandId, numDeformers):

        # Add new deformers and outputs
        for i in xrange(numDeformers):
            name = self._getBoneName(strandId, i)
            tentacleOutput = ComponentOutput(name, parent=self.outputHrcGrp)
            self.boneOutputsTgt.append(tentacleOutput)

            name = self._getBoneName(strandId, i)
            boneDef = Joint(name, parent=self.defCmpGrp)
            boneDef.setComponent(self)
            self.deformerJoints.append(boneDef)

        else:
            name = self._getEndName(strandId)
            tentacleOutput = ComponentOutput(name, parent=self.outputHrcGrp)
            self.endXfoOutputsTgt.append(tentacleOutput)

        return True

    def loadData(self, data=None):
        """Load a saved guide representation from persisted data.

        Arguments:
        data -- object, The JSON data object.

        Return:
        True if successful.

        """

        super(GswSpringStrandComponentRig, self).loadData(data)

        strands = data['strands']
        numJoints = data['numJoints']
        for i, s in enumerate(strands):
            self._loadEachStrand(numJoints, i, s)

        # =============
        # Set IO Attrs
        # =============
        firstBoneLengths = strands[0]['boneLengths']
        tipBoneLen = firstBoneLengths[len(firstBoneLengths) - 1]
        self.tipBoneLenInputAttr.setMax(tipBoneLen * 2.0)
        self.tipBoneLenInputAttr.setValue(tipBoneLen)

        # ====================
        # Evaluate Splice Ops
        # ====================
        # evaluate the nbone op so that all the output transforms are updated.
        self.strandSolverKLOp.evaluate()
        self.outputsToDeformersKLOp.evaluate()

        return True

    def _loadEachStrand(self, numJoints, strandId, strand):
        boneXfos    = strand['boneXfos']
        boneLengths = strand['boneLengths']
        endXfo      = strand['endXfo']

        ##################################################################
        # Add or mod chainbase
        '''
        if strandId >= len(self.chainBase):
            base = Locator(self._getChainBaseName(strandId), parent=self.ctrlCmpGrp)
            self.chainBase.append(base)
        self.chainBase[strandId].xfo = boneXfos[0]
        '''

        # Add extra controls and outputs
        self.setNumControls(strandId, numJoints)
        self.setNumDeformers(strandId, numJoints)

        ##################################################################
        # Scale controls based on bone lengths
        for i, each in enumerate(self.fkCtrlSpaces[strandId]):
            self.fkCtrlSpaces[strandId][i].xfo = boneXfos[i]
            boneScale = Vec3(boneLengths[i] * 0.90, boneLengths[i] * 0.05, boneLengths[i] * 0.35)
            self.fkCtrls[strandId * numJoints + i].xfo = boneXfos[i]
            self.fkCtrls[strandId * numJoints + i].rotatePoints(0, 0, -90)
            self.fkCtrls[strandId * numJoints + i].scalePoints(boneScale)

        ##################################################################
        # Add or mod IK
        if strandId >= len(self.ikCtrlSpace):
            s, c = self.addIKCtrl(strandId)
            # self.ikCtrlSpace[strandId] = s
            # self.ikCtrl[strandId] = c
            self.ikCtrlSpace.append(s)
            self.ikCtrl.append(c)

        self.ikCtrlSpace[strandId].xfo = endXfo
        self.ikCtrl[strandId].xfo = endXfo
        self.setRootInputs(strandId)

        ##################################################################
        # Set IO Xfos
        # FIXME:
        #  self.rootInputTgt[strandId].xfo = boneXfos[0]
        for i in xrange(len(boneLengths)):
            indexAtAll = strandId * numJoints + i  # contains all strand, not one
            self.boneOutputsTgt[indexAtAll].xfo = boneXfos[i]

        self.endXfoOutputsTgt[strandId].xfo = endXfo


from kraken.core.kraken_system import KrakenSystem
ks = KrakenSystem.getInstance()
ks.registerComponent(GswSpringStrandComponentGuide)
ks.registerComponent(GswSpringStrandComponentRig)
