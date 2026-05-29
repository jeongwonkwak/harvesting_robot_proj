#[cfg(feature = "serde")]
use serde::{Deserialize, Serialize};




// Corresponds to my_robot_interfaces__srv__SetTurtleMode_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SetTurtleMode_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub mode_name: std::string::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub target_speed: f64,

}



impl Default for SetTurtleMode_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::SetTurtleMode_Request::default())
  }
}

impl rosidl_runtime_rs::Message for SetTurtleMode_Request {
  type RmwMsg = super::srv::rmw::SetTurtleMode_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        mode_name: msg.mode_name.as_str().into(),
        target_speed: msg.target_speed,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        mode_name: msg.mode_name.as_str().into(),
      target_speed: msg.target_speed,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      mode_name: msg.mode_name.to_string(),
      target_speed: msg.target_speed,
    }
  }
}


// Corresponds to my_robot_interfaces__srv__SetTurtleMode_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SetTurtleMode_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub message: std::string::String,

}



impl Default for SetTurtleMode_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::SetTurtleMode_Response::default())
  }
}

impl rosidl_runtime_rs::Message for SetTurtleMode_Response {
  type RmwMsg = super::srv::rmw::SetTurtleMode_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        success: msg.success,
        message: msg.message.as_str().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      success: msg.success,
        message: msg.message.as_str().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      success: msg.success,
      message: msg.message.to_string(),
    }
  }
}






#[link(name = "my_robot_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__my_robot_interfaces__srv__SetTurtleMode() -> *const std::ffi::c_void;
}

// Corresponds to my_robot_interfaces__srv__SetTurtleMode
#[allow(missing_docs, non_camel_case_types)]
pub struct SetTurtleMode;

impl rosidl_runtime_rs::Service for SetTurtleMode {
    type Request = SetTurtleMode_Request;
    type Response = SetTurtleMode_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__my_robot_interfaces__srv__SetTurtleMode() }
    }
}


