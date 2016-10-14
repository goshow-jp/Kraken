//
// Copyright (C) goshow
// 
// File: Test2Node.h
//
// Dependency Graph Node: bob2
//
// Author: Maya Plug-in Wizard 2.0
//
#pragma once

#define FEC_SHARED
#define FECS_SHARED
#include "FabricDFGWidget.h"
#include "FabricDFGBaseInterface.h"

#include <maya/MPxNode.h>
#include <maya/MFnNumericAttribute.h>
#include <maya/MTypeId.h> 
#include <maya/MNodeMessage.h>
#include <maya/MStringArray.h>

 
class bob2 : public MPxNode, public FabricDFGBaseInterface
{
public:
  static void* creator();
  static MStatus initialize();

  bob2();
  void postConstructor();
  ~bob2();

  // implement pure virtual functions
  virtual MObject getThisMObject() { return thisMObject(); }
  virtual MPlug getSaveDataPlug() { return MPlug(thisMObject(), saveData); }
  virtual MPlug getRefFilePathPlug() { return MPlug(thisMObject(), refFilePath); }

  void loadJSON();
  MStatus compute(const MPlug& plug, MDataBlock& data);
  bool transferStaticInputValuesToDFG(MPlug& plug, MDataBlock& data);
  void transferStaticOutputValuesToMaya(MPlug& plug, MDataBlock& data, bool isDeformer = false);

  // node attributes
  static MTypeId id;
  static MObject saveData;
  static MObject evalID;
  static MObject refFilePath;
  static MObject drawDebug;
  static MObject rigScale;

  
  static MObject m_mainSrt_M_rigScale_klOp_target;
  static MObject m_mainSrt_M_Offset_ctrl;
  static MObject m_cog_M_cog_To_globalSRT_poseCns_spine_M_cog_ctrlSpace;
  static MObject m_spine_M_cog_ctrl;
  static MObject m_spine_M_spine_klOp_length;
  static MObject m_spine_M_spine_klOp_base;
  static MObject m_spine_M_spine_klOp_baseHandle;
  static MObject m_spine_M_spine_klOp_tipHandle;
  static MObject m_spine_M_spine_klOp_tip;
  static MObject m_spine_M_spine_klOp_outputs;
  static MObject m_spine_M_pelvis_ctrl;
  static MObject m_neck01_M_neck01_To_neckBase_poseCns_neck_M_neck01_ctrlSpace;
  static MObject m_neck_M_neck01_ctrl;
  static MObject m_neck_M_neck02_ctrl;
  static MObject m_clavicle_L_clavicle_To_spineEnd_poseCns_clavicle_L_clavicle_ctrlSpace;
  static MObject m_clavicle_L_clavicle_ctrl;
  static MObject m_IK_L_IK_To_globalSRT_poseCns_arm_L_IK_ctrlSpace;
  static MObject m_UpV_L_UpV_To_globalSRT_poseCns_arm_L_UpV_ctrlSpace;
  static MObject m_bicepFK_L_bicepFK_To_root_poseCns_arm_L_bicepFK_ctrlSpace;
  static MObject m_ikPosition_L_ikPosition_To_root_poseCns_arm_L_ikPosition_null;
  static MObject m_arm_L_ikSolver_klOp_rightSide;
  static MObject m_arm_L_ikSolver_klOp_ikblend;
  static MObject m_arm_L_ikSolver_klOp_root;
  static MObject m_arm_L_ikSolver_klOp_bone0FK;
  static MObject m_arm_L_ikSolver_klOp_bone1FK;
  static MObject m_arm_L_ikSolver_klOp_ikHandle;
  static MObject m_arm_L_ikSolver_klOp_upV;
  static MObject m_arm_L_ikSolver_klOp_bone0Len;
  static MObject m_arm_L_ikSolver_klOp_bone1Len;
  static MObject m_arm_L_ikSolver_klOp_bone0Out;
  static MObject m_arm_L_ikSolver_klOp_bone1Out;
  static MObject m_arm_L_ikSolver_klOp_bone2Out;
  static MObject m_arm_L_ikSolver_klOp_midJointOut;
  static MObject m_IK_L_IK_To_globalSRT_poseCns_leg_L_IK_ctrlSpace;
  static MObject m_leg_L_IK_ctrl;
  static MObject m_pivotAll_L_pivotAll_To_ikHandle_poseCns_foot_L_pivotAll_loc;
  static MObject m_foot_L_footPivot_klOp_rightSide;
  static MObject m_foot_L_footPivot_klOp_footRock;
  static MObject m_foot_L_footPivot_klOp_footBank;
  static MObject m_foot_L_footPivot_klOp_pivotAll;
  static MObject m_foot_L_footPivot_klOp_backPivot;
  static MObject m_foot_L_footPivot_klOp_frontPivot;
  static MObject m_foot_L_footPivot_klOp_outerPivot;
  static MObject m_foot_L_footPivot_klOp_innerPivot;
  static MObject m_foot_L_footPivot_klOp_result;
  static MObject m_foot_L_ankleIK_ctrl;
  static MObject m_UpV_L_UpV_To_globalSRT_poseCns_leg_L_UpV_ctrlSpace;
  static MObject m_femurFK_L_femurFK_To_pelvisInput_poseCns_leg_L_femurFK_ctrlSpace;
  static MObject m_ikRootPosition_L_ikRootPosition_To_pelvisInput_poseCns_leg_L_ikRootPosition_null;
  static MObject m_leg_L_ikSolver_klOp_rightSide;
  static MObject m_leg_L_ikSolver_klOp_ikblend;
  static MObject m_leg_L_ikSolver_klOp_root;
  static MObject m_leg_L_ikSolver_klOp_bone0FK;
  static MObject m_leg_L_ikSolver_klOp_bone1FK;
  static MObject m_leg_L_ikSolver_klOp_upV;
  static MObject m_leg_L_ikSolver_klOp_bone0Len;
  static MObject m_leg_L_ikSolver_klOp_bone1Len;
  static MObject m_leg_L_ikSolver_klOp_bone0Out;
  static MObject m_leg_L_ikSolver_klOp_bone1Out;
  static MObject m_leg_L_ikSolver_klOp_bone2Out;
  static MObject m_leg_L_ikSolver_klOp_midJointOut;
  static MObject m_leg_L_shinFK_ctrl;
  static MObject m_ankleFK_L_ankleFK_To_legEndFK_poseCns_foot_L_ankleFK_ctrlSpace;
  static MObject m_foot_L_footSolver_klOp_ikBlend;
  static MObject m_foot_L_footSolver_klOp_ankleLen;
  static MObject m_foot_L_footSolver_klOp_toeLen;
  static MObject m_foot_L_footSolver_klOp_ankleIK;
  static MObject m_foot_L_footSolver_klOp_toeIK;
  static MObject m_foot_L_footSolver_klOp_ankleFK;
  static MObject m_foot_L_footSolver_klOp_toeFK;
  static MObject m_foot_L_footSolver_klOp_ankle_result;
  static MObject m_foot_L_footSolver_klOp_toe_result;
  static MObject m_mainSrt_M_SRT_ctrl;
  static MObject m_neck_M_defConstraint_klOp_constrainers;
  static MObject m_neck_M_defConstraint_klOp_constrainees;
  static MObject m_clavicle_L_defConstraint_klOp_constrainee;
  static MObject m_arm_L_defConstraint_klOp_constrainees;
  static MObject m_leg_L_defConstraint_klOp_constrainees;
  static MObject m_foot_L_defConstraint_klOp_constrainees;
  static MObject m_spine_M_defConstraint_klOp_constrainees;
  static MObject m_spine_M_pelvisDefConstraint_klOp_constrainee;
};