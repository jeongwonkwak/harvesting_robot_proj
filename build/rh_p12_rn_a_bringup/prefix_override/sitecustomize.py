import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/user/robot_workspace/doosan_ws/install/rh_p12_rn_a_bringup'
