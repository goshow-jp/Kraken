from kraken.core.maths import Vec3, Xfo, Quat

from kraken.core.objects.components.base_example_component import BaseExampleComponent

from kraken.core.objects.attributes.attribute_group import AttributeGroup
from kraken.core.objects.attributes.bool_attribute import BoolAttribute
from kraken.core.objects.attributes.scalar_attribute import ScalarAttribute
from kraken.core.objects.attributes.integer_attribute import IntegerAttribute

from kraken.core.objects.joint import Joint
from kraken.core.objects.transform import Transform
from kraken.core.objects.control import Control
from kraken.core.objects.ctrlSpace import CtrlSpace
from kraken.core.objects.component_group import ComponentGroup
# from kraken.core.objects.components.component_output import ComponentOutput

from kraken.core.objects.operators.kl_operator import KLOperator

from kraken.core.profiler import Profiler

import kraken_components.gsw.gsw_icon as icon


class GswNeckHeadComponent(BaseExampleComponent):

    """Neck Head Component"""

    def __init__(self, name="neckBase", parent=None, *args, **kwargs):
        super(GswNeckHeadComponent, self).__init__(name, parent, *args, **kwargs)

        # ===========
        # Declare IO
        # ===========
        # Declare Inputs Xfos
        self.globalSRTInputTgt = self.createInput('globalSRT', dataType='Xfo', parent=self.inputHrcGrp).getTarget()
        self.cogInputTgt = self.createInput('cog', dataType='Xfo', parent=self.inputHrcGrp).getTarget()
        self.neckBaseInputTgt = self.createInput('neckBase', dataType='Xfo', parent=self.inputHrcGrp).getTarget()

        # Declare Output Xfos
        self.neckOutputTgt = self.createOutput('neck', dataType='Xfo', parent=self.outputHrcGrp).getTarget()
        self.headOutputTgt = self.createOutput('head', dataType='Xfo', parent=self.outputHrcGrp).getTarget()

        # Declare Input Attrs
        self.drawDebugInputAttr = self.createInput('drawDebug', dataType='Boolean', value=False, parent=self.cmpInputAttrGrp).getTarget()
        self.rigScaleInputAttr = self.createInput('rigScale', dataType='Float', value=1.0, parent=self.cmpInputAttrGrp).getTarget()

        # Declare Output Attrs


class GswNeckHeadComponentGuide(GswNeckHeadComponent):

    """Neck Component Guide"""

    def __init__(self, name='neckhead', parent=None, *args, **kwargs):

        Profiler.getInstance().push('Construct Neck Head Component:' + name)
        super(GswNeckHeadComponentGuide, self).__init__(name, parent, *args, **kwargs)

        # =========
        # Controls
        # =========
        guideSettingsAttrGrp = AttributeGroup("GuideSettings", parent=self)

        # neck split
        self.neckCtrlCountAttr = IntegerAttribute('neckControls', value=1, minValue=1, maxValue=10, parent=guideSettingsAttrGrp)
        self.neckCtrlCountAttr.setValueChangeCallback(self.updateCervicalCtrls)

        # auto correction ratio attrs
        self.hasEyeLookAtAttr = BoolAttribute('eyeLookAt', value=False, parent=guideSettingsAttrGrp)
        self.neckUpRateAttr = ScalarAttribute('neckUpRate', value=0.6, minValue=-10, maxValue=10, parent=guideSettingsAttrGrp)
        self.neckDownRateAttr = ScalarAttribute('neckDownRate', value=0.33, minValue=-10, maxValue=10, parent=guideSettingsAttrGrp)
        self.neckRollRateAttr = ScalarAttribute('neckRollRate', value=0.45, minValue=-10, maxValue=10, parent=guideSettingsAttrGrp)
        self.neckYawRateAttr = ScalarAttribute('neckYawRate', value=0.6, minValue=-10, maxValue=10, parent=guideSettingsAttrGrp)

        # Guide Controls
        self.neckCtrl = Control('neck', parent=self.ctrlCmpGrp, shape='sphere')
        self.neckCtrl.scalePoints(Vec3(0.5, 0.5, 0.5))
        self.headCtrl = Control('head', parent=self.ctrlCmpGrp, shape='sphere')
        self.headCtrl.scalePoints(Vec3(0.5, 0.5, 0.5))
        self.upvCtrl = Control('upv', parent=self.ctrlCmpGrp, shape='sphere')
        self.upvCtrl.scalePoints(Vec3(0.5, 0.5, 0.5))
        self.lookAtCtrl = Control('lookAt', parent=self.ctrlCmpGrp, shape='sphere')
        self.lookAtCtrl.scalePoints(Vec3(0.5, 0.5, 0.5))

        self.neckCtrlShape = Control('neckPin', parent=self.ctrlCmpGrp, shape='pin')
        self.neckCtrlShape.rotatePoints(90.0, 0.0, 0.0)
        self.neckCtrlShape.rotatePoints(0.0, 90.0, 0.0)
        self.neckCtrlShape.setColor('orange')
        self.headCtrlShape = Control('headPin', parent=self.ctrlCmpGrp, shape='pin')
        self.headCtrlShape.rotatePoints(90.0, 0.0, 0.0)
        self.headCtrlShape.rotatePoints(0.0, 90.0, 0.0)
        self.headCtrlShape.setColor('orange')

        self.cervicalCtrls = []
        self.cervicalPositions = []
        self.cervicalCtrlShapes = []

        # Guide Operator
        self.neckGuideKLOp = KLOperator(name + 'GuideKLOp', 'GSW_NeckHeadGuideSolver', 'GSW_Kraken')
        self.addOperator(self.neckGuideKLOp)

        # Add Att Inputs
        self.neckGuideKLOp.setInput('drawDebug', self.drawDebugInputAttr)
        self.neckGuideKLOp.setInput('rigScale', self.rigScaleInputAttr)

        # Add Source Inputs
        self.neckGuideKLOp.setInput('sources', [self.neckCtrl, self.headCtrl, self.upvCtrl, self.lookAtCtrl])

        # Add Target Outputs
        self.neckGuideKLOp.setOutput('targets', [self.neckCtrlShape, self.headCtrlShape])

        # Calculate default values
        neckVec = Vec3(0.0, 14.17, -0.574)
        headVec = Vec3(0.0, 15.17, -0.182)
        upvVec = Vec3(0.0, 17.17, -0.182)
        lookAtVec = Vec3(0.0, 15.17, 3)
        upVector = Vec3(0.0, 0.0, -1.0)

        neckOri = Quat()
        neckOri.setFromDirectionAndUpvector(
            (headVec - neckVec).unit(), ((neckVec + upVector) - neckVec).unit())

        headOri = Quat()

        self.default_data = {
            "name": name,
            "location": "M",
            "neckXfo": Xfo(tr=neckVec, ori=neckOri),
            "headXfo": Xfo(tr=headVec, ori=headOri),
            "upvXfo": Xfo(tr=upvVec),
            "lookAtXfo": Xfo(tr=lookAtVec),
            "neckCrvData": self.neckCtrlShape.getCurveData(),
            "headCrvData": self.headCtrlShape.getCurveData(),
            "neckUpRate": 0.6,
            "neckDownRate": 0.33,
            "neckRollRate": 0.45,
            "neckYawRate": 0.6,
            "cervicalPositions": []
        }

        self.loadData(self.default_data)

        Profiler.getInstance().pop()

    # =============
    # Data Methods
    # =============
    def saveData(self):
        """Save the data for the component to be persisted.

        Return:
        The JSON data object

        """

        data = super(GswNeckHeadComponentGuide, self).saveData()

        data['neckXfo'] = self.neckCtrl.xfo
        data['headXfo'] = self.headCtrl.xfo
        data['upvXfo'] = self.upvCtrl.xfo
        data['lookAtXfo'] = self.lookAtCtrl.xfo

        data['neckCrvData'] = self.neckCtrlShape.getCurveData()
        data['headCrvData'] = self.headCtrlShape.getCurveData()

        data['neckControls'] = self.neckCtrlCountAttr.getValue()

        data['hasEyeLookAt'] = self.hasEyeLookAtAttr.getValue()
        data['neckUpRate'] = self.neckUpRateAttr.getValue()
        data['neckDownRate'] = self.neckDownRateAttr.getValue()
        data['neckRollRate'] = self.neckRollRateAttr.getValue()
        data['neckYawRate'] = self.neckYawRateAttr.getValue()

        self.cervicalPositions = []
        for i in xrange(len(self.cervicalCtrls)):
            self.cervicalPositions.append(self.cervicalCtrls[i].xfo.tr)

        data['cervicalPositions'] = self.cervicalPositions

        return data

    def loadData(self, data):
        """Load a saved guide representation from persisted data.

        Arguments:
            data (object): The JSON data object.

        Returns:
            bool: True if successful.

        """

        super(GswNeckHeadComponentGuide, self).loadData(data)

        self.neckCtrl.xfo = data.get('neckXfo')
        self.headCtrl.xfo = data.get('headXfo')
        self.upvCtrl.xfo = data.get('upvXfo')
        self.lookAtCtrl.xfo = data.get('lookAtXfo')

        self.neckCtrlShape.setCurveData(data.get('neckCrvData'))
        self.headCtrlShape.setCurveData(data.get('headCrvData'))

        self.neckCtrlCountAttr.setValue(data.get('neckControls', 1))
        self.hasEyeLookAtAttr.setValue(data.get('hasEyeLookAt', False))
        self.neckUpRateAttr.setValue(data.get('neckUpRate'))
        self.neckDownRateAttr.setValue(data.get('neckDownRate'))
        self.neckRollRateAttr.setValue(data.get('neckRollRate'))
        self.neckYawRateAttr.setValue(data.get('neckYawRate'))

        self.cervicalPositions = data.get('cervicalPositions', [])

        # Evaluate guide operators
        self.neckGuideKLOp.evaluate()

        return True

    def getRigBuildData(self):
        """Returns the Guide data used by the Rig Component to define the layout
        of the final rig.

        Return:
        The JSON rig data object.

        """

        data = super(GswNeckHeadComponentGuide, self).getRigBuildData()

        data['neckXfo'] = self.neckCtrlShape.xfo
        data['headXfo'] = self.headCtrlShape.xfo
        data['upvXfo'] = self.upvCtrl.xfo
        data['lookAtXfo'] = self.lookAtCtrl.xfo
        data['neckControls'] = self.neckCtrlCountAttr.getValue()
        data['hasEyeLookAt'] = self.hasEyeLookAtAttr.getValue()
        data['neckUpRate'] = self.neckUpRateAttr.getValue()
        data['neckDownRate'] = self.neckDownRateAttr.getValue()
        data['neckRollRate'] = self.neckRollRateAttr.getValue()
        data['neckYawRate'] = self.neckYawRateAttr.getValue()

        cervicalXfos = []
        for s in self.cervicalCtrlShapes:
            cervicalXfos.append(s.xfo)
        data['cervicalXfos'] = cervicalXfos

        return data

    def updateCervicalCtrls(self, num):

        if not self.cervicalCtrls:
            self.cervicalCtrls = []

        currentCount = len(self.cervicalCtrls)
        if currentCount < num - 1:
            # append ctrls
            for i in xrange(num - 1 - currentCount):
                name = 'cervical' + str(i).zfill(2)
                newCtrl = Control(name, parent=self.ctrlCmpGrp, shape="sphere")
                newCtrl.scalePoints(Vec3(0.5, 0.5, 0.5))
                newCtrl.setColor('blue')
                newCtrl.xfo.tr = self.calculateCervicalPosition(i, num)
                self.cervicalPositions.append(newCtrl.xfo.tr)
                self.cervicalCtrls.append(newCtrl)

                newShape = Control(name, parent=self.ctrlCmpGrp, shape="pin")
                newShape.setColor('orange')
                newShape.rotatePoints(90.0, 0.0, 0.0)
                newShape.rotatePoints(0.0, 90.0, 0.0)
                newShape.xfo = newCtrl.xfo
                self.cervicalCtrlShapes.append(newShape)

        elif num - 1 < currentCount:
            # remove ctrls
            for i in xrange(currentCount - num + 1):
                extraCtrl = self.cervicalCtrls.pop()
                self.ctrlCmpGrp.removeChild(extraCtrl)

                extraShape = self.cervicalCtrlShapes.pop()
                self.ctrlCmpGrp.removeChild(extraShape)

        # update guide op
        src = [self.neckCtrl, self.headCtrl, self.upvCtrl, self.lookAtCtrl]
        dst = [self.neckCtrlShape, self.headCtrlShape]
        src[1:1] = self.cervicalCtrls
        dst[1:1] = self.cervicalCtrlShapes

        self.neckGuideKLOp.setInput('sources', src)
        self.neckGuideKLOp.setOutput('targets', dst)

    def calculateCervicalPosition(self, n, total):
        neck = self.neckCtrl.xfo.tr
        head = self.headCtrl.xfo.tr

        x = (head - neck).x * (float(n + 1) / float(total))
        y = (head - neck).y * (float(n + 1) / float(total))
        z = (head - neck).z * (float(n + 1) / float(total))

        return Vec3(x, y, z) + neck

    # ==============
    # Class Methods
    # ==============
    @classmethod
    def getComponentType(cls):
        """Enables introspection of the class prior to construction to determine
        if it is a guide component.

        Returns:
            bool: Whether the component is a guide component.

        """

        return 'Guide'

    @classmethod
    def getRigComponentClass(cls):
        """Returns the corresponding rig component class for this guide
        component class.

        Returns:
            class: The rig component class.

        """

        return GswNeckHeadComponentRig


class GswNeckHeadComponentRig(GswNeckHeadComponent):

    """Neck Component"""

    def __init__(self, name="neck", parent=None):

        Profiler.getInstance().push("Construct Neck Rig Component:" + name)
        super(GswNeckHeadComponentRig, self).__init__(name, parent)

        self.neckUpRateInputAttr = self.createInput('neckUpRate', dataType='Float', value=0.6, minValue=-10.0, maxValue=10.0, parent=self.cmpInputAttrGrp).getTarget()
        self.neckDownRateInputAttr = self.createInput('neckDownRate', dataType='Float', value=0.33, minValue=-10.0, maxValue=10.0, parent=self.cmpInputAttrGrp).getTarget()
        self.neckRollRateInputAttr = self.createInput('neckRollRate', dataType='Float', value=0.45, minValue=-10.0, maxValue=10.0, parent=self.cmpInputAttrGrp).getTarget()
        self.neckYawRateInputAttr = self.createInput('neckYawRate', dataType='Float', value=0.6, minValue=-10.0, maxValue=10.0, parent=self.cmpInputAttrGrp).getTarget()

        # =========
        # Controls
        # =========
        # Neck
        self.rootSpace = CtrlSpace('root', parent=self.ctrlCmpGrp)

        self.neckCtrlSpace = CtrlSpace(name='neck', parent=self.rootSpace)
        self.neckCtrl = Control('neck', parent=self.neckCtrlSpace, shape="pin")
        self.neckCtrl.setColor("orange")
        self.neckCtrlSpaceDummy = Transform(name='neckCtrlSpaceDummy', parent=self.rootSpace)

        self.headCtrlSpace = CtrlSpace(name='head', parent=self.rootSpace)
        self.headRollCtrl = Control('head', parent=self.headCtrlSpace)
        self.headRollCtrl.setCurveData(icon.bended_arrow)
        self.headRollCtrl.setColor("orange")

        self.headRollDummy = Transform('headRollDummy', parent=self.rootSpace)
        self.headCtrlSpaceDummy = Transform('headCtrlSpaceDummy', parent=self.rootSpace)
        self.headOutDummy = Transform('headOutDummy', parent=self.neckCtrl)

        # lookat
        self.lookAtCtrl = Control('lookAt', parent=self.rootSpace, shape="arrow")
        self.lookAtCtrl.setColor("orange")

        self.lookAtCtrlSpace = self.lookAtCtrl.insertCtrlSpace(name='lookAt')

        # ==========
        # Deformers
        # ==========
        deformersLayer = self.getOrCreateLayer('deformers')
        self.defCmpGrp = ComponentGroup(self.getName(), self, parent=deformersLayer)
        self.addItem('defCmpGrp', self.defCmpGrp)

        self.neckDef = Joint('neck', parent=self.defCmpGrp)
        self.neckDef.setComponent(self)

        self.headDef = Joint('head', parent=self.defCmpGrp)
        self.headDef.setComponent(self)

        # ==============
        # Constrain I/O
        # ==============
        # Constraint inputs
        neckInputConstraintName = '_'.join([self.rootSpace.getName(),
                                            'To',
                                            self.neckBaseInputTgt.getName()])

        self.neckInputCnstr = self.rootSpace.constrainTo(
            self.neckBaseInputTgt,
            'Pose',
            maintainOffset=True,
            name=neckInputConstraintName)

        lookAtInputConstraintName = '_'.join([self.lookAtCtrlSpace.getName(),
                                              'To',
                                              self.cogInputTgt.getName()])

        self.lookAtInputCnstr = self.lookAtCtrlSpace.constrainTo(
            self.cogInputTgt,
            'Pose',
            maintainOffset=True,
            name=lookAtInputConstraintName)

        ##############
        # solver step1
        self.neckSolverStep1KLOp = KLOperator('neckSolverStep1KLOp',
                                              'GSW_NeckHeadSolverStep1',
                                              'GSW_Kraken')
        self.addOperator(self.neckSolverStep1KLOp)

        # Add Att Inputs
        self.neckSolverStep1KLOp.setInput('drawDebug', self.drawDebugInputAttr)
        self.neckSolverStep1KLOp.setInput('rigScale', self.rigScaleInputAttr)

        # Add Source Attrs
        self.neckSolverStep1KLOp.setInput('upRate', self.neckUpRateInputAttr)
        self.neckSolverStep1KLOp.setInput('downRate', self.neckDownRateInputAttr)
        self.neckSolverStep1KLOp.setInput('rollRate', self.neckRollRateInputAttr)
        self.neckSolverStep1KLOp.setInput('yawRate', self.neckYawRateInputAttr)

        # Add Source Inputs
        self.neckSolverStep1KLOp.setInput('base', self.neckBaseInputTgt)
        self.neckSolverStep1KLOp.setInput('root', self.rootSpace)
        self.neckSolverStep1KLOp.setInput('headDummy', self.headRollDummy)
        self.neckSolverStep1KLOp.setInput('lookAt', self.lookAtCtrl)

        # Add Target Outputs
        self.neckSolverStep1KLOp.setOutput('neck', self.neckCtrlSpaceDummy)
        self.neckSolverStep1KLOp.setOutput('head', self.headCtrlSpaceDummy)

        self.neckSolverStep2KLOp = KLOperator('neckSolverStep2KLOp',
                                              'GSW_NeckHeadSolverStep2',
                                              'GSW_Kraken')
        self.addOperator(self.neckSolverStep2KLOp)

        # Add Att Inputs
        self.neckSolverStep2KLOp.setInput('drawDebug', self.drawDebugInputAttr)
        self.neckSolverStep2KLOp.setInput('rigScale', self.rigScaleInputAttr)

        # Add Source Attrs
        self.neckSolverStep2KLOp.setInput('rollRate', self.neckRollRateInputAttr)

        # Add Source Inputs
        self.neckSolverStep2KLOp.setInput('root', self.rootSpace)
        self.neckSolverStep2KLOp.setInput('roll', self.headRollCtrl)
        self.neckSolverStep2KLOp.setInput('neckDummy', self.neckCtrlSpaceDummy)

        # Add Target Outputs
        self.neckSolverStep2KLOp.setOutput('neckCtrlSpaces', [self.neckCtrlSpace])

        self.neckSolverStep3KLOp = KLOperator('neckSolverStep3KLOp',
                                              'GSW_NeckHeadSolverStep3',
                                              'GSW_Kraken')
        self.addOperator(self.neckSolverStep3KLOp)

        # Add Att Inputs
        self.neckSolverStep3KLOp.setInput('drawDebug', self.drawDebugInputAttr)
        self.neckSolverStep3KLOp.setInput('rigScale', self.rigScaleInputAttr)

        # Add Source Inputs
        self.neckSolverStep3KLOp.setInput('root', self.rootSpace)
        self.neckSolverStep3KLOp.setInput('headDummy', self.headCtrlSpaceDummy)

        # Add Target Outputs
        self.neckSolverStep3KLOp.setOutput('head', self.headCtrlSpace)

        # Constraint outputs
        neckOutCnstrName = '_'.join([self.neckOutputTgt.getName(),
                                     'To',
                                     self.neckCtrl.getName()])

        self.neckOutCnstr = self.neckOutputTgt.constrainTo(
            self.neckCtrl,
            'Pose',
            maintainOffset=False,
            name=neckOutCnstrName)

        headOutCnstrName2 = '_'.join([self.headOutDummy.getName(),
                                      'To',
                                      self.headRollCtrl.getName()])

        self.headOutCnstr2 = self.headOutDummy.constrainTo(
            self.headRollCtrl,
            'Orientation',
            maintainOffset=False,
            name=headOutCnstrName2)

        headOutCnstrName = '_'.join([self.headOutputTgt.getName(),
                                     'To',
                                     self.headOutDummy.getName()])

        self.headOutCnstr = self.headOutputTgt.constrainTo(
            self.headOutDummy,
            'Pose',
            maintainOffset=False,
            name=headOutCnstrName)

        # ==============
        # Add Operators
        # ==============
        # Add Deformer KL Op
        self.neckDeformerKLOp = KLOperator('neckDeformerKLOp',
                                           'MultiPoseConstraintSolver',
                                           'Kraken')

        self.addOperator(self.neckDeformerKLOp)

        # Add Att Inputs
        self.neckDeformerKLOp.setInput('drawDebug', self.drawDebugInputAttr)
        self.neckDeformerKLOp.setInput('rigScale', self.rigScaleInputAttr)

        # Add Xfo Inputstrl)
        self.neckDeformerKLOp.setInput('constrainers',
                                       [self.neckCtrl, self.headOutDummy])

        # Add Xfo Outputs
        self.neckDeformerKLOp.setOutput('constrainees',
                                        [self.neckDef, self.headDef])

        Profiler.getInstance().pop()

    def loadData(self, data=None):
        """Load a saved guide representation from persisted data.

        Arguments:
        data -- object, The JSON data object.

        Return:
        True if successful.

        """

        super(GswNeckHeadComponentRig, self).loadData(data)
        neckXfo = data.get('neckXfo')
        headXfo = data.get('headXfo')
        upvXfo = data.get('upvXfo')
        lookAtXfo = data.get('lookAtXfo')
        rootXfo = Xfo(tr=neckXfo.tr, ori=headXfo.ori)

        # TODO:
        # hasEyeLookAt = data.get('hasEyeLookAt')
        self.neckUpRateInputAttr.setValue(data.get('neckUpRate'))
        self.neckDownRateInputAttr.setValue(data.get('neckDownRate'))
        self.neckRollRateInputAttr.setValue(data.get('neckRollRate'))
        self.neckYawRateInputAttr.setValue(data.get('neckYawRate'))

        headLength = headXfo.tr.distanceTo(upvXfo.tr)
        lookAtLength = headXfo.tr.distanceTo(lookAtXfo.tr)

        self.rootSpace.xfo = rootXfo

        self.neckCtrlSpace.xfo = neckXfo
        self.neckCtrl.xfo = neckXfo
        self.neckCtrl.rotatePoints(90, 0, -90)
        self.neckCtrl.scalePoints(Vec3(headLength, headLength, headLength))

        self.headCtrlSpace.xfo = headXfo
        self.headRollCtrl.xfo = headXfo
        self.headRollCtrl.scalePoints(Vec3(headLength * 1.0, headLength * 0.7, headLength * 1.0))
        self.headRollCtrl.rotatePoints(-90, 0, -90)
        self.headRollCtrl.translatePoints(Vec3(headLength * 0.7, 0, 0))
        self.headRollCtrl.lockRotation(True, False, True)
        self.headRollCtrl.lockTranslation(True, True, True)
        self.headRollCtrl.lockScale(True, True, True)

        self.headRollDummy.xfo = headXfo
        self.headRollDummy.lockRotation(True, True, True)
        self.headRollDummy.lockTranslation(True, True, True)
        self.headRollDummy.lockScale(True, True, True)
        self.headRollDummy.setVisibility(False)

        self.headOutDummy.xfo = headXfo
        # self.headOutDummy.lockRotation(True, True, True)
        # self.headOutDummy.lockTranslation(True, True, True)
        # self.headOutDummy.lockScale(True, True, True)
        self.headOutDummy.setVisibility(False)

        self.lookAtCtrlSpace.xfo = lookAtXfo
        self.lookAtCtrl.xfo = lookAtXfo
        self.lookAtCtrl.scalePoints(Vec3(lookAtLength, 1.0, lookAtLength * 0.5))
        self.lookAtCtrl.lockRotation(True, True, True)
        self.lookAtCtrl.lockScale(True, True, True)

        self.neckCtrlSpaceDummy.setVisibility(False)
        self.headCtrlSpaceDummy.setVisibility(False)

        self.updateCervicals(data.get('cervicalXfos'), headLength=headLength)

        # ============
        # Set IO Xfos
        # ============
        self.neckBaseInputTgt.xfo = neckXfo
        self.cogInputTgt.xfo = neckXfo
        self.neckOutputTgt.xfo = neckXfo
        self.headOutputTgt.xfo = headXfo

        # Evaluate Constraints
        self.neckInputCnstr.evaluate()
        self.lookAtInputCnstr.evaluate()
        self.neckOutCnstr.evaluate()
        self.headOutCnstr.evaluate()
        self.headOutCnstr2.evaluate()

        self.neckSolverStep1KLOp.evaluate()
        self.neckSolverStep2KLOp.evaluate()
        self.neckSolverStep3KLOp.evaluate()

    def updateCervicals(self, cervicalXfos, headLength=1.0):

        if not cervicalXfos:
            return

        self.cervicalCtrls = []
        self.cervicalCtrlSpaces = []
        self.cervicalDefs = []

        for i, x in enumerate(cervicalXfos):

            name = 'cervical' + str(i).zfill(2)
            if i == 0:
                parent = self.neckCtrl
            else:
                parent = self.cervicalCtrls[i - 1]

            ctrlSpace = CtrlSpace(name=name, parent=parent)
            ctrlSpace.xfo = x

            ctrl = Control(name, parent=ctrlSpace, shape="pin")
            ctrl.rotatePoints(90, 0, -90)
            ctrl.scalePoints(Vec3(headLength * 0.8, headLength * 0.88, headLength * 0.88))
            ctrl.xfo = x
            ctrl.setColor("orange")

            deformer = Joint(name + 'def', parent=self.defCmpGrp)
            deformer.setComponent(self)

            self.cervicalCtrlSpaces.append(ctrlSpace)
            self.cervicalCtrls.append(ctrl)
            self.cervicalDefs.append(deformer)

        self.cervicalCtrls[-1].addChild(self.headOutDummy)

        # update deformer op i/o put
        deformerSrc = [self.neckCtrl, self.headOutDummy]
        deformerDst = [self.neckDef, self.headDef]
        deformerSrc[1:1] = self.cervicalCtrls
        deformerDst[1:1] = self.cervicalDefs
        self.neckDeformerKLOp.setInput('constrainers', deformerSrc)
        self.neckDeformerKLOp.setOutput('constrainees', deformerDst)

        ctrlSpaces = [self.neckCtrlSpace]
        ctrlSpaces[1:1] = self.cervicalCtrlSpaces
        # self.neckSolverStep2KLOp.setOutput('neckCtrlSpaces', ctrlSpaces)


from kraken.core.kraken_system import KrakenSystem
ks = KrakenSystem.getInstance()
ks.registerComponent(GswNeckHeadComponentGuide)
ks.registerComponent(GswNeckHeadComponentRig)
