# -*- coding: utf-8 -*-
u"""
Make canvasNode into static one.
Read input/output port into static attributes.
"""
import sys

import maya.api.OpenMaya as api
import maya.OpenMaya as oldapi


from monolithic_canvas_template import CanvasWrapper
# ==================================================================================

MAYA_API_VERSION = oldapi.MGlobal.apiVersion()
__author__ = 'yamahigashi'
__version__ = '0.0.1'

_TYPE_IDS = 0x001A0002
maya_useNewAPI = True


# ==================================================================================
class BobCanvas(CanvasWrapper):
    type_name = 'BobCanvas'
    type_id = api.MTypeId(_TYPE_IDS)
    canvasPath = r"D:\fabric\bob.canvas"
    # canvasPath = r"D:\fabric\test_cache_node.canvas"

    ports = [
        {
            "objectType": "ExecPort",
            "name": "exec",
            "nodePortType": "IO",
            "execPortType": "IO",
            "typeSpec": "Execute"
        },
        {
            "objectType": "ExecPort",
            "metadata": {
                "uiPersistValue": "true"
            },
            "name": "drawDebug",
            "nodePortType": "Out",
            "execPortType": "In"
        },
        {
            "objectType": "ExecPort",
            "metadata": {
                "uiPersistValue": "true"
            },
            "name": "rigScale",
            "nodePortType": "Out",
            "execPortType": "In"
        },
        {
            "objectType": "ExecPort",
            "name": "mainSrt_M_rigScale_klOp_target",
            "nodePortType": "In",
            "execPortType": "Out",
            "typeSpec": "Mat44"
        },
        {
            "objectType": "ExecPort",
            "metadata": {
                "uiPersistValue": "true"
            },
            "name": "mainSrt_M_Offset_ctrl",
            "nodePortType": "Out",
            "execPortType": "In",
            "typeSpec": "Mat44"
        },
        {
            "objectType": "ExecPort",
            "name": "cog_M_cog_To_globalSRT_poseCns_spine_M_cog_ctrlSpace",
            "nodePortType": "In",
            "execPortType": "Out",
            "typeSpec": "Mat44"
        },
        {
            "objectType": "ExecPort",
            "metadata": {
                "uiPersistValue": "true"
            },
            "name": "spine_M_cog_ctrl",
            "nodePortType": "Out",
            "execPortType": "In",
            "typeSpec": "Mat44"
        },
        {
            "objectType": "ExecPort",
            "metadata": {
                "uiPersistValue": "true"
            },
            "name": "spine_M_spine_klOp_length",
            "nodePortType": "Out",
            "execPortType": "In",
            "typeSpec": "Scalar"
        },
        {
            "objectType": "ExecPort",
            "metadata": {
                "uiPersistValue": "true"
            },
            "name": "spine_M_spine_klOp_base",
            "nodePortType": "Out",
            "execPortType": "In",
            "typeSpec": "Mat44"
        },
        {
            "objectType": "ExecPort",
            "metadata": {
                "uiPersistValue": "true"
            },
            "name": "spine_M_spine_klOp_baseHandle",
            "nodePortType": "Out",
            "execPortType": "In",
            "typeSpec": "Mat44"
        },
        {
            "objectType": "ExecPort",
            "metadata": {
                "uiPersistValue": "true"
            },
            "name": "spine_M_spine_klOp_tipHandle",
            "nodePortType": "Out",
            "execPortType": "In",
            "typeSpec": "Mat44"
        },
        {
            "objectType": "ExecPort",
            "metadata": {
                "uiPersistValue": "true"
            },
            "name": "spine_M_spine_klOp_tip",
            "nodePortType": "Out",
            "execPortType": "In",
            "typeSpec": "Mat44"
        },
        {
            "objectType": "ExecPort",
            "name": "spine_M_spine_klOp_outputs",
            "nodePortType": "In",
            "execPortType": "Out",
            "typeSpec": "Mat44[]"
        },
        {
            "objectType": "ExecPort",
            "metadata": {
                "uiPersistValue": "true"
            },
            "name": "spine_M_pelvis_ctrl",
            "nodePortType": "Out",
            "execPortType": "In",
            "typeSpec": "Mat44"
        },
        {
            "objectType": "ExecPort",
            "name": "neck01_M_neck01_To_neckBase_poseCns_neck_M_neck01_ctrlSpace",
            "nodePortType": "In",
            "execPortType": "Out",
            "typeSpec": "Mat44"
        },
        {
            "objectType": "ExecPort",
            "metadata": {
                "uiPersistValue": "true"
            },
            "name": "neck_M_neck01_ctrl",
            "nodePortType": "Out",
            "execPortType": "In",
            "typeSpec": "Mat44"
        },
        {
            "objectType": "ExecPort",
            "metadata": {
                "uiPersistValue": "true"
            },
            "name": "neck_M_neck02_ctrl",
            "nodePortType": "Out",
            "execPortType": "In",
            "typeSpec": "Mat44"
        },
        {
            "objectType": "ExecPort",
            "name": "clavicle_R_clavicle_To_spineEnd_poseCns_clavicle_R_clavicle_ctrlSpace",
            "nodePortType": "In",
            "execPortType": "Out",
            "typeSpec": "Mat44"
        },
        {
            "objectType": "ExecPort",
            "metadata": {
                "uiPersistValue": "true"
            },
            "name": "clavicle_R_clavicle_ctrl",
            "nodePortType": "Out",
            "execPortType": "In",
            "typeSpec": "Mat44"
        },
        {
            "objectType": "ExecPort",
            "name": "IK_R_IK_To_globalSRT_poseCns_arm_R_IK_ctrlSpace",
            "nodePortType": "In",
            "execPortType": "Out",
            "typeSpec": "Mat44"
        },
        {
            "objectType": "ExecPort",
            "name": "UpV_R_UpV_To_globalSRT_poseCns_arm_R_UpV_ctrlSpace",
            "nodePortType": "In",
            "execPortType": "Out",
            "typeSpec": "Mat44"
        },
        {
            "objectType": "ExecPort",
            "name": "bicepFK_R_bicepFK_To_root_poseCns_arm_R_bicepFK_ctrlSpace",
            "nodePortType": "In",
            "execPortType": "Out",
            "typeSpec": "Mat44"
        },
        {
            "objectType": "ExecPort",
            "name": "ikPosition_R_ikPosition_To_root_poseCns_arm_R_ikPosition_null",
            "nodePortType": "In",
            "execPortType": "Out",
            "typeSpec": "Mat44"
        },
        {
            "objectType": "ExecPort",
            "metadata": {
                "uiPersistValue": "true"
            },
            "name": "arm_R_ikSolver_klOp_rightSide",
            "nodePortType": "Out",
            "execPortType": "In",
            "typeSpec": "Boolean"
        },
        {
            "objectType": "ExecPort",
            "metadata": {
                "uiPersistValue": "true"
            },
            "name": "arm_R_ikSolver_klOp_ikblend",
            "nodePortType": "Out",
            "execPortType": "In",
            "typeSpec": "Scalar"
        },
        {
            "objectType": "ExecPort",
            "metadata": {
                "uiPersistValue": "true"
            },
            "name": "arm_R_ikSolver_klOp_root",
            "nodePortType": "Out",
            "execPortType": "In",
            "typeSpec": "Mat44"
        },
        {
            "objectType": "ExecPort",
            "metadata": {
                "uiPersistValue": "true"
            },
            "name": "arm_R_ikSolver_klOp_bone0FK",
            "nodePortType": "Out",
            "execPortType": "In",
            "typeSpec": "Mat44"
        },
        {
            "objectType": "ExecPort",
            "metadata": {
                "uiPersistValue": "true"
            },
            "name": "arm_R_ikSolver_klOp_bone1FK",
            "nodePortType": "Out",
            "execPortType": "In",
            "typeSpec": "Mat44"
        },
        {
            "objectType": "ExecPort",
            "metadata": {
                "uiPersistValue": "true"
            },
            "name": "arm_R_ikSolver_klOp_ikHandle",
            "nodePortType": "Out",
            "execPortType": "In",
            "typeSpec": "Mat44"
        },
        {
            "objectType": "ExecPort",
            "metadata": {
                "uiPersistValue": "true"
            },
            "name": "arm_R_ikSolver_klOp_upV",
            "nodePortType": "Out",
            "execPortType": "In",
            "typeSpec": "Mat44"
        },
        {
            "objectType": "ExecPort",
            "metadata": {
                "uiPersistValue": "true"
            },
            "name": "arm_R_ikSolver_klOp_bone0Len",
            "nodePortType": "Out",
            "execPortType": "In",
            "typeSpec": "Scalar"
        },
        {
            "objectType": "ExecPort",
            "metadata": {
                "uiPersistValue": "true"
            },
            "name": "arm_R_ikSolver_klOp_bone1Len",
            "nodePortType": "Out",
            "execPortType": "In",
            "typeSpec": "Scalar"
        },
        {
            "objectType": "ExecPort",
            "name": "arm_R_ikSolver_klOp_bone0Out",
            "nodePortType": "In",
            "execPortType": "Out",
            "typeSpec": "Mat44"
        },
        {
            "objectType": "ExecPort",
            "name": "arm_R_ikSolver_klOp_bone1Out",
            "nodePortType": "In",
            "execPortType": "Out",
            "typeSpec": "Mat44"
        },
        {
            "objectType": "ExecPort",
            "name": "arm_R_ikSolver_klOp_bone2Out",
            "nodePortType": "In",
            "execPortType": "Out",
            "typeSpec": "Mat44"
        },
        {
            "objectType": "ExecPort",
            "name": "arm_R_ikSolver_klOp_midJointOut",
            "nodePortType": "In",
            "execPortType": "Out",
            "typeSpec": "Mat44"
        },
        {
            "objectType": "ExecPort",
            "name": "IK_R_IK_To_globalSRT_poseCns_leg_R_IK_ctrlSpace",
            "nodePortType": "In",
            "execPortType": "Out",
            "typeSpec": "Mat44"
        },
        {
            "objectType": "ExecPort",
            "metadata": {
                "uiPersistValue": "true"
            },
            "name": "leg_R_IK_ctrl",
            "nodePortType": "Out",
            "execPortType": "In",
            "typeSpec": "Mat44"
        },
        {
            "objectType": "ExecPort",
            "name": "pivotAll_R_pivotAll_To_ikHandle_poseCns_foot_R_pivotAll_loc",
            "nodePortType": "In",
            "execPortType": "Out",
            "typeSpec": "Mat44"
        },
        {
            "objectType": "ExecPort",
            "metadata": {
                "uiPersistValue": "true"
            },
            "name": "foot_R_footPivot_klOp_rightSide",
            "nodePortType": "Out",
            "execPortType": "In",
            "typeSpec": "Boolean"
        },
        {
            "objectType": "ExecPort",
            "metadata": {
                "uiPersistValue": "true"
            },
            "name": "foot_R_footPivot_klOp_footRock",
            "nodePortType": "Out",
            "execPortType": "In",
            "typeSpec": "Scalar"
        },
        {
            "objectType": "ExecPort",
            "metadata": {
                "uiPersistValue": "true"
            },
            "name": "foot_R_footPivot_klOp_footBank",
            "nodePortType": "Out",
            "execPortType": "In",
            "typeSpec": "Scalar"
        },
        {
            "objectType": "ExecPort",
            "metadata": {
                "uiPersistValue": "true"
            },
            "name": "foot_R_footPivot_klOp_pivotAll",
            "nodePortType": "Out",
            "execPortType": "In",
            "typeSpec": "Mat44"
        },
        {
            "objectType": "ExecPort",
            "metadata": {
                "uiPersistValue": "true"
            },
            "name": "foot_R_footPivot_klOp_backPivot",
            "nodePortType": "Out",
            "execPortType": "In",
            "typeSpec": "Mat44"
        },
        {
            "objectType": "ExecPort",
            "metadata": {
                "uiPersistValue": "true"
            },
            "name": "foot_R_footPivot_klOp_frontPivot",
            "nodePortType": "Out",
            "execPortType": "In",
            "typeSpec": "Mat44"
        },
        {
            "objectType": "ExecPort",
            "metadata": {
                "uiPersistValue": "true"
            },
            "name": "foot_R_footPivot_klOp_outerPivot",
            "nodePortType": "Out",
            "execPortType": "In",
            "typeSpec": "Mat44"
        },
        {
            "objectType": "ExecPort",
            "metadata": {
                "uiPersistValue": "true"
            },
            "name": "foot_R_footPivot_klOp_innerPivot",
            "nodePortType": "Out",
            "execPortType": "In",
            "typeSpec": "Mat44"
        },
        {
            "objectType": "ExecPort",
            "name": "foot_R_footPivot_klOp_result",
            "nodePortType": "In",
            "execPortType": "Out",
            "typeSpec": "Mat44"
        },
        {
            "objectType": "ExecPort",
            "metadata": {
                "uiPersistValue": "true"
            },
            "name": "foot_R_ankleIK_ctrl",
            "nodePortType": "Out",
            "execPortType": "In",
            "typeSpec": "Mat44"
        },
        {
            "objectType": "ExecPort",
            "name": "UpV_R_UpV_To_globalSRT_poseCns_leg_R_UpV_ctrlSpace",
            "nodePortType": "In",
            "execPortType": "Out",
            "typeSpec": "Mat44"
        },
        {
            "objectType": "ExecPort",
            "name": "femurFK_R_femurFK_To_pelvisInput_poseCns_leg_R_femurFK_ctrlSpace",
            "nodePortType": "In",
            "execPortType": "Out",
            "typeSpec": "Mat44"
        },
        {
            "objectType": "ExecPort",
            "name": "ikRootPosition_R_ikRootPosition_To_pelvisInput_poseCns_leg_R_ikRootPosition_null",
            "nodePortType": "In",
            "execPortType": "Out",
            "typeSpec": "Mat44"
        },
        {
            "objectType": "ExecPort",
            "metadata": {
                "uiPersistValue": "true"
            },
            "name": "leg_R_ikSolver_klOp_rightSide",
            "nodePortType": "Out",
            "execPortType": "In",
            "typeSpec": "Boolean"
        },
        {
            "objectType": "ExecPort",
            "metadata": {
                "uiPersistValue": "true"
            },
            "name": "leg_R_ikSolver_klOp_ikblend",
            "nodePortType": "Out",
            "execPortType": "In",
            "typeSpec": "Scalar"
        },
        {
            "objectType": "ExecPort",
            "metadata": {
                "uiPersistValue": "true"
            },
            "name": "leg_R_ikSolver_klOp_root",
            "nodePortType": "Out",
            "execPortType": "In",
            "typeSpec": "Mat44"
        },
        {
            "objectType": "ExecPort",
            "metadata": {
                "uiPersistValue": "true"
            },
            "name": "leg_R_ikSolver_klOp_bone0FK",
            "nodePortType": "Out",
            "execPortType": "In",
            "typeSpec": "Mat44"
        },
        {
            "objectType": "ExecPort",
            "metadata": {
                "uiPersistValue": "true"
            },
            "name": "leg_R_ikSolver_klOp_bone1FK",
            "nodePortType": "Out",
            "execPortType": "In",
            "typeSpec": "Mat44"
        },
        {
            "objectType": "ExecPort",
            "metadata": {
                "uiPersistValue": "true"
            },
            "name": "leg_R_ikSolver_klOp_upV",
            "nodePortType": "Out",
            "execPortType": "In",
            "typeSpec": "Mat44"
        },
        {
            "objectType": "ExecPort",
            "metadata": {
                "uiPersistValue": "true"
            },
            "name": "leg_R_ikSolver_klOp_bone0Len",
            "nodePortType": "Out",
            "execPortType": "In",
            "typeSpec": "Scalar"
        },
        {
            "objectType": "ExecPort",
            "metadata": {
                "uiPersistValue": "true"
            },
            "name": "leg_R_ikSolver_klOp_bone1Len",
            "nodePortType": "Out",
            "execPortType": "In",
            "typeSpec": "Scalar"
        },
        {
            "objectType": "ExecPort",
            "name": "leg_R_ikSolver_klOp_bone0Out",
            "nodePortType": "In",
            "execPortType": "Out",
            "typeSpec": "Mat44"
        },
        {
            "objectType": "ExecPort",
            "name": "leg_R_ikSolver_klOp_bone1Out",
            "nodePortType": "In",
            "execPortType": "Out",
            "typeSpec": "Mat44"
        },
        {
            "objectType": "ExecPort",
            "name": "leg_R_ikSolver_klOp_bone2Out",
            "nodePortType": "In",
            "execPortType": "Out",
            "typeSpec": "Mat44"
        },
        {
            "objectType": "ExecPort",
            "name": "leg_R_ikSolver_klOp_midJointOut",
            "nodePortType": "In",
            "execPortType": "Out",
            "typeSpec": "Mat44"
        },
        {
            "objectType": "ExecPort",
            "metadata": {
                "uiPersistValue": "true"
            },
            "name": "leg_R_shinFK_ctrl",
            "nodePortType": "Out",
            "execPortType": "In",
            "typeSpec": "Mat44"
        },
        {
            "objectType": "ExecPort",
            "name": "temp",
            "nodePortType": "In",
            "execPortType": "Out"
        },
        {
            "objectType": "ExecPort",
            "name": "ankleFK_R_ankleFK_To_legEndFK_poseCns_foot_R_ankleFK_ctrlSpace",
            "nodePortType": "In",
            "execPortType": "Out",
            "typeSpec": "Mat44"
        },
        {
            "objectType": "ExecPort",
            "metadata": {
                "uiPersistValue": "true"
            },
            "name": "foot_R_footSolver_klOp_ikBlend",
            "nodePortType": "Out",
            "execPortType": "In",
            "typeSpec": "Scalar"
        },
        {
            "objectType": "ExecPort",
            "metadata": {
                "uiPersistValue": "true"
            },
            "name": "foot_R_footSolver_klOp_ankleLen",
            "nodePortType": "Out",
            "execPortType": "In",
            "typeSpec": "Scalar"
        },
        {
            "objectType": "ExecPort",
            "metadata": {
                "uiPersistValue": "true"
            },
            "name": "foot_R_footSolver_klOp_toeLen",
            "nodePortType": "Out",
            "execPortType": "In",
            "typeSpec": "Scalar"
        },
        {
            "objectType": "ExecPort",
            "metadata": {
                "uiPersistValue": "true"
            },
            "name": "foot_R_footSolver_klOp_ankleIK",
            "nodePortType": "Out",
            "execPortType": "In",
            "typeSpec": "Mat44"
        },
        {
            "objectType": "ExecPort",
            "metadata": {
                "uiPersistValue": "true"
            },
            "name": "foot_R_footSolver_klOp_toeIK",
            "nodePortType": "Out",
            "execPortType": "In",
            "typeSpec": "Mat44"
        },
        {
            "objectType": "ExecPort",
            "metadata": {
                "uiPersistValue": "true"
            },
            "name": "foot_R_footSolver_klOp_ankleFK",
            "nodePortType": "Out",
            "execPortType": "In",
            "typeSpec": "Mat44"
        },
        {
            "objectType": "ExecPort",
            "metadata": {
                "uiPersistValue": "true"
            },
            "name": "foot_R_footSolver_klOp_toeFK",
            "nodePortType": "Out",
            "execPortType": "In",
            "typeSpec": "Mat44"
        },
        {
            "objectType": "ExecPort",
            "name": "foot_R_footSolver_klOp_ankle_result",
            "nodePortType": "In",
            "execPortType": "Out",
            "typeSpec": "Mat44"
        },
        {
            "objectType": "ExecPort",
            "name": "foot_R_footSolver_klOp_toe_result",
            "nodePortType": "In",
            "execPortType": "Out",
            "typeSpec": "Mat44"
        },
        {
            "objectType": "ExecPort",
            "metadata": {
                "uiPersistValue": "true"
            },
            "name": "mainSrt_M_SRT_ctrl",
            "nodePortType": "Out",
            "execPortType": "In",
            "typeSpec": "Mat44"
        },
        {
            "objectType": "ExecPort",
            "metadata": {
                "uiPersistValue": "true"
            },
            "name": "neck_M_defConstraint_klOp_constrainers",
            "nodePortType": "Out",
            "execPortType": "In",
            "typeSpec": "Mat44[]"
        },
        {
            "objectType": "ExecPort",
            "name": "neck_M_defConstraint_klOp_constrainees",
            "nodePortType": "In",
            "execPortType": "Out",
            "typeSpec": "Mat44[]"
        },
        {
            "objectType": "ExecPort",
            "name": "clavicle_R_defConstraint_klOp_constrainee",
            "nodePortType": "In",
            "execPortType": "Out",
            "typeSpec": "Mat44"
        },
        {
            "objectType": "ExecPort",
            "name": "arm_R_defConstraint_klOp_constrainees",
            "nodePortType": "In",
            "execPortType": "Out",
            "typeSpec": "Mat44[]"
        },
        {
            "objectType": "ExecPort",
            "name": "leg_R_defConstraint_klOp_constrainees",
            "nodePortType": "In",
            "execPortType": "Out",
            "typeSpec": "Mat44[]"
        },
        {
            "objectType": "ExecPort",
            "name": "foot_R_defConstraint_klOp_constrainees",
            "nodePortType": "In",
            "execPortType": "Out",
            "typeSpec": "Mat44[]"
        },
        {
            "objectType": "ExecPort",
            "name": "spine_M_defConstraint_klOp_constrainees",
            "nodePortType": "In",
            "execPortType": "Out",
            "typeSpec": "Mat44[]"
        },
        {
            "objectType": "ExecPort",
            "name": "spine_M_pelvisDefConstraint_klOp_constrainee",
            "nodePortType": "In",
            "execPortType": "Out",
            "typeSpec": "Mat44"
        }
    ]

    all_ports = [
        {"name": "IK_R_IK_To_globalSRT_poseCns_arm_R_IK_ctrlSpace",                                  "execPortType": "Out", "typeSpec": "Mat44"},
        {"name": "IK_R_IK_To_globalSRT_poseCns_leg_R_IK_ctrlSpace",                                  "execPortType": "Out", "typeSpec": "Mat44"},

        {"name": "UpV_R_UpV_To_globalSRT_poseCns_arm_R_UpV_ctrlSpace",                               "execPortType": "Out", "typeSpec": "Mat44"},
        {"name": "UpV_R_UpV_To_globalSRT_poseCns_leg_R_UpV_ctrlSpace",                               "execPortType": "Out", "typeSpec": "Mat44"},

        {"name": "ankleFK_R_ankleFK_To_legEndFK_poseCns_foot_R_ankleFK_ctrlSpace",                   "execPortType": "Out", "typeSpec": "Mat44"},

        {"name": "arm_R_defConstraint_klOp_constrainees",                                            "execPortType": "Out", "typeSpec": "Mat44[]"},
        {"name": "arm_R_ikSolver_klOp_bone0FK",                                                      "execPortType": "In",  "typeSpec": "Mat44"},
        {"name": "arm_R_ikSolver_klOp_bone0Len",                                                     "execPortType": "In",  "typeSpec": "Scalar"},
        {"name": "arm_R_ikSolver_klOp_bone0Out",                                                     "execPortType": "Out", "typeSpec": "Mat44"},
        {"name": "arm_R_ikSolver_klOp_bone1FK",                                                      "execPortType": "In",  "typeSpec": "Mat44"},
        {"name": "arm_R_ikSolver_klOp_bone1Len",                                                     "execPortType": "In",  "typeSpec": "Scalar"},
        {"name": "arm_R_ikSolver_klOp_bone1Out",                                                     "execPortType": "Out", "typeSpec": "Mat44"},
        {"name": "arm_R_ikSolver_klOp_bone2Out",                                                     "execPortType": "Out", "typeSpec": "Mat44"},
        {"name": "arm_R_ikSolver_klOp_ikHandle",                                                     "execPortType": "In",  "typeSpec": "Mat44"},
        {"name": "arm_R_ikSolver_klOp_ikblend",                                                      "execPortType": "In",  "typeSpec": "Scalar"},
        {"name": "arm_R_ikSolver_klOp_midJointOut",                                                  "execPortType": "Out", "typeSpec": "Mat44"},
        {"name": "arm_R_ikSolver_klOp_rightSide",                                                    "execPortType": "In",  "typeSpec": "Boolean"},
        {"name": "arm_R_ikSolver_klOp_root",                                                         "execPortType": "In",  "typeSpec": "Mat44"},
        {"name": "arm_R_ikSolver_klOp_upV",                                                          "execPortType": "In",  "typeSpec": "Mat44"},
        {"name": "bicepFK_R_bicepFK_To_root_poseCns_arm_R_bicepFK_ctrlSpace",                        "execPortType": "Out", "typeSpec": "Mat44"},
        {"name": "clavicle_R_clavicle_To_spineEnd_poseCns_clavicle_R_clavicle_ctrlSpace",            "execPortType": "Out", "typeSpec": "Mat44"},
        {"name": "clavicle_R_clavicle_ctrl",                                                         "execPortType": "In",  "typeSpec": "Mat44"},
        {"name": "clavicle_R_defConstraint_klOp_constrainee",                                        "execPortType": "Out", "typeSpec": "Mat44"},
        {"name": "cog_M_cog_To_globalSRT_poseCns_spine_M_cog_ctrlSpace",                             "execPortType": "Out", "typeSpec": "Mat44"},
        {"name": "femurFK_R_femurFK_To_pelvisInput_poseCns_leg_R_femurFK_ctrlSpace",                 "execPortType": "Out", "typeSpec": "Mat44"},
        {"name": "foot_R_ankleIK_ctrl",                                                              "execPortType": "In",  "typeSpec": "Mat44"},
        {"name": "foot_R_defConstraint_klOp_constrainees",                                           "execPortType": "Out", "typeSpec": "Mat44[]"},
        {"name": "foot_R_footPivot_klOp_backPivot",                                                  "execPortType": "In",  "typeSpec": "Mat44"},
        {"name": "foot_R_footPivot_klOp_footBank",                                                   "execPortType": "In",  "typeSpec": "Scalar"},
        {"name": "foot_R_footPivot_klOp_footRock",                                                   "execPortType": "In",  "typeSpec": "Scalar"},
        {"name": "foot_R_footPivot_klOp_frontPivot",                                                 "execPortType": "In",  "typeSpec": "Mat44"},
        {"name": "foot_R_footPivot_klOp_innerPivot",                                                 "execPortType": "In",  "typeSpec": "Mat44"},
        {"name": "foot_R_footPivot_klOp_outerPivot",                                                 "execPortType": "In",  "typeSpec": "Mat44"},
        {"name": "foot_R_footPivot_klOp_pivotAll",                                                   "execPortType": "In",  "typeSpec": "Mat44"},
        {"name": "foot_R_footPivot_klOp_result",                                                     "execPortType": "Out", "typeSpec": "Mat44"},
        {"name": "foot_R_footPivot_klOp_rightSide",                                                  "execPortType": "In",  "typeSpec": "Boolean"},
        {"name": "foot_R_footSolver_klOp_ankleFK",                                                   "execPortType": "In",  "typeSpec": "Mat44"},
        {"name": "foot_R_footSolver_klOp_ankleIK",                                                   "execPortType": "In",  "typeSpec": "Mat44"},
        {"name": "foot_R_footSolver_klOp_ankleLen",                                                  "execPortType": "In",  "typeSpec": "Scalar"},
        {"name": "foot_R_footSolver_klOp_ankle_result",                                              "execPortType": "Out", "typeSpec": "Mat44"},
        {"name": "foot_R_footSolver_klOp_ikBlend",                                                   "execPortType": "In",  "typeSpec": "Scalar"},
        {"name": "foot_R_footSolver_klOp_toeFK",                                                     "execPortType": "In",  "typeSpec": "Mat44"},
        {"name": "foot_R_footSolver_klOp_toeIK",                                                     "execPortType": "In",  "typeSpec": "Mat44"},
        {"name": "foot_R_footSolver_klOp_toeLen",                                                    "execPortType": "In",  "typeSpec": "Scalar"},
        {"name": "foot_R_footSolver_klOp_toe_result",                                                "execPortType": "Out", "typeSpec": "Mat44"},
        {"name": "ikPosition_R_ikPosition_To_root_poseCns_arm_R_ikPosition_null",                    "execPortType": "Out", "typeSpec": "Mat44"},
        {"name": "ikRootPosition_R_ikRootPosition_To_pelvisInput_poseCns_leg_R_ikRootPosition_null", "execPortType": "Out", "typeSpec": "Mat44"},
        {"name": "leg_R_IK_ctrl",                                                                    "execPortType": "In",  "typeSpec": "Mat44"},
        {"name": "leg_R_defConstraint_klOp_constrainees",                                            "execPortType": "Out", "typeSpec": "Mat44[]"},
        {"name": "leg_R_ikSolver_klOp_bone0FK",                                                      "execPortType": "In",  "typeSpec": "Mat44"},
        {"name": "leg_R_ikSolver_klOp_bone0Len",                                                     "execPortType": "In",  "typeSpec": "Scalar"},
        {"name": "leg_R_ikSolver_klOp_bone0Out",                                                     "execPortType": "Out", "typeSpec": "Mat44"},
        {"name": "leg_R_ikSolver_klOp_bone1FK",                                                      "execPortType": "In",  "typeSpec": "Mat44"},
        {"name": "leg_R_ikSolver_klOp_bone1Len",                                                     "execPortType": "In",  "typeSpec": "Scalar"},
        {"name": "leg_R_ikSolver_klOp_bone1Out",                                                     "execPortType": "Out", "typeSpec": "Mat44"},
        {"name": "leg_R_ikSolver_klOp_bone2Out",                                                     "execPortType": "Out", "typeSpec": "Mat44"},
        {"name": "leg_R_ikSolver_klOp_ikblend",                                                      "execPortType": "In",  "typeSpec": "Scalar"},
        {"name": "leg_R_ikSolver_klOp_midJointOut",                                                  "execPortType": "Out", "typeSpec": "Mat44"},
        {"name": "leg_R_ikSolver_klOp_rightSide",                                                    "execPortType": "In",  "typeSpec": "Boolean"},
        {"name": "leg_R_ikSolver_klOp_root",                                                         "execPortType": "In",  "typeSpec": "Mat44"},
        {"name": "leg_R_ikSolver_klOp_upV",                                                          "execPortType": "In",  "typeSpec": "Mat44"},
        {"name": "leg_R_shinFK_ctrl",                                                                "execPortType": "In",  "typeSpec": "Mat44"},
        {"name": "mainSrt_M_Offset_ctrl",                                                            "execPortType": "In",  "typeSpec": "Mat44"},
        {"name": "mainSrt_M_SRT_ctrl",                                                               "execPortType": "In",  "typeSpec": "Mat44"},
        {"name": "mainSrt_M_rigScale_klOp_target",                                                   "execPortType": "Out", "typeSpec": "Mat44"},
        {"name": "neck01_M_neck01_To_neckBase_poseCns_neck_M_neck01_ctrlSpace",                      "execPortType": "Out", "typeSpec": "Mat44"},
        {"name": "neck_M_defConstraint_klOp_constrainees",                                           "execPortType": "Out", "typeSpec": "Mat44[]"},
        {"name": "neck_M_defConstraint_klOp_constrainers",                                           "execPortType": "In",  "typeSpec": "Mat44[]"},
        {"name": "neck_M_neck01_ctrl",                                                               "execPortType": "In",  "typeSpec": "Mat44"},
        {"name": "neck_M_neck02_ctrl",                                                               "execPortType": "In",  "typeSpec": "Mat44"},
        {"name": "pivotAll_R_pivotAll_To_ikHandle_poseCns_foot_R_pivotAll_loc",                      "execPortType": "Out", "typeSpec": "Mat44"},
        {"name": "spine_M_cog_ctrl",                                                                 "execPortType": "In",  "typeSpec": "Mat44"},
        {"name": "spine_M_defConstraint_klOp_constrainees",                                          "execPortType": "Out", "typeSpec": "Mat44[]"},
        {"name": "spine_M_pelvisDefConstraint_klOp_constrainee",                                     "execPortType": "Out", "typeSpec": "Mat44"},
        {"name": "spine_M_pelvis_ctrl",                                                              "execPortType": "In",  "typeSpec": "Mat44"},
        {"name": "spine_M_spine_klOp_base",                                                          "execPortType": "In",  "typeSpec": "Mat44"},
        {"name": "spine_M_spine_klOp_baseHandle",                                                    "execPortType": "In",  "typeSpec": "Mat44"},
        {"name": "spine_M_spine_klOp_length",                                                        "execPortType": "In",  "typeSpec": "Scalar"},
        {"name": "spine_M_spine_klOp_outputs",                                                       "execPortType": "Out", "typeSpec": "Mat44[]"},
        {"name": "spine_M_spine_klOp_tip",                                                           "execPortType": "In",  "typeSpec": "Mat44"},
        {"name": "spine_M_spine_klOp_tipHandle",                                                     "execPortType": "In",  "typeSpec": "Mat44"}
    ]

    attributeAffectsPair = []

    arm_R_ikSolver_klOp = {'in': [], 'out': ["arm_R_defConstraint_klOp_constrainees"]}
    for p in all_ports:
        if 'arm_R_ikSolver_klOp' in p['name']:
            if 'In' in p['execPortType']:
                arm_R_ikSolver_klOp['in'].append(p['name'])
            else:
                arm_R_ikSolver_klOp['out'].append(p['name'])

    for out_port in arm_R_ikSolver_klOp['out']:
        for in_port in arm_R_ikSolver_klOp['in']:
            attributeAffectsPair.append([in_port, out_port])


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
    _registerNode(plugin, BobCanvas)


def uninitializePlugin(mobj):
    plugin = api.MFnPlugin(mobj)
    _deregisterNode(plugin, BobCanvas)
