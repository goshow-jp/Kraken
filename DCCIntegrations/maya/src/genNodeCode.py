import os
from jinja2 import Environment, FileSystemLoader


def render(tpl, output_path, **kwargs):

    node = {
        'class_name': "bob2",
        "mtype_id":   "0x1A006",
        "ports": [
            {
                "objectType" : "ExecPort",
                "name" : "mainSrt_M_rigScale_klOp_target",
                "nodePortType" : "In",
                "execPortType" : "Out",
                "typeSpec" : "Mat44"
            },
            {
                "objectType" : "ExecPort",
                "metadata" : {
                    "uiPersistValue" : "true"
                },
                "name" : "mainSrt_M_Offset_ctrl",
                "affects": [
                    "cog_M_cog_To_globalSRT_poseCns_spine_M_cog_ctrlSpace",
                    "IK_L_IK_To_globalSRT_poseCns_arm_L_IK_ctrlSpace",
                    "UpV_L_UpV_To_globalSRT_poseCns_arm_L_UpV_ctrlSpace",
                    "IK_L_IK_To_globalSRT_poseCns_leg_L_IK_ctrlSpace",
                    "UpV_L_UpV_To_globalSRT_poseCns_leg_L_UpV_ctrlSpace"
                ],
                "nodePortType" : "Out",
                "execPortType" : "In",
                "typeSpec" : "Mat44"
            },
            {
                "objectType" : "ExecPort",
                "name" : "cog_M_cog_To_globalSRT_poseCns_spine_M_cog_ctrlSpace",
                "nodePortType" : "In",
                "execPortType" : "Out",
                "typeSpec" : "Mat44"
            },
            {
                "objectType" : "ExecPort",
                "metadata" : {
                    "uiPersistValue" : "true"
                },
                "name" : "spine_M_cog_ctrl",
                "affects": [
                    "spine_M_pelvisDefConstraint_klOp_constrainee",
                    "spine_M_defConstraint_klOp_constrainees",
                    "spine_M_spine_klOp_outputs",
                    "neck01_M_neck01_To_neckBase_poseCns_neck_M_neck01_ctrlSpace",
                    "neck_M_defConstraint_klOp_constrainees",
                    "clavicle_L_clavicle_To_spineEnd_poseCns_clavicle_L_clavicle_ctrlSpace",
                    "femurFK_L_femurFK_To_pelvisInput_poseCns_leg_L_femurFK_ctrlSpace",
                    "ankleFK_L_ankleFK_To_legEndFK_poseCns_foot_L_ankleFK_ctrlSpace",
                ],
                "nodePortType" : "Out",
                "execPortType" : "In",
                "typeSpec" : "Mat44"
            },
            {
                "objectType" : "ExecPort",
                "metadata" : {
                    "uiPersistValue" : "true"
                },
                "name" : "spine_M_spine_klOp_length",
                "affects": [
                    "spine_M_pelvisDefConstraint_klOp_constrainee",
                    "spine_M_defConstraint_klOp_constrainees",
                    "spine_M_spine_klOp_outputs",
                    "neck01_M_neck01_To_neckBase_poseCns_neck_M_neck01_ctrlSpace",
                    "neck_M_defConstraint_klOp_constrainees",
                    "clavicle_L_clavicle_To_spineEnd_poseCns_clavicle_L_clavicle_ctrlSpace",
                    "femurFK_L_femurFK_To_pelvisInput_poseCns_leg_L_femurFK_ctrlSpace",
                    "ankleFK_L_ankleFK_To_legEndFK_poseCns_foot_L_ankleFK_ctrlSpace",
                ],
                "nodePortType" : "Out",
                "execPortType" : "In",
                "typeSpec" : "Scalar"
            },
            {
                "objectType" : "ExecPort",
                "metadata" : {
                    "uiPersistValue" : "true"
                },
                "name" : "spine_M_spine_klOp_base",
                "affects": [
                    "spine_M_pelvisDefConstraint_klOp_constrainee",
                    "spine_M_defConstraint_klOp_constrainees",
                    "spine_M_spine_klOp_outputs",
                    "neck01_M_neck01_To_neckBase_poseCns_neck_M_neck01_ctrlSpace",
                    "neck_M_defConstraint_klOp_constrainees",
                    "clavicle_L_clavicle_To_spineEnd_poseCns_clavicle_L_clavicle_ctrlSpace",
                    "femurFK_L_femurFK_To_pelvisInput_poseCns_leg_L_femurFK_ctrlSpace",
                    "ankleFK_L_ankleFK_To_legEndFK_poseCns_foot_L_ankleFK_ctrlSpace",
                ],
                "nodePortType" : "Out",
                "execPortType" : "In",
                "typeSpec" : "Mat44"
            },
            {
                "objectType" : "ExecPort",
                "metadata" : {
                    "uiPersistValue" : "true"
                },
                "name" : "spine_M_spine_klOp_baseHandle",
                "affects": [
                    "spine_M_pelvisDefConstraint_klOp_constrainee",
                    "spine_M_defConstraint_klOp_constrainees",
                    "spine_M_spine_klOp_outputs",
                    "neck01_M_neck01_To_neckBase_poseCns_neck_M_neck01_ctrlSpace",
                    "neck_M_defConstraint_klOp_constrainees",
                    "clavicle_L_clavicle_To_spineEnd_poseCns_clavicle_L_clavicle_ctrlSpace",
                    "femurFK_L_femurFK_To_pelvisInput_poseCns_leg_L_femurFK_ctrlSpace",
                    "ankleFK_L_ankleFK_To_legEndFK_poseCns_foot_L_ankleFK_ctrlSpace",
                ],
                "nodePortType" : "Out",
                "execPortType" : "In",
                "typeSpec" : "Mat44"
            },
            {
                "objectType" : "ExecPort",
                "metadata" : {
                    "uiPersistValue" : "true"
                },
                "name" : "spine_M_spine_klOp_tipHandle",
                "affects": [
                    "spine_M_pelvisDefConstraint_klOp_constrainee",
                    "spine_M_defConstraint_klOp_constrainees",
                    "spine_M_spine_klOp_outputs",
                    "neck01_M_neck01_To_neckBase_poseCns_neck_M_neck01_ctrlSpace",
                    "neck_M_defConstraint_klOp_constrainees",
                    "clavicle_L_clavicle_To_spineEnd_poseCns_clavicle_L_clavicle_ctrlSpace",
                    "femurFK_L_femurFK_To_pelvisInput_poseCns_leg_L_femurFK_ctrlSpace",
                    "ankleFK_L_ankleFK_To_legEndFK_poseCns_foot_L_ankleFK_ctrlSpace",
                ],
                "nodePortType" : "Out",
                "execPortType" : "In",
                "typeSpec" : "Mat44"
            },
            {
                "objectType" : "ExecPort",
                "metadata" : {
                    "uiPersistValue" : "true"
                },
                "name" : "spine_M_spine_klOp_tip",
                "affects": [
                    "spine_M_pelvisDefConstraint_klOp_constrainee",
                    "spine_M_defConstraint_klOp_constrainees",
                    "spine_M_spine_klOp_outputs",
                    "neck01_M_neck01_To_neckBase_poseCns_neck_M_neck01_ctrlSpace",
                    "neck_M_defConstraint_klOp_constrainees",
                    "clavicle_L_clavicle_To_spineEnd_poseCns_clavicle_L_clavicle_ctrlSpace",
                    "femurFK_L_femurFK_To_pelvisInput_poseCns_leg_L_femurFK_ctrlSpace",
                    "ankleFK_L_ankleFK_To_legEndFK_poseCns_foot_L_ankleFK_ctrlSpace",
                ],
                "nodePortType" : "Out",
                "execPortType" : "In",
                "typeSpec" : "Mat44"
            },
            {
                "objectType" : "ExecPort",
                "name" : "spine_M_spine_klOp_outputs",
                "nodePortType" : "In",
                "execPortType" : "Out",
                "typeSpec" : "Mat44[]"
            },
            {
                "objectType" : "ExecPort",
                "metadata" : {
                    "uiPersistValue" : "true"
                },
                "name" : "spine_M_pelvis_ctrl",
                "affects": [
                    "spine_M_pelvisDefConstraint_klOp_constrainee",
                    "spine_M_defConstraint_klOp_constrainees",
                    "spine_M_spine_klOp_outputs",
                    "neck01_M_neck01_To_neckBase_poseCns_neck_M_neck01_ctrlSpace",
                    "neck_M_defConstraint_klOp_constrainees",
                    "clavicle_L_clavicle_To_spineEnd_poseCns_clavicle_L_clavicle_ctrlSpace",
                    "femurFK_L_femurFK_To_pelvisInput_poseCns_leg_L_femurFK_ctrlSpace",
                    "ankleFK_L_ankleFK_To_legEndFK_poseCns_foot_L_ankleFK_ctrlSpace",
                ],
                "nodePortType" : "Out",
                "execPortType" : "In",
                "typeSpec" : "Mat44"
            },
            {
                "objectType" : "ExecPort",
                "name" : "neck01_M_neck01_To_neckBase_poseCns_neck_M_neck01_ctrlSpace",
                "nodePortType" : "In",
                "execPortType" : "Out",
                "typeSpec" : "Mat44"
            },
            {
                "objectType" : "ExecPort",
                "metadata" : {
                    "uiPersistValue" : "true"
                },
                "name" : "neck_M_neck01_ctrl",
                "affects": [
                    "neck_M_defConstraint_klOp_constrainees"
                ],
                "nodePortType" : "Out",
                "execPortType" : "In",
                "typeSpec" : "Mat44"
            },
            {
                "objectType" : "ExecPort",
                "metadata" : {
                    "uiPersistValue" : "true"
                },
                "name" : "neck_M_neck02_ctrl",
                "affects": [
                    "neck_M_defConstraint_klOp_constrainees"
                ],
                "nodePortType" : "Out",
                "execPortType" : "In",
                "typeSpec" : "Mat44"
            },
            {
                "objectType" : "ExecPort",
                "name" : "clavicle_L_clavicle_To_spineEnd_poseCns_clavicle_L_clavicle_ctrlSpace",
                "nodePortType" : "In",
                "execPortType" : "Out",
                "typeSpec" : "Mat44"
            },
            {
                "objectType" : "ExecPort",
                "metadata" : {
                    "uiPersistValue" : "true"
                },
                "name" : "clavicle_L_clavicle_ctrl",
                "affects": [
                    "clavicle_L_defConstraint_klOp_constrainee",
                    "bicepFK_L_bicepFK_To_root_poseCns_arm_L_bicepFK_ctrlSpace"
                ],
                "nodePortType" : "Out",
                "execPortType" : "In",
                "typeSpec" : "Mat44"
            },
            {
                "objectType" : "ExecPort",
                "name" : "IK_L_IK_To_globalSRT_poseCns_arm_L_IK_ctrlSpace",
                "nodePortType" : "In",
                "execPortType" : "Out",
                "typeSpec" : "Mat44"
            },
            {
                "objectType" : "ExecPort",
                "name" : "UpV_L_UpV_To_globalSRT_poseCns_arm_L_UpV_ctrlSpace",
                "affects": [
                    "arm_L_ikSolver_klOp_bone0Out",
                    "arm_L_ikSolver_klOp_bone1Out",
                    "arm_L_ikSolver_klOp_bone2Out",
                    "arm_L_defConstraint_klOp_constrainees"
                ],
                "nodePortType" : "In",
                "execPortType" : "Out",
                "typeSpec" : "Mat44"
            },
            {
                "objectType" : "ExecPort",
                "name" : "bicepFK_L_bicepFK_To_root_poseCns_arm_L_bicepFK_ctrlSpace",
                "affects": [
                    "arm_L_ikSolver_klOp_bone0Out",
                    "arm_L_ikSolver_klOp_bone1Out",
                    "arm_L_ikSolver_klOp_bone2Out",
                    "arm_L_defConstraint_klOp_constrainees"
                ],
                "nodePortType" : "In",
                "execPortType" : "Out",
                "typeSpec" : "Mat44"
            },
            {
                "objectType" : "ExecPort",
                "name" : "ikPosition_L_ikPosition_To_root_poseCns_arm_L_ikPosition_null",
                "affects": [
                    "arm_L_ikSolver_klOp_bone0Out",
                    "arm_L_ikSolver_klOp_bone1Out",
                    "arm_L_ikSolver_klOp_bone2Out",
                    "arm_L_defConstraint_klOp_constrainees"
                ],
                "nodePortType" : "In",
                "execPortType" : "Out",
                "typeSpec" : "Mat44"
            },
            {
                "objectType" : "ExecPort",
                "metadata" : {
                    "uiPersistValue" : "true"
                },
                "name" : "arm_L_ikSolver_klOp_rightSide",
                "affects": [
                    "arm_L_ikSolver_klOp_bone0Out",
                    "arm_L_ikSolver_klOp_bone1Out",
                    "arm_L_ikSolver_klOp_bone2Out",
                    "arm_L_defConstraint_klOp_constrainees"
                ],
                "nodePortType" : "Out",
                "execPortType" : "In",
                "typeSpec" : "Boolean"
            },
            {
                "objectType" : "ExecPort",
                "metadata" : {
                    "uiPersistValue" : "true"
                },
                "name" : "arm_L_ikSolver_klOp_ikblend",
                "affects": [
                    "arm_L_ikSolver_klOp_bone0Out",
                    "arm_L_ikSolver_klOp_bone1Out",
                    "arm_L_ikSolver_klOp_bone2Out",
                    "arm_L_defConstraint_klOp_constrainees"
                ],
                "nodePortType" : "Out",
                "execPortType" : "In",
                "typeSpec" : "Scalar"
            },
            {
                "objectType" : "ExecPort",
                "metadata" : {
                    "uiPersistValue" : "true"
                },
                "name" : "arm_L_ikSolver_klOp_root",
                "affects": [
                    "arm_L_ikSolver_klOp_bone0Out",
                    "arm_L_ikSolver_klOp_bone1Out",
                    "arm_L_ikSolver_klOp_bone2Out",
                    "arm_L_defConstraint_klOp_constrainees"
                ],
                "nodePortType" : "Out",
                "execPortType" : "In",
                "typeSpec" : "Mat44"
            },
            {
                "objectType" : "ExecPort",
                "metadata" : {
                    "uiPersistValue" : "true"
                },
                "name" : "arm_L_ikSolver_klOp_bone0FK",
                "affects": [
                    "arm_L_ikSolver_klOp_bone0Out",
                    "arm_L_ikSolver_klOp_bone1Out",
                    "arm_L_ikSolver_klOp_bone2Out",
                    "arm_L_defConstraint_klOp_constrainees"
                ],
                "nodePortType" : "Out",
                "execPortType" : "In",
                "typeSpec" : "Mat44"
            },
            {
                "objectType" : "ExecPort",
                "metadata" : {
                    "uiPersistValue" : "true"
                },
                "name" : "arm_L_ikSolver_klOp_bone1FK",
                "nodePortType" : "Out",
                "execPortType" : "In",
                "affects": [
                    "arm_L_ikSolver_klOp_bone0Out",
                    "arm_L_ikSolver_klOp_bone1Out",
                    "arm_L_ikSolver_klOp_bone2Out",
                    "arm_L_defConstraint_klOp_constrainees"
                ],
                "typeSpec" : "Mat44"
            },
            {
                "objectType" : "ExecPort",
                "metadata" : {
                    "uiPersistValue" : "true"
                },
                "name" : "arm_L_ikSolver_klOp_ikHandle",
                "nodePortType" : "Out",
                "execPortType" : "In",
                "affects": [
                    "arm_L_ikSolver_klOp_bone0Out",
                    "arm_L_ikSolver_klOp_bone1Out",
                    "arm_L_ikSolver_klOp_bone2Out",
                    "arm_L_defConstraint_klOp_constrainees"
                ],
                "typeSpec" : "Mat44"
            },
            {
                "objectType" : "ExecPort",
                "metadata" : {
                    "uiPersistValue" : "true"
                },
                "name" : "arm_L_ikSolver_klOp_upV",
                "nodePortType" : "Out",
                "execPortType" : "In",
                "typeSpec" : "Mat44"
            },
            {
                "objectType" : "ExecPort",
                "metadata" : {
                    "uiPersistValue" : "true"
                },
                "name" : "arm_L_ikSolver_klOp_bone0Len",
                "nodePortType" : "Out",
                "execPortType" : "In",
                "typeSpec" : "Scalar"
            },
            {
                "objectType" : "ExecPort",
                "metadata" : {
                    "uiPersistValue" : "true"
                },
                "name" : "arm_L_ikSolver_klOp_bone1Len",
                "nodePortType" : "Out",
                "execPortType" : "In",
                "typeSpec" : "Scalar"
            },
            {
                "objectType" : "ExecPort",
                "name" : "arm_L_ikSolver_klOp_bone0Out",
                "nodePortType" : "In",
                "execPortType" : "Out",
                "typeSpec" : "Mat44"
            },
            {
                "objectType" : "ExecPort",
                "name" : "arm_L_ikSolver_klOp_bone1Out",
                "nodePortType" : "In",
                "execPortType" : "Out",
                "typeSpec" : "Mat44"
            },
            {
                "objectType" : "ExecPort",
                "name" : "arm_L_ikSolver_klOp_bone2Out",
                "nodePortType" : "In",
                "execPortType" : "Out",
                "typeSpec" : "Mat44"
            },
            {
                "objectType" : "ExecPort",
                "name" : "arm_L_ikSolver_klOp_midJointOut",
                "nodePortType" : "In",
                "execPortType" : "Out",
                "typeSpec" : "Mat44"
            },
            {
                "objectType" : "ExecPort",
                "name" : "IK_L_IK_To_globalSRT_poseCns_leg_L_IK_ctrlSpace",
                "nodePortType" : "In",
                "execPortType" : "Out",
                "typeSpec" : "Mat44"
            },
            {
                "objectType" : "ExecPort",
                "metadata" : {
                    "uiPersistValue" : "true"
                },
                "name" : "leg_L_IK_ctrl",
                "nodePortType" : "Out",
                "execPortType" : "In",
                "typeSpec" : "Mat44"
            },
            {
                "objectType" : "ExecPort",
                "name" : "pivotAll_L_pivotAll_To_ikHandle_poseCns_foot_L_pivotAll_loc",
                "nodePortType" : "In",
                "execPortType" : "Out",
                "typeSpec" : "Mat44"
            },
            {
                "objectType" : "ExecPort",
                "metadata" : {
                    "uiPersistValue" : "true"
                },
                "name" : "foot_L_footPivot_klOp_rightSide",
                "nodePortType" : "Out",
                "execPortType" : "In",
                "typeSpec" : "Boolean"
            },
            {
                "objectType" : "ExecPort",
                "metadata" : {
                    "uiPersistValue" : "true"
                },
                "name" : "foot_L_footPivot_klOp_footRock",
                "nodePortType" : "Out",
                "execPortType" : "In",
                "typeSpec" : "Scalar"
            },
            {
                "objectType" : "ExecPort",
                "metadata" : {
                    "uiPersistValue" : "true"
                },
                "name" : "foot_L_footPivot_klOp_footBank",
                "nodePortType" : "Out",
                "execPortType" : "In",
                "typeSpec" : "Scalar"
            },
            {
                "objectType" : "ExecPort",
                "metadata" : {
                    "uiPersistValue" : "true"
                },
                "name" : "foot_L_footPivot_klOp_pivotAll",
                "nodePortType" : "Out",
                "execPortType" : "In",
                "typeSpec" : "Mat44"
            },
            {
                "objectType" : "ExecPort",
                "metadata" : {
                    "uiPersistValue" : "true"
                },
                "name" : "foot_L_footPivot_klOp_backPivot",
                "nodePortType" : "Out",
                "execPortType" : "In",
                "typeSpec" : "Mat44"
            },
            {
                "objectType" : "ExecPort",
                "metadata" : {
                    "uiPersistValue" : "true"
                },
                "name" : "foot_L_footPivot_klOp_frontPivot",
                "nodePortType" : "Out",
                "execPortType" : "In",
                "typeSpec" : "Mat44"
            },
            {
                "objectType" : "ExecPort",
                "metadata" : {
                    "uiPersistValue" : "true"
                },
                "name" : "foot_L_footPivot_klOp_outerPivot",
                "nodePortType" : "Out",
                "execPortType" : "In",
                "typeSpec" : "Mat44"
            },
            {
                "objectType" : "ExecPort",
                "metadata" : {
                    "uiPersistValue" : "true"
                },
                "name" : "foot_L_footPivot_klOp_innerPivot",
                "nodePortType" : "Out",
                "execPortType" : "In",
                "typeSpec" : "Mat44"
            },
            {
                "objectType" : "ExecPort",
                "name" : "foot_L_footPivot_klOp_result",
                "nodePortType" : "In",
                "execPortType" : "Out",
                "typeSpec" : "Mat44"
            },
            {
                "objectType" : "ExecPort",
                "metadata" : {
                    "uiPersistValue" : "true"
                },
                "name" : "foot_L_ankleIK_ctrl",
                "nodePortType" : "Out",
                "execPortType" : "In",
                "typeSpec" : "Mat44"
            },
            {
                "objectType" : "ExecPort",
                "name" : "UpV_L_UpV_To_globalSRT_poseCns_leg_L_UpV_ctrlSpace",
                "nodePortType" : "In",
                "execPortType" : "Out",
                "typeSpec" : "Mat44"
            },
            {
                "objectType" : "ExecPort",
                "name" : "femurFK_L_femurFK_To_pelvisInput_poseCns_leg_L_femurFK_ctrlSpace",
                "nodePortType" : "In",
                "execPortType" : "Out",
                "typeSpec" : "Mat44"
            },
            {
                "objectType" : "ExecPort",
                "name" : "ikRootPosition_L_ikRootPosition_To_pelvisInput_poseCns_leg_L_ikRootPosition_null",
                "nodePortType" : "In",
                "execPortType" : "Out",
                "typeSpec" : "Mat44"
            },
            {
                "objectType" : "ExecPort",
                "metadata" : {
                    "uiPersistValue" : "true"
                },
                "name" : "leg_L_ikSolver_klOp_rightSide",
                "nodePortType" : "Out",
                "execPortType" : "In",
                "typeSpec" : "Boolean"
            },
            {
                "objectType" : "ExecPort",
                "metadata" : {
                    "uiPersistValue" : "true"
                },
                "name" : "leg_L_ikSolver_klOp_ikblend",
                "nodePortType" : "Out",
                "execPortType" : "In",
                "typeSpec" : "Scalar"
            },
            {
                "objectType" : "ExecPort",
                "metadata" : {
                    "uiPersistValue" : "true"
                },
                "name" : "leg_L_ikSolver_klOp_root",
                "nodePortType" : "Out",
                "execPortType" : "In",
                "typeSpec" : "Mat44"
            },
            {
                "objectType" : "ExecPort",
                "metadata" : {
                    "uiPersistValue" : "true"
                },
                "name" : "leg_L_ikSolver_klOp_bone0FK",
                "nodePortType" : "Out",
                "execPortType" : "In",
                "typeSpec" : "Mat44"
            },
            {
                "objectType" : "ExecPort",
                "metadata" : {
                    "uiPersistValue" : "true"
                },
                "name" : "leg_L_ikSolver_klOp_bone1FK",
                "nodePortType" : "Out",
                "execPortType" : "In",
                "typeSpec" : "Mat44"
            },
            {
                "objectType" : "ExecPort",
                "metadata" : {
                    "uiPersistValue" : "true"
                },
                "name" : "leg_L_ikSolver_klOp_upV",
                "nodePortType" : "Out",
                "execPortType" : "In",
                "typeSpec" : "Mat44"
            },
            {
                "objectType" : "ExecPort",
                "metadata" : {
                    "uiPersistValue" : "true"
                },
                "name" : "leg_L_ikSolver_klOp_bone0Len",
                "nodePortType" : "Out",
                "execPortType" : "In",
                "typeSpec" : "Scalar"
            },
            {
                "objectType" : "ExecPort",
                "metadata" : {
                    "uiPersistValue" : "true"
                },
                "name" : "leg_L_ikSolver_klOp_bone1Len",
                "nodePortType" : "Out",
                "execPortType" : "In",
                "typeSpec" : "Scalar"
            },
            {
                "objectType" : "ExecPort",
                "name" : "leg_L_ikSolver_klOp_bone0Out",
                "nodePortType" : "In",
                "execPortType" : "Out",
                "typeSpec" : "Mat44"
            },
            {
                "objectType" : "ExecPort",
                "name" : "leg_L_ikSolver_klOp_bone1Out",
                "nodePortType" : "In",
                "execPortType" : "Out",
                "typeSpec" : "Mat44"
            },
            {
                "objectType" : "ExecPort",
                "name" : "leg_L_ikSolver_klOp_bone2Out",
                "nodePortType" : "In",
                "execPortType" : "Out",
                "typeSpec" : "Mat44"
            },
            {
                "objectType" : "ExecPort",
                "name" : "leg_L_ikSolver_klOp_midJointOut",
                "nodePortType" : "In",
                "execPortType" : "Out",
                "typeSpec" : "Mat44"
            },
            {
                "objectType" : "ExecPort",
                "metadata" : {
                    "uiPersistValue" : "true"
                },
                "name" : "leg_L_shinFK_ctrl",
                "nodePortType" : "Out",
                "execPortType" : "In",
                "typeSpec" : "Mat44"
            },
            {
                "objectType" : "ExecPort",
                "name" : "ankleFK_L_ankleFK_To_legEndFK_poseCns_foot_L_ankleFK_ctrlSpace",
                "nodePortType" : "In",
                "execPortType" : "Out",
                "typeSpec" : "Mat44"
            },
            {
                "objectType" : "ExecPort",
                "metadata" : {
                    "uiPersistValue" : "true"
                },
                "name" : "foot_L_footSolver_klOp_ikBlend",
                "affects": [
                    "foot_L_footSolver_klOp_ankle_result",
                    "foot_L_footSolver_klOp_toe_result",
                    "foot_L_defConstraint_klOp_constrainees",
                ],
                "nodePortType" : "Out",
                "execPortType" : "In",
                "typeSpec" : "Scalar"
            },
            {
                "objectType" : "ExecPort",
                "metadata" : {
                    "uiPersistValue" : "true"
                },
                "name" : "foot_L_footSolver_klOp_ankleLen",
                "affects": [
                    "foot_L_footSolver_klOp_ankle_result",
                    "foot_L_footSolver_klOp_toe_result",
                    "foot_L_defConstraint_klOp_constrainees",
                ],
                "nodePortType" : "Out",
                "execPortType" : "In",
                "typeSpec" : "Scalar"
            },
            {
                "objectType" : "ExecPort",
                "metadata" : {
                    "uiPersistValue" : "true"
                },
                "name" : "foot_L_footSolver_klOp_toeLen",
                "affects": [
                    "foot_L_footSolver_klOp_ankle_result",
                    "foot_L_footSolver_klOp_toe_result",
                    "foot_L_defConstraint_klOp_constrainees",
                ],
                "nodePortType" : "Out",
                "execPortType" : "In",
                "typeSpec" : "Scalar"
            },
            {
                "objectType" : "ExecPort",
                "metadata" : {
                    "uiPersistValue" : "true"
                },
                "name" : "foot_L_footSolver_klOp_ankleIK",
                "affects": [
                    "foot_L_footSolver_klOp_ankle_result",
                    "foot_L_footSolver_klOp_toe_result",
                    "foot_L_defConstraint_klOp_constrainees",
                ],
                "nodePortType" : "Out",
                "execPortType" : "In",
                "typeSpec" : "Mat44"
            },
            {
                "objectType" : "ExecPort",
                "metadata" : {
                    "uiPersistValue" : "true"
                },
                "name" : "foot_L_footSolver_klOp_toeIK",
                "affects": [
                    "foot_L_footSolver_klOp_ankle_result",
                    "foot_L_footSolver_klOp_toe_result",
                    "foot_L_defConstraint_klOp_constrainees",
                ],
                "nodePortType" : "Out",
                "execPortType" : "In",
                "typeSpec" : "Mat44"
            },
            {
                "objectType" : "ExecPort",
                "metadata" : {
                    "uiPersistValue" : "true"
                },
                "name" : "foot_L_footSolver_klOp_ankleFK",
                "affects": [
                    "foot_L_footSolver_klOp_ankle_result",
                    "foot_L_footSolver_klOp_toe_result",
                    "foot_L_defConstraint_klOp_constrainees",
                ],
                "nodePortType" : "Out",
                "execPortType" : "In",
                "typeSpec" : "Mat44"
            },
            {
                "objectType" : "ExecPort",
                "metadata" : {
                    "uiPersistValue" : "true"
                },
                "name" : "foot_L_footSolver_klOp_toeFK",
                "affects": [
                    "foot_L_footSolver_klOp_ankle_result",
                    "foot_L_footSolver_klOp_toe_result",
                    "foot_L_defConstraint_klOp_constrainees",
                ],
                "nodePortType" : "Out",
                "execPortType" : "In",
                "typeSpec" : "Mat44"
            },
            {
                "objectType" : "ExecPort",
                "name" : "foot_L_footSolver_klOp_ankle_result",
                "nodePortType" : "In",
                "execPortType" : "Out",
                "typeSpec" : "Mat44"
            },
            {
                "objectType" : "ExecPort",
                "name" : "foot_L_footSolver_klOp_toe_result",
                "nodePortType" : "In",
                "execPortType" : "Out",
                "typeSpec" : "Mat44"
            },
            {
                "objectType" : "ExecPort",
                "metadata" : {
                    "uiPersistValue" : "true"
                },
                "name" : "mainSrt_M_SRT_ctrl",
                "nodePortType" : "Out",
                "execPortType" : "In",
                "typeSpec" : "Mat44"
            },
            {
                "objectType" : "ExecPort",
                "metadata" : {
                    "uiPersistValue" : "true"
                },
                "name" : "neck_M_defConstraint_klOp_constrainers",
                "affects": [
                    "neck_M_defConstraint_klOp_constrainees"
                ],
                "nodePortType" : "Out",
                "execPortType" : "In",
                "typeSpec" : "Mat44[]"
            },
            {
                "objectType" : "ExecPort",
                "name" : "neck_M_defConstraint_klOp_constrainees",
                "nodePortType" : "In",
                "execPortType" : "Out",
                "typeSpec" : "Mat44[]"
            },
            {
                "objectType" : "ExecPort",
                "name" : "clavicle_L_defConstraint_klOp_constrainee",
                "nodePortType" : "In",
                "execPortType" : "Out",
                "typeSpec" : "Mat44"
            },
            {
                "objectType" : "ExecPort",
                "name" : "arm_L_defConstraint_klOp_constrainees",
                "nodePortType" : "In",
                "execPortType" : "Out",
                "typeSpec" : "Mat44[]"
            },
            {
                "objectType" : "ExecPort",
                "name" : "leg_L_defConstraint_klOp_constrainees",
                "nodePortType" : "In",
                "execPortType" : "Out",
                "typeSpec" : "Mat44[]"
            },
            {
                "objectType" : "ExecPort",
                "name" : "foot_L_defConstraint_klOp_constrainees",
                "nodePortType" : "In",
                "execPortType" : "Out",
                "typeSpec" : "Mat44[]"
            },
            {
                "objectType" : "ExecPort",
                "name" : "spine_M_defConstraint_klOp_constrainees",
                "nodePortType" : "In",
                "execPortType" : "Out",
                "typeSpec" : "Mat44[]"
            },
            {
                "objectType" : "ExecPort",
                "name" : "spine_M_pelvisDefConstraint_klOp_constrainee",
                "nodePortType" : "In",
                "execPortType" : "Out",
                "typeSpec" : "Mat44"
            }
        ]

    }

    canvas_file_path = r"D:\\fabric\\bob2.canvas"

    results = tpl.render(node=node, canvas_file_path=canvas_file_path)

    with open(output_path, 'w') as f:
        f.write(results)

    return results


if __name__ == '__main__':
    cwd = os.path.abspath(os.path.dirname(__file__))
    template_dir = cwd
    # template_dir = os.path.join(cwd, 'node.cpp.tpl')

    env = Environment(loader=FileSystemLoader(template_dir, encoding='utf8'))
    cpp_tpl = env.get_template('node.tpl.cpp')
    render(cpp_tpl, "bob2.cpp")

    cpp_tpl = env.get_template('node.tpl.h')
    render(cpp_tpl, "bob2.h")
