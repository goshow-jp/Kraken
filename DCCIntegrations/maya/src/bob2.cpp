//
// Copyright (C) goshow
// 
// File: bob2Node.cpp
//
// Dependency Graph Node: bob2
//
// Author: Maya Plug-in Wizard 2.0
//


#include "bob2.h"
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
MTypeId bob2::id( 0x1A006 );
MObject bob2::saveData;
MObject bob2::evalID;
MObject bob2::refFilePath;

MObject bob2::drawDebug;
MObject bob2::rigScale;

////////////////////////////////////////////////////////////////////////////
//        dynamic generation here
////////////////////////////////////////////////////////////////////////////

MObject bob2::m_mainSrt_M_rigScale_klOp_target;
MObject bob2::m_mainSrt_M_Offset_ctrl;
MObject bob2::m_cog_M_cog_To_globalSRT_poseCns_spine_M_cog_ctrlSpace;
MObject bob2::m_spine_M_cog_ctrl;
MObject bob2::m_spine_M_spine_klOp_length;
MObject bob2::m_spine_M_spine_klOp_base;
MObject bob2::m_spine_M_spine_klOp_baseHandle;
MObject bob2::m_spine_M_spine_klOp_tipHandle;
MObject bob2::m_spine_M_spine_klOp_tip;
MObject bob2::m_spine_M_spine_klOp_outputs;
MObject bob2::m_spine_M_pelvis_ctrl;
MObject bob2::m_neck01_M_neck01_To_neckBase_poseCns_neck_M_neck01_ctrlSpace;
MObject bob2::m_neck_M_neck01_ctrl;
MObject bob2::m_neck_M_neck02_ctrl;
MObject bob2::m_clavicle_L_clavicle_To_spineEnd_poseCns_clavicle_L_clavicle_ctrlSpace;
MObject bob2::m_clavicle_L_clavicle_ctrl;
MObject bob2::m_IK_L_IK_To_globalSRT_poseCns_arm_L_IK_ctrlSpace;
MObject bob2::m_UpV_L_UpV_To_globalSRT_poseCns_arm_L_UpV_ctrlSpace;
MObject bob2::m_bicepFK_L_bicepFK_To_root_poseCns_arm_L_bicepFK_ctrlSpace;
MObject bob2::m_ikPosition_L_ikPosition_To_root_poseCns_arm_L_ikPosition_null;
MObject bob2::m_arm_L_ikSolver_klOp_rightSide;
MObject bob2::m_arm_L_ikSolver_klOp_ikblend;
MObject bob2::m_arm_L_ikSolver_klOp_root;
MObject bob2::m_arm_L_ikSolver_klOp_bone0FK;
MObject bob2::m_arm_L_ikSolver_klOp_bone1FK;
MObject bob2::m_arm_L_ikSolver_klOp_ikHandle;
MObject bob2::m_arm_L_ikSolver_klOp_upV;
MObject bob2::m_arm_L_ikSolver_klOp_bone0Len;
MObject bob2::m_arm_L_ikSolver_klOp_bone1Len;
MObject bob2::m_arm_L_ikSolver_klOp_bone0Out;
MObject bob2::m_arm_L_ikSolver_klOp_bone1Out;
MObject bob2::m_arm_L_ikSolver_klOp_bone2Out;
MObject bob2::m_arm_L_ikSolver_klOp_midJointOut;
MObject bob2::m_IK_L_IK_To_globalSRT_poseCns_leg_L_IK_ctrlSpace;
MObject bob2::m_leg_L_IK_ctrl;
MObject bob2::m_pivotAll_L_pivotAll_To_ikHandle_poseCns_foot_L_pivotAll_loc;
MObject bob2::m_foot_L_footPivot_klOp_rightSide;
MObject bob2::m_foot_L_footPivot_klOp_footRock;
MObject bob2::m_foot_L_footPivot_klOp_footBank;
MObject bob2::m_foot_L_footPivot_klOp_pivotAll;
MObject bob2::m_foot_L_footPivot_klOp_backPivot;
MObject bob2::m_foot_L_footPivot_klOp_frontPivot;
MObject bob2::m_foot_L_footPivot_klOp_outerPivot;
MObject bob2::m_foot_L_footPivot_klOp_innerPivot;
MObject bob2::m_foot_L_footPivot_klOp_result;
MObject bob2::m_foot_L_ankleIK_ctrl;
MObject bob2::m_UpV_L_UpV_To_globalSRT_poseCns_leg_L_UpV_ctrlSpace;
MObject bob2::m_femurFK_L_femurFK_To_pelvisInput_poseCns_leg_L_femurFK_ctrlSpace;
MObject bob2::m_ikRootPosition_L_ikRootPosition_To_pelvisInput_poseCns_leg_L_ikRootPosition_null;
MObject bob2::m_leg_L_ikSolver_klOp_rightSide;
MObject bob2::m_leg_L_ikSolver_klOp_ikblend;
MObject bob2::m_leg_L_ikSolver_klOp_root;
MObject bob2::m_leg_L_ikSolver_klOp_bone0FK;
MObject bob2::m_leg_L_ikSolver_klOp_bone1FK;
MObject bob2::m_leg_L_ikSolver_klOp_upV;
MObject bob2::m_leg_L_ikSolver_klOp_bone0Len;
MObject bob2::m_leg_L_ikSolver_klOp_bone1Len;
MObject bob2::m_leg_L_ikSolver_klOp_bone0Out;
MObject bob2::m_leg_L_ikSolver_klOp_bone1Out;
MObject bob2::m_leg_L_ikSolver_klOp_bone2Out;
MObject bob2::m_leg_L_ikSolver_klOp_midJointOut;
MObject bob2::m_leg_L_shinFK_ctrl;
MObject bob2::m_ankleFK_L_ankleFK_To_legEndFK_poseCns_foot_L_ankleFK_ctrlSpace;
MObject bob2::m_foot_L_footSolver_klOp_ikBlend;
MObject bob2::m_foot_L_footSolver_klOp_ankleLen;
MObject bob2::m_foot_L_footSolver_klOp_toeLen;
MObject bob2::m_foot_L_footSolver_klOp_ankleIK;
MObject bob2::m_foot_L_footSolver_klOp_toeIK;
MObject bob2::m_foot_L_footSolver_klOp_ankleFK;
MObject bob2::m_foot_L_footSolver_klOp_toeFK;
MObject bob2::m_foot_L_footSolver_klOp_ankle_result;
MObject bob2::m_foot_L_footSolver_klOp_toe_result;
MObject bob2::m_mainSrt_M_SRT_ctrl;
MObject bob2::m_neck_M_defConstraint_klOp_constrainers;
MObject bob2::m_neck_M_defConstraint_klOp_constrainees;
MObject bob2::m_clavicle_L_defConstraint_klOp_constrainee;
MObject bob2::m_arm_L_defConstraint_klOp_constrainees;
MObject bob2::m_leg_L_defConstraint_klOp_constrainees;
MObject bob2::m_foot_L_defConstraint_klOp_constrainees;
MObject bob2::m_spine_M_defConstraint_klOp_constrainees;
MObject bob2::m_spine_M_pelvisDefConstraint_klOp_constrainee;


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



///////////////////////////////////////////////////////////////////////////////
//
//
///////////////////////////////////////////////////////////////////////////////
bob2::bob2()
: FabricDFGBaseInterface()
{
}


void bob2::postConstructor(){
  FabricDFGBaseInterface::constructBaseInterface();
  loadJSON();
  setExistWithoutInConnections(true);
  setExistWithoutOutConnections(true);
}


bob2::~bob2() {}


void* bob2::creator(){
	return new bob2();
}

MStatus bob2::initialize() {

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
  // input
  

  m_mainSrt_M_Offset_ctrl = matAttr.create("mainSrt_M_Offset_ctrl", "mainSrt_M_Offset_ctrl", MFnMatrixAttribute::kDouble);
  matAttr.setStorable(true);
  matAttr.setKeyable(true);
  matAttr.setHidden(false);
  matAttr.setReadable(false);
  addAttribute(m_mainSrt_M_Offset_ctrl);

  m_spine_M_cog_ctrl = matAttr.create("spine_M_cog_ctrl", "spine_M_cog_ctrl", MFnMatrixAttribute::kDouble);
  matAttr.setStorable(true);
  matAttr.setKeyable(true);
  matAttr.setHidden(false);
  matAttr.setReadable(false);
  addAttribute(m_spine_M_cog_ctrl);

  m_spine_M_spine_klOp_length = nAttr.create("spine_M_spine_klOp_length", "spine_M_spine_klOp_length", MFnNumericData::kDouble);
  nAttr.setStorable(true);
  nAttr.setKeyable(true);
  nAttr.setHidden(false);
  nAttr.setReadable(false);
  addAttribute(m_spine_M_spine_klOp_length);

  m_spine_M_spine_klOp_base = matAttr.create("spine_M_spine_klOp_base", "spine_M_spine_klOp_base", MFnMatrixAttribute::kDouble);
  matAttr.setStorable(true);
  matAttr.setKeyable(true);
  matAttr.setHidden(false);
  matAttr.setReadable(false);
  addAttribute(m_spine_M_spine_klOp_base);

  m_spine_M_spine_klOp_baseHandle = matAttr.create("spine_M_spine_klOp_baseHandle", "spine_M_spine_klOp_baseHandle", MFnMatrixAttribute::kDouble);
  matAttr.setStorable(true);
  matAttr.setKeyable(true);
  matAttr.setHidden(false);
  matAttr.setReadable(false);
  addAttribute(m_spine_M_spine_klOp_baseHandle);

  m_spine_M_spine_klOp_tipHandle = matAttr.create("spine_M_spine_klOp_tipHandle", "spine_M_spine_klOp_tipHandle", MFnMatrixAttribute::kDouble);
  matAttr.setStorable(true);
  matAttr.setKeyable(true);
  matAttr.setHidden(false);
  matAttr.setReadable(false);
  addAttribute(m_spine_M_spine_klOp_tipHandle);

  m_spine_M_spine_klOp_tip = matAttr.create("spine_M_spine_klOp_tip", "spine_M_spine_klOp_tip", MFnMatrixAttribute::kDouble);
  matAttr.setStorable(true);
  matAttr.setKeyable(true);
  matAttr.setHidden(false);
  matAttr.setReadable(false);
  addAttribute(m_spine_M_spine_klOp_tip);

  m_spine_M_pelvis_ctrl = matAttr.create("spine_M_pelvis_ctrl", "spine_M_pelvis_ctrl", MFnMatrixAttribute::kDouble);
  matAttr.setStorable(true);
  matAttr.setKeyable(true);
  matAttr.setHidden(false);
  matAttr.setReadable(false);
  addAttribute(m_spine_M_pelvis_ctrl);

  m_neck_M_neck01_ctrl = matAttr.create("neck_M_neck01_ctrl", "neck_M_neck01_ctrl", MFnMatrixAttribute::kDouble);
  matAttr.setStorable(true);
  matAttr.setKeyable(true);
  matAttr.setHidden(false);
  matAttr.setReadable(false);
  addAttribute(m_neck_M_neck01_ctrl);

  m_neck_M_neck02_ctrl = matAttr.create("neck_M_neck02_ctrl", "neck_M_neck02_ctrl", MFnMatrixAttribute::kDouble);
  matAttr.setStorable(true);
  matAttr.setKeyable(true);
  matAttr.setHidden(false);
  matAttr.setReadable(false);
  addAttribute(m_neck_M_neck02_ctrl);

  m_clavicle_L_clavicle_ctrl = matAttr.create("clavicle_L_clavicle_ctrl", "clavicle_L_clavicle_ctrl", MFnMatrixAttribute::kDouble);
  matAttr.setStorable(true);
  matAttr.setKeyable(true);
  matAttr.setHidden(false);
  matAttr.setReadable(false);
  addAttribute(m_clavicle_L_clavicle_ctrl);

  m_arm_L_ikSolver_klOp_rightSide = nAttr.create("arm_L_ikSolver_klOp_rightSide", "arm_L_ikSolver_klOp_rightSide", MFnNumericData::kBoolean);
  nAttr.setStorable(true);
  nAttr.setKeyable(true);
  nAttr.setHidden(false);
  nAttr.setReadable(false);
  addAttribute(m_arm_L_ikSolver_klOp_rightSide);

  m_arm_L_ikSolver_klOp_ikblend = nAttr.create("arm_L_ikSolver_klOp_ikblend", "arm_L_ikSolver_klOp_ikblend", MFnNumericData::kDouble);
  nAttr.setStorable(true);
  nAttr.setKeyable(true);
  nAttr.setHidden(false);
  nAttr.setReadable(false);
  addAttribute(m_arm_L_ikSolver_klOp_ikblend);

  m_arm_L_ikSolver_klOp_root = matAttr.create("arm_L_ikSolver_klOp_root", "arm_L_ikSolver_klOp_root", MFnMatrixAttribute::kDouble);
  matAttr.setStorable(true);
  matAttr.setKeyable(true);
  matAttr.setHidden(false);
  matAttr.setReadable(false);
  addAttribute(m_arm_L_ikSolver_klOp_root);

  m_arm_L_ikSolver_klOp_bone0FK = matAttr.create("arm_L_ikSolver_klOp_bone0FK", "arm_L_ikSolver_klOp_bone0FK", MFnMatrixAttribute::kDouble);
  matAttr.setStorable(true);
  matAttr.setKeyable(true);
  matAttr.setHidden(false);
  matAttr.setReadable(false);
  addAttribute(m_arm_L_ikSolver_klOp_bone0FK);

  m_arm_L_ikSolver_klOp_bone1FK = matAttr.create("arm_L_ikSolver_klOp_bone1FK", "arm_L_ikSolver_klOp_bone1FK", MFnMatrixAttribute::kDouble);
  matAttr.setStorable(true);
  matAttr.setKeyable(true);
  matAttr.setHidden(false);
  matAttr.setReadable(false);
  addAttribute(m_arm_L_ikSolver_klOp_bone1FK);

  m_arm_L_ikSolver_klOp_ikHandle = matAttr.create("arm_L_ikSolver_klOp_ikHandle", "arm_L_ikSolver_klOp_ikHandle", MFnMatrixAttribute::kDouble);
  matAttr.setStorable(true);
  matAttr.setKeyable(true);
  matAttr.setHidden(false);
  matAttr.setReadable(false);
  addAttribute(m_arm_L_ikSolver_klOp_ikHandle);

  m_arm_L_ikSolver_klOp_upV = matAttr.create("arm_L_ikSolver_klOp_upV", "arm_L_ikSolver_klOp_upV", MFnMatrixAttribute::kDouble);
  matAttr.setStorable(true);
  matAttr.setKeyable(true);
  matAttr.setHidden(false);
  matAttr.setReadable(false);
  addAttribute(m_arm_L_ikSolver_klOp_upV);

  m_arm_L_ikSolver_klOp_bone0Len = nAttr.create("arm_L_ikSolver_klOp_bone0Len", "arm_L_ikSolver_klOp_bone0Len", MFnNumericData::kDouble);
  nAttr.setStorable(true);
  nAttr.setKeyable(true);
  nAttr.setHidden(false);
  nAttr.setReadable(false);
  addAttribute(m_arm_L_ikSolver_klOp_bone0Len);

  m_arm_L_ikSolver_klOp_bone1Len = nAttr.create("arm_L_ikSolver_klOp_bone1Len", "arm_L_ikSolver_klOp_bone1Len", MFnNumericData::kDouble);
  nAttr.setStorable(true);
  nAttr.setKeyable(true);
  nAttr.setHidden(false);
  nAttr.setReadable(false);
  addAttribute(m_arm_L_ikSolver_klOp_bone1Len);

  m_leg_L_IK_ctrl = matAttr.create("leg_L_IK_ctrl", "leg_L_IK_ctrl", MFnMatrixAttribute::kDouble);
  matAttr.setStorable(true);
  matAttr.setKeyable(true);
  matAttr.setHidden(false);
  matAttr.setReadable(false);
  addAttribute(m_leg_L_IK_ctrl);

  m_foot_L_footPivot_klOp_rightSide = nAttr.create("foot_L_footPivot_klOp_rightSide", "foot_L_footPivot_klOp_rightSide", MFnNumericData::kBoolean);
  nAttr.setStorable(true);
  nAttr.setKeyable(true);
  nAttr.setHidden(false);
  nAttr.setReadable(false);
  addAttribute(m_foot_L_footPivot_klOp_rightSide);

  m_foot_L_footPivot_klOp_footRock = nAttr.create("foot_L_footPivot_klOp_footRock", "foot_L_footPivot_klOp_footRock", MFnNumericData::kDouble);
  nAttr.setStorable(true);
  nAttr.setKeyable(true);
  nAttr.setHidden(false);
  nAttr.setReadable(false);
  addAttribute(m_foot_L_footPivot_klOp_footRock);

  m_foot_L_footPivot_klOp_footBank = nAttr.create("foot_L_footPivot_klOp_footBank", "foot_L_footPivot_klOp_footBank", MFnNumericData::kDouble);
  nAttr.setStorable(true);
  nAttr.setKeyable(true);
  nAttr.setHidden(false);
  nAttr.setReadable(false);
  addAttribute(m_foot_L_footPivot_klOp_footBank);

  m_foot_L_footPivot_klOp_pivotAll = matAttr.create("foot_L_footPivot_klOp_pivotAll", "foot_L_footPivot_klOp_pivotAll", MFnMatrixAttribute::kDouble);
  matAttr.setStorable(true);
  matAttr.setKeyable(true);
  matAttr.setHidden(false);
  matAttr.setReadable(false);
  addAttribute(m_foot_L_footPivot_klOp_pivotAll);

  m_foot_L_footPivot_klOp_backPivot = matAttr.create("foot_L_footPivot_klOp_backPivot", "foot_L_footPivot_klOp_backPivot", MFnMatrixAttribute::kDouble);
  matAttr.setStorable(true);
  matAttr.setKeyable(true);
  matAttr.setHidden(false);
  matAttr.setReadable(false);
  addAttribute(m_foot_L_footPivot_klOp_backPivot);

  m_foot_L_footPivot_klOp_frontPivot = matAttr.create("foot_L_footPivot_klOp_frontPivot", "foot_L_footPivot_klOp_frontPivot", MFnMatrixAttribute::kDouble);
  matAttr.setStorable(true);
  matAttr.setKeyable(true);
  matAttr.setHidden(false);
  matAttr.setReadable(false);
  addAttribute(m_foot_L_footPivot_klOp_frontPivot);

  m_foot_L_footPivot_klOp_outerPivot = matAttr.create("foot_L_footPivot_klOp_outerPivot", "foot_L_footPivot_klOp_outerPivot", MFnMatrixAttribute::kDouble);
  matAttr.setStorable(true);
  matAttr.setKeyable(true);
  matAttr.setHidden(false);
  matAttr.setReadable(false);
  addAttribute(m_foot_L_footPivot_klOp_outerPivot);

  m_foot_L_footPivot_klOp_innerPivot = matAttr.create("foot_L_footPivot_klOp_innerPivot", "foot_L_footPivot_klOp_innerPivot", MFnMatrixAttribute::kDouble);
  matAttr.setStorable(true);
  matAttr.setKeyable(true);
  matAttr.setHidden(false);
  matAttr.setReadable(false);
  addAttribute(m_foot_L_footPivot_klOp_innerPivot);

  m_foot_L_ankleIK_ctrl = matAttr.create("foot_L_ankleIK_ctrl", "foot_L_ankleIK_ctrl", MFnMatrixAttribute::kDouble);
  matAttr.setStorable(true);
  matAttr.setKeyable(true);
  matAttr.setHidden(false);
  matAttr.setReadable(false);
  addAttribute(m_foot_L_ankleIK_ctrl);

  m_leg_L_ikSolver_klOp_rightSide = nAttr.create("leg_L_ikSolver_klOp_rightSide", "leg_L_ikSolver_klOp_rightSide", MFnNumericData::kBoolean);
  nAttr.setStorable(true);
  nAttr.setKeyable(true);
  nAttr.setHidden(false);
  nAttr.setReadable(false);
  addAttribute(m_leg_L_ikSolver_klOp_rightSide);

  m_leg_L_ikSolver_klOp_ikblend = nAttr.create("leg_L_ikSolver_klOp_ikblend", "leg_L_ikSolver_klOp_ikblend", MFnNumericData::kDouble);
  nAttr.setStorable(true);
  nAttr.setKeyable(true);
  nAttr.setHidden(false);
  nAttr.setReadable(false);
  addAttribute(m_leg_L_ikSolver_klOp_ikblend);

  m_leg_L_ikSolver_klOp_root = matAttr.create("leg_L_ikSolver_klOp_root", "leg_L_ikSolver_klOp_root", MFnMatrixAttribute::kDouble);
  matAttr.setStorable(true);
  matAttr.setKeyable(true);
  matAttr.setHidden(false);
  matAttr.setReadable(false);
  addAttribute(m_leg_L_ikSolver_klOp_root);

  m_leg_L_ikSolver_klOp_bone0FK = matAttr.create("leg_L_ikSolver_klOp_bone0FK", "leg_L_ikSolver_klOp_bone0FK", MFnMatrixAttribute::kDouble);
  matAttr.setStorable(true);
  matAttr.setKeyable(true);
  matAttr.setHidden(false);
  matAttr.setReadable(false);
  addAttribute(m_leg_L_ikSolver_klOp_bone0FK);

  m_leg_L_ikSolver_klOp_bone1FK = matAttr.create("leg_L_ikSolver_klOp_bone1FK", "leg_L_ikSolver_klOp_bone1FK", MFnMatrixAttribute::kDouble);
  matAttr.setStorable(true);
  matAttr.setKeyable(true);
  matAttr.setHidden(false);
  matAttr.setReadable(false);
  addAttribute(m_leg_L_ikSolver_klOp_bone1FK);

  m_leg_L_ikSolver_klOp_upV = matAttr.create("leg_L_ikSolver_klOp_upV", "leg_L_ikSolver_klOp_upV", MFnMatrixAttribute::kDouble);
  matAttr.setStorable(true);
  matAttr.setKeyable(true);
  matAttr.setHidden(false);
  matAttr.setReadable(false);
  addAttribute(m_leg_L_ikSolver_klOp_upV);

  m_leg_L_ikSolver_klOp_bone0Len = nAttr.create("leg_L_ikSolver_klOp_bone0Len", "leg_L_ikSolver_klOp_bone0Len", MFnNumericData::kDouble);
  nAttr.setStorable(true);
  nAttr.setKeyable(true);
  nAttr.setHidden(false);
  nAttr.setReadable(false);
  addAttribute(m_leg_L_ikSolver_klOp_bone0Len);

  m_leg_L_ikSolver_klOp_bone1Len = nAttr.create("leg_L_ikSolver_klOp_bone1Len", "leg_L_ikSolver_klOp_bone1Len", MFnNumericData::kDouble);
  nAttr.setStorable(true);
  nAttr.setKeyable(true);
  nAttr.setHidden(false);
  nAttr.setReadable(false);
  addAttribute(m_leg_L_ikSolver_klOp_bone1Len);

  m_leg_L_shinFK_ctrl = matAttr.create("leg_L_shinFK_ctrl", "leg_L_shinFK_ctrl", MFnMatrixAttribute::kDouble);
  matAttr.setStorable(true);
  matAttr.setKeyable(true);
  matAttr.setHidden(false);
  matAttr.setReadable(false);
  addAttribute(m_leg_L_shinFK_ctrl);

  m_foot_L_footSolver_klOp_ikBlend = nAttr.create("foot_L_footSolver_klOp_ikBlend", "foot_L_footSolver_klOp_ikBlend", MFnNumericData::kDouble);
  nAttr.setStorable(true);
  nAttr.setKeyable(true);
  nAttr.setHidden(false);
  nAttr.setReadable(false);
  addAttribute(m_foot_L_footSolver_klOp_ikBlend);

  m_foot_L_footSolver_klOp_ankleLen = nAttr.create("foot_L_footSolver_klOp_ankleLen", "foot_L_footSolver_klOp_ankleLen", MFnNumericData::kDouble);
  nAttr.setStorable(true);
  nAttr.setKeyable(true);
  nAttr.setHidden(false);
  nAttr.setReadable(false);
  addAttribute(m_foot_L_footSolver_klOp_ankleLen);

  m_foot_L_footSolver_klOp_toeLen = nAttr.create("foot_L_footSolver_klOp_toeLen", "foot_L_footSolver_klOp_toeLen", MFnNumericData::kDouble);
  nAttr.setStorable(true);
  nAttr.setKeyable(true);
  nAttr.setHidden(false);
  nAttr.setReadable(false);
  addAttribute(m_foot_L_footSolver_klOp_toeLen);

  m_foot_L_footSolver_klOp_ankleIK = matAttr.create("foot_L_footSolver_klOp_ankleIK", "foot_L_footSolver_klOp_ankleIK", MFnMatrixAttribute::kDouble);
  matAttr.setStorable(true);
  matAttr.setKeyable(true);
  matAttr.setHidden(false);
  matAttr.setReadable(false);
  addAttribute(m_foot_L_footSolver_klOp_ankleIK);

  m_foot_L_footSolver_klOp_toeIK = matAttr.create("foot_L_footSolver_klOp_toeIK", "foot_L_footSolver_klOp_toeIK", MFnMatrixAttribute::kDouble);
  matAttr.setStorable(true);
  matAttr.setKeyable(true);
  matAttr.setHidden(false);
  matAttr.setReadable(false);
  addAttribute(m_foot_L_footSolver_klOp_toeIK);

  m_foot_L_footSolver_klOp_ankleFK = matAttr.create("foot_L_footSolver_klOp_ankleFK", "foot_L_footSolver_klOp_ankleFK", MFnMatrixAttribute::kDouble);
  matAttr.setStorable(true);
  matAttr.setKeyable(true);
  matAttr.setHidden(false);
  matAttr.setReadable(false);
  addAttribute(m_foot_L_footSolver_klOp_ankleFK);

  m_foot_L_footSolver_klOp_toeFK = matAttr.create("foot_L_footSolver_klOp_toeFK", "foot_L_footSolver_klOp_toeFK", MFnMatrixAttribute::kDouble);
  matAttr.setStorable(true);
  matAttr.setKeyable(true);
  matAttr.setHidden(false);
  matAttr.setReadable(false);
  addAttribute(m_foot_L_footSolver_klOp_toeFK);

  m_mainSrt_M_SRT_ctrl = matAttr.create("mainSrt_M_SRT_ctrl", "mainSrt_M_SRT_ctrl", MFnMatrixAttribute::kDouble);
  matAttr.setStorable(true);
  matAttr.setKeyable(true);
  matAttr.setHidden(false);
  matAttr.setReadable(false);
  addAttribute(m_mainSrt_M_SRT_ctrl);

  m_neck_M_defConstraint_klOp_constrainers = matAttr.create("neck_M_defConstraint_klOp_constrainers", "neck_M_defConstraint_klOp_constrainers", MFnMatrixAttribute::kDouble);
  matAttr.setStorable(true);
  matAttr.setKeyable(true);
  matAttr.setHidden(false);
  matAttr.setArray(true);
  matAttr.setReadable(false);
  addAttribute(m_neck_M_defConstraint_klOp_constrainers);

  // output
  

  m_mainSrt_M_rigScale_klOp_target = matAttr.create("mainSrt_M_rigScale_klOp_target", "mainSrt_M_rigScale_klOp_target", MFnMatrixAttribute::kDouble);
  matAttr.setStorable(true);
  matAttr.setKeyable(false);
  matAttr.setHidden(false);
  matAttr.setWritable(false);
  matAttr.setReadable(true);
  addAttribute(m_mainSrt_M_rigScale_klOp_target);

  m_cog_M_cog_To_globalSRT_poseCns_spine_M_cog_ctrlSpace = matAttr.create("cog_M_cog_To_globalSRT_poseCns_spine_M_cog_ctrlSpace", "cog_M_cog_To_globalSRT_poseCns_spine_M_cog_ctrlSpace", MFnMatrixAttribute::kDouble);
  matAttr.setStorable(true);
  matAttr.setKeyable(false);
  matAttr.setHidden(false);
  matAttr.setWritable(false);
  matAttr.setReadable(true);
  addAttribute(m_cog_M_cog_To_globalSRT_poseCns_spine_M_cog_ctrlSpace);

  m_spine_M_spine_klOp_outputs = matAttr.create("spine_M_spine_klOp_outputs", "spine_M_spine_klOp_outputs", MFnMatrixAttribute::kDouble);
  matAttr.setStorable(true);
  matAttr.setKeyable(false);
  matAttr.setHidden(false);
  matAttr.setArray(true);
  matAttr.setUsesArrayDataBuilder(true);
  matAttr.setWritable(false);
  matAttr.setReadable(true);
  addAttribute(m_spine_M_spine_klOp_outputs);

  m_neck01_M_neck01_To_neckBase_poseCns_neck_M_neck01_ctrlSpace = matAttr.create("neck01_M_neck01_To_neckBase_poseCns_neck_M_neck01_ctrlSpace", "neck01_M_neck01_To_neckBase_poseCns_neck_M_neck01_ctrlSpace", MFnMatrixAttribute::kDouble);
  matAttr.setStorable(true);
  matAttr.setKeyable(false);
  matAttr.setHidden(false);
  matAttr.setWritable(false);
  matAttr.setReadable(true);
  addAttribute(m_neck01_M_neck01_To_neckBase_poseCns_neck_M_neck01_ctrlSpace);

  m_clavicle_L_clavicle_To_spineEnd_poseCns_clavicle_L_clavicle_ctrlSpace = matAttr.create("clavicle_L_clavicle_To_spineEnd_poseCns_clavicle_L_clavicle_ctrlSpace", "clavicle_L_clavicle_To_spineEnd_poseCns_clavicle_L_clavicle_ctrlSpace", MFnMatrixAttribute::kDouble);
  matAttr.setStorable(true);
  matAttr.setKeyable(false);
  matAttr.setHidden(false);
  matAttr.setWritable(false);
  matAttr.setReadable(true);
  addAttribute(m_clavicle_L_clavicle_To_spineEnd_poseCns_clavicle_L_clavicle_ctrlSpace);

  m_IK_L_IK_To_globalSRT_poseCns_arm_L_IK_ctrlSpace = matAttr.create("IK_L_IK_To_globalSRT_poseCns_arm_L_IK_ctrlSpace", "IK_L_IK_To_globalSRT_poseCns_arm_L_IK_ctrlSpace", MFnMatrixAttribute::kDouble);
  matAttr.setStorable(true);
  matAttr.setKeyable(false);
  matAttr.setHidden(false);
  matAttr.setWritable(false);
  matAttr.setReadable(true);
  addAttribute(m_IK_L_IK_To_globalSRT_poseCns_arm_L_IK_ctrlSpace);

  m_UpV_L_UpV_To_globalSRT_poseCns_arm_L_UpV_ctrlSpace = matAttr.create("UpV_L_UpV_To_globalSRT_poseCns_arm_L_UpV_ctrlSpace", "UpV_L_UpV_To_globalSRT_poseCns_arm_L_UpV_ctrlSpace", MFnMatrixAttribute::kDouble);
  matAttr.setStorable(true);
  matAttr.setKeyable(false);
  matAttr.setHidden(false);
  matAttr.setWritable(false);
  matAttr.setReadable(true);
  addAttribute(m_UpV_L_UpV_To_globalSRT_poseCns_arm_L_UpV_ctrlSpace);

  m_bicepFK_L_bicepFK_To_root_poseCns_arm_L_bicepFK_ctrlSpace = matAttr.create("bicepFK_L_bicepFK_To_root_poseCns_arm_L_bicepFK_ctrlSpace", "bicepFK_L_bicepFK_To_root_poseCns_arm_L_bicepFK_ctrlSpace", MFnMatrixAttribute::kDouble);
  matAttr.setStorable(true);
  matAttr.setKeyable(false);
  matAttr.setHidden(false);
  matAttr.setWritable(false);
  matAttr.setReadable(true);
  addAttribute(m_bicepFK_L_bicepFK_To_root_poseCns_arm_L_bicepFK_ctrlSpace);

  m_ikPosition_L_ikPosition_To_root_poseCns_arm_L_ikPosition_null = matAttr.create("ikPosition_L_ikPosition_To_root_poseCns_arm_L_ikPosition_null", "ikPosition_L_ikPosition_To_root_poseCns_arm_L_ikPosition_null", MFnMatrixAttribute::kDouble);
  matAttr.setStorable(true);
  matAttr.setKeyable(false);
  matAttr.setHidden(false);
  matAttr.setWritable(false);
  matAttr.setReadable(true);
  addAttribute(m_ikPosition_L_ikPosition_To_root_poseCns_arm_L_ikPosition_null);

  m_arm_L_ikSolver_klOp_bone0Out = matAttr.create("arm_L_ikSolver_klOp_bone0Out", "arm_L_ikSolver_klOp_bone0Out", MFnMatrixAttribute::kDouble);
  matAttr.setStorable(true);
  matAttr.setKeyable(false);
  matAttr.setHidden(false);
  matAttr.setWritable(false);
  matAttr.setReadable(true);
  addAttribute(m_arm_L_ikSolver_klOp_bone0Out);

  m_arm_L_ikSolver_klOp_bone1Out = matAttr.create("arm_L_ikSolver_klOp_bone1Out", "arm_L_ikSolver_klOp_bone1Out", MFnMatrixAttribute::kDouble);
  matAttr.setStorable(true);
  matAttr.setKeyable(false);
  matAttr.setHidden(false);
  matAttr.setWritable(false);
  matAttr.setReadable(true);
  addAttribute(m_arm_L_ikSolver_klOp_bone1Out);

  m_arm_L_ikSolver_klOp_bone2Out = matAttr.create("arm_L_ikSolver_klOp_bone2Out", "arm_L_ikSolver_klOp_bone2Out", MFnMatrixAttribute::kDouble);
  matAttr.setStorable(true);
  matAttr.setKeyable(false);
  matAttr.setHidden(false);
  matAttr.setWritable(false);
  matAttr.setReadable(true);
  addAttribute(m_arm_L_ikSolver_klOp_bone2Out);

  m_arm_L_ikSolver_klOp_midJointOut = matAttr.create("arm_L_ikSolver_klOp_midJointOut", "arm_L_ikSolver_klOp_midJointOut", MFnMatrixAttribute::kDouble);
  matAttr.setStorable(true);
  matAttr.setKeyable(false);
  matAttr.setHidden(false);
  matAttr.setWritable(false);
  matAttr.setReadable(true);
  addAttribute(m_arm_L_ikSolver_klOp_midJointOut);

  m_IK_L_IK_To_globalSRT_poseCns_leg_L_IK_ctrlSpace = matAttr.create("IK_L_IK_To_globalSRT_poseCns_leg_L_IK_ctrlSpace", "IK_L_IK_To_globalSRT_poseCns_leg_L_IK_ctrlSpace", MFnMatrixAttribute::kDouble);
  matAttr.setStorable(true);
  matAttr.setKeyable(false);
  matAttr.setHidden(false);
  matAttr.setWritable(false);
  matAttr.setReadable(true);
  addAttribute(m_IK_L_IK_To_globalSRT_poseCns_leg_L_IK_ctrlSpace);

  m_pivotAll_L_pivotAll_To_ikHandle_poseCns_foot_L_pivotAll_loc = matAttr.create("pivotAll_L_pivotAll_To_ikHandle_poseCns_foot_L_pivotAll_loc", "pivotAll_L_pivotAll_To_ikHandle_poseCns_foot_L_pivotAll_loc", MFnMatrixAttribute::kDouble);
  matAttr.setStorable(true);
  matAttr.setKeyable(false);
  matAttr.setHidden(false);
  matAttr.setWritable(false);
  matAttr.setReadable(true);
  addAttribute(m_pivotAll_L_pivotAll_To_ikHandle_poseCns_foot_L_pivotAll_loc);

  m_foot_L_footPivot_klOp_result = matAttr.create("foot_L_footPivot_klOp_result", "foot_L_footPivot_klOp_result", MFnMatrixAttribute::kDouble);
  matAttr.setStorable(true);
  matAttr.setKeyable(false);
  matAttr.setHidden(false);
  matAttr.setWritable(false);
  matAttr.setReadable(true);
  addAttribute(m_foot_L_footPivot_klOp_result);

  m_UpV_L_UpV_To_globalSRT_poseCns_leg_L_UpV_ctrlSpace = matAttr.create("UpV_L_UpV_To_globalSRT_poseCns_leg_L_UpV_ctrlSpace", "UpV_L_UpV_To_globalSRT_poseCns_leg_L_UpV_ctrlSpace", MFnMatrixAttribute::kDouble);
  matAttr.setStorable(true);
  matAttr.setKeyable(false);
  matAttr.setHidden(false);
  matAttr.setWritable(false);
  matAttr.setReadable(true);
  addAttribute(m_UpV_L_UpV_To_globalSRT_poseCns_leg_L_UpV_ctrlSpace);

  m_femurFK_L_femurFK_To_pelvisInput_poseCns_leg_L_femurFK_ctrlSpace = matAttr.create("femurFK_L_femurFK_To_pelvisInput_poseCns_leg_L_femurFK_ctrlSpace", "femurFK_L_femurFK_To_pelvisInput_poseCns_leg_L_femurFK_ctrlSpace", MFnMatrixAttribute::kDouble);
  matAttr.setStorable(true);
  matAttr.setKeyable(false);
  matAttr.setHidden(false);
  matAttr.setWritable(false);
  matAttr.setReadable(true);
  addAttribute(m_femurFK_L_femurFK_To_pelvisInput_poseCns_leg_L_femurFK_ctrlSpace);

  m_ikRootPosition_L_ikRootPosition_To_pelvisInput_poseCns_leg_L_ikRootPosition_null = matAttr.create("ikRootPosition_L_ikRootPosition_To_pelvisInput_poseCns_leg_L_ikRootPosition_null", "ikRootPosition_L_ikRootPosition_To_pelvisInput_poseCns_leg_L_ikRootPosition_null", MFnMatrixAttribute::kDouble);
  matAttr.setStorable(true);
  matAttr.setKeyable(false);
  matAttr.setHidden(false);
  matAttr.setWritable(false);
  matAttr.setReadable(true);
  addAttribute(m_ikRootPosition_L_ikRootPosition_To_pelvisInput_poseCns_leg_L_ikRootPosition_null);

  m_leg_L_ikSolver_klOp_bone0Out = matAttr.create("leg_L_ikSolver_klOp_bone0Out", "leg_L_ikSolver_klOp_bone0Out", MFnMatrixAttribute::kDouble);
  matAttr.setStorable(true);
  matAttr.setKeyable(false);
  matAttr.setHidden(false);
  matAttr.setWritable(false);
  matAttr.setReadable(true);
  addAttribute(m_leg_L_ikSolver_klOp_bone0Out);

  m_leg_L_ikSolver_klOp_bone1Out = matAttr.create("leg_L_ikSolver_klOp_bone1Out", "leg_L_ikSolver_klOp_bone1Out", MFnMatrixAttribute::kDouble);
  matAttr.setStorable(true);
  matAttr.setKeyable(false);
  matAttr.setHidden(false);
  matAttr.setWritable(false);
  matAttr.setReadable(true);
  addAttribute(m_leg_L_ikSolver_klOp_bone1Out);

  m_leg_L_ikSolver_klOp_bone2Out = matAttr.create("leg_L_ikSolver_klOp_bone2Out", "leg_L_ikSolver_klOp_bone2Out", MFnMatrixAttribute::kDouble);
  matAttr.setStorable(true);
  matAttr.setKeyable(false);
  matAttr.setHidden(false);
  matAttr.setWritable(false);
  matAttr.setReadable(true);
  addAttribute(m_leg_L_ikSolver_klOp_bone2Out);

  m_leg_L_ikSolver_klOp_midJointOut = matAttr.create("leg_L_ikSolver_klOp_midJointOut", "leg_L_ikSolver_klOp_midJointOut", MFnMatrixAttribute::kDouble);
  matAttr.setStorable(true);
  matAttr.setKeyable(false);
  matAttr.setHidden(false);
  matAttr.setWritable(false);
  matAttr.setReadable(true);
  addAttribute(m_leg_L_ikSolver_klOp_midJointOut);

  m_ankleFK_L_ankleFK_To_legEndFK_poseCns_foot_L_ankleFK_ctrlSpace = matAttr.create("ankleFK_L_ankleFK_To_legEndFK_poseCns_foot_L_ankleFK_ctrlSpace", "ankleFK_L_ankleFK_To_legEndFK_poseCns_foot_L_ankleFK_ctrlSpace", MFnMatrixAttribute::kDouble);
  matAttr.setStorable(true);
  matAttr.setKeyable(false);
  matAttr.setHidden(false);
  matAttr.setWritable(false);
  matAttr.setReadable(true);
  addAttribute(m_ankleFK_L_ankleFK_To_legEndFK_poseCns_foot_L_ankleFK_ctrlSpace);

  m_foot_L_footSolver_klOp_ankle_result = matAttr.create("foot_L_footSolver_klOp_ankle_result", "foot_L_footSolver_klOp_ankle_result", MFnMatrixAttribute::kDouble);
  matAttr.setStorable(true);
  matAttr.setKeyable(false);
  matAttr.setHidden(false);
  matAttr.setWritable(false);
  matAttr.setReadable(true);
  addAttribute(m_foot_L_footSolver_klOp_ankle_result);

  m_foot_L_footSolver_klOp_toe_result = matAttr.create("foot_L_footSolver_klOp_toe_result", "foot_L_footSolver_klOp_toe_result", MFnMatrixAttribute::kDouble);
  matAttr.setStorable(true);
  matAttr.setKeyable(false);
  matAttr.setHidden(false);
  matAttr.setWritable(false);
  matAttr.setReadable(true);
  addAttribute(m_foot_L_footSolver_klOp_toe_result);

  m_neck_M_defConstraint_klOp_constrainees = matAttr.create("neck_M_defConstraint_klOp_constrainees", "neck_M_defConstraint_klOp_constrainees", MFnMatrixAttribute::kDouble);
  matAttr.setStorable(true);
  matAttr.setKeyable(false);
  matAttr.setHidden(false);
  matAttr.setArray(true);
  matAttr.setUsesArrayDataBuilder(true);
  matAttr.setWritable(false);
  matAttr.setReadable(true);
  addAttribute(m_neck_M_defConstraint_klOp_constrainees);

  m_clavicle_L_defConstraint_klOp_constrainee = matAttr.create("clavicle_L_defConstraint_klOp_constrainee", "clavicle_L_defConstraint_klOp_constrainee", MFnMatrixAttribute::kDouble);
  matAttr.setStorable(true);
  matAttr.setKeyable(false);
  matAttr.setHidden(false);
  matAttr.setWritable(false);
  matAttr.setReadable(true);
  addAttribute(m_clavicle_L_defConstraint_klOp_constrainee);

  m_arm_L_defConstraint_klOp_constrainees = matAttr.create("arm_L_defConstraint_klOp_constrainees", "arm_L_defConstraint_klOp_constrainees", MFnMatrixAttribute::kDouble);
  matAttr.setStorable(true);
  matAttr.setKeyable(false);
  matAttr.setHidden(false);
  matAttr.setArray(true);
  matAttr.setUsesArrayDataBuilder(true);
  matAttr.setWritable(false);
  matAttr.setReadable(true);
  addAttribute(m_arm_L_defConstraint_klOp_constrainees);

  m_leg_L_defConstraint_klOp_constrainees = matAttr.create("leg_L_defConstraint_klOp_constrainees", "leg_L_defConstraint_klOp_constrainees", MFnMatrixAttribute::kDouble);
  matAttr.setStorable(true);
  matAttr.setKeyable(false);
  matAttr.setHidden(false);
  matAttr.setArray(true);
  matAttr.setUsesArrayDataBuilder(true);
  matAttr.setWritable(false);
  matAttr.setReadable(true);
  addAttribute(m_leg_L_defConstraint_klOp_constrainees);

  m_foot_L_defConstraint_klOp_constrainees = matAttr.create("foot_L_defConstraint_klOp_constrainees", "foot_L_defConstraint_klOp_constrainees", MFnMatrixAttribute::kDouble);
  matAttr.setStorable(true);
  matAttr.setKeyable(false);
  matAttr.setHidden(false);
  matAttr.setArray(true);
  matAttr.setUsesArrayDataBuilder(true);
  matAttr.setWritable(false);
  matAttr.setReadable(true);
  addAttribute(m_foot_L_defConstraint_klOp_constrainees);

  m_spine_M_defConstraint_klOp_constrainees = matAttr.create("spine_M_defConstraint_klOp_constrainees", "spine_M_defConstraint_klOp_constrainees", MFnMatrixAttribute::kDouble);
  matAttr.setStorable(true);
  matAttr.setKeyable(false);
  matAttr.setHidden(false);
  matAttr.setArray(true);
  matAttr.setUsesArrayDataBuilder(true);
  matAttr.setWritable(false);
  matAttr.setReadable(true);
  addAttribute(m_spine_M_defConstraint_klOp_constrainees);

  m_spine_M_pelvisDefConstraint_klOp_constrainee = matAttr.create("spine_M_pelvisDefConstraint_klOp_constrainee", "spine_M_pelvisDefConstraint_klOp_constrainee", MFnMatrixAttribute::kDouble);
  matAttr.setStorable(true);
  matAttr.setKeyable(false);
  matAttr.setHidden(false);
  matAttr.setWritable(false);
  matAttr.setReadable(true);
  addAttribute(m_spine_M_pelvisDefConstraint_klOp_constrainee);

  
  attributeAffects(m_mainSrt_M_Offset_ctrl, m_cog_M_cog_To_globalSRT_poseCns_spine_M_cog_ctrlSpace);
  attributeAffects(m_mainSrt_M_Offset_ctrl, m_IK_L_IK_To_globalSRT_poseCns_arm_L_IK_ctrlSpace);
  attributeAffects(m_mainSrt_M_Offset_ctrl, m_UpV_L_UpV_To_globalSRT_poseCns_arm_L_UpV_ctrlSpace);
  attributeAffects(m_mainSrt_M_Offset_ctrl, m_IK_L_IK_To_globalSRT_poseCns_leg_L_IK_ctrlSpace);
  attributeAffects(m_mainSrt_M_Offset_ctrl, m_UpV_L_UpV_To_globalSRT_poseCns_leg_L_UpV_ctrlSpace);
  attributeAffects(m_spine_M_cog_ctrl, m_spine_M_pelvisDefConstraint_klOp_constrainee);
  attributeAffects(m_spine_M_cog_ctrl, m_spine_M_defConstraint_klOp_constrainees);
  attributeAffects(m_spine_M_cog_ctrl, m_spine_M_spine_klOp_outputs);
  attributeAffects(m_spine_M_cog_ctrl, m_neck01_M_neck01_To_neckBase_poseCns_neck_M_neck01_ctrlSpace);
  attributeAffects(m_spine_M_cog_ctrl, m_neck_M_defConstraint_klOp_constrainees);
  attributeAffects(m_spine_M_cog_ctrl, m_clavicle_L_clavicle_To_spineEnd_poseCns_clavicle_L_clavicle_ctrlSpace);
  attributeAffects(m_spine_M_cog_ctrl, m_femurFK_L_femurFK_To_pelvisInput_poseCns_leg_L_femurFK_ctrlSpace);
  attributeAffects(m_spine_M_cog_ctrl, m_ankleFK_L_ankleFK_To_legEndFK_poseCns_foot_L_ankleFK_ctrlSpace);
  attributeAffects(m_spine_M_spine_klOp_length, m_spine_M_pelvisDefConstraint_klOp_constrainee);
  attributeAffects(m_spine_M_spine_klOp_length, m_spine_M_defConstraint_klOp_constrainees);
  attributeAffects(m_spine_M_spine_klOp_length, m_spine_M_spine_klOp_outputs);
  attributeAffects(m_spine_M_spine_klOp_length, m_neck01_M_neck01_To_neckBase_poseCns_neck_M_neck01_ctrlSpace);
  attributeAffects(m_spine_M_spine_klOp_length, m_neck_M_defConstraint_klOp_constrainees);
  attributeAffects(m_spine_M_spine_klOp_length, m_clavicle_L_clavicle_To_spineEnd_poseCns_clavicle_L_clavicle_ctrlSpace);
  attributeAffects(m_spine_M_spine_klOp_length, m_femurFK_L_femurFK_To_pelvisInput_poseCns_leg_L_femurFK_ctrlSpace);
  attributeAffects(m_spine_M_spine_klOp_length, m_ankleFK_L_ankleFK_To_legEndFK_poseCns_foot_L_ankleFK_ctrlSpace);
  attributeAffects(m_spine_M_spine_klOp_base, m_spine_M_pelvisDefConstraint_klOp_constrainee);
  attributeAffects(m_spine_M_spine_klOp_base, m_spine_M_defConstraint_klOp_constrainees);
  attributeAffects(m_spine_M_spine_klOp_base, m_spine_M_spine_klOp_outputs);
  attributeAffects(m_spine_M_spine_klOp_base, m_neck01_M_neck01_To_neckBase_poseCns_neck_M_neck01_ctrlSpace);
  attributeAffects(m_spine_M_spine_klOp_base, m_neck_M_defConstraint_klOp_constrainees);
  attributeAffects(m_spine_M_spine_klOp_base, m_clavicle_L_clavicle_To_spineEnd_poseCns_clavicle_L_clavicle_ctrlSpace);
  attributeAffects(m_spine_M_spine_klOp_base, m_femurFK_L_femurFK_To_pelvisInput_poseCns_leg_L_femurFK_ctrlSpace);
  attributeAffects(m_spine_M_spine_klOp_base, m_ankleFK_L_ankleFK_To_legEndFK_poseCns_foot_L_ankleFK_ctrlSpace);
  attributeAffects(m_spine_M_spine_klOp_baseHandle, m_spine_M_pelvisDefConstraint_klOp_constrainee);
  attributeAffects(m_spine_M_spine_klOp_baseHandle, m_spine_M_defConstraint_klOp_constrainees);
  attributeAffects(m_spine_M_spine_klOp_baseHandle, m_spine_M_spine_klOp_outputs);
  attributeAffects(m_spine_M_spine_klOp_baseHandle, m_neck01_M_neck01_To_neckBase_poseCns_neck_M_neck01_ctrlSpace);
  attributeAffects(m_spine_M_spine_klOp_baseHandle, m_neck_M_defConstraint_klOp_constrainees);
  attributeAffects(m_spine_M_spine_klOp_baseHandle, m_clavicle_L_clavicle_To_spineEnd_poseCns_clavicle_L_clavicle_ctrlSpace);
  attributeAffects(m_spine_M_spine_klOp_baseHandle, m_femurFK_L_femurFK_To_pelvisInput_poseCns_leg_L_femurFK_ctrlSpace);
  attributeAffects(m_spine_M_spine_klOp_baseHandle, m_ankleFK_L_ankleFK_To_legEndFK_poseCns_foot_L_ankleFK_ctrlSpace);
  attributeAffects(m_spine_M_spine_klOp_tipHandle, m_spine_M_pelvisDefConstraint_klOp_constrainee);
  attributeAffects(m_spine_M_spine_klOp_tipHandle, m_spine_M_defConstraint_klOp_constrainees);
  attributeAffects(m_spine_M_spine_klOp_tipHandle, m_spine_M_spine_klOp_outputs);
  attributeAffects(m_spine_M_spine_klOp_tipHandle, m_neck01_M_neck01_To_neckBase_poseCns_neck_M_neck01_ctrlSpace);
  attributeAffects(m_spine_M_spine_klOp_tipHandle, m_neck_M_defConstraint_klOp_constrainees);
  attributeAffects(m_spine_M_spine_klOp_tipHandle, m_clavicle_L_clavicle_To_spineEnd_poseCns_clavicle_L_clavicle_ctrlSpace);
  attributeAffects(m_spine_M_spine_klOp_tipHandle, m_femurFK_L_femurFK_To_pelvisInput_poseCns_leg_L_femurFK_ctrlSpace);
  attributeAffects(m_spine_M_spine_klOp_tipHandle, m_ankleFK_L_ankleFK_To_legEndFK_poseCns_foot_L_ankleFK_ctrlSpace);
  attributeAffects(m_spine_M_spine_klOp_tip, m_spine_M_pelvisDefConstraint_klOp_constrainee);
  attributeAffects(m_spine_M_spine_klOp_tip, m_spine_M_defConstraint_klOp_constrainees);
  attributeAffects(m_spine_M_spine_klOp_tip, m_spine_M_spine_klOp_outputs);
  attributeAffects(m_spine_M_spine_klOp_tip, m_neck01_M_neck01_To_neckBase_poseCns_neck_M_neck01_ctrlSpace);
  attributeAffects(m_spine_M_spine_klOp_tip, m_neck_M_defConstraint_klOp_constrainees);
  attributeAffects(m_spine_M_spine_klOp_tip, m_clavicle_L_clavicle_To_spineEnd_poseCns_clavicle_L_clavicle_ctrlSpace);
  attributeAffects(m_spine_M_spine_klOp_tip, m_femurFK_L_femurFK_To_pelvisInput_poseCns_leg_L_femurFK_ctrlSpace);
  attributeAffects(m_spine_M_spine_klOp_tip, m_ankleFK_L_ankleFK_To_legEndFK_poseCns_foot_L_ankleFK_ctrlSpace);
  attributeAffects(m_spine_M_pelvis_ctrl, m_spine_M_pelvisDefConstraint_klOp_constrainee);
  attributeAffects(m_spine_M_pelvis_ctrl, m_spine_M_defConstraint_klOp_constrainees);
  attributeAffects(m_spine_M_pelvis_ctrl, m_spine_M_spine_klOp_outputs);
  attributeAffects(m_spine_M_pelvis_ctrl, m_neck01_M_neck01_To_neckBase_poseCns_neck_M_neck01_ctrlSpace);
  attributeAffects(m_spine_M_pelvis_ctrl, m_neck_M_defConstraint_klOp_constrainees);
  attributeAffects(m_spine_M_pelvis_ctrl, m_clavicle_L_clavicle_To_spineEnd_poseCns_clavicle_L_clavicle_ctrlSpace);
  attributeAffects(m_spine_M_pelvis_ctrl, m_femurFK_L_femurFK_To_pelvisInput_poseCns_leg_L_femurFK_ctrlSpace);
  attributeAffects(m_spine_M_pelvis_ctrl, m_ankleFK_L_ankleFK_To_legEndFK_poseCns_foot_L_ankleFK_ctrlSpace);
  attributeAffects(m_neck_M_neck01_ctrl, m_neck_M_defConstraint_klOp_constrainees);
  attributeAffects(m_neck_M_neck02_ctrl, m_neck_M_defConstraint_klOp_constrainees);
  attributeAffects(m_clavicle_L_clavicle_ctrl, m_clavicle_L_defConstraint_klOp_constrainee);
  attributeAffects(m_clavicle_L_clavicle_ctrl, m_bicepFK_L_bicepFK_To_root_poseCns_arm_L_bicepFK_ctrlSpace);
  attributeAffects(m_arm_L_ikSolver_klOp_rightSide, m_arm_L_ikSolver_klOp_bone0Out);
  attributeAffects(m_arm_L_ikSolver_klOp_rightSide, m_arm_L_ikSolver_klOp_bone1Out);
  attributeAffects(m_arm_L_ikSolver_klOp_rightSide, m_arm_L_ikSolver_klOp_bone2Out);
  attributeAffects(m_arm_L_ikSolver_klOp_rightSide, m_arm_L_defConstraint_klOp_constrainees);
  attributeAffects(m_arm_L_ikSolver_klOp_ikblend, m_arm_L_ikSolver_klOp_bone0Out);
  attributeAffects(m_arm_L_ikSolver_klOp_ikblend, m_arm_L_ikSolver_klOp_bone1Out);
  attributeAffects(m_arm_L_ikSolver_klOp_ikblend, m_arm_L_ikSolver_klOp_bone2Out);
  attributeAffects(m_arm_L_ikSolver_klOp_ikblend, m_arm_L_defConstraint_klOp_constrainees);
  attributeAffects(m_arm_L_ikSolver_klOp_root, m_arm_L_ikSolver_klOp_bone0Out);
  attributeAffects(m_arm_L_ikSolver_klOp_root, m_arm_L_ikSolver_klOp_bone1Out);
  attributeAffects(m_arm_L_ikSolver_klOp_root, m_arm_L_ikSolver_klOp_bone2Out);
  attributeAffects(m_arm_L_ikSolver_klOp_root, m_arm_L_defConstraint_klOp_constrainees);
  attributeAffects(m_arm_L_ikSolver_klOp_bone0FK, m_arm_L_ikSolver_klOp_bone0Out);
  attributeAffects(m_arm_L_ikSolver_klOp_bone0FK, m_arm_L_ikSolver_klOp_bone1Out);
  attributeAffects(m_arm_L_ikSolver_klOp_bone0FK, m_arm_L_ikSolver_klOp_bone2Out);
  attributeAffects(m_arm_L_ikSolver_klOp_bone0FK, m_arm_L_defConstraint_klOp_constrainees);
  attributeAffects(m_arm_L_ikSolver_klOp_bone1FK, m_arm_L_ikSolver_klOp_bone0Out);
  attributeAffects(m_arm_L_ikSolver_klOp_bone1FK, m_arm_L_ikSolver_klOp_bone1Out);
  attributeAffects(m_arm_L_ikSolver_klOp_bone1FK, m_arm_L_ikSolver_klOp_bone2Out);
  attributeAffects(m_arm_L_ikSolver_klOp_bone1FK, m_arm_L_defConstraint_klOp_constrainees);
  attributeAffects(m_arm_L_ikSolver_klOp_ikHandle, m_arm_L_ikSolver_klOp_bone0Out);
  attributeAffects(m_arm_L_ikSolver_klOp_ikHandle, m_arm_L_ikSolver_klOp_bone1Out);
  attributeAffects(m_arm_L_ikSolver_klOp_ikHandle, m_arm_L_ikSolver_klOp_bone2Out);
  attributeAffects(m_arm_L_ikSolver_klOp_ikHandle, m_arm_L_defConstraint_klOp_constrainees);
  attributeAffects(m_foot_L_footSolver_klOp_ikBlend, m_foot_L_footSolver_klOp_ankle_result);
  attributeAffects(m_foot_L_footSolver_klOp_ikBlend, m_foot_L_footSolver_klOp_toe_result);
  attributeAffects(m_foot_L_footSolver_klOp_ikBlend, m_foot_L_defConstraint_klOp_constrainees);
  attributeAffects(m_foot_L_footSolver_klOp_ankleLen, m_foot_L_footSolver_klOp_ankle_result);
  attributeAffects(m_foot_L_footSolver_klOp_ankleLen, m_foot_L_footSolver_klOp_toe_result);
  attributeAffects(m_foot_L_footSolver_klOp_ankleLen, m_foot_L_defConstraint_klOp_constrainees);
  attributeAffects(m_foot_L_footSolver_klOp_toeLen, m_foot_L_footSolver_klOp_ankle_result);
  attributeAffects(m_foot_L_footSolver_klOp_toeLen, m_foot_L_footSolver_klOp_toe_result);
  attributeAffects(m_foot_L_footSolver_klOp_toeLen, m_foot_L_defConstraint_klOp_constrainees);
  attributeAffects(m_foot_L_footSolver_klOp_ankleIK, m_foot_L_footSolver_klOp_ankle_result);
  attributeAffects(m_foot_L_footSolver_klOp_ankleIK, m_foot_L_footSolver_klOp_toe_result);
  attributeAffects(m_foot_L_footSolver_klOp_ankleIK, m_foot_L_defConstraint_klOp_constrainees);
  attributeAffects(m_foot_L_footSolver_klOp_toeIK, m_foot_L_footSolver_klOp_ankle_result);
  attributeAffects(m_foot_L_footSolver_klOp_toeIK, m_foot_L_footSolver_klOp_toe_result);
  attributeAffects(m_foot_L_footSolver_klOp_toeIK, m_foot_L_defConstraint_klOp_constrainees);
  attributeAffects(m_foot_L_footSolver_klOp_ankleFK, m_foot_L_footSolver_klOp_ankle_result);
  attributeAffects(m_foot_L_footSolver_klOp_ankleFK, m_foot_L_footSolver_klOp_toe_result);
  attributeAffects(m_foot_L_footSolver_klOp_ankleFK, m_foot_L_defConstraint_klOp_constrainees);
  attributeAffects(m_foot_L_footSolver_klOp_toeFK, m_foot_L_footSolver_klOp_ankle_result);
  attributeAffects(m_foot_L_footSolver_klOp_toeFK, m_foot_L_footSolver_klOp_toe_result);
  attributeAffects(m_foot_L_footSolver_klOp_toeFK, m_foot_L_defConstraint_klOp_constrainees);
  attributeAffects(m_neck_M_defConstraint_klOp_constrainers, m_neck_M_defConstraint_klOp_constrainees);

  return MS::kSuccess;

}


///////////////////////////////////////////////////////////////////////////////
//
//
///////////////////////////////////////////////////////////////////////////////
void bob2::loadJSON(){

  MStatus stat;
  MAYADFG_CATCH_BEGIN(&stat);

  MString filePath;
  MString json;

  // filePath = argParser.flagArgumentString("filePath", 0);
  filePath = MString("D:\\fabric\\bob2.canvas");
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
MStatus bob2::compute(const MPlug& plug, MDataBlock& data){
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
bool bob2::transferStaticInputValuesToDFG(MPlug& plug, MDataBlock& data){

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

  
  TRANSFER_INPUTPLUG_TO_DFGPORT("mainSrt_M_Offset_ctrl", "cog_M_cog_To_globalSRT_poseCns_spine_M_cog_ctrlSpace", "Mat44");
  TRANSFER_INPUTPLUG_TO_DFGPORT("mainSrt_M_Offset_ctrl", "IK_L_IK_To_globalSRT_poseCns_arm_L_IK_ctrlSpace", "Mat44");
  TRANSFER_INPUTPLUG_TO_DFGPORT("mainSrt_M_Offset_ctrl", "UpV_L_UpV_To_globalSRT_poseCns_arm_L_UpV_ctrlSpace", "Mat44");
  TRANSFER_INPUTPLUG_TO_DFGPORT("mainSrt_M_Offset_ctrl", "IK_L_IK_To_globalSRT_poseCns_leg_L_IK_ctrlSpace", "Mat44");
  TRANSFER_INPUTPLUG_TO_DFGPORT("mainSrt_M_Offset_ctrl", "UpV_L_UpV_To_globalSRT_poseCns_leg_L_UpV_ctrlSpace", "Mat44");
  TRANSFER_INPUTPLUG_TO_DFGPORT("spine_M_cog_ctrl", "spine_M_pelvisDefConstraint_klOp_constrainee", "Mat44");
  TRANSFER_INPUTPLUG_TO_DFGPORT("spine_M_cog_ctrl", "spine_M_defConstraint_klOp_constrainees", "Mat44");
  TRANSFER_INPUTPLUG_TO_DFGPORT("spine_M_cog_ctrl", "spine_M_spine_klOp_outputs", "Mat44");
  TRANSFER_INPUTPLUG_TO_DFGPORT("spine_M_cog_ctrl", "neck01_M_neck01_To_neckBase_poseCns_neck_M_neck01_ctrlSpace", "Mat44");
  TRANSFER_INPUTPLUG_TO_DFGPORT("spine_M_cog_ctrl", "neck_M_defConstraint_klOp_constrainees", "Mat44");
  TRANSFER_INPUTPLUG_TO_DFGPORT("spine_M_cog_ctrl", "clavicle_L_clavicle_To_spineEnd_poseCns_clavicle_L_clavicle_ctrlSpace", "Mat44");
  TRANSFER_INPUTPLUG_TO_DFGPORT("spine_M_cog_ctrl", "femurFK_L_femurFK_To_pelvisInput_poseCns_leg_L_femurFK_ctrlSpace", "Mat44");
  TRANSFER_INPUTPLUG_TO_DFGPORT("spine_M_cog_ctrl", "ankleFK_L_ankleFK_To_legEndFK_poseCns_foot_L_ankleFK_ctrlSpace", "Mat44");
  TRANSFER_INPUTPLUG_TO_DFGPORT("spine_M_spine_klOp_length", "spine_M_pelvisDefConstraint_klOp_constrainee", "Scalar");
  TRANSFER_INPUTPLUG_TO_DFGPORT("spine_M_spine_klOp_length", "spine_M_defConstraint_klOp_constrainees", "Scalar");
  TRANSFER_INPUTPLUG_TO_DFGPORT("spine_M_spine_klOp_length", "spine_M_spine_klOp_outputs", "Scalar");
  TRANSFER_INPUTPLUG_TO_DFGPORT("spine_M_spine_klOp_length", "neck01_M_neck01_To_neckBase_poseCns_neck_M_neck01_ctrlSpace", "Scalar");
  TRANSFER_INPUTPLUG_TO_DFGPORT("spine_M_spine_klOp_length", "neck_M_defConstraint_klOp_constrainees", "Scalar");
  TRANSFER_INPUTPLUG_TO_DFGPORT("spine_M_spine_klOp_length", "clavicle_L_clavicle_To_spineEnd_poseCns_clavicle_L_clavicle_ctrlSpace", "Scalar");
  TRANSFER_INPUTPLUG_TO_DFGPORT("spine_M_spine_klOp_length", "femurFK_L_femurFK_To_pelvisInput_poseCns_leg_L_femurFK_ctrlSpace", "Scalar");
  TRANSFER_INPUTPLUG_TO_DFGPORT("spine_M_spine_klOp_length", "ankleFK_L_ankleFK_To_legEndFK_poseCns_foot_L_ankleFK_ctrlSpace", "Scalar");
  TRANSFER_INPUTPLUG_TO_DFGPORT("spine_M_spine_klOp_base", "spine_M_pelvisDefConstraint_klOp_constrainee", "Mat44");
  TRANSFER_INPUTPLUG_TO_DFGPORT("spine_M_spine_klOp_base", "spine_M_defConstraint_klOp_constrainees", "Mat44");
  TRANSFER_INPUTPLUG_TO_DFGPORT("spine_M_spine_klOp_base", "spine_M_spine_klOp_outputs", "Mat44");
  TRANSFER_INPUTPLUG_TO_DFGPORT("spine_M_spine_klOp_base", "neck01_M_neck01_To_neckBase_poseCns_neck_M_neck01_ctrlSpace", "Mat44");
  TRANSFER_INPUTPLUG_TO_DFGPORT("spine_M_spine_klOp_base", "neck_M_defConstraint_klOp_constrainees", "Mat44");
  TRANSFER_INPUTPLUG_TO_DFGPORT("spine_M_spine_klOp_base", "clavicle_L_clavicle_To_spineEnd_poseCns_clavicle_L_clavicle_ctrlSpace", "Mat44");
  TRANSFER_INPUTPLUG_TO_DFGPORT("spine_M_spine_klOp_base", "femurFK_L_femurFK_To_pelvisInput_poseCns_leg_L_femurFK_ctrlSpace", "Mat44");
  TRANSFER_INPUTPLUG_TO_DFGPORT("spine_M_spine_klOp_base", "ankleFK_L_ankleFK_To_legEndFK_poseCns_foot_L_ankleFK_ctrlSpace", "Mat44");
  TRANSFER_INPUTPLUG_TO_DFGPORT("spine_M_spine_klOp_baseHandle", "spine_M_pelvisDefConstraint_klOp_constrainee", "Mat44");
  TRANSFER_INPUTPLUG_TO_DFGPORT("spine_M_spine_klOp_baseHandle", "spine_M_defConstraint_klOp_constrainees", "Mat44");
  TRANSFER_INPUTPLUG_TO_DFGPORT("spine_M_spine_klOp_baseHandle", "spine_M_spine_klOp_outputs", "Mat44");
  TRANSFER_INPUTPLUG_TO_DFGPORT("spine_M_spine_klOp_baseHandle", "neck01_M_neck01_To_neckBase_poseCns_neck_M_neck01_ctrlSpace", "Mat44");
  TRANSFER_INPUTPLUG_TO_DFGPORT("spine_M_spine_klOp_baseHandle", "neck_M_defConstraint_klOp_constrainees", "Mat44");
  TRANSFER_INPUTPLUG_TO_DFGPORT("spine_M_spine_klOp_baseHandle", "clavicle_L_clavicle_To_spineEnd_poseCns_clavicle_L_clavicle_ctrlSpace", "Mat44");
  TRANSFER_INPUTPLUG_TO_DFGPORT("spine_M_spine_klOp_baseHandle", "femurFK_L_femurFK_To_pelvisInput_poseCns_leg_L_femurFK_ctrlSpace", "Mat44");
  TRANSFER_INPUTPLUG_TO_DFGPORT("spine_M_spine_klOp_baseHandle", "ankleFK_L_ankleFK_To_legEndFK_poseCns_foot_L_ankleFK_ctrlSpace", "Mat44");
  TRANSFER_INPUTPLUG_TO_DFGPORT("spine_M_spine_klOp_tipHandle", "spine_M_pelvisDefConstraint_klOp_constrainee", "Mat44");
  TRANSFER_INPUTPLUG_TO_DFGPORT("spine_M_spine_klOp_tipHandle", "spine_M_defConstraint_klOp_constrainees", "Mat44");
  TRANSFER_INPUTPLUG_TO_DFGPORT("spine_M_spine_klOp_tipHandle", "spine_M_spine_klOp_outputs", "Mat44");
  TRANSFER_INPUTPLUG_TO_DFGPORT("spine_M_spine_klOp_tipHandle", "neck01_M_neck01_To_neckBase_poseCns_neck_M_neck01_ctrlSpace", "Mat44");
  TRANSFER_INPUTPLUG_TO_DFGPORT("spine_M_spine_klOp_tipHandle", "neck_M_defConstraint_klOp_constrainees", "Mat44");
  TRANSFER_INPUTPLUG_TO_DFGPORT("spine_M_spine_klOp_tipHandle", "clavicle_L_clavicle_To_spineEnd_poseCns_clavicle_L_clavicle_ctrlSpace", "Mat44");
  TRANSFER_INPUTPLUG_TO_DFGPORT("spine_M_spine_klOp_tipHandle", "femurFK_L_femurFK_To_pelvisInput_poseCns_leg_L_femurFK_ctrlSpace", "Mat44");
  TRANSFER_INPUTPLUG_TO_DFGPORT("spine_M_spine_klOp_tipHandle", "ankleFK_L_ankleFK_To_legEndFK_poseCns_foot_L_ankleFK_ctrlSpace", "Mat44");
  TRANSFER_INPUTPLUG_TO_DFGPORT("spine_M_spine_klOp_tip", "spine_M_pelvisDefConstraint_klOp_constrainee", "Mat44");
  TRANSFER_INPUTPLUG_TO_DFGPORT("spine_M_spine_klOp_tip", "spine_M_defConstraint_klOp_constrainees", "Mat44");
  TRANSFER_INPUTPLUG_TO_DFGPORT("spine_M_spine_klOp_tip", "spine_M_spine_klOp_outputs", "Mat44");
  TRANSFER_INPUTPLUG_TO_DFGPORT("spine_M_spine_klOp_tip", "neck01_M_neck01_To_neckBase_poseCns_neck_M_neck01_ctrlSpace", "Mat44");
  TRANSFER_INPUTPLUG_TO_DFGPORT("spine_M_spine_klOp_tip", "neck_M_defConstraint_klOp_constrainees", "Mat44");
  TRANSFER_INPUTPLUG_TO_DFGPORT("spine_M_spine_klOp_tip", "clavicle_L_clavicle_To_spineEnd_poseCns_clavicle_L_clavicle_ctrlSpace", "Mat44");
  TRANSFER_INPUTPLUG_TO_DFGPORT("spine_M_spine_klOp_tip", "femurFK_L_femurFK_To_pelvisInput_poseCns_leg_L_femurFK_ctrlSpace", "Mat44");
  TRANSFER_INPUTPLUG_TO_DFGPORT("spine_M_spine_klOp_tip", "ankleFK_L_ankleFK_To_legEndFK_poseCns_foot_L_ankleFK_ctrlSpace", "Mat44");
  TRANSFER_INPUTPLUG_TO_DFGPORT("spine_M_pelvis_ctrl", "spine_M_pelvisDefConstraint_klOp_constrainee", "Mat44");
  TRANSFER_INPUTPLUG_TO_DFGPORT("spine_M_pelvis_ctrl", "spine_M_defConstraint_klOp_constrainees", "Mat44");
  TRANSFER_INPUTPLUG_TO_DFGPORT("spine_M_pelvis_ctrl", "spine_M_spine_klOp_outputs", "Mat44");
  TRANSFER_INPUTPLUG_TO_DFGPORT("spine_M_pelvis_ctrl", "neck01_M_neck01_To_neckBase_poseCns_neck_M_neck01_ctrlSpace", "Mat44");
  TRANSFER_INPUTPLUG_TO_DFGPORT("spine_M_pelvis_ctrl", "neck_M_defConstraint_klOp_constrainees", "Mat44");
  TRANSFER_INPUTPLUG_TO_DFGPORT("spine_M_pelvis_ctrl", "clavicle_L_clavicle_To_spineEnd_poseCns_clavicle_L_clavicle_ctrlSpace", "Mat44");
  TRANSFER_INPUTPLUG_TO_DFGPORT("spine_M_pelvis_ctrl", "femurFK_L_femurFK_To_pelvisInput_poseCns_leg_L_femurFK_ctrlSpace", "Mat44");
  TRANSFER_INPUTPLUG_TO_DFGPORT("spine_M_pelvis_ctrl", "ankleFK_L_ankleFK_To_legEndFK_poseCns_foot_L_ankleFK_ctrlSpace", "Mat44");
  TRANSFER_INPUTPLUG_TO_DFGPORT("neck_M_neck01_ctrl", "neck_M_defConstraint_klOp_constrainees", "Mat44");
  TRANSFER_INPUTPLUG_TO_DFGPORT("neck_M_neck02_ctrl", "neck_M_defConstraint_klOp_constrainees", "Mat44");
  TRANSFER_INPUTPLUG_TO_DFGPORT("clavicle_L_clavicle_ctrl", "clavicle_L_defConstraint_klOp_constrainee", "Mat44");
  TRANSFER_INPUTPLUG_TO_DFGPORT("clavicle_L_clavicle_ctrl", "bicepFK_L_bicepFK_To_root_poseCns_arm_L_bicepFK_ctrlSpace", "Mat44");
  TRANSFER_INPUTPLUG_TO_DFGPORT("arm_L_ikSolver_klOp_rightSide", "arm_L_ikSolver_klOp_bone0Out", "Boolean");
  TRANSFER_INPUTPLUG_TO_DFGPORT("arm_L_ikSolver_klOp_rightSide", "arm_L_ikSolver_klOp_bone1Out", "Boolean");
  TRANSFER_INPUTPLUG_TO_DFGPORT("arm_L_ikSolver_klOp_rightSide", "arm_L_ikSolver_klOp_bone2Out", "Boolean");
  TRANSFER_INPUTPLUG_TO_DFGPORT("arm_L_ikSolver_klOp_rightSide", "arm_L_defConstraint_klOp_constrainees", "Boolean");
  TRANSFER_INPUTPLUG_TO_DFGPORT("arm_L_ikSolver_klOp_ikblend", "arm_L_ikSolver_klOp_bone0Out", "Scalar");
  TRANSFER_INPUTPLUG_TO_DFGPORT("arm_L_ikSolver_klOp_ikblend", "arm_L_ikSolver_klOp_bone1Out", "Scalar");
  TRANSFER_INPUTPLUG_TO_DFGPORT("arm_L_ikSolver_klOp_ikblend", "arm_L_ikSolver_klOp_bone2Out", "Scalar");
  TRANSFER_INPUTPLUG_TO_DFGPORT("arm_L_ikSolver_klOp_ikblend", "arm_L_defConstraint_klOp_constrainees", "Scalar");
  TRANSFER_INPUTPLUG_TO_DFGPORT("arm_L_ikSolver_klOp_root", "arm_L_ikSolver_klOp_bone0Out", "Mat44");
  TRANSFER_INPUTPLUG_TO_DFGPORT("arm_L_ikSolver_klOp_root", "arm_L_ikSolver_klOp_bone1Out", "Mat44");
  TRANSFER_INPUTPLUG_TO_DFGPORT("arm_L_ikSolver_klOp_root", "arm_L_ikSolver_klOp_bone2Out", "Mat44");
  TRANSFER_INPUTPLUG_TO_DFGPORT("arm_L_ikSolver_klOp_root", "arm_L_defConstraint_klOp_constrainees", "Mat44");
  TRANSFER_INPUTPLUG_TO_DFGPORT("arm_L_ikSolver_klOp_bone0FK", "arm_L_ikSolver_klOp_bone0Out", "Mat44");
  TRANSFER_INPUTPLUG_TO_DFGPORT("arm_L_ikSolver_klOp_bone0FK", "arm_L_ikSolver_klOp_bone1Out", "Mat44");
  TRANSFER_INPUTPLUG_TO_DFGPORT("arm_L_ikSolver_klOp_bone0FK", "arm_L_ikSolver_klOp_bone2Out", "Mat44");
  TRANSFER_INPUTPLUG_TO_DFGPORT("arm_L_ikSolver_klOp_bone0FK", "arm_L_defConstraint_klOp_constrainees", "Mat44");
  TRANSFER_INPUTPLUG_TO_DFGPORT("arm_L_ikSolver_klOp_bone1FK", "arm_L_ikSolver_klOp_bone0Out", "Mat44");
  TRANSFER_INPUTPLUG_TO_DFGPORT("arm_L_ikSolver_klOp_bone1FK", "arm_L_ikSolver_klOp_bone1Out", "Mat44");
  TRANSFER_INPUTPLUG_TO_DFGPORT("arm_L_ikSolver_klOp_bone1FK", "arm_L_ikSolver_klOp_bone2Out", "Mat44");
  TRANSFER_INPUTPLUG_TO_DFGPORT("arm_L_ikSolver_klOp_bone1FK", "arm_L_defConstraint_klOp_constrainees", "Mat44");
  TRANSFER_INPUTPLUG_TO_DFGPORT("arm_L_ikSolver_klOp_ikHandle", "arm_L_ikSolver_klOp_bone0Out", "Mat44");
  TRANSFER_INPUTPLUG_TO_DFGPORT("arm_L_ikSolver_klOp_ikHandle", "arm_L_ikSolver_klOp_bone1Out", "Mat44");
  TRANSFER_INPUTPLUG_TO_DFGPORT("arm_L_ikSolver_klOp_ikHandle", "arm_L_ikSolver_klOp_bone2Out", "Mat44");
  TRANSFER_INPUTPLUG_TO_DFGPORT("arm_L_ikSolver_klOp_ikHandle", "arm_L_defConstraint_klOp_constrainees", "Mat44");
  TRANSFER_INPUTPLUG_TO_DFGPORT("foot_L_footSolver_klOp_ikBlend", "foot_L_footSolver_klOp_ankle_result", "Scalar");
  TRANSFER_INPUTPLUG_TO_DFGPORT("foot_L_footSolver_klOp_ikBlend", "foot_L_footSolver_klOp_toe_result", "Scalar");
  TRANSFER_INPUTPLUG_TO_DFGPORT("foot_L_footSolver_klOp_ikBlend", "foot_L_defConstraint_klOp_constrainees", "Scalar");
  TRANSFER_INPUTPLUG_TO_DFGPORT("foot_L_footSolver_klOp_ankleLen", "foot_L_footSolver_klOp_ankle_result", "Scalar");
  TRANSFER_INPUTPLUG_TO_DFGPORT("foot_L_footSolver_klOp_ankleLen", "foot_L_footSolver_klOp_toe_result", "Scalar");
  TRANSFER_INPUTPLUG_TO_DFGPORT("foot_L_footSolver_klOp_ankleLen", "foot_L_defConstraint_klOp_constrainees", "Scalar");
  TRANSFER_INPUTPLUG_TO_DFGPORT("foot_L_footSolver_klOp_toeLen", "foot_L_footSolver_klOp_ankle_result", "Scalar");
  TRANSFER_INPUTPLUG_TO_DFGPORT("foot_L_footSolver_klOp_toeLen", "foot_L_footSolver_klOp_toe_result", "Scalar");
  TRANSFER_INPUTPLUG_TO_DFGPORT("foot_L_footSolver_klOp_toeLen", "foot_L_defConstraint_klOp_constrainees", "Scalar");
  TRANSFER_INPUTPLUG_TO_DFGPORT("foot_L_footSolver_klOp_ankleIK", "foot_L_footSolver_klOp_ankle_result", "Mat44");
  TRANSFER_INPUTPLUG_TO_DFGPORT("foot_L_footSolver_klOp_ankleIK", "foot_L_footSolver_klOp_toe_result", "Mat44");
  TRANSFER_INPUTPLUG_TO_DFGPORT("foot_L_footSolver_klOp_ankleIK", "foot_L_defConstraint_klOp_constrainees", "Mat44");
  TRANSFER_INPUTPLUG_TO_DFGPORT("foot_L_footSolver_klOp_toeIK", "foot_L_footSolver_klOp_ankle_result", "Mat44");
  TRANSFER_INPUTPLUG_TO_DFGPORT("foot_L_footSolver_klOp_toeIK", "foot_L_footSolver_klOp_toe_result", "Mat44");
  TRANSFER_INPUTPLUG_TO_DFGPORT("foot_L_footSolver_klOp_toeIK", "foot_L_defConstraint_klOp_constrainees", "Mat44");
  TRANSFER_INPUTPLUG_TO_DFGPORT("foot_L_footSolver_klOp_ankleFK", "foot_L_footSolver_klOp_ankle_result", "Mat44");
  TRANSFER_INPUTPLUG_TO_DFGPORT("foot_L_footSolver_klOp_ankleFK", "foot_L_footSolver_klOp_toe_result", "Mat44");
  TRANSFER_INPUTPLUG_TO_DFGPORT("foot_L_footSolver_klOp_ankleFK", "foot_L_defConstraint_klOp_constrainees", "Mat44");
  TRANSFER_INPUTPLUG_TO_DFGPORT("foot_L_footSolver_klOp_toeFK", "foot_L_footSolver_klOp_ankle_result", "Mat44");
  TRANSFER_INPUTPLUG_TO_DFGPORT("foot_L_footSolver_klOp_toeFK", "foot_L_footSolver_klOp_toe_result", "Mat44");
  TRANSFER_INPUTPLUG_TO_DFGPORT("foot_L_footSolver_klOp_toeFK", "foot_L_defConstraint_klOp_constrainees", "Mat44");
  TRANSFER_INPUTPLUG_TO_DFGPORT("neck_M_defConstraint_klOp_constrainers", "neck_M_defConstraint_klOp_constrainees", "Mat44");

  return true;

}


///////////////////////////////////////////////////////////////////////////////
//
//
///////////////////////////////////////////////////////////////////////////////
void bob2::transferStaticOutputValuesToMaya(MPlug& plug, MDataBlock& data, bool isDeformer){

  if(_isTransferingInputs)
  {
    return;
  }

  MStatus stat;
  std::string plugName(plug.name(&stat).asChar());
  FabricSplice::Logging::AutoTimer timer("Maya::transferOutputValuesToMaya()");

  if( plug.isElement() )
  {
    plug = plug.array();
  }

  
  TRANSFER_DFGPORT_TO_OUTPUTPLUG("mainSrt_M_rigScale_klOp_target", "mainSrt_M_rigScale_klOp_target", "Mat44");
  TRANSFER_DFGPORT_TO_OUTPUTPLUG("cog_M_cog_To_globalSRT_poseCns_spine_M_cog_ctrlSpace", "cog_M_cog_To_globalSRT_poseCns_spine_M_cog_ctrlSpace", "Mat44");
  TRANSFER_DFGPORT_TO_OUTPUTPLUG("spine_M_spine_klOp_outputs", "spine_M_spine_klOp_outputs", "Mat44");
  TRANSFER_DFGPORT_TO_OUTPUTPLUG("neck01_M_neck01_To_neckBase_poseCns_neck_M_neck01_ctrlSpace", "neck01_M_neck01_To_neckBase_poseCns_neck_M_neck01_ctrlSpace", "Mat44");
  TRANSFER_DFGPORT_TO_OUTPUTPLUG("clavicle_L_clavicle_To_spineEnd_poseCns_clavicle_L_clavicle_ctrlSpace", "clavicle_L_clavicle_To_spineEnd_poseCns_clavicle_L_clavicle_ctrlSpace", "Mat44");
  TRANSFER_DFGPORT_TO_OUTPUTPLUG("IK_L_IK_To_globalSRT_poseCns_arm_L_IK_ctrlSpace", "IK_L_IK_To_globalSRT_poseCns_arm_L_IK_ctrlSpace", "Mat44");
  TRANSFER_DFGPORT_TO_OUTPUTPLUG("UpV_L_UpV_To_globalSRT_poseCns_arm_L_UpV_ctrlSpace", "UpV_L_UpV_To_globalSRT_poseCns_arm_L_UpV_ctrlSpace", "Mat44");
  TRANSFER_DFGPORT_TO_OUTPUTPLUG("bicepFK_L_bicepFK_To_root_poseCns_arm_L_bicepFK_ctrlSpace", "bicepFK_L_bicepFK_To_root_poseCns_arm_L_bicepFK_ctrlSpace", "Mat44");
  TRANSFER_DFGPORT_TO_OUTPUTPLUG("ikPosition_L_ikPosition_To_root_poseCns_arm_L_ikPosition_null", "ikPosition_L_ikPosition_To_root_poseCns_arm_L_ikPosition_null", "Mat44");
  TRANSFER_DFGPORT_TO_OUTPUTPLUG("arm_L_ikSolver_klOp_bone0Out", "arm_L_ikSolver_klOp_bone0Out", "Mat44");
  TRANSFER_DFGPORT_TO_OUTPUTPLUG("arm_L_ikSolver_klOp_bone1Out", "arm_L_ikSolver_klOp_bone1Out", "Mat44");
  TRANSFER_DFGPORT_TO_OUTPUTPLUG("arm_L_ikSolver_klOp_bone2Out", "arm_L_ikSolver_klOp_bone2Out", "Mat44");
  TRANSFER_DFGPORT_TO_OUTPUTPLUG("arm_L_ikSolver_klOp_midJointOut", "arm_L_ikSolver_klOp_midJointOut", "Mat44");
  TRANSFER_DFGPORT_TO_OUTPUTPLUG("IK_L_IK_To_globalSRT_poseCns_leg_L_IK_ctrlSpace", "IK_L_IK_To_globalSRT_poseCns_leg_L_IK_ctrlSpace", "Mat44");
  TRANSFER_DFGPORT_TO_OUTPUTPLUG("pivotAll_L_pivotAll_To_ikHandle_poseCns_foot_L_pivotAll_loc", "pivotAll_L_pivotAll_To_ikHandle_poseCns_foot_L_pivotAll_loc", "Mat44");
  TRANSFER_DFGPORT_TO_OUTPUTPLUG("foot_L_footPivot_klOp_result", "foot_L_footPivot_klOp_result", "Mat44");
  TRANSFER_DFGPORT_TO_OUTPUTPLUG("UpV_L_UpV_To_globalSRT_poseCns_leg_L_UpV_ctrlSpace", "UpV_L_UpV_To_globalSRT_poseCns_leg_L_UpV_ctrlSpace", "Mat44");
  TRANSFER_DFGPORT_TO_OUTPUTPLUG("femurFK_L_femurFK_To_pelvisInput_poseCns_leg_L_femurFK_ctrlSpace", "femurFK_L_femurFK_To_pelvisInput_poseCns_leg_L_femurFK_ctrlSpace", "Mat44");
  TRANSFER_DFGPORT_TO_OUTPUTPLUG("ikRootPosition_L_ikRootPosition_To_pelvisInput_poseCns_leg_L_ikRootPosition_null", "ikRootPosition_L_ikRootPosition_To_pelvisInput_poseCns_leg_L_ikRootPosition_null", "Mat44");
  TRANSFER_DFGPORT_TO_OUTPUTPLUG("leg_L_ikSolver_klOp_bone0Out", "leg_L_ikSolver_klOp_bone0Out", "Mat44");
  TRANSFER_DFGPORT_TO_OUTPUTPLUG("leg_L_ikSolver_klOp_bone1Out", "leg_L_ikSolver_klOp_bone1Out", "Mat44");
  TRANSFER_DFGPORT_TO_OUTPUTPLUG("leg_L_ikSolver_klOp_bone2Out", "leg_L_ikSolver_klOp_bone2Out", "Mat44");
  TRANSFER_DFGPORT_TO_OUTPUTPLUG("leg_L_ikSolver_klOp_midJointOut", "leg_L_ikSolver_klOp_midJointOut", "Mat44");
  TRANSFER_DFGPORT_TO_OUTPUTPLUG("ankleFK_L_ankleFK_To_legEndFK_poseCns_foot_L_ankleFK_ctrlSpace", "ankleFK_L_ankleFK_To_legEndFK_poseCns_foot_L_ankleFK_ctrlSpace", "Mat44");
  TRANSFER_DFGPORT_TO_OUTPUTPLUG("foot_L_footSolver_klOp_ankle_result", "foot_L_footSolver_klOp_ankle_result", "Mat44");
  TRANSFER_DFGPORT_TO_OUTPUTPLUG("foot_L_footSolver_klOp_toe_result", "foot_L_footSolver_klOp_toe_result", "Mat44");
  TRANSFER_DFGPORT_TO_OUTPUTPLUG("neck_M_defConstraint_klOp_constrainees", "neck_M_defConstraint_klOp_constrainees", "Mat44");
  TRANSFER_DFGPORT_TO_OUTPUTPLUG("clavicle_L_defConstraint_klOp_constrainee", "clavicle_L_defConstraint_klOp_constrainee", "Mat44");
  TRANSFER_DFGPORT_TO_OUTPUTPLUG("arm_L_defConstraint_klOp_constrainees", "arm_L_defConstraint_klOp_constrainees", "Mat44");
  TRANSFER_DFGPORT_TO_OUTPUTPLUG("leg_L_defConstraint_klOp_constrainees", "leg_L_defConstraint_klOp_constrainees", "Mat44");
  TRANSFER_DFGPORT_TO_OUTPUTPLUG("foot_L_defConstraint_klOp_constrainees", "foot_L_defConstraint_klOp_constrainees", "Mat44");
  TRANSFER_DFGPORT_TO_OUTPUTPLUG("spine_M_defConstraint_klOp_constrainees", "spine_M_defConstraint_klOp_constrainees", "Mat44");
  TRANSFER_DFGPORT_TO_OUTPUTPLUG("spine_M_pelvisDefConstraint_klOp_constrainee", "spine_M_pelvisDefConstraint_klOp_constrainee", "Mat44");
}