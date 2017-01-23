from kraken.core.maths import Vec3, Xfo
from kraken.core.maths.rotation_order import RotationOrder
from kraken.core.maths.constants import ROT_ORDER_STR_TO_INT_MAP

from kraken.core.objects.components.base_example_component import BaseExampleComponent
from kraken.core.objects.attributes.attribute_group import AttributeGroup
from kraken.core.objects.attributes.scalar_attribute import ScalarAttribute
from kraken.core.objects.control import Control
from kraken.core.objects.operators.kl_operator import KLOperator

from kraken.core.profiler import Profiler

from kraken.core.configs.config import Config

import kraken_components.gsw.gsw_icon as icon


class GswMainComponent(BaseExampleComponent):

    """Main Component Base"""

    def __init__(self, name="main", parent=None, data=None):
        super(GswMainComponent, self).__init__(name, parent)

        # ===========
        # Declare IO
        # ===========
        # Declare Inputs Xfos

        # Declare Output Xfos
        self.globalOutputTgt = self.createOutput('global', dataType='Xfo', parent=self.outputHrcGrp).getTarget()
        self.localOutputTgt = self.createOutput('local', dataType='Xfo', parent=self.outputHrcGrp).getTarget()
        self.cogOutputTgt = self.createOutput('cog', dataType='Xfo', parent=self.outputHrcGrp).getTarget()

        # Declare Input Attrs
        self.drawDebugInputAttr = self.createInput('drawDebug', dataType='Boolean', value=False, parent=self.cmpInputAttrGrp).getTarget()

        # Declare Output Attrs
        self.rigScaleOutputAttr = self.createOutput('rigScale', dataType='Float', value=1.0, parent=self.cmpOutputAttrGrp).getTarget()


class GswMainComponentGuide(GswMainComponent):

    """Main Component Guide"""

    def __init__(self, name="main", parent=None):

        Profiler.getInstance().push("Construct Main Guide Component:" + name)
        super(GswMainComponentGuide, self).__init__(name, parent)

        # =========
        # Attributes
        # =========
        guideSettingsAttrGrp = AttributeGroup("GuideSettings", parent=self)
        self.mainSrtSizeInputAttr = ScalarAttribute('mainSrtSize', value=5.0, minValue=1.0, maxValue=50.0, parent=guideSettingsAttrGrp)

        # =========
        # Controls
        # =========

        # Guide Controls
        self.mainSrtCtrl = Control('global', shape='circle', parent=self.ctrlCmpGrp)

        self.cogCtrl = Control('cogPosition', parent=self.ctrlCmpGrp, shape="square")
        self.cogCtrl.scalePoints(Vec3(2, 2, 2))
        self.cogCtrl.setColor('red')

        self.init_data = {
            "mainSrtXfo": Xfo(tr=Vec3(0.0, 0.0, 0.0)),
            "cogPosition": Vec3(0.0, 8.7, 0.0),
        }

        self.loadData(self.init_data)

        Profiler.getInstance().pop()

    # =============
    # Data Methods
    # =============
    def saveData(self):
        """Save the data for the component to be persisted.

        Return:
        The JSON data object

        """
        data = dict(self.init_data)
        data.update(super(GswMainComponentGuide, self).saveData())

        data["mainSrtXfo"] = self.mainSrtCtrl.xfo
        data["mainSrtSize"] = self.mainSrtSizeInputAttr.getValue()
        data['cogPosition'] = self.cogCtrl.xfo.tr

        return data

    def loadData(self, data):
        """Load a saved guide representation from persisted data.

        Arguments:
        data -- object, The JSON data object.

        Return:
        True if successful.

        """

        # Reset all shapes, but really we should just recreate all controls from loadData instead of init
        for ctrl in self.getHierarchyNodes(classType="Control"):
            ctrl.setShape(ctrl.getShape())

        # saveData() will grab the guide settings values (and are not stored in data arg)
        existing_data = self.saveData()
        existing_data.update(data)
        data = existing_data

        super(GswMainComponentGuide, self).loadData(data)

        self.mainSrtCtrl.xfo = data["mainSrtXfo"]
        self.mainSrtCtrl.scalePoints(Vec3(data["mainSrtSize"], 1.0, data["mainSrtSize"]))

        self.cogCtrl.xfo.tr = data["cogPosition"]

        # self.cogCtrl.scalePoints(Vec3(data["globalComponentCtrlSize"], 1.0, data["globalComponentCtrlSize"]))

        return True

    def getRigBuildData(self):
        """Returns the Guide data used by the Rig Component to define the layout of the final rig.

        Return:
        The JSON rig data object.

        """
        data = super(GswMainComponentGuide, self).getRigBuildData()

        data["mainSrtXfo"] = self.mainSrtCtrl.xfo
        data['cogPosition'] = self.cogCtrl.xfo.tr

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

        return GswMainComponentRig


class GswMainComponentRig(GswMainComponent):

    """Main Component Rig"""

    def __init__(self, name="main", parent=None):

        Profiler.getInstance().push("Construct Main Rig Component:" + name)
        super(GswMainComponentRig, self).__init__(name, parent)

        # =========
        # Controls
        # =========
        # Add Controls
        self.mainSrtCtrl = Control('global', parent=self.ctrlCmpGrp)
        self.mainSrtCtrl.setCurveData(icon.arrows_side3)
        self.mainSrtCtrl.ro = RotationOrder(ROT_ORDER_STR_TO_INT_MAP["ZXY"])  # Set with component settings later
        self.mainSrtCtrl.setColor("blueLightMuted")
        self.mainSrtCtrl.scalePoints(Vec3(3.5, 3.5, 3.5))
        self.mainSrtCtrl.lockScale(x=True, y=True, z=True)
        self.mainSrtCtrlSpace = self.mainSrtCtrl.insertCtrlSpace()

        self.localCtrl = Control('local', parent=self.mainSrtCtrl)
        self.localCtrl.setCurveData(icon.arrows_side3)
        self.localCtrl.ro = RotationOrder(ROT_ORDER_STR_TO_INT_MAP["ZXY"])  # Set with component settings later
        self.localCtrl.setColor("blueDark")
        self.localCtrl.scalePoints(Vec3(2.5, 2.5, 2.5))
        self.localCtrl.lockScale(x=True, y=True, z=True)
        self.localCtrlSpace = self.localCtrl.insertCtrlSpace()

        # COG
        self.cogCtrl = Control('cog', parent=self.localCtrl)
        self.cogCtrl.setCurveData(icon.home_plate)
        self.cogCtrl.ro = RotationOrder(ROT_ORDER_STR_TO_INT_MAP["ZXY"])  # Set with component settings later
        self.cogCtrl.scalePoints(Vec3(8.0, 8.0, 5.5))
        self.cogCtrl.setColor("orange")
        self.cogCtrlSpace = self.cogCtrl.insertCtrlSpace()

        # Add Component Params to IK control
        MainSettingsAttrGrp = AttributeGroup('DisplayInfo_MainSettings', parent=self.mainSrtCtrl)
        self.rigScaleAttr = ScalarAttribute('rigScale', value=1.0, parent=MainSettingsAttrGrp, minValue=0.1, maxValue=100.0)

        self.rigScaleOutputAttr.connect(self.rigScaleAttr)

        # ==========
        # Deformers
        # ==========
        self.deformersLayer = self.getOrCreateLayer('deformers')
        self.deformersParent = self.deformersLayer

        # ==========
        # Deformers
        # ==========

        # ==============
        # Constrain I/O
        # ==============
        # Constraint inputs

        # Constraint outputs
        self.globalOutputTgtConstraint = self.globalOutputTgt.constrainTo(self.mainSrtCtrl)
        self.localOutputTgtConstraint = self.localOutputTgt.constrainTo(self.localCtrl)

        # ===============
        # Add Splice Ops
        # ===============
        # Add Rig Scale Splice Op
        self.rigScaleKLOp = KLOperator('rigScaleKLOp', 'RigScaleSolver', 'Kraken')
        self.addOperator(self.rigScaleKLOp)

        # Add Att Inputs
        self.rigScaleKLOp.setInput('drawDebug', self.drawDebugInputAttr)
        self.rigScaleKLOp.setInput('rigScale', self.rigScaleOutputAttr)

        # Add Xfo Inputs

        # Add Xfo Outputs
        self.rigScaleKLOp.setOutput('target', self.mainSrtCtrlSpace)

        Profiler.getInstance().pop()

    def loadData(self, data=None):
        """Load a saved guide representation from persisted data.

        Arguments:
            data -- object, The JSON data object.

        Return:
            True if successful.

        """

        super(GswMainComponentRig, self).loadData(data)

        # ================
        # Resize Controls
        # ================
        # self.mainSrtCtrl.scalePoints(Vec3(data["globalComponentCtrlSize"], 1.0, data["globalComponentCtrlSize"]))
        # self.localCtrl.scalePoints(Vec3(data["globalComponentCtrlSize"] * 0.6, 1.0, data["globalComponentCtrlSize"] * 0.6))  # fix this scale issue
        # self.cogCtrl.scalePoints(Vec3( data['globalComponentCtrlSize'],1.0, data['globalComponentCtrlSize']))

        # =======================
        # Set Control Transforms
        # =======================
        self.mainSrtCtrlSpace.xfo = data["mainSrtXfo"]
        self.mainSrtCtrl.xfo = data["mainSrtXfo"]
        self.localCtrlSpace.xfo = data["mainSrtXfo"]
        self.localCtrl.xfo = data["mainSrtXfo"]

        self.cogCtrlSpace.xfo.tr = data["cogPosition"]
        self.cogCtrl.xfo.tr = data["cogPosition"]

        # Constraint outputs
        self.cogOutputTgtConstraint = self.cogOutputTgt.constrainTo(self.cogCtrl)

        # Set all parents to rootDef since that is the only joint option
        # self.rootOutputTgt.parentJoint = self.rootDef
        # self.globalOutputTgt.parentJoint = self.rootDef
        # self.localOutputTgt.parentJoint = self.rootDef
        # self.cogOutputTgt.parentJoint = self.rootDef

        # ====================
        # Evaluate Fabric Ops
        # ====================
        # Eval Operators # Order is important
        self.evalOperators()

        self.globalOutputTgtConstraint.evaluate()
        self.localOutputTgtConstraint.evaluate()
        self.cogOutputTgtConstraint.evaluate()


from kraken.core.kraken_system import KrakenSystem
ks = KrakenSystem.getInstance()
ks.registerComponent(GswMainComponentGuide)
ks.registerComponent(GswMainComponentRig)
