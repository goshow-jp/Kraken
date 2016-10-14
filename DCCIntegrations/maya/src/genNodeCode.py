import os
from jinja2 import Environment, FileSystemLoader


def render(tpl, output_path, **kwargs):

    node = {
        'class_name': "bob2",
        "mtype_id":   "0x1A006",
        "ports": [
            {"name": "mainSrt_M_rigScale_klOp_target",                                                   "nodePortType": "In",  "execPortType": "Out", "typeSpec": "Mat44"},
            {"name": "mainSrt_M_Offset_ctrl",                                                            "nodePortType": "Out", "execPortType": "In",  "typeSpec": "Mat44"},
            {"name": "cog_M_cog_To_globalSRT_poseCns_spine_M_cog_ctrlSpace",                             "nodePortType": "In",  "execPortType": "Out", "typeSpec": "Mat44"},
            {"name": "spine_M_cog_ctrl",                                                                 "nodePortType": "Out", "execPortType": "In",  "typeSpec": "Mat44", "affects": ["clavicle_L_clavicle_To_spineEnd_poseCns_clavicle_L_clavicle_ctrlSpace"]},
            {"name": "spine_M_spine_klOp_length",                                                        "nodePortType": "Out", "execPortType": "In",  "typeSpec": "Scalar"},
            {"name": "spine_M_spine_klOp_base",                                                          "nodePortType": "Out", "execPortType": "In",  "typeSpec": "Mat44"},
            {"name": "spine_M_spine_klOp_baseHandle",                                                    "nodePortType": "Out", "execPortType": "In",  "typeSpec": "Mat44"},
            {"name": "spine_M_spine_klOp_tipHandle",                                                     "nodePortType": "Out", "execPortType": "In",  "typeSpec": "Mat44"},
            {"name": "spine_M_spine_klOp_tip",                                                           "nodePortType": "Out", "execPortType": "In",  "typeSpec": "Mat44"},
            {"name": "spine_M_spine_klOp_outputs",                                                       "nodePortType": "In",  "execPortType": "Out", "typeSpec": "Mat44[]"},
            {"name": "spine_M_pelvis_ctrl",                                                              "nodePortType": "Out", "execPortType": "In",  "typeSpec": "Mat44"},
            {"name": "neck01_M_neck01_To_neckBase_poseCns_neck_M_neck01_ctrlSpace",                      "nodePortType": "In",  "execPortType": "Out", "typeSpec": "Mat44"},
            {"name": "neck_M_neck01_ctrl",                                                               "nodePortType": "Out", "execPortType": "In",  "typeSpec": "Mat44"},
            {"name": "neck_M_neck02_ctrl",                                                               "nodePortType": "Out", "execPortType": "In",  "typeSpec": "Mat44"},
            {"name": "clavicle_L_clavicle_To_spineEnd_poseCns_clavicle_L_clavicle_ctrlSpace",            "nodePortType": "In",  "execPortType": "Out", "typeSpec": "Mat44"},
            {"name": "clavicle_L_clavicle_ctrl",                                                         "nodePortType": "Out", "execPortType": "In",  "typeSpec": "Mat44"},
            {"name": "IK_L_IK_To_globalSRT_poseCns_arm_L_IK_ctrlSpace",                                  "nodePortType": "In",  "execPortType": "Out", "typeSpec": "Mat44"},
            {"name": "UpV_L_UpV_To_globalSRT_poseCns_arm_L_UpV_ctrlSpace",                               "nodePortType": "In",  "execPortType": "Out", "typeSpec": "Mat44"},
            {"name": "bicepFK_L_bicepFK_To_root_poseCns_arm_L_bicepFK_ctrlSpace",                        "nodePortType": "In",  "execPortType": "Out", "typeSpec": "Mat44"},
            {"name": "ikPosition_L_ikPosition_To_root_poseCns_arm_L_ikPosition_null",                    "nodePortType": "In",  "execPortType": "Out", "typeSpec": "Mat44"},
            {"name": "arm_L_ikSolver_klOp_rightSide",                                                    "nodePortType": "Out", "execPortType": "In",  "typeSpec": "Boolean"},
            {"name": "arm_L_ikSolver_klOp_ikblend",                                                      "nodePortType": "Out", "execPortType": "In",  "typeSpec": "Scalar"},
            {"name": "arm_L_ikSolver_klOp_root",                                                         "nodePortType": "Out", "execPortType": "In",  "typeSpec": "Mat44"},
            {"name": "arm_L_ikSolver_klOp_bone0FK",                                                      "nodePortType": "Out", "execPortType": "In",  "typeSpec": "Mat44", "affects": ["arm_L_ikSolver_klOp_bone0Out", "arm_L_ikSolver_klOp_bone1Out", "arm_L_ikSolver_klOp_bone2Out", "arm_L_defConstraint_klOp_constrainees"]},
            {"name": "arm_L_ikSolver_klOp_bone1FK",                                                      "nodePortType": "Out", "execPortType": "In",  "typeSpec": "Mat44", "affects": ["arm_L_ikSolver_klOp_bone0Out", "arm_L_ikSolver_klOp_bone1Out", "arm_L_ikSolver_klOp_bone2Out", "arm_L_defConstraint_klOp_constrainees"]},
            {"name": "arm_L_ikSolver_klOp_ikHandle",                                                     "nodePortType": "Out", "execPortType": "In",  "typeSpec": "Mat44", "affects": ["arm_L_ikSolver_klOp_bone0Out", "arm_L_ikSolver_klOp_bone1Out", "arm_L_ikSolver_klOp_bone2Out", "arm_L_defConstraint_klOp_constrainees"]},
            {"name": "arm_L_ikSolver_klOp_upV",                                                          "nodePortType": "Out", "execPortType": "In",  "typeSpec": "Mat44", "affects": ["arm_L_ikSolver_klOp_bone0Out", "arm_L_ikSolver_klOp_bone1Out", "arm_L_ikSolver_klOp_bone2Out", "arm_L_defConstraint_klOp_constrainees"]},
            {"name": "arm_L_ikSolver_klOp_bone0Len",                                                     "nodePortType": "Out", "execPortType": "In",  "typeSpec": "Scalar", "affects": ["arm_L_ikSolver_klOp_bone0Out", "arm_L_ikSolver_klOp_bone1Out", "arm_L_ikSolver_klOp_bone2Out", "arm_L_defConstraint_klOp_constrainees"]},
            {"name": "arm_L_ikSolver_klOp_bone1Len",                                                     "nodePortType": "Out", "execPortType": "In",  "typeSpec": "Scalar", "affects": ["arm_L_ikSolver_klOp_bone0Out", "arm_L_ikSolver_klOp_bone1Out", "arm_L_ikSolver_klOp_bone2Out", "arm_L_defConstraint_klOp_constrainees"]},
            {"name": "arm_L_ikSolver_klOp_bone0Out",                                                     "nodePortType": "In",  "execPortType": "Out", "typeSpec": "Mat44"},
            {"name": "arm_L_ikSolver_klOp_bone1Out",                                                     "nodePortType": "In",  "execPortType": "Out", "typeSpec": "Mat44"},
            {"name": "arm_L_ikSolver_klOp_bone2Out",                                                     "nodePortType": "In",  "execPortType": "Out", "typeSpec": "Mat44"},
            {"name": "arm_L_ikSolver_klOp_midJointOut",                                                  "nodePortType": "In",  "execPortType": "Out", "typeSpec": "Mat44"},
            {"name": "IK_L_IK_To_globalSRT_poseCns_leg_L_IK_ctrlSpace",                                  "nodePortType": "In",  "execPortType": "Out", "typeSpec": "Mat44"},
            {"name": "leg_L_IK_ctrl",                                                                    "nodePortType": "Out", "execPortType": "In",  "typeSpec": "Mat44"},
            {"name": "pivotAll_L_pivotAll_To_ikHandle_poseCns_foot_L_pivotAll_loc",                      "nodePortType": "In",  "execPortType": "Out", "typeSpec": "Mat44"},
            {"name": "foot_L_footPivot_klOp_rightSide",                                                  "nodePortType": "Out", "execPortType": "In",  "typeSpec": "Boolean"},
            {"name": "foot_L_footPivot_klOp_footRock",                                                   "nodePortType": "Out", "execPortType": "In",  "typeSpec": "Scalar"},
            {"name": "foot_L_footPivot_klOp_footBank",                                                   "nodePortType": "Out", "execPortType": "In",  "typeSpec": "Scalar"},
            {"name": "foot_L_footPivot_klOp_pivotAll",                                                   "nodePortType": "Out", "execPortType": "In",  "typeSpec": "Mat44"},
            {"name": "foot_L_footPivot_klOp_backPivot",                                                  "nodePortType": "Out", "execPortType": "In",  "typeSpec": "Mat44"},
            {"name": "foot_L_footPivot_klOp_frontPivot",                                                 "nodePortType": "Out", "execPortType": "In",  "typeSpec": "Mat44"},
            {"name": "foot_L_footPivot_klOp_outerPivot",                                                 "nodePortType": "Out", "execPortType": "In",  "typeSpec": "Mat44"},
            {"name": "foot_L_footPivot_klOp_innerPivot",                                                 "nodePortType": "Out", "execPortType": "In",  "typeSpec": "Mat44"},
            {"name": "foot_L_footPivot_klOp_result",                                                     "nodePortType": "In",  "execPortType": "Out", "typeSpec": "Mat44"},
            {"name": "foot_L_ankleIK_ctrl",                                                              "nodePortType": "Out", "execPortType": "In",  "typeSpec": "Mat44"},
            {"name": "UpV_L_UpV_To_globalSRT_poseCns_leg_L_UpV_ctrlSpace",                               "nodePortType": "In",  "execPortType": "Out", "typeSpec": "Mat44"},

            {"name": "femurFK_L_femurFK_To_pelvisInput_poseCns_leg_L_femurFK_ctrlSpace",                 "nodePortType": "In",  "execPortType": "Out", "typeSpec": "Mat44"},
            {"name": "ikRootPosition_L_ikRootPosition_To_pelvisInput_poseCns_leg_L_ikRootPosition_null", "nodePortType": "In",  "execPortType": "Out", "typeSpec": "Mat44"},
            {"name": "leg_L_ikSolver_klOp_rightSide",                                                    "nodePortType": "Out", "execPortType": "In",  "typeSpec": "Boolean"},
            {"name": "leg_L_ikSolver_klOp_ikblend",                                                      "nodePortType": "Out", "execPortType": "In",  "typeSpec": "Scalar"},
            {"name": "leg_L_ikSolver_klOp_root",                                                         "nodePortType": "Out", "execPortType": "In",  "typeSpec": "Mat44"},
            {"name": "leg_L_ikSolver_klOp_bone0FK",                                                      "nodePortType": "Out", "execPortType": "In",  "typeSpec": "Mat44"},
            {"name": "leg_L_ikSolver_klOp_bone1FK",                                                      "nodePortType": "Out", "execPortType": "In",  "typeSpec": "Mat44"},
            {"name": "leg_L_ikSolver_klOp_upV",                                                          "nodePortType": "Out", "execPortType": "In",  "typeSpec": "Mat44"},
            {"name": "leg_L_ikSolver_klOp_bone0Len",                                                     "nodePortType": "Out", "execPortType": "In",  "typeSpec": "Scalar"},
            {"name": "leg_L_ikSolver_klOp_bone1Len",                                                     "nodePortType": "Out", "execPortType": "In",  "typeSpec": "Scalar"},
            {"name": "leg_L_ikSolver_klOp_bone0Out",                                                     "nodePortType": "In",  "execPortType": "Out", "typeSpec": "Mat44"},
            {"name": "leg_L_ikSolver_klOp_bone1Out",                                                     "nodePortType": "In",  "execPortType": "Out", "typeSpec": "Mat44"},
            {"name": "leg_L_ikSolver_klOp_bone2Out",                                                     "nodePortType": "In",  "execPortType": "Out", "typeSpec": "Mat44"},
            {"name": "leg_L_ikSolver_klOp_midJointOut",                                                  "nodePortType": "In",  "execPortType": "Out", "typeSpec": "Mat44"},
            {"name": "leg_L_shinFK_ctrl",                                                                "nodePortType": "Out", "execPortType": "In",  "typeSpec": "Mat44"},
            {"name": "ankleFK_L_ankleFK_To_legEndFK_poseCns_foot_L_ankleFK_ctrlSpace",                   "nodePortType": "In",  "execPortType": "Out", "typeSpec": "Mat44"},
            {"name": "foot_L_footSolver_klOp_ikBlend",                                                   "nodePortType": "Out", "execPortType": "In",  "typeSpec": "Scalar"},
            {"name": "foot_L_footSolver_klOp_ankleLen",                                                  "nodePortType": "Out", "execPortType": "In",  "typeSpec": "Scalar"},
            {"name": "foot_L_footSolver_klOp_toeLen",                                                    "nodePortType": "Out", "execPortType": "In",  "typeSpec": "Scalar"},
            {"name": "foot_L_footSolver_klOp_ankleIK",                                                   "nodePortType": "Out", "execPortType": "In",  "typeSpec": "Mat44"},
            {"name": "foot_L_footSolver_klOp_toeIK",                                                     "nodePortType": "Out", "execPortType": "In",  "typeSpec": "Mat44"},
            {"name": "foot_L_footSolver_klOp_ankleFK",                                                   "nodePortType": "Out", "execPortType": "In",  "typeSpec": "Mat44"},
            {"name": "foot_L_footSolver_klOp_toeFK",                                                     "nodePortType": "Out", "execPortType": "In",  "typeSpec": "Mat44"},
            {"name": "foot_L_footSolver_klOp_ankle_result",                                              "nodePortType": "In",  "execPortType": "Out", "typeSpec": "Mat44"},
            {"name": "foot_L_footSolver_klOp_toe_result",                                                "nodePortType": "In",  "execPortType": "Out", "typeSpec": "Mat44"},
            {"name": "mainSrt_M_SRT_ctrl",                                                               "nodePortType": "Out", "execPortType": "In",  "typeSpec": "Mat44"},
            {"name": "neck_M_defConstraint_klOp_constrainers",                                           "nodePortType": "Out", "execPortType": "In",  "typeSpec": "Mat44[]"},
            {"name": "neck_M_defConstraint_klOp_constrainees",                                           "nodePortType": "In",  "execPortType": "Out", "typeSpec": "Mat44[]"},
            {"name": "clavicle_L_defConstraint_klOp_constrainee",                                        "nodePortType": "In",  "execPortType": "Out", "typeSpec": "Mat44"},
            {"name": "arm_L_defConstraint_klOp_constrainees",                                            "nodePortType": "In",  "execPortType": "Out", "typeSpec": "Mat44[]"},
            {"name": "leg_L_defConstraint_klOp_constrainees",                                            "nodePortType": "In",  "execPortType": "Out", "typeSpec": "Mat44[]"},
            {"name": "foot_L_defConstraint_klOp_constrainees",                                           "nodePortType": "In",  "execPortType": "Out", "typeSpec": "Mat44[]"},
            {"name": "spine_M_defConstraint_klOp_constrainees",                                          "nodePortType": "In",  "execPortType": "Out", "typeSpec": "Mat44[]"},
            {"name": "spine_M_pelvisDefConstraint_klOp_constrainee",                                     "nodePortType": "In",  "execPortType": "Out", "typeSpec": "Mat44"}
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
