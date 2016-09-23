"""Kraken Maya - Maya Builder module.

Classes:
Builder -- Component representation.

"""

import json
import logging

from kraken.log import getLogger

# from kraken.core.kraken_system import ks
from kraken.core.configs.config import Config

# from kraken.core.maths import Vec2, Vec3, Xfo, Mat44, Math_radToDeg, RotationOrder

from kraken.core.builder import Builder
# from kraken.core.objects.object_3d import Object3D
# from kraken.core.objects.attributes.attribute import Attribute

from kraken.plugins.maya_plugin.graph_manager import MayaGraphManager
from kraken.plugins.maya_plugin.abstract_object3d import AbstractBone, AbstractSkeleton
from kraken.plugins.maya_plugin.canvas_operator_builder import CanvasOperator

import pymel.core as pm
import pymel.core.datatypes as dt
import maya.cmds as cmds


logger = getLogger('kraken')
logger.setLevel(logging.INFO)


class Builder(Builder):

    """Builder object for building Kraken objects in Maya."""

    __rigGraph = None
    __controlGraph = None
    __attributeGraph = None

    __dfgCurves = None
    __dfgLastCurveNode = None
    __dfgLastLinesNode = None

    @property
    def rigGraph(self):
        return self.__rigGraph

    @property
    def controlGraph(self):
        return self.__controlGraph

    @property
    def attributeGraph(self):
        return self.__attributeGraph

    def __init__(self):
        super(Builder, self).__init__()

    def deleteBuildElements(self):
        """Clear out all dcc built elements from the scene if exist."""

        for builtElement in self._buildElements:
            if builtElement['src'].isTypeOf('Attribute'):
                continue

            node = builtElement['tgt']
            if node.exists():
                pm.delete(node)

        self._buildElements = []

        return

    # ========================
    # Object3D Build Methods
    # ========================
    def buildContainer(self, kSceneItem, buildName):
        """Builds a container / namespace object.

        Args:
            kSceneItem (Object): kSceneItem that represents a container to
                be built.
            buildName (str): The name to use on the built object.

        Returns:
            object: Node that is created.

        """

        parentNode = self.getDCCSceneItem(kSceneItem.getParent())

        dccSceneItem = pm.group(name="group", em=True)
        pm.parent(dccSceneItem, parentNode)
        pm.rename(dccSceneItem, buildName)

        if kSceneItem.isTypeOf('Rig'):
            krakenRigAttr = dccSceneItem.addAttr('krakenRig',
                                                 niceName='krakenRig',
                                                 attributeType="bool",
                                                 defaultValue=True,
                                                 keyable=False)

            dccSceneItem.attr('krakenRig').setLocked(True)

            # Put Rig Data on DCC Item
            metaData = kSceneItem.getMetaData()
            if 'guideData' in metaData:
                pureJSON = metaData['guideData']

                krakenRigDataAttr = dccSceneItem.addAttr('krakenRigData',
                                                         niceName='krakenRigData',
                                                         dataType="string",
                                                         keyable=False)

                dccSceneItem.attr('krakenRigData').set(json.dumps(pureJSON, indent=2))
                dccSceneItem.attr('krakenRigData').setLocked(True)

        self._registerSceneItemPair(kSceneItem, dccSceneItem)

        return dccSceneItem

    def buildLayer(self, kSceneItem, buildName):
        """Builds a layer object.

        Args:
            kSceneItem (Object): kSceneItem that represents a layer to
                be built.
            buildName (str): The name to use on the built object.

        Returns:
            object: Node that is created.

        """

        parentNode = self.getDCCSceneItem(kSceneItem.getParent())

        dccSceneItem = pm.group(name="group", em=True)
        pm.parent(dccSceneItem, parentNode)
        pm.rename(dccSceneItem, buildName)

        self._registerSceneItemPair(kSceneItem, dccSceneItem)

        return dccSceneItem

    def buildHierarchyGroup(self, kSceneItem, buildName):
        """Builds a hierarchy group object.

        Args:
            kSceneItem (Object): kSceneItem that represents a group to
                be built.
            buildName (str): The name to use on the built object.

        Return:
            object: DCC Scene Item that is created.

        """

        parentNode = self.getDCCSceneItem(kSceneItem.getParent())

        dccSceneItem = pm.group(name="group", em=True)
        pm.parent(dccSceneItem, parentNode)
        pm.rename(dccSceneItem, buildName)

        self._registerSceneItemPair(kSceneItem, dccSceneItem)

        return dccSceneItem

    def buildGroup(self, kSceneItem, buildName):
        """Builds a group object.

        Args:
            kSceneItem (Object): kSceneItem that represents a group to
                be built.
            buildName (str): The name to use on the built object.

        Returns:
            object: Node that is created.

        """

        parentNode = self.getDCCSceneItem(kSceneItem.getParent())

        dccSceneItem = pm.group(name="group", em=True)
        pm.parent(dccSceneItem, parentNode)
        pm.rename(dccSceneItem, buildName)

        self._registerSceneItemPair(kSceneItem, dccSceneItem)

        return dccSceneItem

    def buildJoint(self, kSceneItem, buildName):
        """Builds a joint object.

        Args:
            kSceneItem (Object): kSceneItem that represents a joint to
                be built.
            buildName (str): The name to use on the built object.

        Return:
            object: DCC Scene Item that is created.

        """

        parentNode = self.getDCCSceneItem(kSceneItem.getParent())

        pm.select(parentNode)
        dccSceneItem = pm.joint(name="joint")
        pm.rename(dccSceneItem, buildName)

        radius = dccSceneItem.attr('radius').set(kSceneItem.getRadius())

        self._registerSceneItemPair(kSceneItem, dccSceneItem)

        return dccSceneItem

    def buildLocator(self, kSceneItem, buildName):
        """Builds a locator / null object.

        Args:
            kSceneItem (Object): locator / null object to be built.
            buildName (str): The name to use on the built object.

        Returns:
            object: Node that is created.

        """

        parentNode = self.getDCCSceneItem(kSceneItem.getParent())

        dccSceneItem = pm.spaceLocator(name="locator")
        pm.parent(dccSceneItem, parentNode)
        pm.rename(dccSceneItem, buildName)

        self._registerSceneItemPair(kSceneItem, dccSceneItem)

        return dccSceneItem

    def buildCurve(self, kSceneItem, buildName):
        """Builds a Curve object.

        Args:
            kSceneItem (Object): kSceneItem that represents a curve to
                be built.
            buildName (str): The name to use on the built object.

        Returns:
            object: Node that is created.

        """

        parentNode = self.getDCCSceneItem(kSceneItem.getParent())

        # Format points for Maya
        curveData = kSceneItem.getCurveData()

        # Scale, rotate, translation shape
        curvePoints = []
        for eachSubCurve in curveData:
            formattedPoints = eachSubCurve["points"]
            curvePoints.append(formattedPoints)

        mainCurve = None
        for i, eachSubCurve in enumerate(curvePoints):
            closedSubCurve = curveData[i]["closed"]
            degreeSubCurve = curveData[i]["degree"]

            currentSubCurve = pm.curve(per=False,
                                       point=curvePoints[i],
                                       degree=degreeSubCurve)

            if closedSubCurve:
                pm.closeCurve(currentSubCurve,
                              preserveShape=True,
                              replaceOriginal=True)

            if mainCurve is None:
                mainCurve = currentSubCurve

            if i > 0:
                pm.parent(currentSubCurve.getShape(),
                          mainCurve,
                          relative=True,
                          shape=True)

                pm.delete(currentSubCurve)

        dccSceneItem = mainCurve
        pm.parent(dccSceneItem, parentNode)
        pm.rename(dccSceneItem, buildName)

        self._registerSceneItemPair(kSceneItem, dccSceneItem)

        return dccSceneItem

    def buildControl(self, kSceneItem, buildName):
        """Builds a Control object.

        Args:
            kSceneItem (Object): kSceneItem that represents a control to
                be built.
            buildName (str): The name to use on the built object.

        Returns:
            object: Node that is created.

        """

        parentNode = self.getDCCSceneItem(kSceneItem.getParent())

        # Format points for Maya
        curveData = kSceneItem.getCurveData()

        # Scale, rotate, translation shape
        curvePoints = []
        for eachSubCurve in curveData:
            formattedPoints = eachSubCurve["points"]
            curvePoints.append(formattedPoints)

        mainCurve = None
        for i, eachSubCurve in enumerate(curvePoints):
            closedSubCurve = curveData[i]["closed"]
            degreeSubCurve = curveData[i]["degree"]

            currentSubCurve = pm.curve(per=False,
                                       point=curvePoints[i],
                                       degree=degreeSubCurve)

            if closedSubCurve:
                pm.closeCurve(currentSubCurve,
                              preserveShape=True,
                              replaceOriginal=True)

            if mainCurve is None:
                mainCurve = currentSubCurve

            if i > 0:
                pm.parent(currentSubCurve.getShape(),
                          mainCurve,
                          relative=True,
                          shape=True)

                pm.delete(currentSubCurve)

        dccSceneItem = mainCurve
        pm.parent(dccSceneItem, parentNode)
        pm.rename(dccSceneItem, buildName)

        self._registerSceneItemPair(kSceneItem, dccSceneItem)

        return dccSceneItem

    def buildSkeleton(self, kSceneItem, buildName):
        """Builds a fabric engine Characters extesion's skeleton object.

        Args:
            kSceneItem (Object): locator / null object to be built.
            buildName (str): The name to use on the built object.

        Returns:
            object: Node that is created.

        """

        if not self._characterSkeleton:
            return

        dccSceneItem = AbstractBone(kSceneItem, buildName, self._characterSkeleton)
        self._registerSceneItemPair(kSceneItem, dccSceneItem)

        return dccSceneItem

    # ========================
    # Attribute Build Methods
    # ========================
    def buildBoolAttribute(self, kAttribute):
        """Builds a Bool attribute.

        Args:
            kAttribute (Object): kAttribute that represents a boolean
                attribute to be built.

        Return:
            bool: True if successful.

        """

        if kAttribute.getParent().getName() == 'implicitAttrGrp':
            return False

        parentDCCSceneItem = self.getDCCSceneItem(kAttribute.getParent().getParent())
        parentDCCSceneItem.addAttr(kAttribute.getName(),
                                   niceName=kAttribute.getName(),
                                   attributeType="bool",
                                   defaultValue=kAttribute.getValue(),
                                   keyable=True)

        dccSceneItem = parentDCCSceneItem.attr(kAttribute.getName())
        dccSceneItem.setLocked(kAttribute.getLock())
        self._registerSceneItemPair(kAttribute, dccSceneItem)

        return True

    def buildScalarAttribute(self, kAttribute):
        """Builds a Float attribute.

        Args:
            kAttribute (Object): kAttribute that represents a float attribute
                to be built.

        Return:
            bool: True if successful.

        """

        if kAttribute.getParent().getName() == 'implicitAttrGrp':
            return False

        parentDCCSceneItem = self.getDCCSceneItem(kAttribute.getParent().getParent())
        parentDCCSceneItem.addAttr(kAttribute.getName(),
                                   niceName=kAttribute.getName(),
                                   attributeType="float",
                                   defaultValue=kAttribute.getValue(),
                                   keyable=True)

        dccSceneItem = parentDCCSceneItem.attr(kAttribute.getName())

        if kAttribute.getMin() is not None:
            dccSceneItem.setMin(kAttribute.getMin())

        if kAttribute.getMax() is not None:
            dccSceneItem.setMax(kAttribute.getMax())

        if kAttribute.getUIMin() is not None:
            dccSceneItem.setSoftMin(kAttribute.getUIMin())

        if kAttribute.getUIMax() is not None:
            dccSceneItem.setSoftMax(kAttribute.getUIMax())

        dccSceneItem.setLocked(kAttribute.getLock())
        self._registerSceneItemPair(kAttribute, dccSceneItem)

        return True

    def buildIntegerAttribute(self, kAttribute):
        """Builds a Integer attribute.

        Args:
            kAttribute (Object): kAttribute that represents a integer attribute to be built.

        Return:
            bool: True if successful.

        """

        if kAttribute.getParent().getName() == 'implicitAttrGrp':
            return False

        mininum = kAttribute.getMin()
        if not mininum:
            mininum = 0

        maximum = kAttribute.getMax()
        if not maximum:
            maximum = kAttribute.getValue() * 2

        parentDCCSceneItem = self.getDCCSceneItem(kAttribute.getParent().getParent())
        parentDCCSceneItem.addAttr(kAttribute.getName(), niceName=kAttribute.getName(), attributeType="long", defaultValue=kAttribute.getValue(), minValue=mininum, maxValue=maximum, keyable=True)
        parentDCCSceneItem.attr(kAttribute.getName())
        dccSceneItem = parentDCCSceneItem.attr(kAttribute.getName())

        if kAttribute.getMin() is not None:
            dccSceneItem.setMin(kAttribute.getMin())

        if kAttribute.getMax() is not None:
            dccSceneItem.setMax(kAttribute.getMax())

        if kAttribute.getUIMin() is not None:
            dccSceneItem.setSoftMin(kAttribute.getUIMin())

        if kAttribute.getUIMax() is not None:
            dccSceneItem.setSoftMax(kAttribute.getUIMax())

        dccSceneItem.setLocked(kAttribute.getLock())
        self._registerSceneItemPair(kAttribute, dccSceneItem)

        return True

    def buildStringAttribute(self, kAttribute):
        """Builds a String attribute.

        Args:
            kAttribute (Object): kAttribute that represents a string attribute
                to be built.

        Return:
            bool: True if successful.

        """

        if kAttribute.getParent().getName() == 'implicitAttrGrp':
            return False

        parentDCCSceneItem = self.getDCCSceneItem(kAttribute.getParent().getParent())
        parentDCCSceneItem.addAttr(kAttribute.getName(),
                                   niceName=kAttribute.getName(),
                                   dataType="string")

        dccSceneItem = parentDCCSceneItem.attr(kAttribute.getName())
        dccSceneItem.set(kAttribute.getValue())
        dccSceneItem.setLocked(kAttribute.getLock())
        self._registerSceneItemPair(kAttribute, dccSceneItem)

        return True

    def buildAttributeGroup(self, kAttributeGroup):
        """Builds attribute groups on the DCC object.

        Args:
            kAttributeGroup (object): Kraken object to build the attribute
                group on.

        Return:
            bool: True if successful.

        """

        parentDCCSceneItem = self.getDCCSceneItem(kAttributeGroup.getParent())

        groupName = kAttributeGroup.getName()
        if groupName == "implicitAttrGrp":
            return False

        parentDCCSceneItem.addAttr(groupName,
                                   niceName=groupName,
                                   attributeType="enum",
                                   enumName="-----",
                                   keyable=True)

        dccSceneItem = parentDCCSceneItem.attr(groupName)
        pm.setAttr(parentDCCSceneItem + "." + groupName, lock=True)

        self._registerSceneItemPair(kAttributeGroup, dccSceneItem)

        return True

    def connectAttribute(self, kAttribute):
        """Connects the driver attribute to this one.

        Args:
            kAttribute (Object): Attribute to connect.

        Return:
            bool: True if successful.

        """

        if kAttribute.isConnected() is True:

            # Detect if driver is visibility attribute and map to correct DCC
            # attribute
            driverAttr = kAttribute.getConnection()
            if driverAttr.getName() == 'visibility' and driverAttr.getParent().getName() == 'implicitAttrGrp':
                dccItem = self.getDCCSceneItem(driverAttr.getParent().getParent())
                driver = dccItem.attr('visibility')

            elif driverAttr.getName() == 'shapeVisibility' and driverAttr.getParent().getName() == 'implicitAttrGrp':
                dccItem = self.getDCCSceneItem(driverAttr.getParent().getParent())
                shape = dccItem.getShape()
                driver = shape.attr('visibility')

            else:
                driver = self.getDCCSceneItem(kAttribute.getConnection())

            # Detect if the driven attribute is a visibility attribute and map
            # to correct DCC attribute
            if kAttribute.getName() == 'visibility' and kAttribute.getParent().getName() == 'implicitAttrGrp':
                dccItem = self.getDCCSceneItem(kAttribute.getParent().getParent())
                driven = dccItem.attr('visibility')

            elif kAttribute.getName() == 'shapeVisibility' and kAttribute.getParent().getName() == 'implicitAttrGrp':
                dccItem = self.getDCCSceneItem(kAttribute.getParent().getParent())
                shape = dccItem.getShape()
                driven = shape.attr('visibility')
            else:
                driven = self.getDCCSceneItem(kAttribute)

            pm.connectAttr(driver, driven, force=True)

        return True

    # =========================
    # Constraint Build Methods
    # =========================
    def buildOrientationConstraint(self, kConstraint, buildName):
        """Builds an orientation constraint represented by the kConstraint.

        Args:
            kConstraint (Object): Kraken constraint object to build.

        Return:
            object: dccSceneItem that was created.

        """

        constraineeDCCSceneItem = self.getDCCSceneItem(kConstraint.getConstrainee())
        dccSceneItem = pm.orientConstraint(
            [self.getDCCSceneItem(x) for x in kConstraint.getConstrainers()],
            constraineeDCCSceneItem,
            name=kConstraint.getName() + "_ori_cns",
            maintainOffset=kConstraint.getMaintainOffset())

        if kConstraint.getMaintainOffset() is True:

            # Maya's rotation order enums:
            # 0 XYZ
            # 1 YZX
            # 2 ZXY
            # 3 XZY
            # 4 YXZ <-- 5 in Fabric
            # 5 ZYX <-- 4 in Fabric
            order = kConstraint.getConstrainee().ro.order
            if order == 4:
                order = 5
            elif order == 5:
                order = 4

            offsetXfo = kConstraint.computeOffset()
            offsetAngles = offsetXfo.ori.toEulerAnglesWithRotOrder(
                RotationOrder(order))

            dccSceneItem.attr('offset').set([offsetAngles.x,
                                             offsetAngles.y,
                                             offsetAngles.z])

        pm.rename(dccSceneItem, buildName)

        self._registerSceneItemPair(kConstraint, dccSceneItem)

        return dccSceneItem

    def buildPoseConstraint(self, kConstraint, buildName):
        """Builds an pose constraint represented by the kConstraint.

        Args:
            kConstraint (Object): kraken constraint object to build.

        Return:
            bool: True if successful.

        """
        pass

    def buildNodeConstraint(self, kConstraint, buildName):
        pass

    def buildDccPoseConstraint(self, kConstraint, buildName):
        constraineeDCCSceneItem = self.getDCCSceneItem(kConstraint.getConstrainee())
        dccSceneItem = pm.parentConstraint(
            [self.getDCCSceneItem(x) for x in kConstraint.getConstrainers()],
            constraineeDCCSceneItem,
            name=buildName,
            maintainOffset=kConstraint.getMaintainOffset())

        # We need this block of code to replace the pose constraint name with
        # the scale constraint name since we don't have a single pos, rot, scl,
        # constraint in Maya.
        config = Config.getInstance()
        nameTemplate = config.getNameTemplate()
        poseCnsName = nameTemplate['types']['PoseConstraint']
        sclCnsName = nameTemplate['types']['ScaleConstraint']

        scaleConstraint = pm.scaleConstraint(
            [self.getDCCSceneItem(x) for x in kConstraint.getConstrainers()],
            constraineeDCCSceneItem,
            name=buildName.replace(poseCnsName, sclCnsName),
            maintainOffset=kConstraint.getMaintainOffset())

        if kConstraint.getMaintainOffset() is True:

            # Fabric's rotation order enums:
            # We need to use the negative rotation order
            # to calculate propery offset values.
            #
            # 0 XYZ
            # 1 YZX
            # 2 ZXY
            # 3 XZY
            # 4 ZYX
            # 5 YXZ

            rotOrderRemap = {
                0: 4,
                1: 3,
                2: 5,
                3: 1,
                4: 0,
                5: 2
            }

            order = rotOrderRemap[kConstraint.getConstrainee().ro.order]
            # if order == 4:
            #     order = 5
            # elif order == 5:
            #     order = 4

            offsetXfo = kConstraint.computeOffset()
            offsetAngles = offsetXfo.ori.toEulerAnglesWithRotOrder(
                RotationOrder(order))

            # Set offsets on parent constraint
            dccSceneItem.target[0].targetOffsetTranslate.set([offsetXfo.tr.x,
                                                              offsetXfo.tr.y,
                                                              offsetXfo.tr.z])

            dccSceneItem.target[0].targetOffsetRotate.set(
                [Math_radToDeg(offsetAngles.x),
                 Math_radToDeg(offsetAngles.y),
                 Math_radToDeg(offsetAngles.z)])

            # Set offsets on the scale constraint
            scaleConstraint.offset.set([offsetXfo.sc.x,
                                        offsetXfo.sc.y,
                                        offsetXfo.sc.z])

        self._registerSceneItemPair(kConstraint, dccSceneItem)

        return dccSceneItem

    def buildPositionConstraint(self, kConstraint, buildName):
        """Builds an position constraint represented by the kConstraint.

        Args:
            kConstraint (Object): Kraken constraint object to build.

        Return:
            bool: True if successful.

        """

        pass

    def buildNodePositionConstraint(self, kConstraint, buildName):
        pass

    def buildDccPositionConstraint(self, kConstraint, buildName):
        constraineeDCCSceneItem = self.getDCCSceneItem(kConstraint.getConstrainee())
        dccSceneItem = pm.pointConstraint(
            [self.getDCCSceneItem(x) for x in kConstraint.getConstrainers()],
            constraineeDCCSceneItem,
            name=buildName,
            maintainOffset=kConstraint.getMaintainOffset())

        if kConstraint.getMaintainOffset() is True:
            offsetXfo = kConstraint.computeOffset()

            # Set offsets on the scale constraint
            dccSceneItem.offset.set([offsetXfo.tr.x,
                                     offsetXfo.tr.y,
                                     offsetXfo.tr.z])

        self._registerSceneItemPair(kConstraint, dccSceneItem)

        return dccSceneItem

    def buildScaleConstraint(self, kConstraint, buildName):
        """Builds an scale constraint represented by the kConstraint.

        Args:
            kConstraint (Object): Kraken constraint object to build.

        Return:
            bool: True if successful.

        """

        constraineeDCCSceneItem = self.getDCCSceneItem(kConstraint.getConstrainee())
        dccSceneItem = pm.scaleConstraint(
            [self.getDCCSceneItem(x) for x in kConstraint.getConstrainers()],
            constraineeDCCSceneItem,
            name=buildName,
            maintainOffset=kConstraint.getMaintainOffset())

        if kConstraint.getMaintainOffset() is True:
            offsetXfo = kConstraint.computeOffset()

            # Set offsets on the scale constraint
            dccSceneItem.offset.set([offsetXfo.sc.x,
                                     offsetXfo.sc.y,
                                     offsetXfo.sc.z])

        self._registerSceneItemPair(kConstraint, dccSceneItem)

        return dccSceneItem

    # ========================
    # Component Build Methods
    # ========================
    def buildAttributeConnection(self, connectionInput):
        """Builds the connection between the attribute and the connection.

        Args:
            connectionInput (Object): Kraken connection to build.

        Return:
            bool: True if successful.

        """

        if connectionInput.isConnected() is False:
            return False

        connection = connectionInput.getConnection()
        connectionTarget = connection.getTarget()
        inputTarget = connectionInput.getTarget()

        if connection.getDataType().endswith('[]'):
            connectionTarget = connection.getTarget()[connectionInput.getIndex()]
        else:
            connectionTarget = connection.getTarget()

        connectionTargetDCCSceneItem = self.getDCCSceneItem(connectionTarget)
        targetDCCSceneItem = self.getDCCSceneItem(inputTarget)

        pm.connectAttr(connectionTargetDCCSceneItem,
                       targetDCCSceneItem,
                       force=True)

        return True

    # =========================
    # Operator Builder Methods
    # =========================
    def buildKLOperator(self, kOperator, buildName):
        """Builds KL Operators on the components.

        Args:
            kOperator (Object): Kraken operator that represents a KL
                operator.
            buildName (str): The name to use on the built object.

        Return:
            bool: True if successful.

        """

        # Code to build KL and Canvas based Operators has been merged.
        # It's important to note here that the 'isKLBased' argument is set
        # to true.
        self.buildCanvasOperator(kOperator, buildName, isKLBased=True)

        return True

    def buildCanvasOperator(self, kOperator, buildName, isKLBased=False):
        """Builds Canvas Operators on the components.

        Args:
            kOperator (object): Kraken operator that represents a Canvas
                operator.
            buildName (str): The name to use on the built object.
            isKLBased (bool): Whether the solver is based on a KL object.

        Return:
            bool: True if successful.

        """

        op = CanvasOperator(self, kOperator, buildName, self.rigGraph, isKLBased)
        return op

    def buildSkeletonContainer(self, buildName):

        self._characterSkeleton = AbstractSkeleton(buildName, self.rigGraph)

    def buildCanvasContainer(self, buildName):

        # Create Canvas Operator

        # config = Config.getInstance()
        # nameTemplate = config.getNameTemplate()

        self.__rigGraph = MayaGraphManager(buildName)
        self.rigGraph.setTitle('Rig')
        self.rigGraph.addExtDep('Kraken')
        self.rigGraph.setNodeAndPort('', '', 'drawDebug')

        self.solverContainer = self.rigGraph.createGraphNode("", "Solvers")

        drawDebugPort = pm.FabricCanvasAddPort(mayaNode=self.rigGraph.nodeName,
                                               execPath="",
                                               desiredPortName="drawDebug",
                                               portType="In",
                                               typeSpec="Boolean",
                                               connectToPortPath="")

        rigScalePort = pm.FabricCanvasAddPort(mayaNode=self.rigGraph.nodeName,
                                              execPath="",
                                              desiredPortName="rigScale",
                                              portType="In",
                                              typeSpec="Float32",
                                              connectToPortPath="")


    def buildConstraintContainer(self, buildName):

        self.constraintContainer = self.rigGraph.createGraphNode("", "Constraints")

    # ==================
    # Parameter Methods
    # ==================
    def lockParameters(self, kSceneItem):
        """Locks flagged SRT parameters.

        Args:
            kSceneItem (Object): Kraken object to lock the SRT parameters on.

        Return:
            bool: True if successful.

        """

        dccSceneItem = self.getDCCSceneItem(kSceneItem)

        # Lock Rotation
        if kSceneItem.testFlag("lockXRotation") is True:
            pm.setAttr(
                dccSceneItem.longName() + "." + 'rx',
                lock=True,
                keyable=False,
                channelBox=False)

        if kSceneItem.testFlag("lockYRotation") is True:
            pm.setAttr(
                dccSceneItem.longName() + "." + 'ry',
                lock=True,
                keyable=False,
                channelBox=False)

        if kSceneItem.testFlag("lockZRotation") is True:
            pm.setAttr(
                dccSceneItem.longName() + "." + 'rz',
                lock=True,
                keyable=False,
                channelBox=False)

        # Lock Scale
        if kSceneItem.testFlag("lockXScale") is True:
            pm.setAttr(
                dccSceneItem.longName() + "." + 'sx',
                lock=True,
                keyable=False,
                channelBox=False)

        if kSceneItem.testFlag("lockYScale") is True:
            pm.setAttr(
                dccSceneItem.longName() + "." + 'sy',
                lock=True,
                keyable=False,
                channelBox=False)

        if kSceneItem.testFlag("lockZScale") is True:
            pm.setAttr(
                dccSceneItem.longName() + "." + 'sz',
                lock=True,
                keyable=False,
                channelBox=False)

        # Lock Translation
        if kSceneItem.testFlag("lockXTranslation") is True:
            pm.setAttr(
                dccSceneItem.longName() + "." + 'tx',
                lock=True,
                keyable=False,
                channelBox=False)

        if kSceneItem.testFlag("lockYTranslation") is True:
            pm.setAttr(
                dccSceneItem.longName() + "." + 'ty',
                lock=True,
                keyable=False,
                channelBox=False)

        if kSceneItem.testFlag("lockZTranslation") is True:
            pm.setAttr(
                dccSceneItem.longName() + "." + 'tz',
                lock=True,
                keyable=False,
                channelBox=False)

        return True

    # ===================
    # Visibility Methods
    # ===================
    def setVisibility(self, kSceneItem):
        """Sets the visibility of the object after its been created.

        Args:
            kSceneItem (Object): The scene item to set the visibility on.

        Return:
            bool: True if successful.

        """

        dccSceneItem = self.getDCCSceneItem(kSceneItem)

        # Set Visibility
        visAttr = kSceneItem.getVisibilityAttr()
        if visAttr.isConnected() is False and kSceneItem.getVisibility() is False:
            dccSceneItem.visibility.set(False)

        # Set Shape Visibility
        shapeVisAttr = kSceneItem.getShapeVisibilityAttr()
        if shapeVisAttr.isConnected() is False and kSceneItem.getShapeVisibility() is False:
            # Get shape node, if it exists, hide it.
            shape = dccSceneItem.getShape()
            if shape is not None:
                shape.visibility.set(False)

        return True

    # ================
    # Display Methods
    # ================
    def setObjectColor(self, kSceneItem):
        """Sets the color on the dccSceneItem.

        Args:
            kSceneItem (object): kraken object to set the color on.

        Return:
            bool: True if successful.

        """

        colors = self.config.getColors()
        dccSceneItem = self.getDCCSceneItem(kSceneItem)
        buildColor = self.getBuildColor(kSceneItem)

        if buildColor is not None:
            dccSceneItem.overrideEnabled.set(True)
            dccSceneItem.overrideRGBColors.set(True)

            if type(buildColor) is str:

                # Color in config is stored as rgb scalar values in a list
                if type(colors[buildColor]) is list:
                    dccSceneItem.overrideColorRGB.set(colors[buildColor][0], colors[buildColor][1], colors[buildColor][2])

                # Color in config is stored as a Color object
                elif type(colors[buildColor]).__name__ == 'Color':
                    dccSceneItem.overrideColorRGB.set(colors[buildColor].r, colors[buildColor].g, colors[buildColor].b)

            elif type(buildColor).__name__ == 'Color':
                dccSceneItem.overrideColorRGB.set(colors[buildColor].r, colors[buildColor].g, colors[buildColor].b)

        return True

    # ==================
    # Transform Methods
    # ==================
    def setTransform(self, kSceneItem):
        """Translates the transform to Maya transform.

        Args:
            kSceneItem -- Object: object to set the transform on.

        Return:
            bool: True if successful.

        """

        dccSceneItem = self.getDCCSceneItem(kSceneItem)

        quat = dt.Quaternion(kSceneItem.xfo.ori.v.x,
                             kSceneItem.xfo.ori.v.y,
                             kSceneItem.xfo.ori.v.z,
                             kSceneItem.xfo.ori.w)

        dccSceneItem.setScale(dt.Vector(
            kSceneItem.xfo.sc.x,
            kSceneItem.xfo.sc.y,
            kSceneItem.xfo.sc.z))

        dccSceneItem.setTranslation(dt.Vector(
            kSceneItem.xfo.tr.x,
            kSceneItem.xfo.tr.y,
            kSceneItem.xfo.tr.z),
            "world")

        dccSceneItem.setRotation(quat, "world")

        # Maya's rotation order enums:
        # 0 XYZ
        # 1 YZX
        # 2 ZXY
        # 3 XZY
        # 4 YXZ <-- 5 in Fabric
        # 5 ZYX <-- 4 in Fabric
        order = kSceneItem.ro.order
        if order == 4:
            order = 5
        elif order == 5:
            order = 4

        #  Maya api is one off from Maya's own node enum pyMel uses API
        dccSceneItem.setRotationOrder(order + 1, False)

        pm.select(clear=True)

        return True

    def setMat44Attr(self, dccSceneItemName, attr, mat44):
        """Sets a matrix attribute directly with values from a fabric Mat44.

        Note: Fabric and Maya's matrix row orders are reversed, so we transpose
        the matrix first.

        Args:
            dccSceneItemName (str): name of dccSceneItem.
            attr (str): name of matrix attribute to set.
            mat44 (Mat44): matrix value.

        Return:
            bool: True if successful.

        """

        mat44 = mat44.transpose()
        matrix = []
        rows = [mat44.row0, mat44.row1, mat44.row2, mat44.row3]
        for row in rows:
            matrix.extend([row.x, row.y, row.z, row.t])

        cmds.setAttr(dccSceneItemName + "." + attr, matrix, type="matrix")

        return True

    # ==============
    # Build Methods
    # ==============
    def _preBuild(self, kSceneItem):
        """Pre-Build commands.

        Args:
            kSceneItem (Object): Kraken kSceneItem object to build.

        Return:
            bool: True if successful.

        """

        self.__rigTitle = self.getConfig().getMetaData('RigName', 'Rig')
        self.__useRigConstants = self.getConfig().getMetaData('UseRigConstants', False)
        self.__profilingFrames = self.getConfig().getMetaData('ProfilingFrames', 0)
        self.__profilingLogFile = self.getConfig().getMetaData('ProfilingLogFile', None)
        self.__debugMode = False
        self.__names = {}
        self.__pathToName = {}
        self.__klExtensions = []
        self.__klMembers = {'members': {}, 'lookup': {}}
        self.__klObjects = []
        self.__klAttributes = []
        self.__klConstraints = []
        self.__klSolvers = []
        self.__klEvalID = {}
        self.__klCanvasOps = []
        self.__klConstants = {}
        self.__klExtExecuted = False
        self.__klArgs = {'members': {}, 'lookup': {}}
        self.__klPreCode = []
        self.__krkItems = {}
        self.__krkAttributes = {}
        self.__krkDeformers = []
        self.__krkVisitedObjects = []
        self.__krkShapes = []

        self.buildCanvasContainer("{}Canvas".format(self.__rigTitle))
        self.buildSkeletonContainer("{}Skeleton".format(self.__rigTitle))
        self.buildConstraintContainer("{}Constraints".format(self.__rigTitle))

        return True

    def _postBuild(self, kSceneItem):
        """Post-Build commands.

        Args:
            kSceneItem (object): kraken kSceneItem object to run post-build
                operations on.

        Return:
            bool: True if successful.

        """

        super(Builder, self)._postBuild(kSceneItem)
        self.rigGraph.implodeNodesByGroup()

        return True
