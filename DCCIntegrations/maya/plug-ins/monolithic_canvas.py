# -*- coding: utf-8 -*-
u"""
Make canvasNode into static one.
Read input/output port into static attributes.
"""
import sys

import maya.api.OpenMaya as api
import maya.OpenMaya as oldapi
import maya.cmds as cmds

import FabricEngine.Core
import kraken.plugins.maya_plugin.conversion as conv
# ==================================================================================

MAYA_API_VERSION = oldapi.MGlobal.apiVersion()
__author__ = 'yamahigashi'
__version__ = '0.0.1'

_TYPE_IDS = 0x001A0001
maya_useNewAPI = True


# ==================================================================================
class CanvasWrapper(api.MPxNode):
    type_name = 'canvasWrapper'
    type_id = api.MTypeId(_TYPE_IDS)
    canvasPath = r"D:\fabric\hogea.canvas"
    # canvasPath = r"D:\fabric\test_cache_node.canvas"

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

        self._client = getClient()
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

        # FabricSplice::setDCCOperatorSourceCodeCallback(
        #     &FabricSpliceEditorWidget::getSourceCodeForOperator)

        # FabricSplice::Logging::AutoTimer globalTimer("Maya::FabricSpliceBaseInterface()")
        # std::string localTimerName = (std::string("Maya::")+_canvasGraph.getName()+"::FabricSpliceBaseInterface()").c_str()
        # FabricSplice::Logging::AutoTimer localTimer(localTimerName.c_str())

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

        matAttr = api.MFnMatrixAttribute()
        cls.aa = matAttr.create("aa", "aa", api.MFnMatrixAttribute.kDouble)
        matAttr.storable = True
        matAttr.keyable = True
        matAttr.hidden = False
        matAttr.array = True
        matAttr.readable = False
        cls.addAttribute(cls.aa)

        cls.bb = matAttr.create("bb", "bb", api.MFnMatrixAttribute.kDouble)
        matAttr.storable = True
        matAttr.keyable = True
        matAttr.hidden = False
        matAttr.array = True
        matAttr.readable = False
        cls.addAttribute(cls.bb)

        matAttr1 = api.MFnMatrixAttribute()
        cls.oo = matAttr1.create("oo", "oo", api.MFnMatrixAttribute.kDouble)
        matAttr1.storable = True
        matAttr1.keyable = False
        matAttr1.hidden = False
        matAttr1.array = True
        matAttr1.usesArrayDataBuilder = True
        matAttr1.writable = False
        matAttr1.readable = True
        cls.addAttribute(cls.oo)

        matAttr2 = api.MFnMatrixAttribute()
        cls.ao = matAttr2.create("ao", "ao", api.MFnMatrixAttribute.kDouble)
        matAttr2.storable = True
        matAttr2.keyable = False
        matAttr2.hidden = False
        matAttr2.array = True
        matAttr2.usesArrayDataBuilder = True
        matAttr2.writable = False
        matAttr2.readable = True
        cls.addAttribute(cls.ao)

        cls.attributeAffects(cls.aa, cls.ao)
        # cls.attributeAffects(cls.aa, cls.oo)
        cls.attributeAffects(cls.bb, cls.oo)

    def compute(self, plug, block):
        """
        Args:
            plug (MPlug): plug representing the attribute that needs to be recomputed.
            block (MDataBlock): data block containing storage for the node's attributes.
        """

        import time
        print("compute {} begin {}".format(plug.name(), time.time()))
        # print("compute {} begin {}".format(plug.name(), plug.parent().logicalIndex()))
        self._outputsDirtied = False

        if self.dfgBinding.getErrors(True) != "[]":
            sys.stderr.write("canvas got error(s) {}".format(len(self.dfgBinding.getErrors(True))))
            sys.stderr.write("error: {}".format(self.dfgBinding.getErrors(True)))
            return False

        # FabricSplice::Logging::AutoTimer timer("Maya::compute()")

        if self.transferInputValuesToSplice(plug, block):
            self.evaluate()
            self.transferOutputValuesToMaya(plug, block, self.isDeformer)
        # print("compute {} finish".format(plug.name()))

    # ////////////////////////////////////////////////////////////////////////
    def evaluate(self):
        # print "evaluate begin"
        # MFnDependencyNode
        # print("evaluate {}".format(self.dgNode.name()))

        # FabricSplice::Logging::AutoTimer globalTimer("Maya::evaluate()");
        # std::string localTimerName = (std::string("Maya::")+_spliceGraph.getName()+"::evaluate()").c_str();
        # FabricSplice::Logging::AutoTimer localTimer(localTimerName.c_str());
        '''
        if self.dfgBinding.usesEvalContext()):
            # setup the context
            FabricCore::RTVal context = _spliceGraph.getEvalContext();
            context.setMember("time", FabricSplice::constructFloat32RTVal(MAnimControl::currentTime().as(MTime::kSeconds)));
        '''

        self.dfgBinding.execute()

    def transferInputValuesToSplice(self, plug, data):
        """
        Args:
            data (MDataBlock):
        """

        if self._isTransferingInputs:
            return False

        self._isTransferingInputs = True

        if "ao" in plug.name():
            plug = self.dgNode.findPlug("aa", False)
            conv.dfgPlugToPort_mat44(plug, data, self.dfgBinding, "aa")

        if "oo" in plug.name():
            plug = self.dgNode.findPlug("bb", False)
            conv.dfgPlugToPort_mat44(plug, data, self.dfgBinding, "bb")

        '''
        for plugName in self._dirtyPlugs:
            plug = self.dgNode.findPlug(plugName, False)
            conv.dfgPlugToPort_mat44(plug, data, self.dfgBinding, plugName)
        # FabricSplice::Logging::AutoTimer globalTimer("Maya::transferInputValuesToSplice()");
        # std::string localTimerName = (std::string("Maya::")+_spliceGraph.getName()+"::transferInputValuesToSplice()").c_str();
        # FabricSplice::Logging::AutoTimer localTimer(localTimerName.c_str());
        # SpliceConversionTimers timers;
        # timers.globalTimer = &globalTimer;
        # timers.localTimer = &localTimer;
        self._dirtyPlugs = []
        '''
        self._isTransferingInputs = False

        return True

    def transferOutputValuesToMaya(self, plug, data, isDeformer=False):
        """
        Args:
            data (MDataBlock):
            isDeformer (bool):
        """
        print "transferOutputValuesToMaya 1: " + plug.name()
        # if self._isTransferingInputs:
        #     return
        if "ao" in plug.name():
            plug = self.dgNode.findPlug("ao", False)
            conv.dfgPortToPlug_mat44(self.dfgBinding, "ao", plug, data)

        if "oo" in plug.name():
            plug = self.dgNode.findPlug("oo", False)
            conv.dfgPortToPlug_mat44(self.dfgBinding, "oo", plug, data)

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


# ------------------------------------------------------------------------------
def _registerNode(plugin, cls):
    try:
        plugin.registerNode(cls.type_name, cls.type_id, lambda: cls(), cls.initialize)
    except RuntimeError:
        sys.stderr.write('Failed to register node: ' + cls.type_name)
        raise


def _deregisterNode(plugin, cls):
    try:
        plugin.deregisterNode(cls.type_id)
    except RuntimeError:
        sys.stderr.write('Failed to deregister node: ' + cls.type_name)
        raise


def initializePlugin(mobj):
    plugin = api.MFnPlugin(mobj, __author__, __version__, 'Any')
    _registerNode(plugin, CanvasWrapper)


def uninitializePlugin(mobj):
    plugin = api.MFnPlugin(mobj)
    _deregisterNode(plugin, CanvasWrapper)
