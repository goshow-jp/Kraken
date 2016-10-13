# import FabricEngine.Core
import maya.api.OpenMaya as om
import kraken.plugins.maya_plugin.fabric_client


client = None
if not client:
    client = kraken.plugins.maya_plugin.fabric_client.getClient()


def getFloat64FromRTVal(rtVal):
    return rtVal.getSimpleType()


def Mat44ToMMatrix(rtVal):
    return om.MMatrix((
        (rtVal.row0.x.getSimpleType(), rtVal.row1.x.getSimpleType(), rtVal.row2.x.getSimpleType(), rtVal.row3.x.getSimpleType()),
        (rtVal.row0.y.getSimpleType(), rtVal.row1.y.getSimpleType(), rtVal.row2.y.getSimpleType(), rtVal.row3.y.getSimpleType()),
        (rtVal.row0.z.getSimpleType(), rtVal.row1.z.getSimpleType(), rtVal.row2.z.getSimpleType(), rtVal.row3.z.getSimpleType()),
        (rtVal.row0.t.getSimpleType(), rtVal.row1.t.getSimpleType(), rtVal.row2.t.getSimpleType(), rtVal.row3.t.getSimpleType())
    ))


def MMatrixToRtVal(mmat, rtVal):
    rtVal.set(
        'Mat44',
        mmat[0], mmat[4], mmat[8],  mmat[12],
        mmat[1], mmat[5], mmat[9],  mmat[13],
        mmat[2], mmat[6], mmat[10], mmat[14],
        mmat[3], mmat[7], mmat[11], mmat[15]
    )

    return rtVal


def dfgPlugToPort_compound_convertMat44(mmat, rtVal=None, f=False):
    if not f:
        rtVal = client.RT.types.Mat44()

    return MMatrixToRtVal(mmat, rtVal)


def _dfgPlugToPort_compound_convertCompound_XYZ_numeric(compound, handle, rtValName, x, y, z):

    if not compound.array:
        xHandle = om.MDataHandle(handle.child(x.object()))
        yHandle = om.MDataHandle(handle.child(y.object()))
        zHandle = om.MDataHandle(handle.child(z.object()))
        value = client.RT.types.Vec3(xHandle.asDouble(), yHandle.asDouble(), zHandle.asDouble())
        rtVal = client.RT.types.Vec3Param.create(rtValName, value)

        return rtVal

    else:
        arrayHandle = om.MArrayDataHandle(handle)
        rtVal = client.RT.types.Vec3ArrayParam(rtValName)
        rtVal.resize('Vec3ArrayParam', len(arrayHandle))

        for i in xrange(len(arrayHandle)):
            elementHandle = arrayHandle.inputValue()
            xHandle = elementHandle.child(x.object())
            yHandle = elementHandle.child(y.object())
            zHandle = elementHandle.child(z.object())
            value = client.RT.types.Vec3(xHandle.asDouble(), yHandle.asDouble, zHandle.asDouble)

            rtVal.setValue("", i, value)
            arrayHandle.next()

        return rtVal


def _dfgPlugToPort_compound_convertCompound_XYZ_unit(compound, handle, rtValName, x, y, z):

    if not compound.array:
        xHandle = om.MDataHandle(handle.child(x.object()))
        yHandle = om.MDataHandle(handle.child(y.object()))
        zHandle = om.MDataHandle(handle.child(z.object()))
        value = client.RT.types.Euler(xHandle.asAngle().asRadians(), yHandle.asAngle().asRadians(), zHandle.asAngle().asRadians())
        rtVal = client.RT.types.EulerParam.create(rtValName, value)

        return rtVal

    else:
        arrayHandle = om.MArrayDataHandle(handle)
        rtVal = client.RT.types.EulerArrayParam(rtValName)
        rtVal.resize('EulerArrayParam', len(arrayHandle))

        for i in xrange(len(arrayHandle)):
            elementHandle = arrayHandle.inputValue()
            xHandle = elementHandle.child(x.object())
            yHandle = elementHandle.child(y.object())
            zHandle = elementHandle.child(z.object())
            value = client.RT.types.Euler(xHandle.asAngle().asRadians(), yHandle.asAngle().asRadians, zHandle.asAngle().asRadians)

            rtVal.setValue("", i, value)
            arrayHandle.next()

        return rtVal


def _dfgPlugToPort_compound_convertCompound_boolean(compound, handle, rtValName, nAttr, child):

    if not nAttr.array:
        childHandle = om.MDataHandle(handle.child(child.object()))
        value = client.RT.types.Boolean(childHandle.asBool())
        rtVal = client.RT.types.BooleanParam.create(rtValName, value)

        return rtVal

    else:
        childHandle = om.MArrayDataHandle(handle.child(child.object()))
        rtVal = client.RT.types.BooleanArrayParam(rtValName)
        rtVal.resize('BooleanArrayParam', len(childHandle))

        for i in xrange(len(childHandle)):
            value = client.RT.types.Boolean(childHandle.inputValue().asBool())

            rtVal.setValue("", i, value)
            childHandle.next()

        return rtVal


def _dfgPlugToPort_compound_convertCompound_int(compound, handle, rtValName, nAttr, child):

    if not nAttr.array:
        childHandle = om.MDataHandle(handle.child(child.object()))
        value = client.RT.types.SInt32(childHandle.asInt())
        rtVal = client.RT.types.SInt32Param.create(rtValName, value)

        return rtVal

    else:
        childHandle = om.MArrayDataHandle(handle.child(child.object()))
        rtVal = client.RT.types.SInt32ArrayParam(rtValName)
        rtVal.resize('SInt32ArrayParam', len(childHandle))

        for i in xrange(len(childHandle)):
            value = client.RT.types.SInt32(childHandle.inputValue().asInt())

            rtVal.setValue("", i, value)
            childHandle.next()

        return rtVal


def _dfgPlugToPort_compound_convertCompound_float(compound, handle, rtValName, nAttr, child):

    if not nAttr.array:
        childHandle = om.MDataHandle(handle.child(child.object()))
        value = client.RT.types.Float64(childHandle.asFloat())
        rtVal = client.RT.types.Float64Param.create(rtValName, value)

        return rtVal

    else:
        childHandle = om.MArrayDataHandle(handle.child(child.object()))
        rtVal = client.RT.types.Float64ArrayParam(rtValName)
        rtVal.resize('Float64ArrayParam', len(childHandle))

        for i in xrange(len(childHandle)):
            value = client.RT.types.Float64(childHandle.inputValue().asFloat())

            rtVal.setValue("", i, value)
            childHandle.next()

        return rtVal


def _dfgPlugToPort_compound_convertCompound_double(compound, handle, rtValName, nAttr, child):

    if not nAttr.array:
        childHandle = om.MDataHandle(handle.child(child.object()))
        value = client.RT.types.Float64(childHandle.asDouble())
        rtVal = client.RT.types.Float64Param.create(rtValName, value)

        return rtVal

    else:
        childHandle = om.MArrayDataHandle(handle.child(child.object()))
        rtVal = client.RT.types.Float64ArrayParam(rtValName)
        rtVal.resize('Float64ArrayParam', len(childHandle))

        for i in xrange(len(childHandle)):
            value = client.RT.types.Float64(childHandle.inputValue().asDouble())

            rtVal.setValue("", i, value)
            childHandle.next()

        return rtVal


def _dfgPlugToPort_compound_convertCompound_k3double(compound, handle, rtValName, nAttr, child):

    if not nAttr.array:
        childHandle = om.MDataHandle(handle.child(child.object()))
        v = childHandle.asFloatVector()
        value = client.RT.types.Vec3(v.x, v.y, v.z)
        rtVal = client.RT.types.Vec3Param.create(rtValName, value)

        return rtVal

    else:
        childHandle = om.MArrayDataHandle(handle.child(child.object()))
        rtVal = client.RT.types.Vec3ArrayParam(rtValName)
        rtVal.resize('Vec3ArrayParam', len(childHandle))

        for i in xrange(len(childHandle)):
            v = childHandle.inputValue().asFloatVector()
            value = client.RT.types.Vec3(v.x, v.y, v.z)

            rtVal.setValue("", i, value)
            childHandle.next()

        return rtVal


def _dfgPlugToPort_compound_convertCompound_k3float(compound, handle, rtValName, nAttr, child):

    if not nAttr.array:
        childHandle = om.MDataHandle(handle.child(child.object()))
        v = childHandle.asFloatVector()
        value = client.RT.types.Color(v.x, v.y, v.z, 1.0)  # FIXME: hardcoding alpha
        rtVal = client.RT.types.ColorParam.create(rtValName, value)

        return rtVal

    else:
        childHandle = om.MArrayDataHandle(handle.child(child.object()))
        rtVal = client.RT.types.ColorArrayParam(rtValName)
        rtVal.resize('ColorArrayParam', len(childHandle))

        for i in xrange(len(childHandle)):
            v = childHandle.inputValue().asFloatVector()
            value = client.RT.types.Color(v.x, v.y, v.z, 1.0)  # FIXME: hardcoding alpha

            rtVal.setValue("", i, value)
            childHandle.next()

        return rtVal


def _dfgPlugToPort_compound_convertCompound_typed_string(compound, handle, rtValName, nAttr, child):

    if not nAttr.array:
        childHandle = om.MDataHandle(handle.child(child.object()))
        value = client.RT.types.String(childHandle.asString())
        rtVal = client.RT.types.StringParam.create(rtValName, value)

        return rtVal

    else:
        childHandle = om.MArrayDataHandle(handle.child(child.object()))
        rtVal = client.RT.types.StringArrayParam(rtValName)
        rtVal.resize('StringArrayParam', len(childHandle))

        for i in xrange(len(childHandle)):
            value = client.RT.types.String(childHandle.inputValue().asString())

            rtVal.setValue("", i, value)
            childHandle.next()

        return rtVal


def _dfgPlugToPort_compound_convertCompound_typed_intarray(compound, handle, rtValName, nAttr, child):

    if not nAttr.array:
        arrayValues = om.MFnIntArrayData(handle.data().array())
        arrayLength = len(arrayValues)
        rtVal = client.RT.types.SInt32ArrayParam(rtValName)
        rtVal.resize('SInt32ArrayParam', arrayLength)

        values = rtVal.maybeGetMemberRef("values")
        # FIXME:
        values.setData(arrayValues)

        return rtVal

    else:
        childName = child.name()
        raise "Arrays of MFnData::kIntArray are not supported for {}.".format(childName)
        return


def _dfgPlugToPort_compound_convertCompound_typed_doublearray(compound, handle, rtValName, nAttr, child):

    if not nAttr.array:
        childHandle = om.MDataHandle(handle.child(child.object()))
        value = client.RT.types.String(childHandle.asString())
        rtVal = client.RT.types.StringParam.create(rtValName, value)

        return rtVal

    else:
        childHandle = om.MArrayDataHandle(handle.child(child.object()))
        rtVal = client.RT.types.StringArrayParam(rtValName)
        rtVal.resize('StringArrayParam', len(childHandle))

        for i in xrange(len(childHandle)):
            value = client.RT.types.String(childHandle.inputValue().asString())

            rtVal.setValue("", i, value)
            childHandle.next()

        return rtVal


def _dfgPlugToPort_compound_convertCompound_typed_vectorarray(compound, handle, rtValName, nAttr, child):

    if not nAttr.array:
        childHandle = om.MDataHandle(handle.child(child.object()))
        value = client.RT.types.String(childHandle.asString())
        rtVal = client.RT.types.StringParam.create(rtValName, value)

        return rtVal

    else:
        childHandle = om.MArrayDataHandle(handle.child(child.object()))
        rtVal = client.RT.types.StringArrayParam(rtValName)
        rtVal.resize('StringArrayParam', len(childHandle))

        for i in xrange(len(childHandle)):
            value = client.RT.types.String(childHandle.inputValue().asString())

            rtVal.setValue("", i, value)
            childHandle.next()

        return rtVal


def _dfgPlugToPort_compound_convertCompound_numeric(compound, handle, compoundNameRTVal, nAttr, child):

    if nAttr.unitType() == om.MFnNumericData.kBoolean:
        return _dfgPlugToPort_compound_convertCompound_boolean(compound, handle, compoundNameRTVal, nAttr, child)

    elif nAttr.unityType() == om.MFnNumericData.kInt:
        return _dfgPlugToPort_compound_convertCompound_int(compound, handle, compoundNameRTVal, nAttr, child)

    elif nAttr.unityType() == om.MFnNumericData.kFloat:
        return _dfgPlugToPort_compound_convertCompound_float(compound, handle, compoundNameRTVal, nAttr, child)

    elif nAttr.unityType() == om.MFnNumericData.kDouble:
        return _dfgPlugToPort_compound_convertCompound_double(compound, handle, compoundNameRTVal, nAttr, child)

    elif nAttr.unityType() == om.MFnNumericData.k3Double:  # vec3
        return _dfgPlugToPort_compound_convertCompound_k3double(compound, handle, compoundNameRTVal, nAttr, child)

    elif nAttr.unityType() == om.MFnNumericData.k3Float:  # color
        return _dfgPlugToPort_compound_convertCompound_k3float(compound, handle, compoundNameRTVal, nAttr, child)

    else:
        childName = child.name()
        raise "Unsupported numeric attribute '{}.".format(childName)
        return


def _dfgPlugToPort_compound_convertCompound_typed(compound, handle, compoundNameRTVal, tAttr, child):

    if tAttr.attrType() == om.MFnData.kString:
        return _dfgPlugToPort_compound_convertCompound_typed_string(compound, handle, compoundNameRTVal, tAttr, child)

    elif tAttr.attrType() == om.MFnData.kIntArray:
        return _dfgPlugToPort_compound_convertCompound_typed_intarray(compound, handle, compoundNameRTVal, tAttr, child)

    elif tAttr.attrType() == om.MFnData.kDoubleArray:
        return _dfgPlugToPort_compound_convertCompound_typed_doublearray(compound, handle, compoundNameRTVal, tAttr, child)

    elif tAttr.attrType() == om.MFnData.kVectorArray:
        return _dfgPlugToPort_compound_convertCompound_typed_vectorarray(compound, handle, compoundNameRTVal, tAttr, child)

    else:
        childName = child.name()
        raise "Unsupported typed attribute '{}.".format(childName)
        return


def _dfgPlugToPort_compound_convertCompound_matrix(compound, handle, compoundNameRTVal, mAttr, child):
    pass


def _dfgPlugToPort_compound_convertCompound_compound(compound, handle, compoundNameRTVal, cAttr, child):
    pass


def dfgPlugToPort_compound_convertCompound(compound, handle, rtVal=None):

    # treat special cases
    if compound.numChildren() == 3:
        compoundName = compound.name()
        compoundNameRTVal = client.RT.types.String(compoundName)

        x = compound.child(0)  # MFnAttribute
        y = compound.child(1)  # MFnAttribute
        z = compound.child(2)  # MFnAttribute

        # --------------------------------------------------------------------
        if (
            x.name() == "{}X".format(compoundName) and
            y.name() == "{}Y".format(compoundName) and
            z.name() == "{}Z".format(compoundName)
        ):

            # type detection
            try:
                om.MFnNumericAttribute(x.object())
                return _dfgPlugToPort_compound_convertCompound_XYZ_numeric(compound, handle, compoundNameRTVal, x, y, z)
            except RuntimeError:
                pass

            try:
                om.MFnUnitAttribute(x.object())
                return _dfgPlugToPort_compound_convertCompound_XYZ_unit(compound, handle, compoundNameRTVal, x, y, z)
            except RuntimeError:
                pass

        # --------------------------------------------------------------------
        for i in xrange(compound.numChildren()):
            child = compound.child(i)  # MFnAttribute

            try:
                nAttr = om.MFnNumericAttribute(child.object())
                return _dfgPlugToPort_compound_convertCompound_numeric(compound, handle, compoundNameRTVal, nAttr, child)

            except RuntimeError:
                pass

            try:
                tAttr = om.MFnTypedAttribute(child.object())
                return _dfgPlugToPort_compound_convertCompound_typed(compound, handle, compoundNameRTVal, tAttr, child)

            except RuntimeError:
                pass

            try:
                mAttr = om.MFnMatrixAttribute(child.object())
                return _dfgPlugToPort_compound_convertCompound_matrix(compound, handle, compoundNameRTVal, mAttr, child)

            except RuntimeError:
                pass

            try:
                cAttr = om.MFnCompoundAttribute(child.object())
                return _dfgPlugToPort_compound_convertCompound_compound(compound, handle, compoundNameRTVal, cAttr, child)

            except RuntimeError:
                pass


def dfgPlugToPort_mat44(plug, data, binding, argName):

    if plug.isArray:
        arrayHandle = data.inputArrayValue(plug)
        elementCount = len(arrayHandle)

        rtVal = binding.getArgValue(argName)
        rtVal.resize(elementCount)
        # dataRtVal = rtVal.data

        for i in xrange(elementCount):
            arrayHandle.jumpToLogicalElement(i)
            handle = arrayHandle.inputValue()
            mayaMat = handle.asMatrix()
            rtVal[i] = dfgPlugToPort_compound_convertMat44(mayaMat, f=False)

    else:
        rtVal = binding.getArgValue(argName)
        if rtVal.isArray():
            return

        handle = data.inputValue(plug)
        mayaMat = handle.asMatrix()
        rtVal = dfgPlugToPort_compound_convertMat44(mayaMat, rtVal, f=True)

    binding.setArgValue(argName, rtVal, False)


def dfgPortToPlug_mat44(binding, argName, plug, data):

    if plug.isArray:
        arrayHandle = data.outputArrayValue(plug)
        elementCount = len(arrayHandle)
        arrayBuilder = arrayHandle.builder()

        rtVal = binding.getArgValue(argName)
        rtVal.resize(elementCount)

        for i in xrange(elementCount):
            handle = arrayBuilder.addElement(i)
            mayaMat = Mat44ToMMatrix(rtVal[i])

            handle.setMMatrix(mayaMat)

        arrayHandle.set(arrayBuilder)
        arrayHandle.setAllClean()

    else:
        handle = data.outputValue(plug)
        rtVal = binding.getArgValue(argName)
        mayaMat = Mat44ToMMatrix(rtVal)

        handle.setMMatrix(mayaMat)
