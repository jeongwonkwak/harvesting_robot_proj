#[cfg(feature = "serde")]
use serde::{Deserialize, Serialize};


#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__dsr_msgs2__msg__LogAlarm() -> *const std::ffi::c_void;
}

#[link(name = "dsr_msgs2__rosidl_generator_c")]
extern "C" {
    fn dsr_msgs2__msg__LogAlarm__init(msg: *mut LogAlarm) -> bool;
    fn dsr_msgs2__msg__LogAlarm__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<LogAlarm>, size: usize) -> bool;
    fn dsr_msgs2__msg__LogAlarm__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<LogAlarm>);
    fn dsr_msgs2__msg__LogAlarm__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<LogAlarm>, out_seq: *mut rosidl_runtime_rs::Sequence<LogAlarm>) -> bool;
}

// Corresponds to dsr_msgs2__msg__LogAlarm
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]

/// ____________________________________________________________________________________________
///  log of alarm
/// ____________________________________________________________________________________________

#[repr(C)]
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
    pub param: [rosidl_runtime_rs::String; 3],

}



impl Default for LogAlarm {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !dsr_msgs2__msg__LogAlarm__init(&mut msg as *mut _) {
        panic!("Call to dsr_msgs2__msg__LogAlarm__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for LogAlarm {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dsr_msgs2__msg__LogAlarm__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dsr_msgs2__msg__LogAlarm__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dsr_msgs2__msg__LogAlarm__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for LogAlarm {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for LogAlarm where Self: Sized {
  const TYPE_NAME: &'static str = "dsr_msgs2/msg/LogAlarm";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__dsr_msgs2__msg__LogAlarm() }
  }
}


#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__dsr_msgs2__msg__ModbusState() -> *const std::ffi::c_void;
}

#[link(name = "dsr_msgs2__rosidl_generator_c")]
extern "C" {
    fn dsr_msgs2__msg__ModbusState__init(msg: *mut ModbusState) -> bool;
    fn dsr_msgs2__msg__ModbusState__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<ModbusState>, size: usize) -> bool;
    fn dsr_msgs2__msg__ModbusState__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<ModbusState>);
    fn dsr_msgs2__msg__ModbusState__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<ModbusState>, out_seq: *mut rosidl_runtime_rs::Sequence<ModbusState>) -> bool;
}

// Corresponds to dsr_msgs2__msg__ModbusState
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]

/// ____________________________________________________________________________________________
/// Custom msg for RobotState.msg -- MAX_SIZE = 100
/// ____________________________________________________________________________________________

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ModbusState {
    /// Modbus Signal Name
    pub modbus_symbol: rosidl_runtime_rs::String,

    /// Modbus Register Value (Unsigned : 0 ~ 65535)
    pub modbus_value: i32,

}



impl Default for ModbusState {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !dsr_msgs2__msg__ModbusState__init(&mut msg as *mut _) {
        panic!("Call to dsr_msgs2__msg__ModbusState__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for ModbusState {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dsr_msgs2__msg__ModbusState__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dsr_msgs2__msg__ModbusState__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dsr_msgs2__msg__ModbusState__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for ModbusState {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for ModbusState where Self: Sized {
  const TYPE_NAME: &'static str = "dsr_msgs2/msg/ModbusState";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__dsr_msgs2__msg__ModbusState() }
  }
}


#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__dsr_msgs2__msg__RobotError() -> *const std::ffi::c_void;
}

#[link(name = "dsr_msgs2__rosidl_generator_c")]
extern "C" {
    fn dsr_msgs2__msg__RobotError__init(msg: *mut RobotError) -> bool;
    fn dsr_msgs2__msg__RobotError__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<RobotError>, size: usize) -> bool;
    fn dsr_msgs2__msg__RobotError__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<RobotError>);
    fn dsr_msgs2__msg__RobotError__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<RobotError>, out_seq: *mut rosidl_runtime_rs::Sequence<RobotError>) -> bool;
}

// Corresponds to dsr_msgs2__msg__RobotError
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]

/// ____________________________________________________________________________________________
///  [ robot error msg ] 
/// ____________________________________________________________________________________________

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct RobotError {
    /// INFO =1, WARN =2, ERROR =3
    pub level: i32,

    /// SYSTEM =1, MOTION =2, TP =3, INVERTER =4, SAFETY_CONTROLLER =5
    pub group: i32,

    /// error code
    pub code: i32,

    /// error msg 1
    pub msg1: rosidl_runtime_rs::String,

    /// error msg 2
    pub msg2: rosidl_runtime_rs::String,

    /// error msg 3
    pub msg3: rosidl_runtime_rs::String,

}



impl Default for RobotError {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !dsr_msgs2__msg__RobotError__init(&mut msg as *mut _) {
        panic!("Call to dsr_msgs2__msg__RobotError__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for RobotError {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dsr_msgs2__msg__RobotError__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dsr_msgs2__msg__RobotError__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dsr_msgs2__msg__RobotError__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for RobotError {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for RobotError where Self: Sized {
  const TYPE_NAME: &'static str = "dsr_msgs2/msg/RobotError";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__dsr_msgs2__msg__RobotError() }
  }
}


#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__dsr_msgs2__msg__RobotState() -> *const std::ffi::c_void;
}

#[link(name = "dsr_msgs2__rosidl_generator_c")]
extern "C" {
    fn dsr_msgs2__msg__RobotState__init(msg: *mut RobotState) -> bool;
    fn dsr_msgs2__msg__RobotState__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<RobotState>, size: usize) -> bool;
    fn dsr_msgs2__msg__RobotState__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<RobotState>);
    fn dsr_msgs2__msg__RobotState__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<RobotState>, out_seq: *mut rosidl_runtime_rs::Sequence<RobotState>) -> bool;
}

// Corresponds to dsr_msgs2__msg__RobotState
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]

/// ____________________________________________________________________________________________
///  state of robot
/// ____________________________________________________________________________________________

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct RobotState {
    /// 0 : STATE_INITIALIZING,   1 : STATE_STANDBY,   2 : STATE_MOVING,    3 : STATE_SAFE_OFF
    /// 4 : STATE_TEACHING,       5 : STATE_SAFE_STOP, 6 : STATE_EMERGENCY_STOP,
    /// 7 : STATE_EMERGENCY_STOP, 8 : STATE_HOMMING,   9 : STATE_RECOVERY,  10: STATE_SAFE_STOP2,
    /// 11: STATE_SAFE_OFF2,      12: STATE_RESERVED1, 13: STATE_RESERVED2, 14: STATE_RESERVED3,
    /// 15: STATE_NOT_READY       16: STATE_LAST
    pub robot_state: i32,

    /// Convert robot_state id to string
    pub robot_state_str: rosidl_runtime_rs::String,

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
    pub rotation_matrix: rosidl_runtime_rs::Sequence<std_msgs::msg::rmw::Float64MultiArray>,

    /// Digital Input in Control Box(0 ~ 15 ; 0 : ON, 1 : OFF)
    pub ctrlbox_digital_input: [i8; 16],

    /// Digital Output in Control Box(0 ~ 15 ; 0 : ON, 1 : OFF)
    pub ctrlbox_digital_output: [i8; 16],

    /// Digital Input in Flange(0 ~ 5 ; 0 : ON, 1 : OFF) x1 port : 0 ~ 2, x2 port : 3 ~ 5
    pub flange_digital_input: [i8; 6],

    /// Digital Output in Flange(0 ~ 5 ; 0 : ON, 1 : OFF)
    pub flange_digital_output: [i8; 6],

    /// Custom msg for modbus state(refer to ModbusState.msg)
    pub modbus_state: rosidl_runtime_rs::Sequence<super::super::msg::rmw::ModbusState>,


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
    pub f_current_pos_world: rosidl_runtime_rs::Sequence<std_msgs::msg::rmw::Float64MultiArray>,

    /// World velocity Actual Value [mm/sec, degree/sec]
    pub f_current_vel_world: [f64; 6],

    /// External Task Force/Torque [N, Nm]
    pub f_world_ext_target_torque: [f64; 6],

    /// World target Position [mm, degree]
    pub f_target_pos_world: [f64; 6],

    /// World target Velocity [mm/sec, degree/sec]
    pub f_target_vel_world: [f64; 6],

    /// World rotation matrix [3][3]
    pub f_rotation_matrix_world: rosidl_runtime_rs::Sequence<std_msgs::msg::rmw::Float64MultiArray>,

    /// Actual user coord number ## 101 ~ 120
    pub i_actual_user_coord_num: i8,

    /// Coordinate Reference(base : 0  world : 2)
    pub i_coord_ref: i8,

    /// User position Actual Value [2][6] : (0:tool, 1:flange) [mm, degree]
    pub f_current_pos_user: rosidl_runtime_rs::Sequence<std_msgs::msg::rmw::Float64MultiArray>,

    /// User velocity Actual Value [mm/sec, degree/sec]
    pub f_current_vel_user: [f64; 6],

    /// External Task Force/Torque [N, Nm]
    pub f_user_ext_task_torque: [f64; 6],

    /// User target Position [mm, degree]
    pub f_target_pos_user: [f64; 6],

    /// User target Velocity [mm/sec, degree/sec]
    pub f_target_vel_user: [f64; 6],

    /// User rotation matrix [3][3]
    pub f_rotation_matrix_user: rosidl_runtime_rs::Sequence<std_msgs::msg::rmw::Float64MultiArray>,

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
    unsafe {
      let mut msg = std::mem::zeroed();
      if !dsr_msgs2__msg__RobotState__init(&mut msg as *mut _) {
        panic!("Call to dsr_msgs2__msg__RobotState__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for RobotState {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dsr_msgs2__msg__RobotState__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dsr_msgs2__msg__RobotState__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dsr_msgs2__msg__RobotState__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for RobotState {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for RobotState where Self: Sized {
  const TYPE_NAME: &'static str = "dsr_msgs2/msg/RobotState";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__dsr_msgs2__msg__RobotState() }
  }
}


#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__dsr_msgs2__msg__RobotStop() -> *const std::ffi::c_void;
}

#[link(name = "dsr_msgs2__rosidl_generator_c")]
extern "C" {
    fn dsr_msgs2__msg__RobotStop__init(msg: *mut RobotStop) -> bool;
    fn dsr_msgs2__msg__RobotStop__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<RobotStop>, size: usize) -> bool;
    fn dsr_msgs2__msg__RobotStop__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<RobotStop>);
    fn dsr_msgs2__msg__RobotStop__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<RobotStop>, out_seq: *mut rosidl_runtime_rs::Sequence<RobotStop>) -> bool;
}

// Corresponds to dsr_msgs2__msg__RobotStop
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]

/// ____________________________________________________________________________________________
///  [ robot stop mode ] 
///  0 : STOP_TYPE_QUICK_STO
///  1 : STOP_TYPE_QUICK
///  2 : STOP_TYPE_SLOW
///  3 : STOP_TYPE_HOLD = STOP_TYPE_EMERGENCY
///
/// ____________________________________________________________________________________________

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct RobotStop {

    // This member is not documented.
    #[allow(missing_docs)]
    pub stop_mode: i32,

}



impl Default for RobotStop {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !dsr_msgs2__msg__RobotStop__init(&mut msg as *mut _) {
        panic!("Call to dsr_msgs2__msg__RobotStop__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for RobotStop {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dsr_msgs2__msg__RobotStop__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dsr_msgs2__msg__RobotStop__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dsr_msgs2__msg__RobotStop__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for RobotStop {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for RobotStop where Self: Sized {
  const TYPE_NAME: &'static str = "dsr_msgs2/msg/RobotStop";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__dsr_msgs2__msg__RobotStop() }
  }
}


#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__dsr_msgs2__msg__JogMultiAxis() -> *const std::ffi::c_void;
}

#[link(name = "dsr_msgs2__rosidl_generator_c")]
extern "C" {
    fn dsr_msgs2__msg__JogMultiAxis__init(msg: *mut JogMultiAxis) -> bool;
    fn dsr_msgs2__msg__JogMultiAxis__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<JogMultiAxis>, size: usize) -> bool;
    fn dsr_msgs2__msg__JogMultiAxis__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<JogMultiAxis>);
    fn dsr_msgs2__msg__JogMultiAxis__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<JogMultiAxis>, out_seq: *mut rosidl_runtime_rs::Sequence<JogMultiAxis>) -> bool;
}

// Corresponds to dsr_msgs2__msg__JogMultiAxis
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]

/// ____________________________________________________________________________________________
///  multi jog
///  multi jog speed = (250mm/s x 1.73) x unit vecter x speed 
/// ____________________________________________________________________________________________

#[repr(C)]
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
    unsafe {
      let mut msg = std::mem::zeroed();
      if !dsr_msgs2__msg__JogMultiAxis__init(&mut msg as *mut _) {
        panic!("Call to dsr_msgs2__msg__JogMultiAxis__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for JogMultiAxis {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dsr_msgs2__msg__JogMultiAxis__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dsr_msgs2__msg__JogMultiAxis__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dsr_msgs2__msg__JogMultiAxis__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for JogMultiAxis {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for JogMultiAxis where Self: Sized {
  const TYPE_NAME: &'static str = "dsr_msgs2/msg/JogMultiAxis";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__dsr_msgs2__msg__JogMultiAxis() }
  }
}


#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__dsr_msgs2__msg__AlterMotionStream() -> *const std::ffi::c_void;
}

#[link(name = "dsr_msgs2__rosidl_generator_c")]
extern "C" {
    fn dsr_msgs2__msg__AlterMotionStream__init(msg: *mut AlterMotionStream) -> bool;
    fn dsr_msgs2__msg__AlterMotionStream__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<AlterMotionStream>, size: usize) -> bool;
    fn dsr_msgs2__msg__AlterMotionStream__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<AlterMotionStream>);
    fn dsr_msgs2__msg__AlterMotionStream__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<AlterMotionStream>, out_seq: *mut rosidl_runtime_rs::Sequence<AlterMotionStream>) -> bool;
}

// Corresponds to dsr_msgs2__msg__AlterMotionStream
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]

/// ____________________________________________________________________________________________
///  alter_motion  
///
/// ____________________________________________________________________________________________

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct AlterMotionStream {
    /// position
    pub pos: [f64; 6],

}



impl Default for AlterMotionStream {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !dsr_msgs2__msg__AlterMotionStream__init(&mut msg as *mut _) {
        panic!("Call to dsr_msgs2__msg__AlterMotionStream__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for AlterMotionStream {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dsr_msgs2__msg__AlterMotionStream__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dsr_msgs2__msg__AlterMotionStream__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dsr_msgs2__msg__AlterMotionStream__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for AlterMotionStream {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for AlterMotionStream where Self: Sized {
  const TYPE_NAME: &'static str = "dsr_msgs2/msg/AlterMotionStream";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__dsr_msgs2__msg__AlterMotionStream() }
  }
}


#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__dsr_msgs2__msg__ServojStream() -> *const std::ffi::c_void;
}

#[link(name = "dsr_msgs2__rosidl_generator_c")]
extern "C" {
    fn dsr_msgs2__msg__ServojStream__init(msg: *mut ServojStream) -> bool;
    fn dsr_msgs2__msg__ServojStream__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<ServojStream>, size: usize) -> bool;
    fn dsr_msgs2__msg__ServojStream__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<ServojStream>);
    fn dsr_msgs2__msg__ServojStream__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<ServojStream>, out_seq: *mut rosidl_runtime_rs::Sequence<ServojStream>) -> bool;
}

// Corresponds to dsr_msgs2__msg__ServojStream
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]

/// ____________________________________________________________________________________________
///  servoj
///
/// ____________________________________________________________________________________________

#[repr(C)]
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
    unsafe {
      let mut msg = std::mem::zeroed();
      if !dsr_msgs2__msg__ServojStream__init(&mut msg as *mut _) {
        panic!("Call to dsr_msgs2__msg__ServojStream__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for ServojStream {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dsr_msgs2__msg__ServojStream__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dsr_msgs2__msg__ServojStream__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dsr_msgs2__msg__ServojStream__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for ServojStream {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for ServojStream where Self: Sized {
  const TYPE_NAME: &'static str = "dsr_msgs2/msg/ServojStream";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__dsr_msgs2__msg__ServojStream() }
  }
}


#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__dsr_msgs2__msg__ServolStream() -> *const std::ffi::c_void;
}

#[link(name = "dsr_msgs2__rosidl_generator_c")]
extern "C" {
    fn dsr_msgs2__msg__ServolStream__init(msg: *mut ServolStream) -> bool;
    fn dsr_msgs2__msg__ServolStream__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<ServolStream>, size: usize) -> bool;
    fn dsr_msgs2__msg__ServolStream__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<ServolStream>);
    fn dsr_msgs2__msg__ServolStream__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<ServolStream>, out_seq: *mut rosidl_runtime_rs::Sequence<ServolStream>) -> bool;
}

// Corresponds to dsr_msgs2__msg__ServolStream
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]

/// ____________________________________________________________________________________________
///  servol
///
/// ____________________________________________________________________________________________

#[repr(C)]
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
    unsafe {
      let mut msg = std::mem::zeroed();
      if !dsr_msgs2__msg__ServolStream__init(&mut msg as *mut _) {
        panic!("Call to dsr_msgs2__msg__ServolStream__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for ServolStream {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dsr_msgs2__msg__ServolStream__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dsr_msgs2__msg__ServolStream__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dsr_msgs2__msg__ServolStream__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for ServolStream {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for ServolStream where Self: Sized {
  const TYPE_NAME: &'static str = "dsr_msgs2/msg/ServolStream";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__dsr_msgs2__msg__ServolStream() }
  }
}


#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__dsr_msgs2__msg__SpeedjStream() -> *const std::ffi::c_void;
}

#[link(name = "dsr_msgs2__rosidl_generator_c")]
extern "C" {
    fn dsr_msgs2__msg__SpeedjStream__init(msg: *mut SpeedjStream) -> bool;
    fn dsr_msgs2__msg__SpeedjStream__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<SpeedjStream>, size: usize) -> bool;
    fn dsr_msgs2__msg__SpeedjStream__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<SpeedjStream>);
    fn dsr_msgs2__msg__SpeedjStream__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<SpeedjStream>, out_seq: *mut rosidl_runtime_rs::Sequence<SpeedjStream>) -> bool;
}

// Corresponds to dsr_msgs2__msg__SpeedjStream
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]

/// ____________________________________________________________________________________________
///  speedj
///
/// ____________________________________________________________________________________________

#[repr(C)]
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
    unsafe {
      let mut msg = std::mem::zeroed();
      if !dsr_msgs2__msg__SpeedjStream__init(&mut msg as *mut _) {
        panic!("Call to dsr_msgs2__msg__SpeedjStream__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for SpeedjStream {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dsr_msgs2__msg__SpeedjStream__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dsr_msgs2__msg__SpeedjStream__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dsr_msgs2__msg__SpeedjStream__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for SpeedjStream {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for SpeedjStream where Self: Sized {
  const TYPE_NAME: &'static str = "dsr_msgs2/msg/SpeedjStream";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__dsr_msgs2__msg__SpeedjStream() }
  }
}


#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__dsr_msgs2__msg__SpeedlStream() -> *const std::ffi::c_void;
}

#[link(name = "dsr_msgs2__rosidl_generator_c")]
extern "C" {
    fn dsr_msgs2__msg__SpeedlStream__init(msg: *mut SpeedlStream) -> bool;
    fn dsr_msgs2__msg__SpeedlStream__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<SpeedlStream>, size: usize) -> bool;
    fn dsr_msgs2__msg__SpeedlStream__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<SpeedlStream>);
    fn dsr_msgs2__msg__SpeedlStream__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<SpeedlStream>, out_seq: *mut rosidl_runtime_rs::Sequence<SpeedlStream>) -> bool;
}

// Corresponds to dsr_msgs2__msg__SpeedlStream
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]

/// ____________________________________________________________________________________________
///  speedl
///
/// ____________________________________________________________________________________________

#[repr(C)]
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
    unsafe {
      let mut msg = std::mem::zeroed();
      if !dsr_msgs2__msg__SpeedlStream__init(&mut msg as *mut _) {
        panic!("Call to dsr_msgs2__msg__SpeedlStream__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for SpeedlStream {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dsr_msgs2__msg__SpeedlStream__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dsr_msgs2__msg__SpeedlStream__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dsr_msgs2__msg__SpeedlStream__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for SpeedlStream {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for SpeedlStream where Self: Sized {
  const TYPE_NAME: &'static str = "dsr_msgs2/msg/SpeedlStream";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__dsr_msgs2__msg__SpeedlStream() }
  }
}


#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__dsr_msgs2__msg__RobotDisconnection() -> *const std::ffi::c_void;
}

#[link(name = "dsr_msgs2__rosidl_generator_c")]
extern "C" {
    fn dsr_msgs2__msg__RobotDisconnection__init(msg: *mut RobotDisconnection) -> bool;
    fn dsr_msgs2__msg__RobotDisconnection__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<RobotDisconnection>, size: usize) -> bool;
    fn dsr_msgs2__msg__RobotDisconnection__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<RobotDisconnection>);
    fn dsr_msgs2__msg__RobotDisconnection__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<RobotDisconnection>, out_seq: *mut rosidl_runtime_rs::Sequence<RobotDisconnection>) -> bool;
}

// Corresponds to dsr_msgs2__msg__RobotDisconnection
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]

/// Event driven when the robot connection losts.

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct RobotDisconnection {

    // This member is not documented.
    #[allow(missing_docs)]
    pub structure_needs_at_least_one_member: u8,

}



impl Default for RobotDisconnection {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !dsr_msgs2__msg__RobotDisconnection__init(&mut msg as *mut _) {
        panic!("Call to dsr_msgs2__msg__RobotDisconnection__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for RobotDisconnection {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dsr_msgs2__msg__RobotDisconnection__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dsr_msgs2__msg__RobotDisconnection__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dsr_msgs2__msg__RobotDisconnection__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for RobotDisconnection {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for RobotDisconnection where Self: Sized {
  const TYPE_NAME: &'static str = "dsr_msgs2/msg/RobotDisconnection";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__dsr_msgs2__msg__RobotDisconnection() }
  }
}


#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__dsr_msgs2__msg__RobotStateRt() -> *const std::ffi::c_void;
}

#[link(name = "dsr_msgs2__rosidl_generator_c")]
extern "C" {
    fn dsr_msgs2__msg__RobotStateRt__init(msg: *mut RobotStateRt) -> bool;
    fn dsr_msgs2__msg__RobotStateRt__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<RobotStateRt>, size: usize) -> bool;
    fn dsr_msgs2__msg__RobotStateRt__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<RobotStateRt>);
    fn dsr_msgs2__msg__RobotStateRt__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<RobotStateRt>, out_seq: *mut rosidl_runtime_rs::Sequence<RobotStateRt>) -> bool;
}

// Corresponds to dsr_msgs2__msg__RobotStateRt
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]

/// timestamp at the data of data acquisition

#[repr(C)]
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
    pub jacobian_matrix: rosidl_runtime_rs::Sequence<std_msgs::msg::rmw::Float64MultiArray>,

    /// gravity torque=g(q)
    pub gravity_torque: [f64; 6],

    /// coriolis matrix=C(q,q_dot)  [6][6]
    pub coriolis_matrix: rosidl_runtime_rs::Sequence<std_msgs::msg::rmw::Float64MultiArray>,

    /// mass matrix=M(q) [6][6]
    pub mass_matrix: rosidl_runtime_rs::Sequence<std_msgs::msg::rmw::Float64MultiArray>,

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
    unsafe {
      let mut msg = std::mem::zeroed();
      if !dsr_msgs2__msg__RobotStateRt__init(&mut msg as *mut _) {
        panic!("Call to dsr_msgs2__msg__RobotStateRt__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for RobotStateRt {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dsr_msgs2__msg__RobotStateRt__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dsr_msgs2__msg__RobotStateRt__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dsr_msgs2__msg__RobotStateRt__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for RobotStateRt {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for RobotStateRt where Self: Sized {
  const TYPE_NAME: &'static str = "dsr_msgs2/msg/RobotStateRt";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__dsr_msgs2__msg__RobotStateRt() }
  }
}


#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__dsr_msgs2__msg__ServojRtStream() -> *const std::ffi::c_void;
}

#[link(name = "dsr_msgs2__rosidl_generator_c")]
extern "C" {
    fn dsr_msgs2__msg__ServojRtStream__init(msg: *mut ServojRtStream) -> bool;
    fn dsr_msgs2__msg__ServojRtStream__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<ServojRtStream>, size: usize) -> bool;
    fn dsr_msgs2__msg__ServojRtStream__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<ServojRtStream>);
    fn dsr_msgs2__msg__ServojRtStream__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<ServojRtStream>, out_seq: *mut rosidl_runtime_rs::Sequence<ServojRtStream>) -> bool;
}

// Corresponds to dsr_msgs2__msg__ServojRtStream
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]

/// ____________________________________________________________________________________________
///  servoj_rt
///
/// ____________________________________________________________________________________________

#[repr(C)]
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
    unsafe {
      let mut msg = std::mem::zeroed();
      if !dsr_msgs2__msg__ServojRtStream__init(&mut msg as *mut _) {
        panic!("Call to dsr_msgs2__msg__ServojRtStream__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for ServojRtStream {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dsr_msgs2__msg__ServojRtStream__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dsr_msgs2__msg__ServojRtStream__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dsr_msgs2__msg__ServojRtStream__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for ServojRtStream {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for ServojRtStream where Self: Sized {
  const TYPE_NAME: &'static str = "dsr_msgs2/msg/ServojRtStream";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__dsr_msgs2__msg__ServojRtStream() }
  }
}


#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__dsr_msgs2__msg__ServolRtStream() -> *const std::ffi::c_void;
}

#[link(name = "dsr_msgs2__rosidl_generator_c")]
extern "C" {
    fn dsr_msgs2__msg__ServolRtStream__init(msg: *mut ServolRtStream) -> bool;
    fn dsr_msgs2__msg__ServolRtStream__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<ServolRtStream>, size: usize) -> bool;
    fn dsr_msgs2__msg__ServolRtStream__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<ServolRtStream>);
    fn dsr_msgs2__msg__ServolRtStream__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<ServolRtStream>, out_seq: *mut rosidl_runtime_rs::Sequence<ServolRtStream>) -> bool;
}

// Corresponds to dsr_msgs2__msg__ServolRtStream
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]

/// ____________________________________________________________________________________________
///  servol_rt
///
/// ____________________________________________________________________________________________

#[repr(C)]
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
    unsafe {
      let mut msg = std::mem::zeroed();
      if !dsr_msgs2__msg__ServolRtStream__init(&mut msg as *mut _) {
        panic!("Call to dsr_msgs2__msg__ServolRtStream__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for ServolRtStream {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dsr_msgs2__msg__ServolRtStream__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dsr_msgs2__msg__ServolRtStream__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dsr_msgs2__msg__ServolRtStream__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for ServolRtStream {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for ServolRtStream where Self: Sized {
  const TYPE_NAME: &'static str = "dsr_msgs2/msg/ServolRtStream";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__dsr_msgs2__msg__ServolRtStream() }
  }
}


#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__dsr_msgs2__msg__SpeedjRtStream() -> *const std::ffi::c_void;
}

#[link(name = "dsr_msgs2__rosidl_generator_c")]
extern "C" {
    fn dsr_msgs2__msg__SpeedjRtStream__init(msg: *mut SpeedjRtStream) -> bool;
    fn dsr_msgs2__msg__SpeedjRtStream__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<SpeedjRtStream>, size: usize) -> bool;
    fn dsr_msgs2__msg__SpeedjRtStream__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<SpeedjRtStream>);
    fn dsr_msgs2__msg__SpeedjRtStream__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<SpeedjRtStream>, out_seq: *mut rosidl_runtime_rs::Sequence<SpeedjRtStream>) -> bool;
}

// Corresponds to dsr_msgs2__msg__SpeedjRtStream
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]

/// ____________________________________________________________________________________________
///  speedj_rt
///
/// ____________________________________________________________________________________________

#[repr(C)]
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
    unsafe {
      let mut msg = std::mem::zeroed();
      if !dsr_msgs2__msg__SpeedjRtStream__init(&mut msg as *mut _) {
        panic!("Call to dsr_msgs2__msg__SpeedjRtStream__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for SpeedjRtStream {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dsr_msgs2__msg__SpeedjRtStream__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dsr_msgs2__msg__SpeedjRtStream__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dsr_msgs2__msg__SpeedjRtStream__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for SpeedjRtStream {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for SpeedjRtStream where Self: Sized {
  const TYPE_NAME: &'static str = "dsr_msgs2/msg/SpeedjRtStream";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__dsr_msgs2__msg__SpeedjRtStream() }
  }
}


#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__dsr_msgs2__msg__SpeedlRtStream() -> *const std::ffi::c_void;
}

#[link(name = "dsr_msgs2__rosidl_generator_c")]
extern "C" {
    fn dsr_msgs2__msg__SpeedlRtStream__init(msg: *mut SpeedlRtStream) -> bool;
    fn dsr_msgs2__msg__SpeedlRtStream__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<SpeedlRtStream>, size: usize) -> bool;
    fn dsr_msgs2__msg__SpeedlRtStream__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<SpeedlRtStream>);
    fn dsr_msgs2__msg__SpeedlRtStream__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<SpeedlRtStream>, out_seq: *mut rosidl_runtime_rs::Sequence<SpeedlRtStream>) -> bool;
}

// Corresponds to dsr_msgs2__msg__SpeedlRtStream
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]

/// ____________________________________________________________________________________________
///  speedl_rt
///
/// ____________________________________________________________________________________________

#[repr(C)]
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
    unsafe {
      let mut msg = std::mem::zeroed();
      if !dsr_msgs2__msg__SpeedlRtStream__init(&mut msg as *mut _) {
        panic!("Call to dsr_msgs2__msg__SpeedlRtStream__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for SpeedlRtStream {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dsr_msgs2__msg__SpeedlRtStream__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dsr_msgs2__msg__SpeedlRtStream__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dsr_msgs2__msg__SpeedlRtStream__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for SpeedlRtStream {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for SpeedlRtStream where Self: Sized {
  const TYPE_NAME: &'static str = "dsr_msgs2/msg/SpeedlRtStream";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__dsr_msgs2__msg__SpeedlRtStream() }
  }
}


#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__dsr_msgs2__msg__TorqueRtStream() -> *const std::ffi::c_void;
}

#[link(name = "dsr_msgs2__rosidl_generator_c")]
extern "C" {
    fn dsr_msgs2__msg__TorqueRtStream__init(msg: *mut TorqueRtStream) -> bool;
    fn dsr_msgs2__msg__TorqueRtStream__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<TorqueRtStream>, size: usize) -> bool;
    fn dsr_msgs2__msg__TorqueRtStream__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<TorqueRtStream>);
    fn dsr_msgs2__msg__TorqueRtStream__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<TorqueRtStream>, out_seq: *mut rosidl_runtime_rs::Sequence<TorqueRtStream>) -> bool;
}

// Corresponds to dsr_msgs2__msg__TorqueRtStream
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]

/// ____________________________________________________________________________________________
///  torque_rt
///
/// ____________________________________________________________________________________________

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct TorqueRtStream {
    /// motor torque
    pub tor: [f64; 6],

    /// time
    pub time: f64,

}



impl Default for TorqueRtStream {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !dsr_msgs2__msg__TorqueRtStream__init(&mut msg as *mut _) {
        panic!("Call to dsr_msgs2__msg__TorqueRtStream__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for TorqueRtStream {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dsr_msgs2__msg__TorqueRtStream__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dsr_msgs2__msg__TorqueRtStream__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dsr_msgs2__msg__TorqueRtStream__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for TorqueRtStream {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for TorqueRtStream where Self: Sized {
  const TYPE_NAME: &'static str = "dsr_msgs2/msg/TorqueRtStream";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__dsr_msgs2__msg__TorqueRtStream() }
  }
}


