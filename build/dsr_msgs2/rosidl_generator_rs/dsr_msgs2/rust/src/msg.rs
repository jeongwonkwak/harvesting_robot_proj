#[cfg(feature = "serde")]
use serde::{Deserialize, Serialize};



// Corresponds to dsr_msgs2__msg__LogAlarm
/// ____________________________________________________________________________________________
///  log of alarm
/// ____________________________________________________________________________________________

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct LogAlarm {

    // This member is not documented.
    #[allow(missing_docs)]
    pub level: i32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub group: i32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub index: i32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub param: [std::string::String; 3],

}



impl Default for LogAlarm {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::LogAlarm::default())
  }
}

impl rosidl_runtime_rs::Message for LogAlarm {
  type RmwMsg = super::msg::rmw::LogAlarm;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        level: msg.level,
        group: msg.group,
        index: msg.index,
        param: msg.param
          .map(|elem| elem.as_str().into()),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      level: msg.level,
      group: msg.group,
      index: msg.index,
        param: msg.param
          .iter()
          .map(|elem| elem.as_str().into())
          .collect::<Vec<_>>()
          .try_into()
          .unwrap(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      level: msg.level,
      group: msg.group,
      index: msg.index,
      param: msg.param
        .map(|elem| elem.to_string()),
    }
  }
}


// Corresponds to dsr_msgs2__msg__ModbusState
/// ____________________________________________________________________________________________
/// Custom msg for RobotState.msg -- MAX_SIZE = 100
/// ____________________________________________________________________________________________

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ModbusState {
    /// Modbus Signal Name
    pub modbus_symbol: std::string::String,

    /// Modbus Register Value (Unsigned : 0 ~ 65535)
    pub modbus_value: i32,

}



impl Default for ModbusState {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::ModbusState::default())
  }
}

impl rosidl_runtime_rs::Message for ModbusState {
  type RmwMsg = super::msg::rmw::ModbusState;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        modbus_symbol: msg.modbus_symbol.as_str().into(),
        modbus_value: msg.modbus_value,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        modbus_symbol: msg.modbus_symbol.as_str().into(),
      modbus_value: msg.modbus_value,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      modbus_symbol: msg.modbus_symbol.to_string(),
      modbus_value: msg.modbus_value,
    }
  }
}


// Corresponds to dsr_msgs2__msg__RobotError
/// ____________________________________________________________________________________________
///  [ robot error msg ] 
/// ____________________________________________________________________________________________

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct RobotError {
    /// INFO =1, WARN =2, ERROR =3
    pub level: i32,

    /// SYSTEM =1, MOTION =2, TP =3, INVERTER =4, SAFETY_CONTROLLER =5
    pub group: i32,

    /// error code
    pub code: i32,

    /// error msg 1
    pub msg1: std::string::String,

    /// error msg 2
    pub msg2: std::string::String,

    /// error msg 3
    pub msg3: std::string::String,

}



impl Default for RobotError {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::RobotError::default())
  }
}

impl rosidl_runtime_rs::Message for RobotError {
  type RmwMsg = super::msg::rmw::RobotError;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        level: msg.level,
        group: msg.group,
        code: msg.code,
        msg1: msg.msg1.as_str().into(),
        msg2: msg.msg2.as_str().into(),
        msg3: msg.msg3.as_str().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      level: msg.level,
      group: msg.group,
      code: msg.code,
        msg1: msg.msg1.as_str().into(),
        msg2: msg.msg2.as_str().into(),
        msg3: msg.msg3.as_str().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      level: msg.level,
      group: msg.group,
      code: msg.code,
      msg1: msg.msg1.to_string(),
      msg2: msg.msg2.to_string(),
      msg3: msg.msg3.to_string(),
    }
  }
}


// Corresponds to dsr_msgs2__msg__RobotState
/// ____________________________________________________________________________________________
///  state of robot
/// ____________________________________________________________________________________________

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct RobotState {
    /// 0 : STATE_INITIALIZING,   1 : STATE_STANDBY,   2 : STATE_MOVING,    3 : STATE_SAFE_OFF
    /// 4 : STATE_TEACHING,       5 : STATE_SAFE_STOP, 6 : STATE_EMERGENCY_STOP,
    /// 7 : STATE_EMERGENCY_STOP, 8 : STATE_HOMMING,   9 : STATE_RECOVERY,  10: STATE_SAFE_STOP2,
    /// 11: STATE_SAFE_OFF2,      12: STATE_RESERVED1, 13: STATE_RESERVED2, 14: STATE_RESERVED3,
    /// 15: STATE_NOT_READY       16: STATE_LAST
    pub robot_state: i32,

    /// Convert robot_state id to string
    pub robot_state_str: std::string::String,

    /// position control: 0, torque control: 1
    pub actual_mode: i8,

    /// joint space: 0, task space: 1
    pub actual_space: i8,

    /// current joint angle list
    pub current_posj: [f64; 6],

    /// current joint velocity list []
    pub current_velj: [f64; 6],

    /// Position Actual Value in ABS
    pub joint_abs: [f64; 6],

    /// Joint Error
    pub joint_err: [f64; 6],

    /// target joint angle list
    pub target_posj: [f64; 6],

    /// target joint velocity list []
    pub target_velj: [f64; 6],

    /// current task angle list []
    pub current_posx: [f64; 6],

    /// current task tool angle list []
    pub current_tool_posx: [f64; 6],

    /// current task velocity list []
    pub current_velx: [f64; 6],

    /// Task Error
    pub task_err: [f64; 6],

    /// target task velocity list []
    pub target_velx: [f64; 6],

    /// target task position list []
    pub target_posx: [f64; 6],

    /// dynamic torque
    pub dynamic_tor: [f64; 6],

    /// joint torque sensor
    pub actual_jts: [f64; 6],

    /// external joint torque
    pub actual_ejt: [f64; 6],

    /// external tool torque
    pub actual_ett: [f64; 6],

    /// brake status
    pub actual_bk: [i8; 6],

    /// motor current
    pub actual_mc: [f64; 6],

    /// motor temperature
    pub actual_mt: [f64; 6],

    /// Solution Space (0 ~ 7)
    pub solution_space: i8,

    /// internal clock counter
    pub sync_time: f64,

    /// cockpit(robot button) info.
    pub actual_bt: [i8; 5],

    /// Rotation Matrix [3][3]
    pub rotation_matrix: Vec<std_msgs::msg::Float64MultiArray>,

    /// Digital Input in Control Box(0 ~ 15 ; 0 : ON, 1 : OFF)
    pub ctrlbox_digital_input: [i8; 16],

    /// Digital Output in Control Box(0 ~ 15 ; 0 : ON, 1 : OFF)
    pub ctrlbox_digital_output: [i8; 16],

    /// Digital Input in Flange(0 ~ 5 ; 0 : ON, 1 : OFF) x1 port : 0 ~ 2, x2 port : 3 ~ 5
    pub flange_digital_input: [i8; 6],

    /// Digital Output in Flange(0 ~ 5 ; 0 : ON, 1 : OFF)
    pub flange_digital_output: [i8; 6],

    /// Custom msg for modbus state(refer to ModbusState.msg)
    pub modbus_state: Vec<super::msg::ModbusState>,


    // This member is not documented.
    #[allow(missing_docs)]
    pub access_control: i32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub homming_completed: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub tp_initialized: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub mastering_need: i8,


    // This member is not documented.
    #[allow(missing_docs)]
    pub drl_stopped: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub disconnected: bool,

    /// ____________________________________________________________________________________________
    ///  The following messages have been updated since version M2.50 or higher.
    /// ____________________________________________________________________________________________
    ///  world to base releation
    pub f_actual_w2b: [f64; 6],

    /// Wolrd position actual value [2][6] : (0: tool, 1: flange) [mm, degree]
    pub f_current_pos_world: Vec<std_msgs::msg::Float64MultiArray>,

    /// World velocity Actual Value [mm/sec, degree/sec]
    pub f_current_vel_world: [f64; 6],

    /// External Task Force/Torque [N, Nm]
    pub f_world_ext_target_torque: [f64; 6],

    /// World target Position [mm, degree]
    pub f_target_pos_world: [f64; 6],

    /// World target Velocity [mm/sec, degree/sec]
    pub f_target_vel_world: [f64; 6],

    /// World rotation matrix [3][3]
    pub f_rotation_matrix_world: Vec<std_msgs::msg::Float64MultiArray>,

    /// Actual user coord number ## 101 ~ 120
    pub i_actual_user_coord_num: i8,

    /// Coordinate Reference(base : 0  world : 2)
    pub i_coord_ref: i8,

    /// User position Actual Value [2][6] : (0:tool, 1:flange) [mm, degree]
    pub f_current_pos_user: Vec<std_msgs::msg::Float64MultiArray>,

    /// User velocity Actual Value [mm/sec, degree/sec]
    pub f_current_vel_user: [f64; 6],

    /// External Task Force/Torque [N, Nm]
    pub f_user_ext_task_torque: [f64; 6],

    /// User target Position [mm, degree]
    pub f_target_pos_user: [f64; 6],

    /// User target Velocity [mm/sec, degree/sec]
    pub f_target_vel_user: [f64; 6],

    /// User rotation matrix [3][3]
    pub f_rotation_matrix_user: Vec<std_msgs::msg::Float64MultiArray>,

    /// Analog input data ## Current mode : 0~20.0[mA] , Voltage mode : 0~10.0[V]
    pub f_actual_analog_input: [f64; 6],

    /// Switch input data
    pub b_actual_switch_input: [bool; 3],

    /// Safety input data
    pub b_actual_safety_input: [bool; 2],

    /// Analog input type  index = channel, type: current(0), voltage(1)
    pub i_actual_analog_input_type: [i8; 2],

    /// Analog output data ## Current mode : 0~20.0[mA] , Voltage mode : 0~10.0[V]
    pub f_target_analog_output: [f64; 2],

    /// Analog output type index = channel, type: current(0), voltage(1)
    pub i_target_analog_output_type: [i8; 2],

    /// Encorder strove signal
    pub b_actual_encorder_strove_signal: [bool; 2],

    /// Encorder raw data
    pub i_actual_encorder_raw_data: [i8; 2],

    /// Encorder reset signal
    pub b_actual_encorder_reset_signal: [bool; 2],

}



impl Default for RobotState {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::RobotState::default())
  }
}

impl rosidl_runtime_rs::Message for RobotState {
  type RmwMsg = super::msg::rmw::RobotState;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        robot_state: msg.robot_state,
        robot_state_str: msg.robot_state_str.as_str().into(),
        actual_mode: msg.actual_mode,
        actual_space: msg.actual_space,
        current_posj: msg.current_posj,
        current_velj: msg.current_velj,
        joint_abs: msg.joint_abs,
        joint_err: msg.joint_err,
        target_posj: msg.target_posj,
        target_velj: msg.target_velj,
        current_posx: msg.current_posx,
        current_tool_posx: msg.current_tool_posx,
        current_velx: msg.current_velx,
        task_err: msg.task_err,
        target_velx: msg.target_velx,
        target_posx: msg.target_posx,
        dynamic_tor: msg.dynamic_tor,
        actual_jts: msg.actual_jts,
        actual_ejt: msg.actual_ejt,
        actual_ett: msg.actual_ett,
        actual_bk: msg.actual_bk,
        actual_mc: msg.actual_mc,
        actual_mt: msg.actual_mt,
        solution_space: msg.solution_space,
        sync_time: msg.sync_time,
        actual_bt: msg.actual_bt,
        rotation_matrix: msg.rotation_matrix
          .into_iter()
          .map(|elem| std_msgs::msg::Float64MultiArray::into_rmw_message(std::borrow::Cow::Owned(elem)).into_owned())
          .collect(),
        ctrlbox_digital_input: msg.ctrlbox_digital_input,
        ctrlbox_digital_output: msg.ctrlbox_digital_output,
        flange_digital_input: msg.flange_digital_input,
        flange_digital_output: msg.flange_digital_output,
        modbus_state: msg.modbus_state
          .into_iter()
          .map(|elem| super::msg::ModbusState::into_rmw_message(std::borrow::Cow::Owned(elem)).into_owned())
          .collect(),
        access_control: msg.access_control,
        homming_completed: msg.homming_completed,
        tp_initialized: msg.tp_initialized,
        mastering_need: msg.mastering_need,
        drl_stopped: msg.drl_stopped,
        disconnected: msg.disconnected,
        f_actual_w2b: msg.f_actual_w2b,
        f_current_pos_world: msg.f_current_pos_world
          .into_iter()
          .map(|elem| std_msgs::msg::Float64MultiArray::into_rmw_message(std::borrow::Cow::Owned(elem)).into_owned())
          .collect(),
        f_current_vel_world: msg.f_current_vel_world,
        f_world_ext_target_torque: msg.f_world_ext_target_torque,
        f_target_pos_world: msg.f_target_pos_world,
        f_target_vel_world: msg.f_target_vel_world,
        f_rotation_matrix_world: msg.f_rotation_matrix_world
          .into_iter()
          .map(|elem| std_msgs::msg::Float64MultiArray::into_rmw_message(std::borrow::Cow::Owned(elem)).into_owned())
          .collect(),
        i_actual_user_coord_num: msg.i_actual_user_coord_num,
        i_coord_ref: msg.i_coord_ref,
        f_current_pos_user: msg.f_current_pos_user
          .into_iter()
          .map(|elem| std_msgs::msg::Float64MultiArray::into_rmw_message(std::borrow::Cow::Owned(elem)).into_owned())
          .collect(),
        f_current_vel_user: msg.f_current_vel_user,
        f_user_ext_task_torque: msg.f_user_ext_task_torque,
        f_target_pos_user: msg.f_target_pos_user,
        f_target_vel_user: msg.f_target_vel_user,
        f_rotation_matrix_user: msg.f_rotation_matrix_user
          .into_iter()
          .map(|elem| std_msgs::msg::Float64MultiArray::into_rmw_message(std::borrow::Cow::Owned(elem)).into_owned())
          .collect(),
        f_actual_analog_input: msg.f_actual_analog_input,
        b_actual_switch_input: msg.b_actual_switch_input,
        b_actual_safety_input: msg.b_actual_safety_input,
        i_actual_analog_input_type: msg.i_actual_analog_input_type,
        f_target_analog_output: msg.f_target_analog_output,
        i_target_analog_output_type: msg.i_target_analog_output_type,
        b_actual_encorder_strove_signal: msg.b_actual_encorder_strove_signal,
        i_actual_encorder_raw_data: msg.i_actual_encorder_raw_data,
        b_actual_encorder_reset_signal: msg.b_actual_encorder_reset_signal,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      robot_state: msg.robot_state,
        robot_state_str: msg.robot_state_str.as_str().into(),
      actual_mode: msg.actual_mode,
      actual_space: msg.actual_space,
        current_posj: msg.current_posj,
        current_velj: msg.current_velj,
        joint_abs: msg.joint_abs,
        joint_err: msg.joint_err,
        target_posj: msg.target_posj,
        target_velj: msg.target_velj,
        current_posx: msg.current_posx,
        current_tool_posx: msg.current_tool_posx,
        current_velx: msg.current_velx,
        task_err: msg.task_err,
        target_velx: msg.target_velx,
        target_posx: msg.target_posx,
        dynamic_tor: msg.dynamic_tor,
        actual_jts: msg.actual_jts,
        actual_ejt: msg.actual_ejt,
        actual_ett: msg.actual_ett,
        actual_bk: msg.actual_bk,
        actual_mc: msg.actual_mc,
        actual_mt: msg.actual_mt,
      solution_space: msg.solution_space,
      sync_time: msg.sync_time,
        actual_bt: msg.actual_bt,
        rotation_matrix: msg.rotation_matrix
          .iter()
          .map(|elem| std_msgs::msg::Float64MultiArray::into_rmw_message(std::borrow::Cow::Borrowed(elem)).into_owned())
          .collect(),
        ctrlbox_digital_input: msg.ctrlbox_digital_input,
        ctrlbox_digital_output: msg.ctrlbox_digital_output,
        flange_digital_input: msg.flange_digital_input,
        flange_digital_output: msg.flange_digital_output,
        modbus_state: msg.modbus_state
          .iter()
          .map(|elem| super::msg::ModbusState::into_rmw_message(std::borrow::Cow::Borrowed(elem)).into_owned())
          .collect(),
      access_control: msg.access_control,
      homming_completed: msg.homming_completed,
      tp_initialized: msg.tp_initialized,
      mastering_need: msg.mastering_need,
      drl_stopped: msg.drl_stopped,
      disconnected: msg.disconnected,
        f_actual_w2b: msg.f_actual_w2b,
        f_current_pos_world: msg.f_current_pos_world
          .iter()
          .map(|elem| std_msgs::msg::Float64MultiArray::into_rmw_message(std::borrow::Cow::Borrowed(elem)).into_owned())
          .collect(),
        f_current_vel_world: msg.f_current_vel_world,
        f_world_ext_target_torque: msg.f_world_ext_target_torque,
        f_target_pos_world: msg.f_target_pos_world,
        f_target_vel_world: msg.f_target_vel_world,
        f_rotation_matrix_world: msg.f_rotation_matrix_world
          .iter()
          .map(|elem| std_msgs::msg::Float64MultiArray::into_rmw_message(std::borrow::Cow::Borrowed(elem)).into_owned())
          .collect(),
      i_actual_user_coord_num: msg.i_actual_user_coord_num,
      i_coord_ref: msg.i_coord_ref,
        f_current_pos_user: msg.f_current_pos_user
          .iter()
          .map(|elem| std_msgs::msg::Float64MultiArray::into_rmw_message(std::borrow::Cow::Borrowed(elem)).into_owned())
          .collect(),
        f_current_vel_user: msg.f_current_vel_user,
        f_user_ext_task_torque: msg.f_user_ext_task_torque,
        f_target_pos_user: msg.f_target_pos_user,
        f_target_vel_user: msg.f_target_vel_user,
        f_rotation_matrix_user: msg.f_rotation_matrix_user
          .iter()
          .map(|elem| std_msgs::msg::Float64MultiArray::into_rmw_message(std::borrow::Cow::Borrowed(elem)).into_owned())
          .collect(),
        f_actual_analog_input: msg.f_actual_analog_input,
        b_actual_switch_input: msg.b_actual_switch_input,
        b_actual_safety_input: msg.b_actual_safety_input,
        i_actual_analog_input_type: msg.i_actual_analog_input_type,
        f_target_analog_output: msg.f_target_analog_output,
        i_target_analog_output_type: msg.i_target_analog_output_type,
        b_actual_encorder_strove_signal: msg.b_actual_encorder_strove_signal,
        i_actual_encorder_raw_data: msg.i_actual_encorder_raw_data,
        b_actual_encorder_reset_signal: msg.b_actual_encorder_reset_signal,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      robot_state: msg.robot_state,
      robot_state_str: msg.robot_state_str.to_string(),
      actual_mode: msg.actual_mode,
      actual_space: msg.actual_space,
      current_posj: msg.current_posj,
      current_velj: msg.current_velj,
      joint_abs: msg.joint_abs,
      joint_err: msg.joint_err,
      target_posj: msg.target_posj,
      target_velj: msg.target_velj,
      current_posx: msg.current_posx,
      current_tool_posx: msg.current_tool_posx,
      current_velx: msg.current_velx,
      task_err: msg.task_err,
      target_velx: msg.target_velx,
      target_posx: msg.target_posx,
      dynamic_tor: msg.dynamic_tor,
      actual_jts: msg.actual_jts,
      actual_ejt: msg.actual_ejt,
      actual_ett: msg.actual_ett,
      actual_bk: msg.actual_bk,
      actual_mc: msg.actual_mc,
      actual_mt: msg.actual_mt,
      solution_space: msg.solution_space,
      sync_time: msg.sync_time,
      actual_bt: msg.actual_bt,
      rotation_matrix: msg.rotation_matrix
          .into_iter()
          .map(std_msgs::msg::Float64MultiArray::from_rmw_message)
          .collect(),
      ctrlbox_digital_input: msg.ctrlbox_digital_input,
      ctrlbox_digital_output: msg.ctrlbox_digital_output,
      flange_digital_input: msg.flange_digital_input,
      flange_digital_output: msg.flange_digital_output,
      modbus_state: msg.modbus_state
          .into_iter()
          .map(super::msg::ModbusState::from_rmw_message)
          .collect(),
      access_control: msg.access_control,
      homming_completed: msg.homming_completed,
      tp_initialized: msg.tp_initialized,
      mastering_need: msg.mastering_need,
      drl_stopped: msg.drl_stopped,
      disconnected: msg.disconnected,
      f_actual_w2b: msg.f_actual_w2b,
      f_current_pos_world: msg.f_current_pos_world
          .into_iter()
          .map(std_msgs::msg::Float64MultiArray::from_rmw_message)
          .collect(),
      f_current_vel_world: msg.f_current_vel_world,
      f_world_ext_target_torque: msg.f_world_ext_target_torque,
      f_target_pos_world: msg.f_target_pos_world,
      f_target_vel_world: msg.f_target_vel_world,
      f_rotation_matrix_world: msg.f_rotation_matrix_world
          .into_iter()
          .map(std_msgs::msg::Float64MultiArray::from_rmw_message)
          .collect(),
      i_actual_user_coord_num: msg.i_actual_user_coord_num,
      i_coord_ref: msg.i_coord_ref,
      f_current_pos_user: msg.f_current_pos_user
          .into_iter()
          .map(std_msgs::msg::Float64MultiArray::from_rmw_message)
          .collect(),
      f_current_vel_user: msg.f_current_vel_user,
      f_user_ext_task_torque: msg.f_user_ext_task_torque,
      f_target_pos_user: msg.f_target_pos_user,
      f_target_vel_user: msg.f_target_vel_user,
      f_rotation_matrix_user: msg.f_rotation_matrix_user
          .into_iter()
          .map(std_msgs::msg::Float64MultiArray::from_rmw_message)
          .collect(),
      f_actual_analog_input: msg.f_actual_analog_input,
      b_actual_switch_input: msg.b_actual_switch_input,
      b_actual_safety_input: msg.b_actual_safety_input,
      i_actual_analog_input_type: msg.i_actual_analog_input_type,
      f_target_analog_output: msg.f_target_analog_output,
      i_target_analog_output_type: msg.i_target_analog_output_type,
      b_actual_encorder_strove_signal: msg.b_actual_encorder_strove_signal,
      i_actual_encorder_raw_data: msg.i_actual_encorder_raw_data,
      b_actual_encorder_reset_signal: msg.b_actual_encorder_reset_signal,
    }
  }
}


// Corresponds to dsr_msgs2__msg__RobotStop
/// ____________________________________________________________________________________________
///  [ robot stop mode ] 
///  0 : STOP_TYPE_QUICK_STO
///  1 : STOP_TYPE_QUICK
///  2 : STOP_TYPE_SLOW
///  3 : STOP_TYPE_HOLD = STOP_TYPE_EMERGENCY
///
/// ____________________________________________________________________________________________

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct RobotStop {

    // This member is not documented.
    #[allow(missing_docs)]
    pub stop_mode: i32,

}



impl Default for RobotStop {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::RobotStop::default())
  }
}

impl rosidl_runtime_rs::Message for RobotStop {
  type RmwMsg = super::msg::rmw::RobotStop;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        stop_mode: msg.stop_mode,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      stop_mode: msg.stop_mode,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      stop_mode: msg.stop_mode,
    }
  }
}


// Corresponds to dsr_msgs2__msg__JogMultiAxis
/// ____________________________________________________________________________________________
///  multi jog
///  multi jog speed = (250mm/s x 1.73) x unit vecter x speed 
/// ____________________________________________________________________________________________

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct JogMultiAxis {
    /// unit vecter of Task space [Tx, Ty, Tz, Rx, Ry, Rz] : -1.0 ~ +1.0
    pub jog_axis: [f64; 6],

    /// 0 : MOVE_REFERENCE_BASE, 1 : MOVE_REFERENCE_TOOL, 2 : MOVE_REFERENCE_WORLD
    pub move_reference: i8,

    /// jog speed
    pub speed: f64,

}



impl Default for JogMultiAxis {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::JogMultiAxis::default())
  }
}

impl rosidl_runtime_rs::Message for JogMultiAxis {
  type RmwMsg = super::msg::rmw::JogMultiAxis;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        jog_axis: msg.jog_axis,
        move_reference: msg.move_reference,
        speed: msg.speed,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        jog_axis: msg.jog_axis,
      move_reference: msg.move_reference,
      speed: msg.speed,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      jog_axis: msg.jog_axis,
      move_reference: msg.move_reference,
      speed: msg.speed,
    }
  }
}


// Corresponds to dsr_msgs2__msg__AlterMotionStream
/// ____________________________________________________________________________________________
///  alter_motion  
///
/// ____________________________________________________________________________________________

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct AlterMotionStream {
    /// position
    pub pos: [f64; 6],

}



impl Default for AlterMotionStream {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::AlterMotionStream::default())
  }
}

impl rosidl_runtime_rs::Message for AlterMotionStream {
  type RmwMsg = super::msg::rmw::AlterMotionStream;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        pos: msg.pos,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        pos: msg.pos,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      pos: msg.pos,
    }
  }
}


// Corresponds to dsr_msgs2__msg__ServojStream
/// ____________________________________________________________________________________________
///  servoj
///
/// ____________________________________________________________________________________________

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ServojStream {
    /// position
    pub pos: [f64; 6],

    /// velocity
    pub vel: [f64; 6],

    /// acceleration
    pub acc: [f64; 6],

    /// time
    pub time: f64,

    /// servoj mode; 0:DR_SERVO_OVERRIDE, 1:DR_SERVO_QUEUE
    pub mode: i8,

}



impl Default for ServojStream {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::ServojStream::default())
  }
}

impl rosidl_runtime_rs::Message for ServojStream {
  type RmwMsg = super::msg::rmw::ServojStream;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        pos: msg.pos,
        vel: msg.vel,
        acc: msg.acc,
        time: msg.time,
        mode: msg.mode,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        pos: msg.pos,
        vel: msg.vel,
        acc: msg.acc,
      time: msg.time,
      mode: msg.mode,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      pos: msg.pos,
      vel: msg.vel,
      acc: msg.acc,
      time: msg.time,
      mode: msg.mode,
    }
  }
}


// Corresponds to dsr_msgs2__msg__ServolStream
/// ____________________________________________________________________________________________
///  servol
///
/// ____________________________________________________________________________________________

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ServolStream {
    /// position
    pub pos: [f64; 6],

    /// velocity
    pub vel: [f64; 2],

    /// acceleration
    pub acc: [f64; 2],

    /// time
    pub time: f64,

}



impl Default for ServolStream {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::ServolStream::default())
  }
}

impl rosidl_runtime_rs::Message for ServolStream {
  type RmwMsg = super::msg::rmw::ServolStream;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        pos: msg.pos,
        vel: msg.vel,
        acc: msg.acc,
        time: msg.time,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        pos: msg.pos,
        vel: msg.vel,
        acc: msg.acc,
      time: msg.time,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      pos: msg.pos,
      vel: msg.vel,
      acc: msg.acc,
      time: msg.time,
    }
  }
}


// Corresponds to dsr_msgs2__msg__SpeedjStream
/// ____________________________________________________________________________________________
///  speedj
///
/// ____________________________________________________________________________________________

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SpeedjStream {
    /// velocity
    pub vel: [f64; 6],

    /// acceleration
    pub acc: [f64; 6],

    /// time
    pub time: f64,

}



impl Default for SpeedjStream {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::SpeedjStream::default())
  }
}

impl rosidl_runtime_rs::Message for SpeedjStream {
  type RmwMsg = super::msg::rmw::SpeedjStream;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        vel: msg.vel,
        acc: msg.acc,
        time: msg.time,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        vel: msg.vel,
        acc: msg.acc,
      time: msg.time,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      vel: msg.vel,
      acc: msg.acc,
      time: msg.time,
    }
  }
}


// Corresponds to dsr_msgs2__msg__SpeedlStream
/// ____________________________________________________________________________________________
///  speedl
///
/// ____________________________________________________________________________________________

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SpeedlStream {
    /// velocity
    pub vel: [f64; 6],

    /// acceleration
    pub acc: [f64; 2],

    /// time
    pub time: f64,

}



impl Default for SpeedlStream {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::SpeedlStream::default())
  }
}

impl rosidl_runtime_rs::Message for SpeedlStream {
  type RmwMsg = super::msg::rmw::SpeedlStream;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        vel: msg.vel,
        acc: msg.acc,
        time: msg.time,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        vel: msg.vel,
        acc: msg.acc,
      time: msg.time,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      vel: msg.vel,
      acc: msg.acc,
      time: msg.time,
    }
  }
}


// Corresponds to dsr_msgs2__msg__RobotDisconnection
/// Event driven when the robot connection losts.

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct RobotDisconnection {

    // This member is not documented.
    #[allow(missing_docs)]
    pub structure_needs_at_least_one_member: u8,

}



impl Default for RobotDisconnection {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::RobotDisconnection::default())
  }
}

impl rosidl_runtime_rs::Message for RobotDisconnection {
  type RmwMsg = super::msg::rmw::RobotDisconnection;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        structure_needs_at_least_one_member: msg.structure_needs_at_least_one_member,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      structure_needs_at_least_one_member: msg.structure_needs_at_least_one_member,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      structure_needs_at_least_one_member: msg.structure_needs_at_least_one_member,
    }
  }
}


// Corresponds to dsr_msgs2__msg__RobotStateRt
/// timestamp at the data of data acquisition

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct RobotStateRt {

    // This member is not documented.
    #[allow(missing_docs)]
    pub time_stamp: f64,

    /// actual joint position from incremental encoder at motor side(used for control)
    pub actual_joint_position: [f64; 6],

    /// actual joint position from absolute encoder at link side (used for exact link position)
    pub actual_joint_position_abs: [f64; 6],

    /// actual joint velocity from incremental encoder at motor side
    pub actual_joint_velocity: [f64; 6],

    /// actual joint velocity from absolute encoder at link side
    pub actual_joint_velocity_abs: [f64; 6],

    /// actual robot tcp position w.r.t. base coordinates: (x, y, z, a, b, c), where (a, b, c) follows Euler ZYZ notation [mm, deg]
    pub actual_tcp_position: [f64; 6],

    /// actual robot tcp velocity w.r.t. base coordinates [mm, deg/s]
    pub actual_tcp_velocity: [f64; 6],

    /// actual robot flange position w.r.t. base coordinates: (x, y, z, a, b, c), where (a, b, c) follows Euler ZYZ notation [mm, deg]
    pub actual_flange_position: [f64; 6],

    /// robot flange velocity w.r.t. base coordinates [mm, deg/s]
    pub actual_flange_velocity: [f64; 6],

    /// actual motor torque applying gear ratio = gear_ratio * current2torque_constant * motor current
    pub actual_motor_torque: [f64; 6],

    /// estimated joint torque by robot controller
    pub actual_joint_torque: [f64; 6],

    /// calibrated joint torque sensor data
    pub raw_joint_torque: [f64; 6],

    /// calibrated force torque sensor data w.r.t. flange coordinates [N, Nm]
    pub raw_force_torque: [f64; 6],

    /// estimated external joint torque
    pub external_joint_torque: [f64; 6],

    /// estimated tcp force w.r.t. base coordinates [N, Nm]
    pub external_tcp_force: [f64; 6],

    /// target joint position
    pub target_joint_position: [f64; 6],

    /// target joint velocity
    pub target_joint_velocity: [f64; 6],

    /// target joint acceleration
    pub target_joint_acceleration: [f64; 6],

    /// target motor torque
    pub target_motor_torque: [f64; 6],

    /// target tcp position w.r.t. base coordinates: (x, y, z, a, b, c), where (a, b, c) follows Euler ZYZ notation [mm, deg]
    pub target_tcp_position: [f64; 6],

    /// target tcp velocity w.r.t. base coordinates [mm, deg/s]
    pub target_tcp_velocity: [f64; 6],

    /// jacobian matrix=J(q) w.r.t. base coordinates
    pub jacobian_matrix: Vec<std_msgs::msg::Float64MultiArray>,

    /// gravity torque=g(q)
    pub gravity_torque: [f64; 6],

    /// coriolis matrix=C(q,q_dot)  [6][6]
    pub coriolis_matrix: Vec<std_msgs::msg::Float64MultiArray>,

    /// mass matrix=M(q) [6][6]
    pub mass_matrix: Vec<std_msgs::msg::Float64MultiArray>,

    /// robot configuration
    pub solution_space: u16,

    /// minimum singular value
    pub singularity: f64,

    /// current operation speed rate(1~100 %)
    pub operation_speed_rate: f64,

    /// joint temperature(celsius)
    pub joint_temperature: [f64; 6],

    /// controller digital input(16 channel)
    pub controller_digital_input: u16,

    /// controller digital output(16 channel)
    pub controller_digital_output: u16,

    /// controller analog input type(2 channel)
    pub controller_analog_input_type: [u8; 2],

    /// controller analog input(2 channel)
    pub controller_analog_input: [f64; 2],

    /// controller analog output type(2 channel)
    pub controller_analog_output_type: [u8; 2],

    /// controller analog output(2 channel)
    pub controller_analog_output: [f64; 2],

    /// flange digital input(A-Series: 2 channel, M/H-Series: 6 channel)
    pub flange_digital_input: u8,

    /// flange digital output(A-Series: 2 channel, M/H-Series: 6 channel)
    pub flange_digital_output: u8,

    /// flange analog input(A-Series: 2 channel, M/H-Series: 4 channel)
    pub flange_analog_input: [f64; 4],

    /// strobe count(increased by 1 when detecting setting edge)
    pub external_encoder_strobe_count: [u8; 2],

    /// external encoder count
    pub external_encoder_count: [u16; 2],

    /// final goal joint position (reserved)
    pub goal_joint_position: [f64; 6],

    /// final goal tcp position (reserved)
    pub goal_tcp_position: [f64; 6],

    /// ROBOT_MODE_MANUAL(0), ROBOT_MODE_AUTONOMOUS(1), ROBOT_MODE_MEASURE(2)
    pub robot_mode: u8,

    /// STATE_INITIALIZING(0), STATE_STANDBY(1), STATE_MOVING(2), STATE_SAFE_OFF(3), STATE_TEACHING(4), STATE_SAFE_STOP(5), STATE_EMERGENCY_STOP, STATE_HOMMING, STATE_RECOVERY, STATE_SAFE_STOP2, STATE_SAFE_OFF2,
    pub robot_state: u8,

    /// position control mode, torque mode
    pub control_mode: u16,

    /// Reserved
    #[cfg_attr(feature = "serde", serde(with = "serde_big_array::BigArray"))]
    pub reserved: [u8; 256],

}



impl Default for RobotStateRt {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::RobotStateRt::default())
  }
}

impl rosidl_runtime_rs::Message for RobotStateRt {
  type RmwMsg = super::msg::rmw::RobotStateRt;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        time_stamp: msg.time_stamp,
        actual_joint_position: msg.actual_joint_position,
        actual_joint_position_abs: msg.actual_joint_position_abs,
        actual_joint_velocity: msg.actual_joint_velocity,
        actual_joint_velocity_abs: msg.actual_joint_velocity_abs,
        actual_tcp_position: msg.actual_tcp_position,
        actual_tcp_velocity: msg.actual_tcp_velocity,
        actual_flange_position: msg.actual_flange_position,
        actual_flange_velocity: msg.actual_flange_velocity,
        actual_motor_torque: msg.actual_motor_torque,
        actual_joint_torque: msg.actual_joint_torque,
        raw_joint_torque: msg.raw_joint_torque,
        raw_force_torque: msg.raw_force_torque,
        external_joint_torque: msg.external_joint_torque,
        external_tcp_force: msg.external_tcp_force,
        target_joint_position: msg.target_joint_position,
        target_joint_velocity: msg.target_joint_velocity,
        target_joint_acceleration: msg.target_joint_acceleration,
        target_motor_torque: msg.target_motor_torque,
        target_tcp_position: msg.target_tcp_position,
        target_tcp_velocity: msg.target_tcp_velocity,
        jacobian_matrix: msg.jacobian_matrix
          .into_iter()
          .map(|elem| std_msgs::msg::Float64MultiArray::into_rmw_message(std::borrow::Cow::Owned(elem)).into_owned())
          .collect(),
        gravity_torque: msg.gravity_torque,
        coriolis_matrix: msg.coriolis_matrix
          .into_iter()
          .map(|elem| std_msgs::msg::Float64MultiArray::into_rmw_message(std::borrow::Cow::Owned(elem)).into_owned())
          .collect(),
        mass_matrix: msg.mass_matrix
          .into_iter()
          .map(|elem| std_msgs::msg::Float64MultiArray::into_rmw_message(std::borrow::Cow::Owned(elem)).into_owned())
          .collect(),
        solution_space: msg.solution_space,
        singularity: msg.singularity,
        operation_speed_rate: msg.operation_speed_rate,
        joint_temperature: msg.joint_temperature,
        controller_digital_input: msg.controller_digital_input,
        controller_digital_output: msg.controller_digital_output,
        controller_analog_input_type: msg.controller_analog_input_type,
        controller_analog_input: msg.controller_analog_input,
        controller_analog_output_type: msg.controller_analog_output_type,
        controller_analog_output: msg.controller_analog_output,
        flange_digital_input: msg.flange_digital_input,
        flange_digital_output: msg.flange_digital_output,
        flange_analog_input: msg.flange_analog_input,
        external_encoder_strobe_count: msg.external_encoder_strobe_count,
        external_encoder_count: msg.external_encoder_count,
        goal_joint_position: msg.goal_joint_position,
        goal_tcp_position: msg.goal_tcp_position,
        robot_mode: msg.robot_mode,
        robot_state: msg.robot_state,
        control_mode: msg.control_mode,
        reserved: msg.reserved,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      time_stamp: msg.time_stamp,
        actual_joint_position: msg.actual_joint_position,
        actual_joint_position_abs: msg.actual_joint_position_abs,
        actual_joint_velocity: msg.actual_joint_velocity,
        actual_joint_velocity_abs: msg.actual_joint_velocity_abs,
        actual_tcp_position: msg.actual_tcp_position,
        actual_tcp_velocity: msg.actual_tcp_velocity,
        actual_flange_position: msg.actual_flange_position,
        actual_flange_velocity: msg.actual_flange_velocity,
        actual_motor_torque: msg.actual_motor_torque,
        actual_joint_torque: msg.actual_joint_torque,
        raw_joint_torque: msg.raw_joint_torque,
        raw_force_torque: msg.raw_force_torque,
        external_joint_torque: msg.external_joint_torque,
        external_tcp_force: msg.external_tcp_force,
        target_joint_position: msg.target_joint_position,
        target_joint_velocity: msg.target_joint_velocity,
        target_joint_acceleration: msg.target_joint_acceleration,
        target_motor_torque: msg.target_motor_torque,
        target_tcp_position: msg.target_tcp_position,
        target_tcp_velocity: msg.target_tcp_velocity,
        jacobian_matrix: msg.jacobian_matrix
          .iter()
          .map(|elem| std_msgs::msg::Float64MultiArray::into_rmw_message(std::borrow::Cow::Borrowed(elem)).into_owned())
          .collect(),
        gravity_torque: msg.gravity_torque,
        coriolis_matrix: msg.coriolis_matrix
          .iter()
          .map(|elem| std_msgs::msg::Float64MultiArray::into_rmw_message(std::borrow::Cow::Borrowed(elem)).into_owned())
          .collect(),
        mass_matrix: msg.mass_matrix
          .iter()
          .map(|elem| std_msgs::msg::Float64MultiArray::into_rmw_message(std::borrow::Cow::Borrowed(elem)).into_owned())
          .collect(),
      solution_space: msg.solution_space,
      singularity: msg.singularity,
      operation_speed_rate: msg.operation_speed_rate,
        joint_temperature: msg.joint_temperature,
      controller_digital_input: msg.controller_digital_input,
      controller_digital_output: msg.controller_digital_output,
        controller_analog_input_type: msg.controller_analog_input_type,
        controller_analog_input: msg.controller_analog_input,
        controller_analog_output_type: msg.controller_analog_output_type,
        controller_analog_output: msg.controller_analog_output,
      flange_digital_input: msg.flange_digital_input,
      flange_digital_output: msg.flange_digital_output,
        flange_analog_input: msg.flange_analog_input,
        external_encoder_strobe_count: msg.external_encoder_strobe_count,
        external_encoder_count: msg.external_encoder_count,
        goal_joint_position: msg.goal_joint_position,
        goal_tcp_position: msg.goal_tcp_position,
      robot_mode: msg.robot_mode,
      robot_state: msg.robot_state,
      control_mode: msg.control_mode,
        reserved: msg.reserved,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      time_stamp: msg.time_stamp,
      actual_joint_position: msg.actual_joint_position,
      actual_joint_position_abs: msg.actual_joint_position_abs,
      actual_joint_velocity: msg.actual_joint_velocity,
      actual_joint_velocity_abs: msg.actual_joint_velocity_abs,
      actual_tcp_position: msg.actual_tcp_position,
      actual_tcp_velocity: msg.actual_tcp_velocity,
      actual_flange_position: msg.actual_flange_position,
      actual_flange_velocity: msg.actual_flange_velocity,
      actual_motor_torque: msg.actual_motor_torque,
      actual_joint_torque: msg.actual_joint_torque,
      raw_joint_torque: msg.raw_joint_torque,
      raw_force_torque: msg.raw_force_torque,
      external_joint_torque: msg.external_joint_torque,
      external_tcp_force: msg.external_tcp_force,
      target_joint_position: msg.target_joint_position,
      target_joint_velocity: msg.target_joint_velocity,
      target_joint_acceleration: msg.target_joint_acceleration,
      target_motor_torque: msg.target_motor_torque,
      target_tcp_position: msg.target_tcp_position,
      target_tcp_velocity: msg.target_tcp_velocity,
      jacobian_matrix: msg.jacobian_matrix
          .into_iter()
          .map(std_msgs::msg::Float64MultiArray::from_rmw_message)
          .collect(),
      gravity_torque: msg.gravity_torque,
      coriolis_matrix: msg.coriolis_matrix
          .into_iter()
          .map(std_msgs::msg::Float64MultiArray::from_rmw_message)
          .collect(),
      mass_matrix: msg.mass_matrix
          .into_iter()
          .map(std_msgs::msg::Float64MultiArray::from_rmw_message)
          .collect(),
      solution_space: msg.solution_space,
      singularity: msg.singularity,
      operation_speed_rate: msg.operation_speed_rate,
      joint_temperature: msg.joint_temperature,
      controller_digital_input: msg.controller_digital_input,
      controller_digital_output: msg.controller_digital_output,
      controller_analog_input_type: msg.controller_analog_input_type,
      controller_analog_input: msg.controller_analog_input,
      controller_analog_output_type: msg.controller_analog_output_type,
      controller_analog_output: msg.controller_analog_output,
      flange_digital_input: msg.flange_digital_input,
      flange_digital_output: msg.flange_digital_output,
      flange_analog_input: msg.flange_analog_input,
      external_encoder_strobe_count: msg.external_encoder_strobe_count,
      external_encoder_count: msg.external_encoder_count,
      goal_joint_position: msg.goal_joint_position,
      goal_tcp_position: msg.goal_tcp_position,
      robot_mode: msg.robot_mode,
      robot_state: msg.robot_state,
      control_mode: msg.control_mode,
      reserved: msg.reserved,
    }
  }
}


// Corresponds to dsr_msgs2__msg__ServojRtStream
/// ____________________________________________________________________________________________
///  servoj_rt
///
/// ____________________________________________________________________________________________

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ServojRtStream {
    /// position
    pub pos: [f64; 6],

    /// velocity
    pub vel: [f64; 6],

    /// acceleration
    pub acc: [f64; 6],

    /// time
    pub time: f64,

}



impl Default for ServojRtStream {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::ServojRtStream::default())
  }
}

impl rosidl_runtime_rs::Message for ServojRtStream {
  type RmwMsg = super::msg::rmw::ServojRtStream;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        pos: msg.pos,
        vel: msg.vel,
        acc: msg.acc,
        time: msg.time,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        pos: msg.pos,
        vel: msg.vel,
        acc: msg.acc,
      time: msg.time,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      pos: msg.pos,
      vel: msg.vel,
      acc: msg.acc,
      time: msg.time,
    }
  }
}


// Corresponds to dsr_msgs2__msg__ServolRtStream
/// ____________________________________________________________________________________________
///  servol_rt
///
/// ____________________________________________________________________________________________

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ServolRtStream {
    /// position
    pub pos: [f64; 6],

    /// velocity
    pub vel: [f64; 6],

    /// acceleration
    pub acc: [f64; 6],

    /// time
    pub time: f64,

}



impl Default for ServolRtStream {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::ServolRtStream::default())
  }
}

impl rosidl_runtime_rs::Message for ServolRtStream {
  type RmwMsg = super::msg::rmw::ServolRtStream;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        pos: msg.pos,
        vel: msg.vel,
        acc: msg.acc,
        time: msg.time,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        pos: msg.pos,
        vel: msg.vel,
        acc: msg.acc,
      time: msg.time,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      pos: msg.pos,
      vel: msg.vel,
      acc: msg.acc,
      time: msg.time,
    }
  }
}


// Corresponds to dsr_msgs2__msg__SpeedjRtStream
/// ____________________________________________________________________________________________
///  speedj_rt
///
/// ____________________________________________________________________________________________

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SpeedjRtStream {
    /// velocity
    pub vel: [f64; 6],

    /// acceleration
    pub acc: [f64; 6],

    /// time
    pub time: f64,

}



impl Default for SpeedjRtStream {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::SpeedjRtStream::default())
  }
}

impl rosidl_runtime_rs::Message for SpeedjRtStream {
  type RmwMsg = super::msg::rmw::SpeedjRtStream;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        vel: msg.vel,
        acc: msg.acc,
        time: msg.time,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        vel: msg.vel,
        acc: msg.acc,
      time: msg.time,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      vel: msg.vel,
      acc: msg.acc,
      time: msg.time,
    }
  }
}


// Corresponds to dsr_msgs2__msg__SpeedlRtStream
/// ____________________________________________________________________________________________
///  speedl_rt
///
/// ____________________________________________________________________________________________

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SpeedlRtStream {
    /// velocity
    pub vel: [f64; 6],

    /// acceleration
    pub acc: [f64; 6],

    /// time
    pub time: f64,

}



impl Default for SpeedlRtStream {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::SpeedlRtStream::default())
  }
}

impl rosidl_runtime_rs::Message for SpeedlRtStream {
  type RmwMsg = super::msg::rmw::SpeedlRtStream;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        vel: msg.vel,
        acc: msg.acc,
        time: msg.time,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        vel: msg.vel,
        acc: msg.acc,
      time: msg.time,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      vel: msg.vel,
      acc: msg.acc,
      time: msg.time,
    }
  }
}


// Corresponds to dsr_msgs2__msg__TorqueRtStream
/// ____________________________________________________________________________________________
///  torque_rt
///
/// ____________________________________________________________________________________________

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct TorqueRtStream {
    /// motor torque
    pub tor: [f64; 6],

    /// time
    pub time: f64,

}



impl Default for TorqueRtStream {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::TorqueRtStream::default())
  }
}

impl rosidl_runtime_rs::Message for TorqueRtStream {
  type RmwMsg = super::msg::rmw::TorqueRtStream;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        tor: msg.tor,
        time: msg.time,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        tor: msg.tor,
      time: msg.time,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      tor: msg.tor,
      time: msg.time,
    }
  }
}


