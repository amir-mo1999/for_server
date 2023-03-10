from typing import Union
import numpy as np
import pybullet as pyb
from robot.robot import Robot

class CameraHolderUR5(Robot):

    def __init__(self, name: str, world, **kwargs):
        super().__init__(name, world, **kwargs)
        self.joints_limits_lower = np.array([-np.pi, -np.pi, -np.pi, -np.pi, -np.pi, -np.pi])
        self.joints_limits_upper = np.array([np.pi, np.pi, np.pi, np.pi, np.pi, np.pi])
        self.joints_range = self.joints_limits_upper - self.joints_limits_lower

        self.end_effector_link_id = 7
        self.base_link_id = 1

    def get_action_space_dims(self):
        return (1,1)  # 6 joints

    def build(self):

        self.object_id = pyb.loadURDF("ur5/urdf/ur5.urdf", basePosition=self.base_position.tolist(), baseOrientation=self.base_orientation.tolist(), useFixedBase=True)
        joints_info = [pyb.getJointInfo(self.id, i) for i in range(pyb.getNumJoints(self.id))]
        self.joints_ids = np.array([j[0] for j in joints_info if j[2] == pyb.JOINT_REVOLUTE])

        self.joints_forces = np.array([j[10] for j in joints_info if j[2] == pyb.JOINT_REVOLUTE])
        self.joints_vel_delta = np.array([j[11] for j in joints_info if j[2] == pyb.JOINT_REVOLUTE])

        self.moveto_joints(self.resting_pose_angles, False) 