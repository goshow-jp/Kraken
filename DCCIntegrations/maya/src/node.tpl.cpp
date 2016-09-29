//
// Copyright (C) goshow
// 
// File: {{ node.class_name }}Node.cpp
//
// Dependency Graph Node: {{ node.class_name }}
//
// Author: Maya Plug-in Wizard 2.0
//


#include "{{ node.class_name }}.h"
#include "FabricDFGConversion.h"
#include "FabricDFGCommands.h"
#include <FTL/AutoSet.h>

#include <string>

#include <maya/MGlobal.h>
#include <maya/MPlug.h>
#include <maya/MFnDependencyNode.h>

#include <maya/MFnNumericAttribute.h>
#include <maya/MFnTypedAttribute.h>
#include <maya/MFnUnitAttribute.h>
#include <maya/MFnMatrixAttribute.h>
#include <maya/MFnCompoundAttribute.h>
#include <maya/MFnMessageAttribute.h>
#include <maya/MArrayDataBuilder.h>

// ------------------------------------------------------------------------- //
MTypeId {{ node.class_name }}::id( {{ node.mtype_id }} );
MObject {{ node.class_name }}::saveData;
MObject {{ node.class_name }}::evalID;
MObject {{ node.class_name }}::refFilePath;

MObject {{ node.class_name }}::drawDebug;
MObject {{ node.class_name }}::rigScale;

////////////////////////////////////////////////////////////////////////////
//        dynamic generation here
////////////////////////////////////////////////////////////////////////////
{% for in_port in node.input_ports %}
MObject {{ node.class_name }}::m_{{ in_port.name }};
{% endfor %}
{% for out_port in node.output_ports %}
MObject {{ node.class_name }}::m_{{ out_port.name }};
{% endfor %}


#define TRANSFER_INPUTPLUG_TO_DFGPORT(inputPortName, outputPortName, portDataType) \
  if (plugName.rfind(std::string(outputPortName), plugName.find(".") + 1) != -1) \
  { \
    DFGPlugToArgFunc func = getDFGPlugToArgFunc(portDataType); \
    if(func != NULL) \
    { \
      MFnDependencyNode thisNode(thisMObject()); \
      (*func)(thisNode.findPlug(inputPortName, false), data, m_binding, getLockType(), inputPortName, &timers); \
    } \
  } \

/*
  if (plugName.rfind(std::string(inputPortName), plugName.find(".") + 1) != -1) \
  { \
    DFGPlugToArgFunc func = getDFGPlugToArgFunc(portDataType); \
    if(func != NULL) \
    { \
      (*func)(plug, data, m_binding, getLockType(), inputPortName, &timers); \
    } \
  } \
*/

// mayaLogErrorFunc(("input to port: " + plug.name()).asChar()); \

#define TRANSFER_DFGPORT_TO_OUTPUTPLUG(inputPortName, outputPortName, portDataType) \
  if (plugName.rfind(std::string(outputPortName), plugName.find(".") + 1) != -1) \
  { \
    DFGArgToPlugFunc func = getDFGArgToPlugFunc(portDataType); \
    if(func != NULL) \
    { \
      FabricCore::RTVal rtVal = m_binding.getArgValue(outputPortName); \
      if(rtVal.isArray() && (rtVal.getArraySize() == 0)) \
      { \
      } \
      else \
      { \
        FabricSplice::Logging::AutoTimer timer("Maya::transferOutputValuesToMaya::conversionFunc()"); \
        (*func)(m_binding, getLockType(), outputPortName, plug, data); \
        data.setClean(plug); \
      } \
    } \
  } \

/*
  if (plugName.rfind(std::string(inputPortName), plugName.find(".") + 1) != -1) \
  { \
    DFGArgToPlugFunc func = getDFGArgToPlugFunc(portDataType); \
    if(func != NULL) \
    { \
      FabricSplice::Logging::AutoTimer timer("Maya::transferOutputValuesToMaya::conversionFunc()"); \
      MFnDependencyNode thisNode(thisMObject()); \
      (*func)(m_binding, getLockType(), outputPortName, thisNode.findPlug(outputPortName, false), data); \
    } \
  } \
*/



///////////////////////////////////////////////////////////////////////////////
//
//
///////////////////////////////////////////////////////////////////////////////
{{ node.class_name }}::{{ node.class_name }}()
: FabricDFGBaseInterface()
{
}


void {{ node.class_name }}::postConstructor(){
  FabricDFGBaseInterface::constructBaseInterface();
  loadJSON();
  setExistWithoutInConnections(true);
  setExistWithoutOutConnections(true);
}


{{ node.class_name }}::~{{ node.class_name }}() {}


void* {{ node.class_name }}::creator(){
	return new {{ node.class_name }}();
}

MStatus {{ node.class_name }}::initialize() {

  MFnTypedAttribute typedAttr;
  MFnNumericAttribute nAttr;
  MFnMatrixAttribute matAttr;

  ////////////////////////////////////////////////////////////////////////////
  //        Fabric Canvas common attribute
  saveData = typedAttr.create("saveData", "svd", MFnData::kString);
  typedAttr.setHidden(true);
  typedAttr.setInternal(true);
  addAttribute(saveData);

  evalID = nAttr.create("evalID", "evalID", MFnNumericData::kInt);
  nAttr.setHidden(true);
  addAttribute(evalID);

  refFilePath = typedAttr.create("refFilePath", "rfp", MFnData::kString);
  typedAttr.setHidden(true);
  addAttribute(refFilePath);

  ////////////////////////////////////////////////////////////////////////////
  //        Kraken common attributes
  drawDebug = nAttr.create("drawDebug", "drawDebug", MFnNumericData::kBoolean);
  nAttr.setHidden(false);
  nAttr.setKeyable(true);
  nAttr.setReadable(true);
  nAttr.setStorable(true);
  nAttr.setDefault(false);
  addAttribute(drawDebug);

  rigScale = nAttr.create("rigScale", "rigScale", MFnNumericData::kDouble);
  nAttr.setHidden(false);
  nAttr.setKeyable(true);
  nAttr.setReadable(true);
  nAttr.setStorable(true);
  nAttr.setDefault(1.0f);
  addAttribute(rigScale);

  ////////////////////////////////////////////////////////////////////////////
  //        dynamic generated attributes
  {% for in_port in node.input_ports %}
  m_{{ in_port.name }} = matAttr.create("{{ in_port.name }}", "{{ in_port.name }}", MFnMatrixAttribute::kDouble);
  matAttr.setStorable(true);
  matAttr.setKeyable(true);
  matAttr.setHidden(false);
  matAttr.setArray(true);
  matAttr.setReadable(false);
  addAttribute(m_{{ in_port.name }});
  {% endfor %}

  {% for out_port in node.output_ports %}
  m_{{ out_port.name }} = matAttr.create("{{ out_port.name }}", "{{ out_port.name }}", MFnMatrixAttribute::kDouble);
  matAttr.setStorable(true);
  matAttr.setKeyable(false);
  matAttr.setHidden(false);
  matAttr.setArray(true);
  matAttr.setUsesArrayDataBuilder(true);
  matAttr.setWritable(false);
  matAttr.setReadable(true);
  addAttribute(m_{{ out_port.name }});
  {% endfor %}

  {% for in_port in node.input_ports %}
    {% for affect in in_port.affects %}
  attributeAffects(m_{{ in_port.name }}, m_{{ affect }});
    {% endfor %}
  {% endfor %}

  return MS::kSuccess;

}


///////////////////////////////////////////////////////////////////////////////
//
//
///////////////////////////////////////////////////////////////////////////////
void {{ node.class_name }}::loadJSON(){

  MStatus stat;
  MAYADFG_CATCH_BEGIN(&stat);

  MString filePath;
  MString json;

  // filePath = argParser.flagArgumentString("filePath", 0);
  filePath = MString("{{ canvas_file_path }}");
  FILE * file = fopen(filePath.asChar(), "rb");
  if(!file)
  {
    throw FabricCore::Exception(("File path (-f, -filePath) '"+filePath+"' cannot be found.").asChar());
  }

  fseek( file, 0, SEEK_END );
  long fileSize = ftell( file );
  rewind( file );

  char * buffer = (char*) malloc(fileSize + 1);
  buffer[fileSize] = '\0';

  size_t readBytes = fread(buffer, 1, fileSize, file);
  assert(readBytes == size_t(fileSize));
  (void)readBytes;

  fclose(file);

  json = buffer;
  free(buffer);

  // check if the graph is not empty
  FabricCore::DFGExec exec = getDFGExec();
  restoreFromJSON(json);
  setReferencedFilePath(filePath);

  MAYADFG_CATCH_END(&stat);
}


///////////////////////////////////////////////////////////////////////////////
//
//
///////////////////////////////////////////////////////////////////////////////
MStatus {{ node.class_name }}::compute(const MPlug& plug, MDataBlock& data){
  _outputsDirtied = false;

  MStatus stat;

  // get the node's state data handle.
  MDataHandle stateData = data.outputValue(state, &stat);
  CHECK_MSTATUS_AND_RETURN_IT(stat);

  if (stateData.asShort() == 0)       // 0: Normal.
  {
    MAYADFG_CATCH_BEGIN(&stat);

    FabricSplice::Logging::AutoTimer timer("Maya::compute()");
    MPlug& _plug = const_cast<MPlug&>(plug);

    if(transferStaticInputValuesToDFG(_plug, data))
    {
      evaluate();
      transferStaticOutputValuesToMaya(_plug, data);
    }

    MAYADFG_CATCH_END(&stat);
  }
  else if (stateData.asShort() == 1)  // 1: HasNoEffect.
  {
    stat = MS::kNotImplemented;
  }
  else                                // not supported by Canvas node.
  {
    stat = MS::kNotImplemented;
  }

  CHECK_MSTATUS(stat);
  return stat;
}


///////////////////////////////////////////////////////////////////////////////
//
//
///////////////////////////////////////////////////////////////////////////////
bool {{ node.class_name }}::transferStaticInputValuesToDFG(MPlug& plug, MDataBlock& data){

  if(_isTransferingInputs)
  {
    return false;
  }

  FabricSplice::Logging::AutoTimer timer("Maya::transferInputValuesToDFG()");
  DFGConversionTimers timers;
  timers.globalTimer = &timer;

  FTL::AutoSet<bool> transfersInputs(_isTransferingInputs, true);
  MStatus stat;
  std::string plugName(plug.name(&stat).asChar());
  CHECK_MSTATUS_AND_RETURN(stat, false);

  TRANSFER_INPUTPLUG_TO_DFGPORT("drawDebug", "drawDebug", "Boolean");
  TRANSFER_INPUTPLUG_TO_DFGPORT("rigScale", "rigScale", "Scalar");

  {% for in_port in node.input_ports %}
    {% for affect in in_port.affects %}
  TRANSFER_INPUTPLUG_TO_DFGPORT("{{ in_port.name }}", "{{ affect }}", "{{ in_port.type }}");
  {% endfor %}
  {% endfor %}

  return true;

}


///////////////////////////////////////////////////////////////////////////////
//
//
///////////////////////////////////////////////////////////////////////////////
void {{ node.class_name }}::transferStaticOutputValuesToMaya(MPlug& plug, MDataBlock& data, bool isDeformer){

  if(_isTransferingInputs)
  {
    return;
  }

  MStatus stat;
  std::string plugName(plug.name(&stat).asChar());
  FabricSplice::Logging::AutoTimer timer("Maya::transferOutputValuesToMaya()");

  {% for out_port in node.output_ports %}
  TRANSFER_DFGPORT_TO_OUTPUTPLUG("{{ out_port.name }}", "{{ out_port.name }}", "{{ out_port.type }}");
  {% endfor %}
}
