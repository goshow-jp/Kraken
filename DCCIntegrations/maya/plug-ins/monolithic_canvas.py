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
from kraken.core.kraken_system import KrakenSystem
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

        self.ks = KrakenSystem()

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

    def ssetDependentsDirty(self, dirtyPlug, outPlugs):
        """
        Args:
            MPlug const &dirtyPlug,
            MPlugArray &outPlugs
        """

        print "<<<------------------------", dirtyPlug.name()
        self._affectedPlugs.clear()
        if MAYA_API_VERSION < 201600:
            constructingEvaluationGraph = False
        else:
            constructingEvaluationGraph = False
            # constructingEvaluationGraph = api.MEvaluationManager.graphConstructionActive()

        inAttr = api.MFnAttribute(dirtyPlug.attribute())
        # if ((not inAttr.hidden) and inAttr.dynamic and inAttr.writable):
        if ((not inAttr.hidden) and inAttr.writable):
            # print "dirty ", dirtyPlug.name(), inAttr, inAttr.hidden, inAttr.dynamic, inAttr.writable

            try:
                thisNode = self.dgNode
            except RuntimeError:
                sys.stderr.write("Unable to obtain MFnDependencyNode for " + dirtyPlug.name())
                return False

        else:
            return

        # FabricSplice::Logging::AutoTimer globalTimer("Maya::setDependentsDirty()");
        # std::string localTimerName = (std::string("Maya::")+_spliceGraph.getName()+"::setDependentsDirty()").c_str();
        # FabricSplice::Logging::AutoTimer localTimer(localTimerName.c_str());

        if not constructingEvaluationGraph:
            # we can't ask for the plug value here, so we fill an array
            # for the compute to only transfer newly dirtied values
            self.collectDirtyPlug(dirtyPlug)

            if self._outputsDirtied:
                # printf( "_outputsDirtied\n");
                print "_outputsDirtied"
                print "------------------------>>>"
                # return True

        if self._affectedPlugsDirty:
            self._affectedPlugs.clear()

            try:
                numAttrs = thisNode.attributeCount()
            except RuntimeError:
                sys.stderr.write("attributeCount(): failure")
                return False

            # collect affected plugs
            for i in xrange(numAttrs):
                try:
                    attr = api.MFnAttribute(thisNode.attribute(i))
                except RuntimeError:
                    sys.stderr.write("attribute(): failure")
                    return False

                # output port
                # if attr.hidden or not attr.dynamic or not attr.readable or not attr.parent.isNull():
                if attr.hidden or not attr.readable or not attr.parent.isNull():
                    continue

                try:
                    outPlug = thisNode.findPlug(attr.object(), False)
                except RuntimeError:
                    continue
                print outPlug.name()

                # assert( !outPlug.isNull() );
                if not self.isPlugInArray(outPlug, self._affectedPlugs):

                    # FIXME:
                    if ("nodeState" in outPlug.name() or "caching" in outPlug.name() or "frozen" in outPlug.name()):
                        continue

                    if "bb" in dirtyPlug.name() and "ao" in outPlug.name():
                        continue
                    self._affectedPlugs.append(outPlug)
                    print "append", outPlug.name()
                    self.affectChildPlugs(outPlug, self._affectedPlugs)

            # self._affectedPlugsDirty = False

        outPlugs = self._affectedPlugs
        print "-------------------------->>>"

        if not constructingEvaluationGraph:
            self._outputsDirtied = True

        return api.MPxNode.setDependentsDirty(self, dirtyPlug, outPlugs)

    # def preEvaluation(MObject thisMObject, const MDGContext& context, const MEvaluationNode& evaluationNode)
    def preEvaluation(self, thisMObject, context, evaluationNode):
        if not context.isNormal():
            return False

        # [andrew 20150616] in 2016 this needs to also happen here because
        # setDependentsDirty isn't called in Serial or Parallel eval mode
        for dirtyIt in evaluationNode:
            # print dirtyIt, dirtyIt.plug().name()
            self.collectDirtyPlug(dirtyIt.plug())

        return True

    # ////////////////////////////////////////////////////////////////////////
    def evaluate(self):
        # print "evaluate begin"
        # MFnDependencyNode
        # print("evaluate {}".format(self.dgNode.name()))

        # FabricSplice::Logging::AutoTimer globalTimer("Maya::evaluate()");
        # std::string localTimerName = (std::string("Maya::")+_spliceGraph.getName()+"::evaluate()").c_str();
        # FabricSplice::Logging::AutoTimer localTimer(localTimerName.c_str());
        # self.managePortObjectValues(False)  # recreate objects if not there yet
        '''
        if self.dfgBinding.usesEvalContext()):
            # setup the context
            FabricCore::RTVal context = _spliceGraph.getEvalContext();
            context.setMember("time", FabricSplice::constructFloat32RTVal(MAnimControl::currentTime().as(MTime::kSeconds)));
        '''

        self.dfgBinding.execute()

    def isPlugInArray(self, plug, array):
        for ele in array:
            if ele == plug:
                return True

        return False

    def managePortObjectValues(self, destroy):
        '''
            Args:
                destroy (bool)
        '''

        if self._portObjectsDestroyed == destroy:
            return

        '''
        # for(unsigned int i = 0; i < _spliceGraph.getDGPortCount(); ++i) {
        dfgExec = self.dfgBinding.getExec()
        for i in dfgExec.getExecPortCount():
            port = dfgExec.getDGPort(i);
            if(!port.isValid())
            continue;
            if(!port.isObject())
            continue
        '''

        for i in self.dfgExec.getExecPortCount():
            try:
                value = self.dfgBinding.getArgValue(i)
                if value.isNullObject():
                    continue

                objectRtVal = self._client.RT.types.Object(value)
                if not objectRtVal:
                    continue

                '''
                detachable = FabricSplice::constructInterfaceRTVal("Detachable", objectRtVal);
                if detachable.isNullObject():
                    continue

                if destroy:
                    detachable.callMethod("", "detach", 0, 0);
                else
                    detachable.callMethod("", "attach", 0, 0);
                '''
            except Exception as e:
                sys.stderr.write('monolith: managePortObjectValues: {}'.format(e))

        self._portObjectsDestroyed = destroy

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
        '''

        self._dirtyPlugs = []

        # self.managePortObjectValues(False)  # recreate objects if not there yet
        # plug = self.dgNode.findPlug("aa", False)
        # conv.dfgPlugToPort_mat44(plug, data, self.dfgBinding, "aa")

        # plug = self.dgNode.findPlug("bb", False)
        # conv.dfgPlugToPort_mat44(plug, data, self.dfgBinding, "bb")

        '''
        # FabricSplice::Logging::AutoTimer globalTimer("Maya::transferInputValuesToSplice()");
        # std::string localTimerName = (std::string("Maya::")+_spliceGraph.getName()+"::transferInputValuesToSplice()").c_str();
        # FabricSplice::Logging::AutoTimer localTimer(localTimerName.c_str());
        # SpliceConversionTimers timers;
        # timers.globalTimer = &globalTimer;
        # timers.localTimer = &localTimer;

        self._isTransferingInputs = True

        for plug in self._dirtyPlugs:

            # port = self.dfgExec.getDGPort(plug.name())
            # if not port:
            #     continue

            if not portInfo.isOut:

                dataType = portInfo.getDataType()
                for od in self.spliceMayaDataOverride:
                    if od == plugName:
                        dataType = "SpliceMayaData"
                        break

                func = getSplicePlugToPortFunc(dataType)
                if func:
                    func(plug, data)
                    # func(plug, data, port)

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
        # print "transferOutputValuesToMaya 1"
        # if self._isTransferingInputs:
        #     return
        if "ao" in plug.name():
            plug = self.dgNode.findPlug("ao", False)
            conv.dfgPortToPlug_mat44(self.dfgBinding, "ao", plug, data)

        if "oo" in plug.name():
            plug = self.dgNode.findPlug("oo", False)
            conv.dfgPortToPlug_mat44(self.dfgBinding, "oo", plug, data)

        # plug = self.dgNode.findPlug("oo", False)
        # conv.dfgPortToPlug_mat44(self.dfgBinding, "oo", plug, data)

        # plug = self.dgNode.findPlug("ao", False)
        # conv.dfgPortToPlug_mat44(self.dfgBinding, "ao", plug, data)
        # print "transferOutputValuesToMaya 4"

    def collectDirtyPlug(self, inPlug):
        """
        Args:
            inPlug (MPlug):
        """
        # FabricSplice::Logging::AutoTimer globalTimer("Maya::collectDirtyPlug()");
        # std::string localTimerName = (std::string("Maya::")+_spliceGraph.getName()+"::collectDirtyPlug()").c_str();
        # FabricSplice::Logging::AutoTimer localTimer(localTimerName.c_str());

        plugName = inPlug.name().split('.')[-1]
        plugName = plugName.split('[')[0]

        if inPlug.isChild:
            #  if plug belongs to translation or rotation we collect the parent to transfer all x,y,z values
            if inPlug.parent().isElement():
                self.collectDirtyPlug(inPlug.parent().array())
                return
            else:
                self.collectDirtyPlug(inPlug.parent())
                return

        if plugName not in self._dirtyPlugs:
            self._dirtyPlugs.append(plugName)

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

    def createAttributeForPort(self, portPath):
        '''
        Args:
            port (FabricSplice::DGPort)
        '''

        print "!!!!!!!!!createAttributeForPort!!!!!!!!!!!!!!!!!!"

        # getting dataType, portMode, arrayType with default value at first

        portInfo = PortInfo(self.dfgExec, portPath)
        dataType = portInfo.getDataType()
        print dataType
        print dataType
        print dataType
        print dataType
        print dataType
        if portInfo.isOpaque:
            dataType = "SpliceMayaData"

        if portInfo.isInternal:
            print "internal"
            print "internal"
            print "internal"
            return  # to do nothing more

        print(portInfo.name)
        print(portInfo.name)
        print(portInfo.name)
        print(portInfo.name)
        print(portInfo.name)
        print(portInfo.name)

        try:
            plug = self.dgNode.findPlug(portInfo.name, True)
            if plug is not None:
                # already exists
                return True
        except RuntimeError:
            # not found
            pass

        # self.addMayaAttribute(self.getPortName(portPath), dataType, arrayType, portMode, false, compoundStructure)
        addSuccess = self.addMayaAttribute(portInfo)
        # if not addSuccess:
        #     return False

        # if not portInfo.isOut and not portInfo.isArray:
        #     plug = self.dgNode.findPlug(portInfo.name, False)
        #     if not plug:
        #         return False

        defaultValue = portInfo.getDefaultValue()
        print defaultValue
        print defaultValue
        print defaultValue
        print defaultValue
        print defaultValue
        print defaultValue
        print defaultValue
        '''
        if variant.isString():
          plug.setString(variant.getStringData())
        else if variant.isBoolean():
          plug.setBool(variant.getBoolean())
        else if variant.isNull():
          return MStatus::kSuccess
        else if variant.isArray():
          return MStatus::kSuccess
        else if variant.isDict():
        {
          if dataType == "Vec3":
          {
            MPlug x = plug.child(0)
            MPlug y = plug.child(1)
            MPlug z = plug.child(2)
            if !x.isNull() && !x.isNull() && !z.isNull():
            {
              const FabricCore::Variant * xVar = variant.getDictValue("x")
              const FabricCore::Variant * yVar = variant.getDictValue("y")
              const FabricCore::Variant * zVar = variant.getDictValue("z")
              if xVar && yVar && zVar:
              {
                createAttributeForPort_setFloatOnPlug(x, createAttributeForPort_getFloatFromVariant(xVar))
                createAttributeForPort_setFloatOnPlug(y, createAttributeForPort_getFloatFromVariant(yVar))
                createAttributeForPort_setFloatOnPlug(z, createAttributeForPort_getFloatFromVariant(zVar))
              }
            }
          }
          else if dataType == "Euler":
          {
            MPlug x = plug.child(0)
            MPlug y = plug.child(1)
            MPlug z = plug.child(2)
            if !x.isNull() && !x.isNull() && !z.isNull():
            {
              const FabricCore::Variant * xVar = variant.getDictValue("x")
              const FabricCore::Variant * yVar = variant.getDictValue("y")
              const FabricCore::Variant * zVar = variant.getDictValue("z")
              if xVar && yVar && zVar:
              {
                MAngle xangle(createAttributeForPort_getFloatFromVariant(xVar), MAngle::kRadians)
                x.setMAngle(xangle)
                MAngle yangle(createAttributeForPort_getFloatFromVariant(yVar), MAngle::kRadians)
                y.setMAngle(yangle)
                MAngle zangle(createAttributeForPort_getFloatFromVariant(zVar), MAngle::kRadians)
                z.setMAngle(zangle)
              }
            }
          }
          else if dataType == "Color":
          {
            const FabricCore::Variant * rVar = variant.getDictValue("r")
            const FabricCore::Variant * gVar = variant.getDictValue("g")
            const FabricCore::Variant * bVar = variant.getDictValue("b")
            if rVar && gVar && bVar:
            {
              MDataHandle handle = plug.asMDataHandle()
              if handle.numericType() == MFnNumericData::k3Float || handle.numericType() == MFnNumericData::kFloat:{
                handle.setMFloatVector(MFloatVector(
                  createAttributeForPort_getFloatFromVariant(rVar),
                  createAttributeForPort_getFloatFromVariant(gVar),
                  createAttributeForPort_getFloatFromVariant(bVar)
                ))
              }else{
                handle.setMVector(MVector(
                  createAttributeForPort_getFloatFromVariant(rVar),
                  createAttributeForPort_getFloatFromVariant(gVar),
                  createAttributeForPort_getFloatFromVariant(bVar)
                ))
              }
            }
          }
        }
        else
        {
          float value = createAttributeForPort_getFloatFromVariant(&variant)
          createAttributeForPort_setFloatOnPlug(plug, value)
        }
      }
    }
  }

  MAYASPLICE_CATCH_END(&portStatus)

  return portStatus
}
        '''


class PortInfo(object):

    # --------------------------------------------------------------------------
    # utility for manipulation canvas graph
    # --------------------------------------------------------------------------

    def __init__(self, dfgExec, portPath):
        self.dfgExec = dfgExec
        self.portPath = portPath

        self.name = self.getName()

    # -------------------------------------------------------------------------
    # for manage port path
    def getDataType(self):
        return self.dfgExec.getPortResolvedType(self.portPath)

    def getData(self, metadataKey):
        return self.dfgExec.getPortMetadata(self.portPath, metadataKey)

    def getDefaultValue(self):
        typeName = self.getDataType()
        return self.dfgExec.getPortDefaultValue(self.portPath, typeName)

    def isData(self, metadataKey, value="true"):
        return self.dfgExec.getPortMetadata(self.portPath, metadataKey) == value

    def getName(self):
        name = self.portPath.split(".")[-1]
        name = name.rstrip("[]")

        return name

    def getMode(self):
        return self.dfgExec.getPortType(self.portPath)

    @property
    def isArray(self):
        return "[]" in self.portPath

    @property
    def isOpaque(self):
        return self.isData("opaque")

    @property
    def isInternal(self):
        return self.isData("internal")

    @property
    def isNativeArray(self):
        return self.isData("nativeArray")

    @property
    def isIn(self):
        return "In" in self.getMode()

    @property
    def isIO(self):
        return "IO" in self.getMode()

    @property
    def isOut(self):
        return "Out" in self.getMode()


# -----------------------------------------------------------------------------
# conversion function
# -----------------------------------------------------------------------------
def plugToPort_compound(port, plug, data):
    pass


def plugToPort_compoundArray(port, plug, data):
    pass


def plugToPort_bool(port, plug, data):
    pass


def plugToPort_integer(port, plug, data):
    pass


def plugToPort_scalar(port, plug, data):
    pass


def plugToPort_string(port, plug, data):
    pass


def plugToPort_color(port, plug, data):
    pass


def plugToPort_vec3(port, plug, data):
    pass


def plugToPort_euler(port, plug, data):
    pass


def plugToPort_mat44(port, plug, data):
    if plug.isArray:
        arrayHandle = data.inputArrayValue(plug)

        elements = arrayHandle.elementCount()
        for i in xrange(elements):

            arrayHandle.jumpToArrayElement(i)
            handle = arrayHandle.inputValue()
            mayaMat = handle.asMatrix()

            '''
            rtVal = ks.rtVal("Mat44")
            rtVal.setRows('',
                          ks.rtVal("Vec4", ks.rtVal("Scalar", mayaMat[0][0]), ks.rtVal("Scalar", mayaMat[0][1]),  ks.rtVal("Scalar", mayaMat[0][2]), ks.rtVal("Scalar", mayaMat[0][3])),
                          ks.rtVal("Vec4", ks.rtVal("Scalar", mayaMat[1][0]), ks.rtVal("Scalar", mayaMat[1][1]),  ks.rtVal("Scalar", mayaMat[1][2]), ks.rtVal("Scalar", mayaMat[1][3])),
                          ks.rtVal("Vec4", ks.rtVal("Scalar", mayaMat[2][0]), ks.rtVal("Scalar", mayaMat[2][1]),  ks.rtVal("Scalar", mayaMat[2][2]), ks.rtVal("Scalar", mayaMat[2][3])),
                          ks.rtVal("Vec4", ks.rtVal("Scalar", mayaMat[3][0]), ks.rtVal("Scalar", mayaMat[3][1]),  ks.rtVal("Scalar", mayaMat[3][2]), ks.rtVal("Scalar", mayaMat[3][3]))
                          )

            # dfgBinding.setArgValue(port.index, rtVal, False)
            '''


def plugToPort_PolygonMesh(port, plug, data):
    pass


def plugToPort_Lines(port, plug, data):
    pass


def plugToPort_KeyframeTrack(port, plug, data):
    pass


def plugToPort_spliceMayaData(port, plug, data):
    pass


def portToPlug_compound(port, plug, data):
    pass


def portToPlug_bool(port, plug, data):
    pass


def portToPlug_integer(port, plug, data):
    pass


def portToPlug_scalar(port, plug, data):
    pass


def portToPlug_string(port, plug, data):
    pass


def portToPlug_color(port, plug, data):
    pass


def portToPlug_vec3(port, plug, data):
    pass


def portToPlug_euler(port, plug, data):
    pass


def portToPlug_mat44(port, plug, data):
    pass


def portToPlug_PolygonMesh(port, plug, data):
    pass


def portToPlug_Lines(port, plug, data):
    pass


def portToPlug_spliceMayaData(port, plug, data):
    pass


splicePlugToPortTable = {
    "CompoundParam":        plugToPort_compound,
    "CompoundArrayParam":   plugToPort_compoundArray,
    "Boolean":              plugToPort_bool,
    "Integer":              plugToPort_integer,
    "Scalar":               plugToPort_scalar,
    "String":               plugToPort_string,
    "Color":                plugToPort_color,
    "Vec3":                 plugToPort_vec3,
    "Euler":                plugToPort_euler,
    "Mat44":                plugToPort_mat44,
    "PolygonMesh":          plugToPort_PolygonMesh,
    "Lines":                plugToPort_Lines,
    "KeyframeTrack":        plugToPort_KeyframeTrack,
    "SpliceMayaData":       plugToPort_spliceMayaData
}

splicePortToPlugTable = {
    "CompoundParam":       portToPlug_compound,
    "Boolean":             portToPlug_bool,
    "Integer":             portToPlug_integer,
    "Scalar":              portToPlug_scalar,
    "String":              portToPlug_string,
    "Color":               portToPlug_color,
    "Vec3":                portToPlug_vec3,
    "Euler":               portToPlug_euler,
    "Mat44":               portToPlug_mat44,
    "PolygonMesh":         portToPlug_PolygonMesh,
    "Lines":               portToPlug_Lines,
    "SpliceMayaData":      portToPlug_spliceMayaData
}


def getSplicePlugToPortFunc(dataType):
    return splicePlugToPortTable.get(dataType, None)


def getSplicePortToPlugFunc(dataType):
    return splicePortToPlugTable.get(dataType, None)


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
