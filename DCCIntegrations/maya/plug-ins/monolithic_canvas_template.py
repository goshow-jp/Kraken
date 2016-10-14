# -*- coding: utf-8 -*-
u"""
Make canvasNode into static one.
Read input/output port into static attributes.
"""
import sys
import textwrap

import maya.api.OpenMaya as api
import maya.OpenMaya as oldapi
import maya.cmds as cmds

import FabricEngine.Core
import kraken.plugins.maya_plugin.conversion as conv
# ==================================================================================

MAYA_API_VERSION = oldapi.MGlobal.apiVersion()
__author__ = 'yamahigashi'
__version__ = '0.0.1'

# _TYPE_IDS = 0x001A0002
maya_useNewAPI = True


# ==================================================================================
class CanvasWrapper(api.MPxNode):
    type_name = 'canvasWrapper'
    # type_id = api.MTypeId(_TYPE_IDS)
    canvasPath = r"D:\fabric\hogea.canvas"

    @property
    def dgNode(self):
        '''for shortcut.'''
        return api.MFnDependencyNode(self.thisMObject())

    @property
    def dfgExec(self):
        '''for shortcut.'''
        return self._canvasGraph.getExec()

    @property
    def dfgBinding(self):
        '''for shortcut.'''
        return self._canvasGraph

    @property
    def host(self):
        '''for shortcut.'''
        return self._client.DFG.host

    def postConstructor(self):

        self._restoredFromPersistenceData = False
        self._dummyValue = 17
        self._isTransferingInputs = False
        # self._instances.push_back(this)
        self._dgDirtyEnabled = True
        self._portObjectsDestroyed = False
        self._affectedPlugsDirty = True
        self._affectedPlugs = api.MPlugArray()
        self._outputsDirtied = False
        self.isDeformer = False

        # store internal state for evaluation
        self._dirtyPlugs = []
        self.spliceMayaDataOverride = []

        self._client = getClient()
        with open(self.canvasPath, 'r') as f:
            self.canvasJson = f.read()
        self._canvasGraph = self.host.createBindingFromJSON(self.canvasJson)

    @classmethod
    def initialize(cls):
        fnTyped = api.MFnTypedAttribute()
        fnNumeric = api.MFnNumericAttribute()

        saveData = fnTyped.create("saveData", "svd", api.MFnData.kString)
        fnTyped.hidden = True
        cls.addAttribute(saveData)

        evalId = fnNumeric.create("evalID", "evalID", api.MFnNumericData.kInt, 0)
        fnNumeric.keyable = True
        fnNumeric.hidden = True
        fnNumeric.readable = True
        fnNumeric.writable = True
        fnNumeric.storable = False
        fnNumeric.cached = False
        cls.addAttribute(evalId)

        # ------------------------------------------------------------------ #

        for a in cls.ports:
            attrName = a['name']
            ioType = a.get('execPortType', None)
            typeSpec = a.get('typeSpec', None)

            if typeSpec and "mat44" in typeSpec.lower():
                cls._addMat44Attr(attrName, ioType, typeSpec)

            elif typeSpec and "scalar" in typeSpec.lower():
                cls._addFloatAttr(attrName, ioType, typeSpec)

        cls.attributeAffects(cls.arm_R_ikSolver_klOp_bone0FK,  cls.arm_R_defConstraint_klOp_constrainees)
        cls.attributeAffects(cls.arm_R_ikSolver_klOp_bone0FK,  cls.arm_R_ikSolver_klOp_bone0Out)
        cls.attributeAffects(cls.arm_R_ikSolver_klOp_bone0FK,  cls.arm_R_ikSolver_klOp_bone1Out)
        cls.attributeAffects(cls.arm_R_ikSolver_klOp_bone0FK,  cls.arm_R_ikSolver_klOp_bone2Out)
        cls.attributeAffects(cls.arm_R_ikSolver_klOp_bone0FK,  cls.arm_R_ikSolver_klOp_midJointOut)
        cls.attributeAffects(cls.arm_R_ikSolver_klOp_bone1FK,  cls.arm_R_defConstraint_klOp_constrainees)
        cls.attributeAffects(cls.arm_R_ikSolver_klOp_bone1FK,  cls.arm_R_ikSolver_klOp_bone0Out)
        cls.attributeAffects(cls.arm_R_ikSolver_klOp_bone1FK,  cls.arm_R_ikSolver_klOp_bone1Out)
        cls.attributeAffects(cls.arm_R_ikSolver_klOp_bone1FK,  cls.arm_R_ikSolver_klOp_bone2Out)
        cls.attributeAffects(cls.arm_R_ikSolver_klOp_bone1FK,  cls.arm_R_ikSolver_klOp_midJointOut)
        cls.attributeAffects(cls.arm_R_ikSolver_klOp_ikHandle, cls.arm_R_defConstraint_klOp_constrainees)
        cls.attributeAffects(cls.arm_R_ikSolver_klOp_ikHandle, cls.arm_R_ikSolver_klOp_bone0Out)
        cls.attributeAffects(cls.arm_R_ikSolver_klOp_ikHandle, cls.arm_R_ikSolver_klOp_bone1Out)
        cls.attributeAffects(cls.arm_R_ikSolver_klOp_ikHandle, cls.arm_R_ikSolver_klOp_bone2Out)
        cls.attributeAffects(cls.arm_R_ikSolver_klOp_ikHandle, cls.arm_R_ikSolver_klOp_midJointOut)
        cls.attributeAffects(cls.arm_R_ikSolver_klOp_root,     cls.arm_R_defConstraint_klOp_constrainees)
        cls.attributeAffects(cls.arm_R_ikSolver_klOp_root,     cls.arm_R_ikSolver_klOp_bone0Out)
        cls.attributeAffects(cls.arm_R_ikSolver_klOp_root,     cls.arm_R_ikSolver_klOp_bone1Out)
        cls.attributeAffects(cls.arm_R_ikSolver_klOp_root,     cls.arm_R_ikSolver_klOp_bone2Out)
        cls.attributeAffects(cls.arm_R_ikSolver_klOp_root,     cls.arm_R_ikSolver_klOp_midJointOut)
        cls.attributeAffects(cls.arm_R_ikSolver_klOp_upV,      cls.arm_R_defConstraint_klOp_constrainees)
        cls.attributeAffects(cls.arm_R_ikSolver_klOp_upV,      cls.arm_R_ikSolver_klOp_bone0Out)
        cls.attributeAffects(cls.arm_R_ikSolver_klOp_upV,      cls.arm_R_ikSolver_klOp_bone1Out)
        cls.attributeAffects(cls.arm_R_ikSolver_klOp_upV,      cls.arm_R_ikSolver_klOp_bone2Out)
        cls.attributeAffects(cls.arm_R_ikSolver_klOp_upV,      cls.arm_R_ikSolver_klOp_midJointOut)

    @classmethod
    def _addFloatAttr(cls, attrName, ioType, typeSpec):
        fnNumeric = api.MFnNumericAttribute()

        exec("""cls.{0} = fnNumeric.create("{0}", "{0}", api.MFnNumericData.kDouble)""".format(attrName))
        if 'in' in ioType.lower():
            fnNumeric.keyable = True
            fnNumeric.readable = False
            fnNumeric.writable = True
            fnNumeric.storable = False

        else:
            fnNumeric.keyable = False
            fnNumeric.readable = True
            fnNumeric.writable = False
            fnNumeric.storable = False

        exec("""cls.addAttribute(cls.{})""".format(attrName))

    @classmethod
    def _addMat44Attr(cls, attrName, ioType, typeSpec):
        matAttr = api.MFnMatrixAttribute()

        exec("""cls.{0} = matAttr.create("{0}", "{0}", api.MFnMatrixAttribute.kDouble)""".format(attrName))
        if 'in' in ioType.lower():
            matAttr.storable = True
            matAttr.keyable = True
            matAttr.hidden = False
            if "[]" in typeSpec:
                matAttr.array = True
            matAttr.readable = False

        else:
            matAttr.storable = True
            matAttr.keyable = False
            matAttr.hidden = False
            if "[]" in typeSpec:
                matAttr.array = True
                matAttr.usesArrayDataBuilder = True
            matAttr.writable = False
            matAttr.readable = True

        exec("""cls.addAttribute(cls.{})""".format(attrName))

    def compute(self, plug, block):
        """
        Args:
            plug (MPlug): plug representing the attribute that needs to be recomputed.
            block (MDataBlock): data block containing storage for the node's attributes.
        """

        import time
        print("compute {} begin {}".format(plug.name(), time.time()))
        self._outputsDirtied = False

        if self.dfgBinding.getErrors(True) != "[]":
            sys.stderr.write("canvas got error(s) {}".format(len(self.dfgBinding.getErrors(True))))
            sys.stderr.write("error: {}".format(self.dfgBinding.getErrors(True)))
            return False

        # FabricSplice::Logging::AutoTimer timer("Maya::compute()")

        if self.transferInputValuesToSplice(plug, block):
            self.evaluate()
            self.transferOutputValuesToMaya(plug, block, self.isDeformer)
        print("compute {} finish".format(plug.name()))

    # ////////////////////////////////////////////////////////////////////////
    def evaluate(self):
        self.dfgBinding.execute()

    def transferInputValuesToSplice(self, plug, data):
        """
        Args:
            data (MDataBlock):
        """

        if self._isTransferingInputs:
            return False

        self._isTransferingInputs = True

        for p in self.attributeAffectsPair:
            src = p[0]
            dst = p[1]
            code = textwrap.dedent("""
                if "{dst}" in plug.name():
                        plug = self.dgNode.findPlug("{src}", False)
                        conv.dfgPlugToPort_mat44(plug, data, self.dfgBinding, "{src}")
                """.format(src=src, dst=dst))
            exec(code)

        self._isTransferingInputs = False

        return True

    def transferOutputValuesToMaya(self, plug, data, isDeformer=False):
        """
        Args:
            data (MDataBlock):
            isDeformer (bool):
        """
        # print "transferOutputValuesToMaya 1: " + plug.name()
        # if self._isTransferingInputs:
        #     return

        for p in self.attributeAffectsPair:
            dst = p[1]
            code = textwrap.dedent("""
                if "{0}" in plug.name():
                        plug = self.dgNode.findPlug("{0}", False)
                        conv.dfgPortToPlug_mat44(self.dfgBinding, "{0}", plug, data)
                """.format(dst))
            exec(code)

    def affectChildPlugs(self, plug, affectedPlugs):
        """
        Args:
            plug (MPlug):
            affectedPlugs (MPlugArray):

        Returns:
            affectedPlugs (MPlugArray):
        """

        pass

    def setupMayaAttributeAffects(self, portName, portMode, newAttribute):
        '''
        Args:
            portName (str):
            portMode (Port_Mode):
            newAttribute (MObject):
        '''
        # FabricSplice::Logging::AutoTimer globalTimer("Maya::setupMayaAttributeAffects()");
        # std::string localTimerName = (std::string("Maya::")+_spliceGraph.getName()+"::setupMayaAttributeAffects()").c_str();
        # FabricSplice::Logging::AutoTimer localTimer(localTimerName.c_str());


# -----------------------------------------------------------------------------
def getClient():
    """Gets the Fabric client from the DCC. This ensures that the same client
    is used, instead of a new one being created each time one is requiredself.

    Returns:
        Fabric Client.

    """

    print("get fabric client")
    contextID = cmds.fabricSplice('getClientContextID')
    if not contextID:
        cmds.fabricSplice('constructClient')
        contextID = cmds.fabricSplice('getClientContextID')

    options = {
        'contextID': contextID,
        'guarded': False
    }

    client = FabricEngine.Core.createClient(options)
    print(client)

    return client
