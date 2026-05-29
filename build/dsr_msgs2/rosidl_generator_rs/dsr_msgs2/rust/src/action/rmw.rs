
#[cfg(feature = "serde")]
use serde::{Deserialize, Serialize};


#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__dsr_msgs2__action__JogH2r_Goal() -> *const std::ffi::c_void;
}

#[link(name = "dsr_msgs2__rosidl_generator_c")]
extern "C" {
    fn dsr_msgs2__action__JogH2r_Goal__init(msg: *mut JogH2r_Goal) -> bool;
    fn dsr_msgs2__action__JogH2r_Goal__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<JogH2r_Goal>, size: usize) -> bool;
    fn dsr_msgs2__action__JogH2r_Goal__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<JogH2r_Goal>);
    fn dsr_msgs2__action__JogH2r_Goal__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<JogH2r_Goal>, out_seq: *mut rosidl_runtime_rs::Sequence<JogH2r_Goal>) -> bool;
}

// Corresponds to dsr_msgs2__action__JogH2r_Goal
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct JogH2r_Goal {

    // This member is not documented.
    #[allow(missing_docs)]
    pub jog_axis: i8,


    // This member is not documented.
    #[allow(missing_docs)]
    pub move_reference: i8,


    // This member is not documented.
    #[allow(missing_docs)]
    pub velocity: f64,

}



impl Default for JogH2r_Goal {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !dsr_msgs2__action__JogH2r_Goal__init(&mut msg as *mut _) {
        panic!("Call to dsr_msgs2__action__JogH2r_Goal__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for JogH2r_Goal {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dsr_msgs2__action__JogH2r_Goal__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dsr_msgs2__action__JogH2r_Goal__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dsr_msgs2__action__JogH2r_Goal__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for JogH2r_Goal {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for JogH2r_Goal where Self: Sized {
  const TYPE_NAME: &'static str = "dsr_msgs2/action/JogH2r_Goal";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__dsr_msgs2__action__JogH2r_Goal() }
  }
}


#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__dsr_msgs2__action__JogH2r_Result() -> *const std::ffi::c_void;
}

#[link(name = "dsr_msgs2__rosidl_generator_c")]
extern "C" {
    fn dsr_msgs2__action__JogH2r_Result__init(msg: *mut JogH2r_Result) -> bool;
    fn dsr_msgs2__action__JogH2r_Result__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<JogH2r_Result>, size: usize) -> bool;
    fn dsr_msgs2__action__JogH2r_Result__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<JogH2r_Result>);
    fn dsr_msgs2__action__JogH2r_Result__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<JogH2r_Result>, out_seq: *mut rosidl_runtime_rs::Sequence<JogH2r_Result>) -> bool;
}

// Corresponds to dsr_msgs2__action__JogH2r_Result
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct JogH2r_Result {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,

}



impl Default for JogH2r_Result {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !dsr_msgs2__action__JogH2r_Result__init(&mut msg as *mut _) {
        panic!("Call to dsr_msgs2__action__JogH2r_Result__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for JogH2r_Result {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dsr_msgs2__action__JogH2r_Result__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dsr_msgs2__action__JogH2r_Result__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dsr_msgs2__action__JogH2r_Result__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for JogH2r_Result {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for JogH2r_Result where Self: Sized {
  const TYPE_NAME: &'static str = "dsr_msgs2/action/JogH2r_Result";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__dsr_msgs2__action__JogH2r_Result() }
  }
}


#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__dsr_msgs2__action__JogH2r_Feedback() -> *const std::ffi::c_void;
}

#[link(name = "dsr_msgs2__rosidl_generator_c")]
extern "C" {
    fn dsr_msgs2__action__JogH2r_Feedback__init(msg: *mut JogH2r_Feedback) -> bool;
    fn dsr_msgs2__action__JogH2r_Feedback__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<JogH2r_Feedback>, size: usize) -> bool;
    fn dsr_msgs2__action__JogH2r_Feedback__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<JogH2r_Feedback>);
    fn dsr_msgs2__action__JogH2r_Feedback__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<JogH2r_Feedback>, out_seq: *mut rosidl_runtime_rs::Sequence<JogH2r_Feedback>) -> bool;
}

// Corresponds to dsr_msgs2__action__JogH2r_Feedback
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct JogH2r_Feedback {

    // This member is not documented.
    #[allow(missing_docs)]
    pub pos: [f64; 6],

}



impl Default for JogH2r_Feedback {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !dsr_msgs2__action__JogH2r_Feedback__init(&mut msg as *mut _) {
        panic!("Call to dsr_msgs2__action__JogH2r_Feedback__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for JogH2r_Feedback {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dsr_msgs2__action__JogH2r_Feedback__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dsr_msgs2__action__JogH2r_Feedback__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dsr_msgs2__action__JogH2r_Feedback__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for JogH2r_Feedback {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for JogH2r_Feedback where Self: Sized {
  const TYPE_NAME: &'static str = "dsr_msgs2/action/JogH2r_Feedback";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__dsr_msgs2__action__JogH2r_Feedback() }
  }
}


#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__dsr_msgs2__action__JogH2r_FeedbackMessage() -> *const std::ffi::c_void;
}

#[link(name = "dsr_msgs2__rosidl_generator_c")]
extern "C" {
    fn dsr_msgs2__action__JogH2r_FeedbackMessage__init(msg: *mut JogH2r_FeedbackMessage) -> bool;
    fn dsr_msgs2__action__JogH2r_FeedbackMessage__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<JogH2r_FeedbackMessage>, size: usize) -> bool;
    fn dsr_msgs2__action__JogH2r_FeedbackMessage__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<JogH2r_FeedbackMessage>);
    fn dsr_msgs2__action__JogH2r_FeedbackMessage__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<JogH2r_FeedbackMessage>, out_seq: *mut rosidl_runtime_rs::Sequence<JogH2r_FeedbackMessage>) -> bool;
}

// Corresponds to dsr_msgs2__action__JogH2r_FeedbackMessage
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct JogH2r_FeedbackMessage {

    // This member is not documented.
    #[allow(missing_docs)]
    pub goal_id: unique_identifier_msgs::msg::rmw::UUID,


    // This member is not documented.
    #[allow(missing_docs)]
    pub feedback: super::super::action::rmw::JogH2r_Feedback,

}



impl Default for JogH2r_FeedbackMessage {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !dsr_msgs2__action__JogH2r_FeedbackMessage__init(&mut msg as *mut _) {
        panic!("Call to dsr_msgs2__action__JogH2r_FeedbackMessage__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for JogH2r_FeedbackMessage {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dsr_msgs2__action__JogH2r_FeedbackMessage__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dsr_msgs2__action__JogH2r_FeedbackMessage__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dsr_msgs2__action__JogH2r_FeedbackMessage__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for JogH2r_FeedbackMessage {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for JogH2r_FeedbackMessage where Self: Sized {
  const TYPE_NAME: &'static str = "dsr_msgs2/action/JogH2r_FeedbackMessage";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__dsr_msgs2__action__JogH2r_FeedbackMessage() }
  }
}


#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__dsr_msgs2__action__MovejH2r_Goal() -> *const std::ffi::c_void;
}

#[link(name = "dsr_msgs2__rosidl_generator_c")]
extern "C" {
    fn dsr_msgs2__action__MovejH2r_Goal__init(msg: *mut MovejH2r_Goal) -> bool;
    fn dsr_msgs2__action__MovejH2r_Goal__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<MovejH2r_Goal>, size: usize) -> bool;
    fn dsr_msgs2__action__MovejH2r_Goal__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<MovejH2r_Goal>);
    fn dsr_msgs2__action__MovejH2r_Goal__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<MovejH2r_Goal>, out_seq: *mut rosidl_runtime_rs::Sequence<MovejH2r_Goal>) -> bool;
}

// Corresponds to dsr_msgs2__action__MovejH2r_Goal
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct MovejH2r_Goal {

    // This member is not documented.
    #[allow(missing_docs)]
    pub target_pos: [f64; 6],


    // This member is not documented.
    #[allow(missing_docs)]
    pub target_vel: [f64; 6],


    // This member is not documented.
    #[allow(missing_docs)]
    pub target_acc: [f64; 6],

}



impl Default for MovejH2r_Goal {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !dsr_msgs2__action__MovejH2r_Goal__init(&mut msg as *mut _) {
        panic!("Call to dsr_msgs2__action__MovejH2r_Goal__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for MovejH2r_Goal {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dsr_msgs2__action__MovejH2r_Goal__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dsr_msgs2__action__MovejH2r_Goal__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dsr_msgs2__action__MovejH2r_Goal__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for MovejH2r_Goal {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for MovejH2r_Goal where Self: Sized {
  const TYPE_NAME: &'static str = "dsr_msgs2/action/MovejH2r_Goal";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__dsr_msgs2__action__MovejH2r_Goal() }
  }
}


#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__dsr_msgs2__action__MovejH2r_Result() -> *const std::ffi::c_void;
}

#[link(name = "dsr_msgs2__rosidl_generator_c")]
extern "C" {
    fn dsr_msgs2__action__MovejH2r_Result__init(msg: *mut MovejH2r_Result) -> bool;
    fn dsr_msgs2__action__MovejH2r_Result__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<MovejH2r_Result>, size: usize) -> bool;
    fn dsr_msgs2__action__MovejH2r_Result__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<MovejH2r_Result>);
    fn dsr_msgs2__action__MovejH2r_Result__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<MovejH2r_Result>, out_seq: *mut rosidl_runtime_rs::Sequence<MovejH2r_Result>) -> bool;
}

// Corresponds to dsr_msgs2__action__MovejH2r_Result
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct MovejH2r_Result {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,

}



impl Default for MovejH2r_Result {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !dsr_msgs2__action__MovejH2r_Result__init(&mut msg as *mut _) {
        panic!("Call to dsr_msgs2__action__MovejH2r_Result__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for MovejH2r_Result {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dsr_msgs2__action__MovejH2r_Result__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dsr_msgs2__action__MovejH2r_Result__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dsr_msgs2__action__MovejH2r_Result__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for MovejH2r_Result {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for MovejH2r_Result where Self: Sized {
  const TYPE_NAME: &'static str = "dsr_msgs2/action/MovejH2r_Result";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__dsr_msgs2__action__MovejH2r_Result() }
  }
}


#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__dsr_msgs2__action__MovejH2r_Feedback() -> *const std::ffi::c_void;
}

#[link(name = "dsr_msgs2__rosidl_generator_c")]
extern "C" {
    fn dsr_msgs2__action__MovejH2r_Feedback__init(msg: *mut MovejH2r_Feedback) -> bool;
    fn dsr_msgs2__action__MovejH2r_Feedback__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<MovejH2r_Feedback>, size: usize) -> bool;
    fn dsr_msgs2__action__MovejH2r_Feedback__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<MovejH2r_Feedback>);
    fn dsr_msgs2__action__MovejH2r_Feedback__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<MovejH2r_Feedback>, out_seq: *mut rosidl_runtime_rs::Sequence<MovejH2r_Feedback>) -> bool;
}

// Corresponds to dsr_msgs2__action__MovejH2r_Feedback
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct MovejH2r_Feedback {

    // This member is not documented.
    #[allow(missing_docs)]
    pub pos: [f64; 6],

}



impl Default for MovejH2r_Feedback {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !dsr_msgs2__action__MovejH2r_Feedback__init(&mut msg as *mut _) {
        panic!("Call to dsr_msgs2__action__MovejH2r_Feedback__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for MovejH2r_Feedback {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dsr_msgs2__action__MovejH2r_Feedback__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dsr_msgs2__action__MovejH2r_Feedback__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dsr_msgs2__action__MovejH2r_Feedback__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for MovejH2r_Feedback {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for MovejH2r_Feedback where Self: Sized {
  const TYPE_NAME: &'static str = "dsr_msgs2/action/MovejH2r_Feedback";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__dsr_msgs2__action__MovejH2r_Feedback() }
  }
}


#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__dsr_msgs2__action__MovejH2r_FeedbackMessage() -> *const std::ffi::c_void;
}

#[link(name = "dsr_msgs2__rosidl_generator_c")]
extern "C" {
    fn dsr_msgs2__action__MovejH2r_FeedbackMessage__init(msg: *mut MovejH2r_FeedbackMessage) -> bool;
    fn dsr_msgs2__action__MovejH2r_FeedbackMessage__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<MovejH2r_FeedbackMessage>, size: usize) -> bool;
    fn dsr_msgs2__action__MovejH2r_FeedbackMessage__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<MovejH2r_FeedbackMessage>);
    fn dsr_msgs2__action__MovejH2r_FeedbackMessage__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<MovejH2r_FeedbackMessage>, out_seq: *mut rosidl_runtime_rs::Sequence<MovejH2r_FeedbackMessage>) -> bool;
}

// Corresponds to dsr_msgs2__action__MovejH2r_FeedbackMessage
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct MovejH2r_FeedbackMessage {

    // This member is not documented.
    #[allow(missing_docs)]
    pub goal_id: unique_identifier_msgs::msg::rmw::UUID,


    // This member is not documented.
    #[allow(missing_docs)]
    pub feedback: super::super::action::rmw::MovejH2r_Feedback,

}



impl Default for MovejH2r_FeedbackMessage {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !dsr_msgs2__action__MovejH2r_FeedbackMessage__init(&mut msg as *mut _) {
        panic!("Call to dsr_msgs2__action__MovejH2r_FeedbackMessage__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for MovejH2r_FeedbackMessage {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dsr_msgs2__action__MovejH2r_FeedbackMessage__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dsr_msgs2__action__MovejH2r_FeedbackMessage__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dsr_msgs2__action__MovejH2r_FeedbackMessage__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for MovejH2r_FeedbackMessage {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for MovejH2r_FeedbackMessage where Self: Sized {
  const TYPE_NAME: &'static str = "dsr_msgs2/action/MovejH2r_FeedbackMessage";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__dsr_msgs2__action__MovejH2r_FeedbackMessage() }
  }
}


#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__dsr_msgs2__action__MovelH2r_Goal() -> *const std::ffi::c_void;
}

#[link(name = "dsr_msgs2__rosidl_generator_c")]
extern "C" {
    fn dsr_msgs2__action__MovelH2r_Goal__init(msg: *mut MovelH2r_Goal) -> bool;
    fn dsr_msgs2__action__MovelH2r_Goal__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<MovelH2r_Goal>, size: usize) -> bool;
    fn dsr_msgs2__action__MovelH2r_Goal__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<MovelH2r_Goal>);
    fn dsr_msgs2__action__MovelH2r_Goal__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<MovelH2r_Goal>, out_seq: *mut rosidl_runtime_rs::Sequence<MovelH2r_Goal>) -> bool;
}

// Corresponds to dsr_msgs2__action__MovelH2r_Goal
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct MovelH2r_Goal {

    // This member is not documented.
    #[allow(missing_docs)]
    pub target_pos: [f64; 6],


    // This member is not documented.
    #[allow(missing_docs)]
    pub target_vel: [f64; 2],


    // This member is not documented.
    #[allow(missing_docs)]
    pub target_acc: [f64; 2],

}



impl Default for MovelH2r_Goal {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !dsr_msgs2__action__MovelH2r_Goal__init(&mut msg as *mut _) {
        panic!("Call to dsr_msgs2__action__MovelH2r_Goal__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for MovelH2r_Goal {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dsr_msgs2__action__MovelH2r_Goal__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dsr_msgs2__action__MovelH2r_Goal__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dsr_msgs2__action__MovelH2r_Goal__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for MovelH2r_Goal {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for MovelH2r_Goal where Self: Sized {
  const TYPE_NAME: &'static str = "dsr_msgs2/action/MovelH2r_Goal";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__dsr_msgs2__action__MovelH2r_Goal() }
  }
}


#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__dsr_msgs2__action__MovelH2r_Result() -> *const std::ffi::c_void;
}

#[link(name = "dsr_msgs2__rosidl_generator_c")]
extern "C" {
    fn dsr_msgs2__action__MovelH2r_Result__init(msg: *mut MovelH2r_Result) -> bool;
    fn dsr_msgs2__action__MovelH2r_Result__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<MovelH2r_Result>, size: usize) -> bool;
    fn dsr_msgs2__action__MovelH2r_Result__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<MovelH2r_Result>);
    fn dsr_msgs2__action__MovelH2r_Result__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<MovelH2r_Result>, out_seq: *mut rosidl_runtime_rs::Sequence<MovelH2r_Result>) -> bool;
}

// Corresponds to dsr_msgs2__action__MovelH2r_Result
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct MovelH2r_Result {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,

}



impl Default for MovelH2r_Result {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !dsr_msgs2__action__MovelH2r_Result__init(&mut msg as *mut _) {
        panic!("Call to dsr_msgs2__action__MovelH2r_Result__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for MovelH2r_Result {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dsr_msgs2__action__MovelH2r_Result__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dsr_msgs2__action__MovelH2r_Result__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dsr_msgs2__action__MovelH2r_Result__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for MovelH2r_Result {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for MovelH2r_Result where Self: Sized {
  const TYPE_NAME: &'static str = "dsr_msgs2/action/MovelH2r_Result";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__dsr_msgs2__action__MovelH2r_Result() }
  }
}


#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__dsr_msgs2__action__MovelH2r_Feedback() -> *const std::ffi::c_void;
}

#[link(name = "dsr_msgs2__rosidl_generator_c")]
extern "C" {
    fn dsr_msgs2__action__MovelH2r_Feedback__init(msg: *mut MovelH2r_Feedback) -> bool;
    fn dsr_msgs2__action__MovelH2r_Feedback__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<MovelH2r_Feedback>, size: usize) -> bool;
    fn dsr_msgs2__action__MovelH2r_Feedback__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<MovelH2r_Feedback>);
    fn dsr_msgs2__action__MovelH2r_Feedback__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<MovelH2r_Feedback>, out_seq: *mut rosidl_runtime_rs::Sequence<MovelH2r_Feedback>) -> bool;
}

// Corresponds to dsr_msgs2__action__MovelH2r_Feedback
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct MovelH2r_Feedback {

    // This member is not documented.
    #[allow(missing_docs)]
    pub pos: [f64; 6],

}



impl Default for MovelH2r_Feedback {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !dsr_msgs2__action__MovelH2r_Feedback__init(&mut msg as *mut _) {
        panic!("Call to dsr_msgs2__action__MovelH2r_Feedback__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for MovelH2r_Feedback {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dsr_msgs2__action__MovelH2r_Feedback__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dsr_msgs2__action__MovelH2r_Feedback__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dsr_msgs2__action__MovelH2r_Feedback__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for MovelH2r_Feedback {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for MovelH2r_Feedback where Self: Sized {
  const TYPE_NAME: &'static str = "dsr_msgs2/action/MovelH2r_Feedback";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__dsr_msgs2__action__MovelH2r_Feedback() }
  }
}


#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__dsr_msgs2__action__MovelH2r_FeedbackMessage() -> *const std::ffi::c_void;
}

#[link(name = "dsr_msgs2__rosidl_generator_c")]
extern "C" {
    fn dsr_msgs2__action__MovelH2r_FeedbackMessage__init(msg: *mut MovelH2r_FeedbackMessage) -> bool;
    fn dsr_msgs2__action__MovelH2r_FeedbackMessage__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<MovelH2r_FeedbackMessage>, size: usize) -> bool;
    fn dsr_msgs2__action__MovelH2r_FeedbackMessage__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<MovelH2r_FeedbackMessage>);
    fn dsr_msgs2__action__MovelH2r_FeedbackMessage__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<MovelH2r_FeedbackMessage>, out_seq: *mut rosidl_runtime_rs::Sequence<MovelH2r_FeedbackMessage>) -> bool;
}

// Corresponds to dsr_msgs2__action__MovelH2r_FeedbackMessage
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct MovelH2r_FeedbackMessage {

    // This member is not documented.
    #[allow(missing_docs)]
    pub goal_id: unique_identifier_msgs::msg::rmw::UUID,


    // This member is not documented.
    #[allow(missing_docs)]
    pub feedback: super::super::action::rmw::MovelH2r_Feedback,

}



impl Default for MovelH2r_FeedbackMessage {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !dsr_msgs2__action__MovelH2r_FeedbackMessage__init(&mut msg as *mut _) {
        panic!("Call to dsr_msgs2__action__MovelH2r_FeedbackMessage__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for MovelH2r_FeedbackMessage {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dsr_msgs2__action__MovelH2r_FeedbackMessage__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dsr_msgs2__action__MovelH2r_FeedbackMessage__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dsr_msgs2__action__MovelH2r_FeedbackMessage__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for MovelH2r_FeedbackMessage {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for MovelH2r_FeedbackMessage where Self: Sized {
  const TYPE_NAME: &'static str = "dsr_msgs2/action/MovelH2r_FeedbackMessage";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__dsr_msgs2__action__MovelH2r_FeedbackMessage() }
  }
}




#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__dsr_msgs2__action__JogH2r_SendGoal_Request() -> *const std::ffi::c_void;
}

#[link(name = "dsr_msgs2__rosidl_generator_c")]
extern "C" {
    fn dsr_msgs2__action__JogH2r_SendGoal_Request__init(msg: *mut JogH2r_SendGoal_Request) -> bool;
    fn dsr_msgs2__action__JogH2r_SendGoal_Request__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<JogH2r_SendGoal_Request>, size: usize) -> bool;
    fn dsr_msgs2__action__JogH2r_SendGoal_Request__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<JogH2r_SendGoal_Request>);
    fn dsr_msgs2__action__JogH2r_SendGoal_Request__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<JogH2r_SendGoal_Request>, out_seq: *mut rosidl_runtime_rs::Sequence<JogH2r_SendGoal_Request>) -> bool;
}

// Corresponds to dsr_msgs2__action__JogH2r_SendGoal_Request
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct JogH2r_SendGoal_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub goal_id: unique_identifier_msgs::msg::rmw::UUID,


    // This member is not documented.
    #[allow(missing_docs)]
    pub goal: super::super::action::rmw::JogH2r_Goal,

}



impl Default for JogH2r_SendGoal_Request {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !dsr_msgs2__action__JogH2r_SendGoal_Request__init(&mut msg as *mut _) {
        panic!("Call to dsr_msgs2__action__JogH2r_SendGoal_Request__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for JogH2r_SendGoal_Request {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dsr_msgs2__action__JogH2r_SendGoal_Request__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dsr_msgs2__action__JogH2r_SendGoal_Request__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dsr_msgs2__action__JogH2r_SendGoal_Request__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for JogH2r_SendGoal_Request {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for JogH2r_SendGoal_Request where Self: Sized {
  const TYPE_NAME: &'static str = "dsr_msgs2/action/JogH2r_SendGoal_Request";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__dsr_msgs2__action__JogH2r_SendGoal_Request() }
  }
}


#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__dsr_msgs2__action__JogH2r_SendGoal_Response() -> *const std::ffi::c_void;
}

#[link(name = "dsr_msgs2__rosidl_generator_c")]
extern "C" {
    fn dsr_msgs2__action__JogH2r_SendGoal_Response__init(msg: *mut JogH2r_SendGoal_Response) -> bool;
    fn dsr_msgs2__action__JogH2r_SendGoal_Response__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<JogH2r_SendGoal_Response>, size: usize) -> bool;
    fn dsr_msgs2__action__JogH2r_SendGoal_Response__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<JogH2r_SendGoal_Response>);
    fn dsr_msgs2__action__JogH2r_SendGoal_Response__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<JogH2r_SendGoal_Response>, out_seq: *mut rosidl_runtime_rs::Sequence<JogH2r_SendGoal_Response>) -> bool;
}

// Corresponds to dsr_msgs2__action__JogH2r_SendGoal_Response
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct JogH2r_SendGoal_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub accepted: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub stamp: builtin_interfaces::msg::rmw::Time,

}



impl Default for JogH2r_SendGoal_Response {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !dsr_msgs2__action__JogH2r_SendGoal_Response__init(&mut msg as *mut _) {
        panic!("Call to dsr_msgs2__action__JogH2r_SendGoal_Response__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for JogH2r_SendGoal_Response {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dsr_msgs2__action__JogH2r_SendGoal_Response__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dsr_msgs2__action__JogH2r_SendGoal_Response__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dsr_msgs2__action__JogH2r_SendGoal_Response__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for JogH2r_SendGoal_Response {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for JogH2r_SendGoal_Response where Self: Sized {
  const TYPE_NAME: &'static str = "dsr_msgs2/action/JogH2r_SendGoal_Response";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__dsr_msgs2__action__JogH2r_SendGoal_Response() }
  }
}


#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__dsr_msgs2__action__JogH2r_GetResult_Request() -> *const std::ffi::c_void;
}

#[link(name = "dsr_msgs2__rosidl_generator_c")]
extern "C" {
    fn dsr_msgs2__action__JogH2r_GetResult_Request__init(msg: *mut JogH2r_GetResult_Request) -> bool;
    fn dsr_msgs2__action__JogH2r_GetResult_Request__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<JogH2r_GetResult_Request>, size: usize) -> bool;
    fn dsr_msgs2__action__JogH2r_GetResult_Request__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<JogH2r_GetResult_Request>);
    fn dsr_msgs2__action__JogH2r_GetResult_Request__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<JogH2r_GetResult_Request>, out_seq: *mut rosidl_runtime_rs::Sequence<JogH2r_GetResult_Request>) -> bool;
}

// Corresponds to dsr_msgs2__action__JogH2r_GetResult_Request
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct JogH2r_GetResult_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub goal_id: unique_identifier_msgs::msg::rmw::UUID,

}



impl Default for JogH2r_GetResult_Request {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !dsr_msgs2__action__JogH2r_GetResult_Request__init(&mut msg as *mut _) {
        panic!("Call to dsr_msgs2__action__JogH2r_GetResult_Request__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for JogH2r_GetResult_Request {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dsr_msgs2__action__JogH2r_GetResult_Request__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dsr_msgs2__action__JogH2r_GetResult_Request__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dsr_msgs2__action__JogH2r_GetResult_Request__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for JogH2r_GetResult_Request {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for JogH2r_GetResult_Request where Self: Sized {
  const TYPE_NAME: &'static str = "dsr_msgs2/action/JogH2r_GetResult_Request";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__dsr_msgs2__action__JogH2r_GetResult_Request() }
  }
}


#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__dsr_msgs2__action__JogH2r_GetResult_Response() -> *const std::ffi::c_void;
}

#[link(name = "dsr_msgs2__rosidl_generator_c")]
extern "C" {
    fn dsr_msgs2__action__JogH2r_GetResult_Response__init(msg: *mut JogH2r_GetResult_Response) -> bool;
    fn dsr_msgs2__action__JogH2r_GetResult_Response__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<JogH2r_GetResult_Response>, size: usize) -> bool;
    fn dsr_msgs2__action__JogH2r_GetResult_Response__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<JogH2r_GetResult_Response>);
    fn dsr_msgs2__action__JogH2r_GetResult_Response__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<JogH2r_GetResult_Response>, out_seq: *mut rosidl_runtime_rs::Sequence<JogH2r_GetResult_Response>) -> bool;
}

// Corresponds to dsr_msgs2__action__JogH2r_GetResult_Response
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct JogH2r_GetResult_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub status: i8,


    // This member is not documented.
    #[allow(missing_docs)]
    pub result: super::super::action::rmw::JogH2r_Result,

}



impl Default for JogH2r_GetResult_Response {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !dsr_msgs2__action__JogH2r_GetResult_Response__init(&mut msg as *mut _) {
        panic!("Call to dsr_msgs2__action__JogH2r_GetResult_Response__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for JogH2r_GetResult_Response {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dsr_msgs2__action__JogH2r_GetResult_Response__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dsr_msgs2__action__JogH2r_GetResult_Response__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dsr_msgs2__action__JogH2r_GetResult_Response__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for JogH2r_GetResult_Response {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for JogH2r_GetResult_Response where Self: Sized {
  const TYPE_NAME: &'static str = "dsr_msgs2/action/JogH2r_GetResult_Response";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__dsr_msgs2__action__JogH2r_GetResult_Response() }
  }
}


#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__dsr_msgs2__action__MovejH2r_SendGoal_Request() -> *const std::ffi::c_void;
}

#[link(name = "dsr_msgs2__rosidl_generator_c")]
extern "C" {
    fn dsr_msgs2__action__MovejH2r_SendGoal_Request__init(msg: *mut MovejH2r_SendGoal_Request) -> bool;
    fn dsr_msgs2__action__MovejH2r_SendGoal_Request__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<MovejH2r_SendGoal_Request>, size: usize) -> bool;
    fn dsr_msgs2__action__MovejH2r_SendGoal_Request__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<MovejH2r_SendGoal_Request>);
    fn dsr_msgs2__action__MovejH2r_SendGoal_Request__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<MovejH2r_SendGoal_Request>, out_seq: *mut rosidl_runtime_rs::Sequence<MovejH2r_SendGoal_Request>) -> bool;
}

// Corresponds to dsr_msgs2__action__MovejH2r_SendGoal_Request
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct MovejH2r_SendGoal_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub goal_id: unique_identifier_msgs::msg::rmw::UUID,


    // This member is not documented.
    #[allow(missing_docs)]
    pub goal: super::super::action::rmw::MovejH2r_Goal,

}



impl Default for MovejH2r_SendGoal_Request {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !dsr_msgs2__action__MovejH2r_SendGoal_Request__init(&mut msg as *mut _) {
        panic!("Call to dsr_msgs2__action__MovejH2r_SendGoal_Request__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for MovejH2r_SendGoal_Request {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dsr_msgs2__action__MovejH2r_SendGoal_Request__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dsr_msgs2__action__MovejH2r_SendGoal_Request__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dsr_msgs2__action__MovejH2r_SendGoal_Request__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for MovejH2r_SendGoal_Request {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for MovejH2r_SendGoal_Request where Self: Sized {
  const TYPE_NAME: &'static str = "dsr_msgs2/action/MovejH2r_SendGoal_Request";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__dsr_msgs2__action__MovejH2r_SendGoal_Request() }
  }
}


#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__dsr_msgs2__action__MovejH2r_SendGoal_Response() -> *const std::ffi::c_void;
}

#[link(name = "dsr_msgs2__rosidl_generator_c")]
extern "C" {
    fn dsr_msgs2__action__MovejH2r_SendGoal_Response__init(msg: *mut MovejH2r_SendGoal_Response) -> bool;
    fn dsr_msgs2__action__MovejH2r_SendGoal_Response__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<MovejH2r_SendGoal_Response>, size: usize) -> bool;
    fn dsr_msgs2__action__MovejH2r_SendGoal_Response__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<MovejH2r_SendGoal_Response>);
    fn dsr_msgs2__action__MovejH2r_SendGoal_Response__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<MovejH2r_SendGoal_Response>, out_seq: *mut rosidl_runtime_rs::Sequence<MovejH2r_SendGoal_Response>) -> bool;
}

// Corresponds to dsr_msgs2__action__MovejH2r_SendGoal_Response
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct MovejH2r_SendGoal_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub accepted: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub stamp: builtin_interfaces::msg::rmw::Time,

}



impl Default for MovejH2r_SendGoal_Response {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !dsr_msgs2__action__MovejH2r_SendGoal_Response__init(&mut msg as *mut _) {
        panic!("Call to dsr_msgs2__action__MovejH2r_SendGoal_Response__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for MovejH2r_SendGoal_Response {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dsr_msgs2__action__MovejH2r_SendGoal_Response__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dsr_msgs2__action__MovejH2r_SendGoal_Response__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dsr_msgs2__action__MovejH2r_SendGoal_Response__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for MovejH2r_SendGoal_Response {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for MovejH2r_SendGoal_Response where Self: Sized {
  const TYPE_NAME: &'static str = "dsr_msgs2/action/MovejH2r_SendGoal_Response";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__dsr_msgs2__action__MovejH2r_SendGoal_Response() }
  }
}


#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__dsr_msgs2__action__MovejH2r_GetResult_Request() -> *const std::ffi::c_void;
}

#[link(name = "dsr_msgs2__rosidl_generator_c")]
extern "C" {
    fn dsr_msgs2__action__MovejH2r_GetResult_Request__init(msg: *mut MovejH2r_GetResult_Request) -> bool;
    fn dsr_msgs2__action__MovejH2r_GetResult_Request__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<MovejH2r_GetResult_Request>, size: usize) -> bool;
    fn dsr_msgs2__action__MovejH2r_GetResult_Request__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<MovejH2r_GetResult_Request>);
    fn dsr_msgs2__action__MovejH2r_GetResult_Request__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<MovejH2r_GetResult_Request>, out_seq: *mut rosidl_runtime_rs::Sequence<MovejH2r_GetResult_Request>) -> bool;
}

// Corresponds to dsr_msgs2__action__MovejH2r_GetResult_Request
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct MovejH2r_GetResult_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub goal_id: unique_identifier_msgs::msg::rmw::UUID,

}



impl Default for MovejH2r_GetResult_Request {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !dsr_msgs2__action__MovejH2r_GetResult_Request__init(&mut msg as *mut _) {
        panic!("Call to dsr_msgs2__action__MovejH2r_GetResult_Request__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for MovejH2r_GetResult_Request {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dsr_msgs2__action__MovejH2r_GetResult_Request__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dsr_msgs2__action__MovejH2r_GetResult_Request__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dsr_msgs2__action__MovejH2r_GetResult_Request__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for MovejH2r_GetResult_Request {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for MovejH2r_GetResult_Request where Self: Sized {
  const TYPE_NAME: &'static str = "dsr_msgs2/action/MovejH2r_GetResult_Request";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__dsr_msgs2__action__MovejH2r_GetResult_Request() }
  }
}


#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__dsr_msgs2__action__MovejH2r_GetResult_Response() -> *const std::ffi::c_void;
}

#[link(name = "dsr_msgs2__rosidl_generator_c")]
extern "C" {
    fn dsr_msgs2__action__MovejH2r_GetResult_Response__init(msg: *mut MovejH2r_GetResult_Response) -> bool;
    fn dsr_msgs2__action__MovejH2r_GetResult_Response__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<MovejH2r_GetResult_Response>, size: usize) -> bool;
    fn dsr_msgs2__action__MovejH2r_GetResult_Response__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<MovejH2r_GetResult_Response>);
    fn dsr_msgs2__action__MovejH2r_GetResult_Response__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<MovejH2r_GetResult_Response>, out_seq: *mut rosidl_runtime_rs::Sequence<MovejH2r_GetResult_Response>) -> bool;
}

// Corresponds to dsr_msgs2__action__MovejH2r_GetResult_Response
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct MovejH2r_GetResult_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub status: i8,


    // This member is not documented.
    #[allow(missing_docs)]
    pub result: super::super::action::rmw::MovejH2r_Result,

}



impl Default for MovejH2r_GetResult_Response {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !dsr_msgs2__action__MovejH2r_GetResult_Response__init(&mut msg as *mut _) {
        panic!("Call to dsr_msgs2__action__MovejH2r_GetResult_Response__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for MovejH2r_GetResult_Response {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dsr_msgs2__action__MovejH2r_GetResult_Response__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dsr_msgs2__action__MovejH2r_GetResult_Response__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dsr_msgs2__action__MovejH2r_GetResult_Response__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for MovejH2r_GetResult_Response {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for MovejH2r_GetResult_Response where Self: Sized {
  const TYPE_NAME: &'static str = "dsr_msgs2/action/MovejH2r_GetResult_Response";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__dsr_msgs2__action__MovejH2r_GetResult_Response() }
  }
}


#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__dsr_msgs2__action__MovelH2r_SendGoal_Request() -> *const std::ffi::c_void;
}

#[link(name = "dsr_msgs2__rosidl_generator_c")]
extern "C" {
    fn dsr_msgs2__action__MovelH2r_SendGoal_Request__init(msg: *mut MovelH2r_SendGoal_Request) -> bool;
    fn dsr_msgs2__action__MovelH2r_SendGoal_Request__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<MovelH2r_SendGoal_Request>, size: usize) -> bool;
    fn dsr_msgs2__action__MovelH2r_SendGoal_Request__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<MovelH2r_SendGoal_Request>);
    fn dsr_msgs2__action__MovelH2r_SendGoal_Request__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<MovelH2r_SendGoal_Request>, out_seq: *mut rosidl_runtime_rs::Sequence<MovelH2r_SendGoal_Request>) -> bool;
}

// Corresponds to dsr_msgs2__action__MovelH2r_SendGoal_Request
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct MovelH2r_SendGoal_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub goal_id: unique_identifier_msgs::msg::rmw::UUID,


    // This member is not documented.
    #[allow(missing_docs)]
    pub goal: super::super::action::rmw::MovelH2r_Goal,

}



impl Default for MovelH2r_SendGoal_Request {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !dsr_msgs2__action__MovelH2r_SendGoal_Request__init(&mut msg as *mut _) {
        panic!("Call to dsr_msgs2__action__MovelH2r_SendGoal_Request__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for MovelH2r_SendGoal_Request {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dsr_msgs2__action__MovelH2r_SendGoal_Request__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dsr_msgs2__action__MovelH2r_SendGoal_Request__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dsr_msgs2__action__MovelH2r_SendGoal_Request__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for MovelH2r_SendGoal_Request {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for MovelH2r_SendGoal_Request where Self: Sized {
  const TYPE_NAME: &'static str = "dsr_msgs2/action/MovelH2r_SendGoal_Request";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__dsr_msgs2__action__MovelH2r_SendGoal_Request() }
  }
}


#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__dsr_msgs2__action__MovelH2r_SendGoal_Response() -> *const std::ffi::c_void;
}

#[link(name = "dsr_msgs2__rosidl_generator_c")]
extern "C" {
    fn dsr_msgs2__action__MovelH2r_SendGoal_Response__init(msg: *mut MovelH2r_SendGoal_Response) -> bool;
    fn dsr_msgs2__action__MovelH2r_SendGoal_Response__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<MovelH2r_SendGoal_Response>, size: usize) -> bool;
    fn dsr_msgs2__action__MovelH2r_SendGoal_Response__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<MovelH2r_SendGoal_Response>);
    fn dsr_msgs2__action__MovelH2r_SendGoal_Response__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<MovelH2r_SendGoal_Response>, out_seq: *mut rosidl_runtime_rs::Sequence<MovelH2r_SendGoal_Response>) -> bool;
}

// Corresponds to dsr_msgs2__action__MovelH2r_SendGoal_Response
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct MovelH2r_SendGoal_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub accepted: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub stamp: builtin_interfaces::msg::rmw::Time,

}



impl Default for MovelH2r_SendGoal_Response {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !dsr_msgs2__action__MovelH2r_SendGoal_Response__init(&mut msg as *mut _) {
        panic!("Call to dsr_msgs2__action__MovelH2r_SendGoal_Response__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for MovelH2r_SendGoal_Response {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dsr_msgs2__action__MovelH2r_SendGoal_Response__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dsr_msgs2__action__MovelH2r_SendGoal_Response__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dsr_msgs2__action__MovelH2r_SendGoal_Response__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for MovelH2r_SendGoal_Response {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for MovelH2r_SendGoal_Response where Self: Sized {
  const TYPE_NAME: &'static str = "dsr_msgs2/action/MovelH2r_SendGoal_Response";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__dsr_msgs2__action__MovelH2r_SendGoal_Response() }
  }
}


#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__dsr_msgs2__action__MovelH2r_GetResult_Request() -> *const std::ffi::c_void;
}

#[link(name = "dsr_msgs2__rosidl_generator_c")]
extern "C" {
    fn dsr_msgs2__action__MovelH2r_GetResult_Request__init(msg: *mut MovelH2r_GetResult_Request) -> bool;
    fn dsr_msgs2__action__MovelH2r_GetResult_Request__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<MovelH2r_GetResult_Request>, size: usize) -> bool;
    fn dsr_msgs2__action__MovelH2r_GetResult_Request__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<MovelH2r_GetResult_Request>);
    fn dsr_msgs2__action__MovelH2r_GetResult_Request__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<MovelH2r_GetResult_Request>, out_seq: *mut rosidl_runtime_rs::Sequence<MovelH2r_GetResult_Request>) -> bool;
}

// Corresponds to dsr_msgs2__action__MovelH2r_GetResult_Request
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct MovelH2r_GetResult_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub goal_id: unique_identifier_msgs::msg::rmw::UUID,

}



impl Default for MovelH2r_GetResult_Request {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !dsr_msgs2__action__MovelH2r_GetResult_Request__init(&mut msg as *mut _) {
        panic!("Call to dsr_msgs2__action__MovelH2r_GetResult_Request__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for MovelH2r_GetResult_Request {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dsr_msgs2__action__MovelH2r_GetResult_Request__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dsr_msgs2__action__MovelH2r_GetResult_Request__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dsr_msgs2__action__MovelH2r_GetResult_Request__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for MovelH2r_GetResult_Request {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for MovelH2r_GetResult_Request where Self: Sized {
  const TYPE_NAME: &'static str = "dsr_msgs2/action/MovelH2r_GetResult_Request";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__dsr_msgs2__action__MovelH2r_GetResult_Request() }
  }
}


#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__dsr_msgs2__action__MovelH2r_GetResult_Response() -> *const std::ffi::c_void;
}

#[link(name = "dsr_msgs2__rosidl_generator_c")]
extern "C" {
    fn dsr_msgs2__action__MovelH2r_GetResult_Response__init(msg: *mut MovelH2r_GetResult_Response) -> bool;
    fn dsr_msgs2__action__MovelH2r_GetResult_Response__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<MovelH2r_GetResult_Response>, size: usize) -> bool;
    fn dsr_msgs2__action__MovelH2r_GetResult_Response__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<MovelH2r_GetResult_Response>);
    fn dsr_msgs2__action__MovelH2r_GetResult_Response__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<MovelH2r_GetResult_Response>, out_seq: *mut rosidl_runtime_rs::Sequence<MovelH2r_GetResult_Response>) -> bool;
}

// Corresponds to dsr_msgs2__action__MovelH2r_GetResult_Response
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct MovelH2r_GetResult_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub status: i8,


    // This member is not documented.
    #[allow(missing_docs)]
    pub result: super::super::action::rmw::MovelH2r_Result,

}



impl Default for MovelH2r_GetResult_Response {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !dsr_msgs2__action__MovelH2r_GetResult_Response__init(&mut msg as *mut _) {
        panic!("Call to dsr_msgs2__action__MovelH2r_GetResult_Response__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for MovelH2r_GetResult_Response {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dsr_msgs2__action__MovelH2r_GetResult_Response__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dsr_msgs2__action__MovelH2r_GetResult_Response__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dsr_msgs2__action__MovelH2r_GetResult_Response__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for MovelH2r_GetResult_Response {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for MovelH2r_GetResult_Response where Self: Sized {
  const TYPE_NAME: &'static str = "dsr_msgs2/action/MovelH2r_GetResult_Response";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__dsr_msgs2__action__MovelH2r_GetResult_Response() }
  }
}






#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__action__JogH2r_SendGoal() -> *const std::ffi::c_void;
}

// Corresponds to dsr_msgs2__action__JogH2r_SendGoal
#[allow(missing_docs, non_camel_case_types)]
pub struct JogH2r_SendGoal;

impl rosidl_runtime_rs::Service for JogH2r_SendGoal {
    type Request = JogH2r_SendGoal_Request;
    type Response = JogH2r_SendGoal_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__action__JogH2r_SendGoal() }
    }
}




#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__action__JogH2r_GetResult() -> *const std::ffi::c_void;
}

// Corresponds to dsr_msgs2__action__JogH2r_GetResult
#[allow(missing_docs, non_camel_case_types)]
pub struct JogH2r_GetResult;

impl rosidl_runtime_rs::Service for JogH2r_GetResult {
    type Request = JogH2r_GetResult_Request;
    type Response = JogH2r_GetResult_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__action__JogH2r_GetResult() }
    }
}




#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__action__MovejH2r_SendGoal() -> *const std::ffi::c_void;
}

// Corresponds to dsr_msgs2__action__MovejH2r_SendGoal
#[allow(missing_docs, non_camel_case_types)]
pub struct MovejH2r_SendGoal;

impl rosidl_runtime_rs::Service for MovejH2r_SendGoal {
    type Request = MovejH2r_SendGoal_Request;
    type Response = MovejH2r_SendGoal_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__action__MovejH2r_SendGoal() }
    }
}




#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__action__MovejH2r_GetResult() -> *const std::ffi::c_void;
}

// Corresponds to dsr_msgs2__action__MovejH2r_GetResult
#[allow(missing_docs, non_camel_case_types)]
pub struct MovejH2r_GetResult;

impl rosidl_runtime_rs::Service for MovejH2r_GetResult {
    type Request = MovejH2r_GetResult_Request;
    type Response = MovejH2r_GetResult_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__action__MovejH2r_GetResult() }
    }
}




#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__action__MovelH2r_SendGoal() -> *const std::ffi::c_void;
}

// Corresponds to dsr_msgs2__action__MovelH2r_SendGoal
#[allow(missing_docs, non_camel_case_types)]
pub struct MovelH2r_SendGoal;

impl rosidl_runtime_rs::Service for MovelH2r_SendGoal {
    type Request = MovelH2r_SendGoal_Request;
    type Response = MovelH2r_SendGoal_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__action__MovelH2r_SendGoal() }
    }
}




#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__action__MovelH2r_GetResult() -> *const std::ffi::c_void;
}

// Corresponds to dsr_msgs2__action__MovelH2r_GetResult
#[allow(missing_docs, non_camel_case_types)]
pub struct MovelH2r_GetResult;

impl rosidl_runtime_rs::Service for MovelH2r_GetResult {
    type Request = MovelH2r_GetResult_Request;
    type Response = MovelH2r_GetResult_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__action__MovelH2r_GetResult() }
    }
}


