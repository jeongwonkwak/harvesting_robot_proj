#[cfg(feature = "serde")]
use serde::{Deserialize, Serialize};


#[link(name = "my_robot_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__my_robot_interfaces__msg__TurtleStatus() -> *const std::ffi::c_void;
}

#[link(name = "my_robot_interfaces__rosidl_generator_c")]
extern "C" {
    fn my_robot_interfaces__msg__TurtleStatus__init(msg: *mut TurtleStatus) -> bool;
    fn my_robot_interfaces__msg__TurtleStatus__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<TurtleStatus>, size: usize) -> bool;
    fn my_robot_interfaces__msg__TurtleStatus__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<TurtleStatus>);
    fn my_robot_interfaces__msg__TurtleStatus__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<TurtleStatus>, out_seq: *mut rosidl_runtime_rs::Sequence<TurtleStatus>) -> bool;
}

// Corresponds to my_robot_interfaces__msg__TurtleStatus
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct TurtleStatus {
    /// 벽까지의 남은 거리
    pub distance_to_wall: f64,

    /// 로봇의 상태 (예: NORMAL, WARN, STOP)
    pub current_state: rosidl_runtime_rs::String,

    /// 이동 중 여부
    pub is_moving: bool,

}



impl Default for TurtleStatus {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !my_robot_interfaces__msg__TurtleStatus__init(&mut msg as *mut _) {
        panic!("Call to my_robot_interfaces__msg__TurtleStatus__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for TurtleStatus {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { my_robot_interfaces__msg__TurtleStatus__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { my_robot_interfaces__msg__TurtleStatus__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { my_robot_interfaces__msg__TurtleStatus__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for TurtleStatus {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for TurtleStatus where Self: Sized {
  const TYPE_NAME: &'static str = "my_robot_interfaces/msg/TurtleStatus";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__my_robot_interfaces__msg__TurtleStatus() }
  }
}


