import sys
if sys.prefix == '/home/user/anaconda3/envs/robot_env':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/user/robot_workspace/vla_ws/install/grasp_vla'
