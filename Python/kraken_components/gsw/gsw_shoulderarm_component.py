from kraken.core.maths import Vec3, Quat, Euler, Math_degToRad
from kraken.core.maths.xfo import Xfo
from kraken.core.maths.xfo import xfoFromDirAndUpV

from kraken.core.objects.components.base_example_component import BaseExampleComponent

from kraken.core.objects.attributes.attribute_group import AttributeGroup
from kraken.core.objects.attributes.scalar_attribute import ScalarAttribute
from kraken.core.objects.attributes.bool_attribute import BoolAttribute
# from kraken.core.objects.attributes.string_attribute import StringAttribute

from kraken.core.objects.constraints.pose_constraint import PoseConstraint
from kraken.core.objects.constraints.position_constraint import PositionConstraint

from kraken.core.objects.component_group import ComponentGroup
# from kraken.core.objects.hierarchy_group import HierarchyGroup
# from kraken.core.objects.locator import Locator
from kraken.core.objects.transform import Transform
from kraken.core.objects.joint import Joint
from kraken.core.objects.ctrlSpace import CtrlSpace
from kraken.core.objects.control import Control

from kraken.core.objects.operators.kl_operator import KLOperator

from kraken.core.profiler import Profiler
# from kraken.helpers.utility_methods import logHierarchy

import kraken_components.gsw.gsw_icon as icon


class GswShoulderArmComponent(BaseExampleComponent):

    """Clavicle Component Base"""

    def __init__(self, name='shoulderarm', parent=None, *args, **kwargs):
        super(GswShoulderArmComponent, self).__init__(name, parent, *args, **kwargs)

        # ===========
        # Declare IO
        # ===========
        # Declare Inputs Xfos
        self.globalSRTInputTgt = self.createInput('globalSRT', dataType='Xfo', parent=self.inputHrcGrp).getTarget()
        self.cogInputTgt = self.createInput('cog', dataType='Xfo', parent=self.inputHrcGrp).getTarget()
        self.spineEndInputTgt = self.createInput('spineEnd', dataType='Xfo', parent=self.inputHrcGrp).getTarget()

        # Declare Output Xfos
        self.clavicleOutputTgt = self.createOutput('clavicle', dataType='Xfo', parent=self.outputHrcGrp).getTarget()
        self.clavicleEndOutputTgt = self.createOutput('clavicleEnd', dataType='Xfo', parent=self.outputHrcGrp).getTarget()

        self.bicepOutputTgt = self.createOutput('bicep', dataType='Xfo', parent=self.outputHrcGrp).getTarget()
        self.elbowOutputTgt = self.createOutput('elbow', dataType='Xfo', parent=self.outputHrcGrp).getTarget()
        self.forearmOutputTgt = self.createOutput('forearm', dataType='Xfo', parent=self.outputHrcGrp).getTarget()
        self.wristOutputTgt = self.createOutput('wrist', dataType='Xfo', parent=self.outputHrcGrp).getTarget()

        # Declare Input Attrs
        self.drawDebugInputAttr = self.createInput('drawDebug', dataType='Boolean', value=False, parent=self.cmpInputAttrGrp).getTarget()
        self.rigScaleInputAttr = self.createInput('rigScale', dataType='Float', value=1.0, parent=self.cmpInputAttrGrp).getTarget()
        self.rightSideInputAttr = self.createInput('rightSide', dataType='Boolean', value=self.getLocation() is 'R', parent=self.cmpInputAttrGrp).getTarget()

        # Declare Output Attrs
        self.drawDebugOutputAttr = self.createOutput('drawDebug', dataType='Boolean', value=False, parent=self.cmpOutputAttrGrp).getTarget()
        self.ikBlendOutputAttr = self.createOutput('ikBlend', dataType='Float', value=0.0, parent=self.cmpOutputAttrGrp).getTarget()


class GswShoulderArmComponentGuide(GswShoulderArmComponent):

    """Clavicle Component Guide"""

    def __init__(self, name='arm', parent=None, *args, **kwargs):

        Profiler.getInstance().push("Construct Clavicle Guide Component:" + name)
        super(GswShoulderArmComponentGuide, self).__init__(name, parent, *args, **kwargs)

        # ===========
        # Attributes
        # ===========
        # Add Component Params to IK control
        guideSettingsAttrGrp = AttributeGroup("GuideSettings", parent=self)

        self.bicepFKCtrlSizeInputAttr = ScalarAttribute('bicepFKCtrlSize', value=1.5, minValue=0.0, maxValue=10.0, parent=guideSettingsAttrGrp)
        self.forearmFKCtrlSizeInputAttr = ScalarAttribute('forearmFKCtrlSize', value=1.5, minValue=0.0, maxValue=10.0, parent=guideSettingsAttrGrp)
        self.modifierInputAttr = ScalarAttribute('modifier', value=1.0, minValue=0.0, maxValue=1.0, parent=guideSettingsAttrGrp)
        self.upRateInputAttr = ScalarAttribute('upRate', value=0.66, minValue=0.0, maxValue=1.0, parent=guideSettingsAttrGrp)
        self.downRateInputAttr = ScalarAttribute('downRate', value=0.1, minValue=0.0, maxValue=1.0, parent=guideSettingsAttrGrp)
        self.forwardRateInputAttr = ScalarAttribute('forwardRate', value=0.5, minValue=0.0, maxValue=1.0, parent=guideSettingsAttrGrp)
        self.backwardRateInputAttr = ScalarAttribute('backwardRate', value=0.5, minValue=0.0, maxValue=1.0, parent=guideSettingsAttrGrp)

        # =========
        # Controls
        # =========
        # Guide Controls

        self.clavicleCtrl = Control('clavicle', parent=self.ctrlCmpGrp, shape="circle")
        self.clavicleCtrl.scalePoints(Vec3(0.75, 0.75, 0.75))
        self.clavicleCtrl.rotatePoints(0.0, 0.0, 90.0)

        self.clavicleGuideSettingsAttrGrp = AttributeGroup("Settings", parent=self.clavicleCtrl)
        self.handDebugInputAttr = BoolAttribute('drawDebug', value=False, parent=self.clavicleGuideSettingsAttrGrp)
        self.drawDebugInputAttr.connect(self.handDebugInputAttr)

        self.clavicleBladeCtrl = Control('clavicleBlade', parent=self.clavicleCtrl)
        self.clavicleBladeCtrl.setCurveData(icon.pointed_box)
        self.clavicleBladeCtrl.setColor('red')
        self.clavicleBladeCtrl.translatePoints(Vec3(0.5, 0.0, 0.5))

        self.clavicleEndCtrl = Control('clavicleEnd', parent=self.ctrlCmpGrp, shape="cube")
        self.clavicleEndCtrl.scalePoints(Vec3(0.25, 0.25, 0.25))

        self.bicepCtrl = Control('bicep', parent=self.ctrlCmpGrp, shape="sphere")
        self.bicepCtrl.setColor('blue')
        self.forearmCtrl = Control('forearm', parent=self.ctrlCmpGrp, shape="sphere")
        self.forearmCtrl.setColor('blue')
        self.wristCtrl = Control('wrist', parent=self.ctrlCmpGrp, shape="sphere")
        self.wristCtrl.setColor('blue')
        self.armBladeCtrl = Control('armBlade', parent=self.bicepCtrl)
        self.armBladeCtrl.setCurveData(icon.pointed_box)
        self.armBladeCtrl.setColor('red')
        self.armBladeCtrl.translatePoints(Vec3(0.5, 0.0, 0.5))

        armGuideSettingsAttrGrp = AttributeGroup("DisplayInfo_ArmSettings", parent=self.bicepCtrl)
        self.armGuideDebugAttr = BoolAttribute('drawDebug', value=True, parent=armGuideSettingsAttrGrp)

        self.guideOpHost = Transform('guideOpHost', self.ctrlCmpGrp)

        # Guide Operator
        self.armGuideKLOp = KLOperator(name + self.getLocation() + 'GuideKLOp', 'TwoBoneIKGuideSolver', 'Kraken')
        self.addOperator(self.armGuideKLOp)

        # Add Att Inputs
        self.armGuideKLOp.setInput('drawDebug', self.armGuideDebugAttr)
        self.armGuideKLOp.setInput('rigScale', self.rigScaleInputAttr)

        # Add Source Inputs
        self.armGuideKLOp.setInput('root', self.bicepCtrl)
        self.armGuideKLOp.setInput('mid', self.forearmCtrl)
        self.armGuideKLOp.setInput('end', self.wristCtrl)

        # Add Target Outputs
        self.armGuideKLOp.setOutput('guideOpHost', self.guideOpHost)

        self.default_data = {
            "name": name,
            "location": "L",
            "clavicleXfo": Xfo(Vec3(0.227, 13.45, -0.4)),
            "clavicleEndXfo": Xfo(Vec3(1.75, 13.5, -0.43)),
            "clavicleBladeXfo": Xfo(Vec3(0.227, 13.45, -0.4)),
            "bicepXfo": Xfo(Vec3(1.758, 13.57, -0.432)),
            "forearmXfo": Xfo(Vec3(4.177, 13.512, -0.511)),
            "wristXfo": Xfo(Vec3(6.56, 13.58, -0.438)),
            "bladeXfo": Xfo(Vec3(1.758, 13.57, -0.432)),
            "bicepFKCtrlSize": self.bicepFKCtrlSizeInputAttr.getValue(),
            "forearmFKCtrlSize": self.forearmFKCtrlSizeInputAttr.getValue(),
            "modifier": self.modifierInputAttr.getValue(),
            "upRate": self.upRateInputAttr.getValue(),
            "downRate": self.downRateInputAttr.getValue(),
            "forwardRate": self.forwardRateInputAttr.getValue(),
            "backwardRate": self.backwardRateInputAttr.getValue()
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

        data = super(GswShoulderArmComponentGuide, self).saveData()

        data['clavicleXfo'] = self.clavicleCtrl.xfo
        data['clavicleBladeXfo'] = self.clavicleBladeCtrl.xfo
        data['clavicleEndXfo'] = self.clavicleEndCtrl.xfo

        data['bicepXfo'] = self.bicepCtrl.xfo
        data['forearmXfo'] = self.forearmCtrl.xfo
        data['wristXfo'] = self.wristCtrl.xfo
        data['bladeXfo'] = self.armBladeCtrl.xfo

        if self.getLocation() == "R":
            data['clavicleBladeXfo'] *= Quat(Euler(Math_degToRad(180), 0,  0))
            data['bladeXfo'] *= Quat(Euler(Math_degToRad(180), 0,  0))

        return data

    def loadData(self, data):
        """Load a saved guide representation from persisted data.

        Arguments:
        data -- object, The JSON data object.

        Return:
        True if successful.

        """

        super(GswShoulderArmComponentGuide, self).loadData(data)

        self.clavicleCtrl.xfo = data['clavicleXfo']
        self.clavicleBladeCtrl.xfo = data['clavicleBladeXfo']
        self.clavicleEndCtrl.xfo = data['clavicleEndXfo']

        self.bicepCtrl.xfo = data['bicepXfo']
        self.forearmCtrl.xfo = data['forearmXfo']
        self.wristCtrl.xfo = data['wristXfo']
        self.armBladeCtrl.xfo = data['bladeXfo']

        if self.getLocation() == "R":
            self.clavicleBladeCtrl.xfo.ori *= Quat(Euler(Math_degToRad(180), 0,  0))
            self.armBladeCtrl.xfo *= Quat(Euler(Math_degToRad(180), 0,  0))

        guideOpName = ''.join([self.getName().split('GuideKLOp')[0],
                               self.getLocation(),
                               'GuideKLOp'])
        self.armGuideKLOp.setName(guideOpName)

        return True

    def getRigBuildData(self):
        """Returns the Guide data used by the Rig Component to define the layout of the final rig..

        Return:
        The JSON rig data object.

        """

        data = super(GswShoulderArmComponentGuide, self).getRigBuildData()

        # Values
        claviclePosition = self.clavicleCtrl.xfo.tr
        clavicleBladeXfo = self.clavicleBladeCtrl.xfo
        clavicleEndPosition = self.clavicleEndCtrl.xfo.tr

        # Calculate Clavicle Xfo
        rootToEnd = clavicleEndPosition.subtract(claviclePosition).unit()
        # targetForward = clavicleBladeXfo.ori.rotateVector(Vec3(1, 0, 0))
        targetNormal = clavicleBladeXfo.ori.rotateVector(Vec3(0, 1, 0))

        if self.getLocation() == "R":
            targetUp = clavicleBladeXfo.ori.rotateVector(Vec3(0, 0, -1))
        else:
            targetUp = clavicleBladeXfo.ori.rotateVector(Vec3(0, 0, 1))

        bone1Normal = targetNormal.unit()
        bone1ZAxis = targetUp.unit()

        clavicleXfo = Xfo()
        clavicleXfo.setFromVectors(rootToEnd, bone1Normal, bone1ZAxis, claviclePosition)

        clavicleLen = claviclePosition.subtract(clavicleEndPosition).length()

        data['clavicleXfo'] = clavicleXfo
        data['clavicleLen'] = clavicleLen

        # arm
        bicepPosition = self.bicepCtrl.xfo.tr
        forearmPosition = self.forearmCtrl.xfo.tr
        wristPosition = self.wristCtrl.xfo.tr

        # Calculate Bicep Xfo
        # rootToWrist = wristPosition.subtract(bicepPosition).unit()
        rootToElbow = forearmPosition.subtract(bicepPosition).unit()

        # targetForward = self.armBladeCtrl.xfo.ori.rotateVector(Vec3(1, 0, 0))
        targetNormal = self.armBladeCtrl.xfo.ori.rotateVector(Vec3(0, 1, 0))
        if self.getLocation() == "R":
            targetUp = self.armBladeCtrl.xfo.ori.rotateVector(Vec3(0, 0, -1))
        else:
            targetUp = self.armBladeCtrl.xfo.ori.rotateVector(Vec3(0, 0, 1))

        bone1Normal = targetNormal.unit()
        bone1ZAxis = targetUp.unit()

        bicepXfo = Xfo()
        bicepXfo.setFromVectors(rootToElbow, bone1Normal, bone1ZAxis, bicepPosition)

        # Calculate Forearm Xfo
        elbowToWrist = wristPosition.subtract(forearmPosition).unit()
        # elbowToRoot = bicepPosition.subtract(forearmPosition).unit()

        # bone2Normal = elbowToRoot.cross(elbowToWrist).unit()
        # bone2ZAxis = elbowToWrist.cross(bone2Normal).unit()
        forearmXfo = Xfo()
        forearmXfo.setFromVectors(elbowToWrist, bone1Normal, bone1ZAxis, forearmPosition)

        # Calculate Wrist Xfo
        wristXfo = Xfo()
        wristXfo.tr = self.wristCtrl.xfo.tr
        wristXfo.ori = forearmXfo.ori

        upVXfo = xfoFromDirAndUpV(bicepPosition, wristPosition, forearmPosition)
        upVXfo.ori = self.armBladeCtrl.xfo.ori * Quat(Euler(Math_degToRad(180.0), 0.0, 0.0))
        upVXfo.tr = forearmPosition
        upVXfo.tr = upVXfo.transformVector(Vec3(0, 0, 5))

        # Lengths
        bicepLen = bicepPosition.subtract(forearmPosition).length()
        forearmLen = forearmPosition.subtract(wristPosition).length()

        data['bicepXfo'] = bicepXfo
        data['forearmXfo'] = forearmXfo
        data['wristXfo'] = wristXfo
        data['upVXfo'] = upVXfo
        data['bicepLen'] = bicepLen
        data['forearmLen'] = forearmLen

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

        return GswShoulderArmComponentRig


class GswShoulderArmComponentRig(GswShoulderArmComponent):

    """Clavicle Component"""

    def __init__(self, name='arm', parent=None):

        Profiler.getInstance().push("Construct Clavicle Rig Component:" + name)
        super(GswShoulderArmComponentRig, self).__init__(name, parent)

        # =========
        # Controls
        # =========
        # Clavicle
        self.clavicleCtrlSpace = CtrlSpace('clavicle', parent=self.ctrlCmpGrp)
        self.clavicleCtrl = Control('clavicle', parent=self.clavicleCtrlSpace, shape="cube")
        self.clavicleCtrl.alignOnXAxis()
        self.clavicleRefPosition = Transform('clavicleRefPosition', parent=self.ctrlCmpGrp)

        # Bicep
        self.bicepFKCtrlSpace = CtrlSpace('bicepFK', parent=self.ctrlCmpGrp)

        self.bicepFKCtrl = Control('bicepFK', parent=self.bicepFKCtrlSpace, shape="cube")
        self.bicepFKCtrl.alignOnXAxis()

        # Forearm
        self.forearmFKCtrlSpace = CtrlSpace('forearmFK', parent=self.bicepFKCtrl)

        self.forearmFKCtrl = Control('forearmFK', parent=self.forearmFKCtrlSpace, shape="cube")
        self.forearmFKCtrl.alignOnXAxis()

        # Arm IK
        self.armIKCtrlSpace = CtrlSpace('IK', parent=self.ctrlCmpGrp)
        self.armIKCtrl = Control('IK', parent=self.armIKCtrlSpace, shape="pin")

        # Add Params to IK control
        armSettingsAttrGrp = AttributeGroup("DisplayInfo_ArmSettings", parent=self.armIKCtrl)
        self.armDebugInputAttr = BoolAttribute('drawDebug', value=False, parent=armSettingsAttrGrp)
        self.armBone0LenInputAttr = ScalarAttribute('bone1Len', value=0.0, parent=armSettingsAttrGrp)
        self.armBone1LenInputAttr = ScalarAttribute('bone2Len', value=0.0, parent=armSettingsAttrGrp)
        self.armIKBlendInputAttr = ScalarAttribute('fkik', value=1.0, minValue=0.0, maxValue=1.0, parent=armSettingsAttrGrp)

        self.modifierInputAttr = ScalarAttribute('modifier', value=1.0, minValue=0.0, maxValue=1.0, parent=armSettingsAttrGrp)
        self.upRateInputAttr = ScalarAttribute('upRate', value=0.66, minValue=0.0, maxValue=1.0, parent=armSettingsAttrGrp)
        self.downRateInputAttr = ScalarAttribute('downRate', value=0.1, minValue=0.0, maxValue=1.0, parent=armSettingsAttrGrp)
        self.forwardRateInputAttr = ScalarAttribute('forwardRate', value=0.5, minValue=0.0, maxValue=1.0, parent=armSettingsAttrGrp)
        self.backwardRateInputAttr = ScalarAttribute('backwardRate', value=0.5, minValue=0.0, maxValue=1.0, parent=armSettingsAttrGrp)

        # Util Objects
        self.ikRootPosition = Transform("ikPosition1st", parent=self.ctrlCmpGrp)
        self.elbow1stPositionCtrlSpace = CtrlSpace("elbow1stPositionSpace", parent=self.ctrlCmpGrp)
        self.elbow1stPosition = Transform("elbow1stPosition", parent=self.elbow1stPositionCtrlSpace)
        self.elbowRefPosition = Transform("elbowRefPosition", parent=self.ctrlCmpGrp)
        self.ikRoot2ndPosition = Transform("ikPosition2nd", parent=self.clavicleCtrl)

        # Connect Input Attrs
        self.drawDebugInputAttr.connect(self.armDebugInputAttr)

        # Connect Output Attrs
        self.drawDebugOutputAttr.connect(self.armDebugInputAttr)
        self.ikBlendOutputAttr.connect(self.armIKBlendInputAttr)

        # UpV
        self.armUpVCtrlSpace = CtrlSpace('UpV', parent=self.ctrlCmpGrp)
        self.armUpVCtrl = Control('UpV', parent=self.armUpVCtrlSpace, shape="triangle")
        self.armUpVCtrl.alignOnZAxis()
        self.armUpVCtrl.rotatePoints(180, 0, 0)

        # ==========
        # Deformers
        # ==========
        # clavicle
        self.deformersLayer = self.getOrCreateLayer('deformers')
        self.defCmpGrp = ComponentGroup(self.getName(), self, parent=self.deformersLayer)
        self.addItem('defCmpGrp', self.defCmpGrp)

        self.clavicleDef = Joint('clavicle', parent=self.defCmpGrp)
        self.clavicleDef.setComponent(self)

        # arm
        self.bicepDef = Joint('bicep', parent=self.defCmpGrp)
        self.bicepDef.setComponent(self)

        self.elbowDef = Joint('elbow', parent=self.defCmpGrp)
        self.elbowDef.setComponent(self)

        self.forearmDef = Joint('forearm', parent=self.defCmpGrp)
        self.forearmDef.setComponent(self)

        self.wristDef = Joint('wrist', parent=self.defCmpGrp)
        self.wristDef.setComponent(self)

        # ==============
        # Constrain I/O
        # ==============
        # Constraint inputs
        self.armIKCtrlSpaceInputConstraint = PoseConstraint('_'.join([self.armIKCtrlSpace.getName(), 'To', self.globalSRTInputTgt.getName()]))
        self.armIKCtrlSpaceInputConstraint.setMaintainOffset(True)
        self.armIKCtrlSpaceInputConstraint.addConstrainer(self.globalSRTInputTgt)
        self.armIKCtrlSpace.addConstraint(self.armIKCtrlSpaceInputConstraint)

        self.armUpVCtrlSpaceInputConstraint = PoseConstraint('_'.join([self.armUpVCtrlSpace.getName(), 'To', self.globalSRTInputTgt.getName()]))
        self.armUpVCtrlSpaceInputConstraint.setMaintainOffset(True)
        self.armUpVCtrlSpaceInputConstraint.addConstrainer(self.globalSRTInputTgt)
        self.armUpVCtrlSpace.addConstraint(self.armUpVCtrlSpaceInputConstraint)

        self.armRootInputConstraint = PoseConstraint('_'.join([self.bicepFKCtrlSpace.getName(), 'To', self.spineEndInputTgt.getName()]))
        self.armRootInputConstraint.setMaintainOffset(True)
        self.armRootInputConstraint.addConstrainer(self.spineEndInputTgt)
        self.bicepFKCtrlSpace.addConstraint(self.armRootInputConstraint)

        self.ikPosInputConstraint = PoseConstraint('_'.join([self.ikRootPosition.getName(), 'To', self.spineEndInputTgt.getName()]))
        self.ikPosInputConstraint.setMaintainOffset(True)
        self.ikPosInputConstraint.addConstrainer(self.spineEndInputTgt)
        self.ikRootPosition.addConstraint(self.ikPosInputConstraint)

        self.clavicleRefPosInputConstraint = PoseConstraint('_'.join([self.clavicleRefPosition.getName(), 'To', self.spineEndInputTgt.getName()]))
        self.clavicleRefPosInputConstraint.setMaintainOffset(True)
        self.clavicleRefPosInputConstraint.addConstrainer(self.spineEndInputTgt)
        self.clavicleRefPosition.addConstraint(self.clavicleRefPosInputConstraint)

        self.elbowRefPosInputConstraint = PoseConstraint('_'.join([self.elbowRefPosition.getName(), 'To', self.spineEndInputTgt.getName()]))
        self.elbowRefPosInputConstraint.setMaintainOffset(True)
        self.elbowRefPosInputConstraint.addConstrainer(self.spineEndInputTgt)
        self.elbowRefPosition.addConstraint(self.elbowRefPosInputConstraint)

        self.forearmFKRefPositioConstraint = PositionConstraint('_'.join([self.forearmFKCtrlSpace.getName(), 'To', self.ikRoot2ndPosition.getName()]))
        self.forearmFKRefPositioConstraint .setMaintainOffset(True)
        self.forearmFKRefPositioConstraint .addConstrainer(self.ikRoot2ndPosition)
        self.forearmFKCtrlSpace.addConstraint(self.forearmFKRefPositioConstraint)

        # Constraint outputs
        self.clavicleConstraint = PoseConstraint('_'.join([self.clavicleOutputTgt.getName(), 'To', self.clavicleCtrl.getName()]))
        self.clavicleConstraint.addConstrainer(self.clavicleCtrl)
        self.clavicleOutputTgt.addConstraint(self.clavicleConstraint)

        self.clavicleEndConstraint = PoseConstraint('_'.join([self.clavicleEndOutputTgt.getName(), 'To', self.clavicleCtrl.getName()]))
        self.clavicleEndConstraint.setMaintainOffset(True)
        self.clavicleEndConstraint.addConstrainer(self.clavicleCtrl)
        self.clavicleEndOutputTgt.addConstraint(self.clavicleEndConstraint)

        # ===============
        # Add Splice Ops
        # ===============

        # ARM -----------------------------------------------------------------------------------
        # Add Splice Op Step1
        self.armSolverStep1KLOperator = KLOperator('armStep1KLOp', 'GswShoulderArmSolverStep1', 'GSW_Kraken')
        self.addOperator(self.armSolverStep1KLOperator)

        # Add Att Inputs
        self.armSolverStep1KLOperator.setInput('drawDebug', self.drawDebugInputAttr)
        self.armSolverStep1KLOperator.setInput('rigScale', self.rigScaleInputAttr)

        self.armSolverStep1KLOperator.setInput('bone0Len', self.armBone0LenInputAttr)
        self.armSolverStep1KLOperator.setInput('bone1Len', self.armBone1LenInputAttr)
        self.armSolverStep1KLOperator.setInput('ikblend', self.armIKBlendInputAttr)
        self.armSolverStep1KLOperator.setInput('rightSide', self.rightSideInputAttr)

        # Add Xfo Inputs
        self.armSolverStep1KLOperator.setInput('refParentComp', self.spineEndInputTgt)
        self.armSolverStep1KLOperator.setInput('root', self.ikRootPosition)
        self.armSolverStep1KLOperator.setInput('bone0FK', self.bicepFKCtrl)
        self.armSolverStep1KLOperator.setInput('ikHandle', self.armIKCtrl)
        self.armSolverStep1KLOperator.setInput('upV', self.armUpVCtrl)

        # Add Xfo Outputs
        self.armSolverStep1KLOperator.setOutput('midJointOut', self.elbow1stPositionCtrlSpace)

        # Add Splice Op Step2
        self.armSolverStep2KLOperator = KLOperator('armStep2KLOp', 'GswShoulderArmSolverStep2', 'GSW_Kraken')
        self.addOperator(self.armSolverStep2KLOperator)

        # Add Att Inputs
        self.armSolverStep2KLOperator.setInput('drawDebug', self.drawDebugInputAttr)
        self.armSolverStep2KLOperator.setInput('rigScale', self.rigScaleInputAttr)
        self.armSolverStep2KLOperator.setInput('rightSide', self.rightSideInputAttr)
        self.armSolverStep2KLOperator.setInput('bone0Len', self.armBone0LenInputAttr)

        self.armSolverStep2KLOperator.setInput('modifier', self.modifierInputAttr)
        self.armSolverStep2KLOperator.setInput('upRate', self.upRateInputAttr)
        self.armSolverStep2KLOperator.setInput('downRate', self.downRateInputAttr)
        self.armSolverStep2KLOperator.setInput('forwardRate', self.forwardRateInputAttr)
        self.armSolverStep2KLOperator.setInput('backwardRate', self.backwardRateInputAttr)

        # Add Xfo Inputs
        self.armSolverStep2KLOperator.setInput('clavicleRoot', self.clavicleRefPosition)
        self.armSolverStep2KLOperator.setInput('elbowRefPosition', self.ikRootPosition)
        self.armSolverStep2KLOperator.setInput('elbow1stPosition', self.elbow1stPosition)

        # Add Xfo Outputs
        self.armSolverStep2KLOperator.setOutput('clavicleOut', self.clavicleCtrlSpace)

        # Add Splice Op Step3
        self.armSolverStep3KLOperator = KLOperator('armStep3KLOp', 'GswShoulderArmSolverStep3', 'GSW_Kraken')
        self.addOperator(self.armSolverStep3KLOperator)

        # Add Att Inputs
        self.armSolverStep3KLOperator.setInput('drawDebug', self.drawDebugInputAttr)
        self.armSolverStep3KLOperator.setInput('rigScale', self.rigScaleInputAttr)

        self.armSolverStep3KLOperator.setInput('bone0Len', self.armBone0LenInputAttr)
        self.armSolverStep3KLOperator.setInput('bone1Len', self.armBone1LenInputAttr)
        self.armSolverStep3KLOperator.setInput('ikblend', self.armIKBlendInputAttr)
        self.armSolverStep3KLOperator.setInput('rightSide', self.rightSideInputAttr)

        # Add Xfo Inputs
        self.armSolverStep3KLOperator.setInput('refParentComp', self.spineEndInputTgt)
        self.armSolverStep3KLOperator.setInput('root1st', self.ikRootPosition)
        self.armSolverStep3KLOperator.setInput('root2nd', self.ikRoot2ndPosition)
        self.armSolverStep3KLOperator.setInput('bone0FK', self.bicepFKCtrl)
        self.armSolverStep3KLOperator.setInput('bone1FK', self.forearmFKCtrl)
        self.armSolverStep3KLOperator.setInput('ikHandle', self.armIKCtrl)
        self.armSolverStep3KLOperator.setInput('upV', self.armUpVCtrl)

        # Add Xfo Outputs
        self.armSolverStep3KLOperator.setOutput('bone0Out', self.bicepOutputTgt)
        self.armSolverStep3KLOperator.setOutput('bone1Out', self.forearmOutputTgt)
        self.armSolverStep3KLOperator.setOutput('bone2Out', self.wristOutputTgt)
        self.armSolverStep3KLOperator.setOutput('midJointOut', self.elbowOutputTgt)

        # Add Deformer Splice Op
        self.outputsToDeformersKLOp = KLOperator('armDeformerKLOp', 'MultiPoseConstraintSolver', 'Kraken')
        self.addOperator(self.outputsToDeformersKLOp)

        # Add Att Inputs
        self.outputsToDeformersKLOp.setInput('drawDebug', self.drawDebugInputAttr)
        self.outputsToDeformersKLOp.setInput('rigScale', self.rigScaleInputAttr)

        # Add Xfo Inputs
        self.outputsToDeformersKLOp.setInput(
            'constrainers',
            [
                self.clavicleOutputTgt,
                self.bicepOutputTgt,
                self.elbowOutputTgt,
                self.forearmOutputTgt,
                self.wristOutputTgt
            ])

        # Add Xfo Outputs
        self.outputsToDeformersKLOp.setOutput(
            'constrainees',
            [
                self.clavicleDef,
                self.bicepDef,
                self.elbowDef,
                self.forearmDef,
                self.wristDef
            ])

        Profiler.getInstance().pop()

    def loadData(self, data=None):
        """Load a saved guide representation from persisted data.

        Arguments:
        data -- object, The JSON data object.

        Return:
        True if successful.

        """

        super(GswShoulderArmComponentRig, self).loadData(data)

        self.rightSideInputAttr.setValue(self.getLocation() is 'R')
        clavicleXfo = data.get('clavicleXfo')
        clavicleLen = data.get('clavicleLen')

        clavicleLenVec = Vec3(clavicleLen, 0.75, 0.75)

        self.clavicleCtrlSpace.xfo = clavicleXfo
        self.clavicleCtrl.xfo = clavicleXfo
        self.clavicleCtrl.scalePoints(clavicleLenVec)
        self.clavicleRefPosition.xfo = clavicleXfo

        if data['location'] == "R":
            self.clavicleCtrl.translatePoints(Vec3(0.0, 0.0, -1.0))
        else:
            self.clavicleCtrl.translatePoints(Vec3(0.0, 0.0, 1.0))

        # Set IO Xfos
        self.spineEndInputTgt.xfo = clavicleXfo
        self.clavicleEndOutputTgt.xfo = clavicleXfo
        self.clavicleEndOutputTgt.xfo.tr = clavicleXfo.transformVector(Vec3(clavicleLen, 0.0, 0.0))
        self.clavicleOutputTgt.xfo = clavicleXfo

        # Eval Constraints
        self.elbowRefPosInputConstraint.evaluate()
        self.clavicleConstraint.evaluate()
        self.clavicleEndConstraint.evaluate()

        bicepXfo = data.get('bicepXfo')
        forearmXfo = data.get('forearmXfo')
        wristXfo = data.get('wristXfo')
        upVXfo = data.get('upVXfo')
        bicepLen = data.get('bicepLen')
        forearmLen = data.get('forearmLen')
        bicepFKCtrlSize = data.get('bicepFKCtrlSize')
        forearmFKCtrlSize = data.get('forearmFKCtrlSize')

        self.cogInputTgt.xfo.tr = bicepXfo.tr

        self.bicepFKCtrlSpace.xfo = bicepXfo
        self.bicepFKCtrl.xfo = bicepXfo
        self.bicepFKCtrl.scalePoints(Vec3(bicepLen * 0.95, bicepFKCtrlSize, bicepFKCtrlSize * 0.1))

        self.forearmFKCtrlSpace.xfo = forearmXfo
        self.forearmFKCtrl.xfo = forearmXfo
        self.forearmFKCtrl.scalePoints(Vec3(forearmLen * 0.95, forearmFKCtrlSize, forearmFKCtrlSize * 0.1))

        self.ikRootPosition.xfo = bicepXfo
        self.elbow1stPositionCtrlSpace.xfo = forearmXfo
        self.elbow1stPosition.xfo = forearmXfo
        self.elbowRefPosition.xfo = forearmXfo
        self.ikRoot2ndPosition.xfo = bicepXfo

        self.armIKCtrlSpace.xfo.tr = wristXfo.tr
        self.armIKCtrl.xfo.tr = wristXfo.tr

        if self.getLocation() == "R":
            self.armIKCtrl.rotatePoints(0, 90, 0)
            self.clavicleCtrl.scalePoints(Vec3(-1, 1, 1))
            self.bicepFKCtrl.scalePoints(Vec3(-1, 1, 1))
            self.forearmFKCtrl.scalePoints(Vec3(-1, 1, 1))
        else:
            self.armIKCtrl.rotatePoints(0, -90, 0)

        self.armUpVCtrlSpace.xfo.tr = upVXfo.tr
        self.armUpVCtrl.xfo.tr = upVXfo.tr

        self.armBone0LenInputAttr.setMin(0.0)
        self.armBone0LenInputAttr.setMax(bicepLen * 3.0)
        self.armBone0LenInputAttr.setValue(bicepLen)
        self.armBone1LenInputAttr.setMin(0.0)
        self.armBone1LenInputAttr.setMax(forearmLen * 3.0)
        self.armBone1LenInputAttr.setValue(forearmLen)

        self.modifierInputAttr.setValue(data.get('modifier'))
        self.upRateInputAttr.setValue(data.get('upRate'))
        self.downRateInputAttr.setValue(data.get('downRate'))
        self.forwardRateInputAttr.setValue(data.get('forwardRate'))
        self.backwardRateInputAttr.setValue(data.get('backwardRate'))

        # Outputs
        self.bicepOutputTgt.xfo = bicepXfo
        self.forearmOutputTgt.xfo = forearmXfo
        self.wristOutputTgt.xfo = wristXfo

        # Eval Constraints
        self.ikPosInputConstraint.evaluate()
        self.armIKCtrlSpaceInputConstraint.evaluate()
        self.armUpVCtrlSpaceInputConstraint.evaluate()
        self.armRootInputConstraint.evaluate()
        self.armRootInputConstraint.evaluate()

        # Eval Operators
        self.armSolverStep1KLOperator.evaluate()
        self.outputsToDeformersKLOp.evaluate()


from kraken.core.kraken_system import KrakenSystem
ks = KrakenSystem.getInstance()
ks.registerComponent(GswShoulderArmComponentGuide)
ks.registerComponent(GswShoulderArmComponentRig)
