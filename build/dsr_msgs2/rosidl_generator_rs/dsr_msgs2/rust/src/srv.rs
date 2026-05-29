#[cfg(feature = "serde")]
use serde::{Deserialize, Serialize};




// Corresponds to dsr_msgs2__srv__SetRobotMode_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SetRobotMode_Request {
    /// <Robot_Mode>
    pub robot_mode: i8,

}



impl Default for SetRobotMode_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::SetRobotMode_Request::default())
  }
}

impl rosidl_runtime_rs::Message for SetRobotMode_Request {
  type RmwMsg = super::srv::rmw::SetRobotMode_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        robot_mode: msg.robot_mode,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      robot_mode: msg.robot_mode,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      robot_mode: msg.robot_mode,
    }
  }
}


// Corresponds to dsr_msgs2__srv__SetRobotMode_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SetRobotMode_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,

}



impl Default for SetRobotMode_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::SetRobotMode_Response::default())
  }
}

impl rosidl_runtime_rs::Message for SetRobotMode_Response {
  type RmwMsg = super::srv::rmw::SetRobotMode_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        success: msg.success,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      success: msg.success,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      success: msg.success,
    }
  }
}


// Corresponds to dsr_msgs2__srv__GetRobotMode_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetRobotMode_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub structure_needs_at_least_one_member: u8,

}



impl Default for GetRobotMode_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::GetRobotMode_Request::default())
  }
}

impl rosidl_runtime_rs::Message for GetRobotMode_Request {
  type RmwMsg = super::srv::rmw::GetRobotMode_Request;

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


// Corresponds to dsr_msgs2__srv__GetRobotMode_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetRobotMode_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub robot_mode: i8,


    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,

}



impl Default for GetRobotMode_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::GetRobotMode_Response::default())
  }
}

impl rosidl_runtime_rs::Message for GetRobotMode_Response {
  type RmwMsg = super::srv::rmw::GetRobotMode_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        robot_mode: msg.robot_mode,
        success: msg.success,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      robot_mode: msg.robot_mode,
      success: msg.success,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      robot_mode: msg.robot_mode,
      success: msg.success,
    }
  }
}


// Corresponds to dsr_msgs2__srv__SetRobotSystem_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SetRobotSystem_Request {
    /// 0 : ROBOT_SYSTEM_REAL, 1 : ROBOT_SYSTEM_VIRTUAL
    pub robot_system: i8,

}



impl Default for SetRobotSystem_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::SetRobotSystem_Request::default())
  }
}

impl rosidl_runtime_rs::Message for SetRobotSystem_Request {
  type RmwMsg = super::srv::rmw::SetRobotSystem_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        robot_system: msg.robot_system,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      robot_system: msg.robot_system,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      robot_system: msg.robot_system,
    }
  }
}


// Corresponds to dsr_msgs2__srv__SetRobotSystem_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SetRobotSystem_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,

}



impl Default for SetRobotSystem_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::SetRobotSystem_Response::default())
  }
}

impl rosidl_runtime_rs::Message for SetRobotSystem_Response {
  type RmwMsg = super::srv::rmw::SetRobotSystem_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        success: msg.success,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      success: msg.success,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      success: msg.success,
    }
  }
}


// Corresponds to dsr_msgs2__srv__GetRobotSystem_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetRobotSystem_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub structure_needs_at_least_one_member: u8,

}



impl Default for GetRobotSystem_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::GetRobotSystem_Request::default())
  }
}

impl rosidl_runtime_rs::Message for GetRobotSystem_Request {
  type RmwMsg = super::srv::rmw::GetRobotSystem_Request;

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


// Corresponds to dsr_msgs2__srv__GetRobotSystem_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetRobotSystem_Response {
    /// 0 : ROBOT_SYSTEM_REAL
    /// 1 : ROBOT_SYSTEM_VIRTUAL
    pub robot_system: i8,


    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,

}



impl Default for GetRobotSystem_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::GetRobotSystem_Response::default())
  }
}

impl rosidl_runtime_rs::Message for GetRobotSystem_Response {
  type RmwMsg = super::srv::rmw::GetRobotSystem_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        robot_system: msg.robot_system,
        success: msg.success,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      robot_system: msg.robot_system,
      success: msg.success,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      robot_system: msg.robot_system,
      success: msg.success,
    }
  }
}


// Corresponds to dsr_msgs2__srv__SetRobotSpeedMode_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SetRobotSpeedMode_Request {
    /// 0 : SPEED_NORMAL_MODE, 1 : SPEED_REDUCED_MODE
    pub speed_mode: i8,

}



impl Default for SetRobotSpeedMode_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::SetRobotSpeedMode_Request::default())
  }
}

impl rosidl_runtime_rs::Message for SetRobotSpeedMode_Request {
  type RmwMsg = super::srv::rmw::SetRobotSpeedMode_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        speed_mode: msg.speed_mode,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      speed_mode: msg.speed_mode,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      speed_mode: msg.speed_mode,
    }
  }
}


// Corresponds to dsr_msgs2__srv__SetRobotSpeedMode_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SetRobotSpeedMode_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,

}



impl Default for SetRobotSpeedMode_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::SetRobotSpeedMode_Response::default())
  }
}

impl rosidl_runtime_rs::Message for SetRobotSpeedMode_Response {
  type RmwMsg = super::srv::rmw::SetRobotSpeedMode_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        success: msg.success,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      success: msg.success,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      success: msg.success,
    }
  }
}


// Corresponds to dsr_msgs2__srv__GetRobotSpeedMode_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetRobotSpeedMode_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub structure_needs_at_least_one_member: u8,

}



impl Default for GetRobotSpeedMode_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::GetRobotSpeedMode_Request::default())
  }
}

impl rosidl_runtime_rs::Message for GetRobotSpeedMode_Request {
  type RmwMsg = super::srv::rmw::GetRobotSpeedMode_Request;

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


// Corresponds to dsr_msgs2__srv__GetRobotSpeedMode_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetRobotSpeedMode_Response {
    /// 0 : SPEED_NORMAL_MODE
    /// 1 : SPEED_REDUCED_MODE
    pub speed_mode: i8,


    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,

}



impl Default for GetRobotSpeedMode_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::GetRobotSpeedMode_Response::default())
  }
}

impl rosidl_runtime_rs::Message for GetRobotSpeedMode_Response {
  type RmwMsg = super::srv::rmw::GetRobotSpeedMode_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        speed_mode: msg.speed_mode,
        success: msg.success,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      speed_mode: msg.speed_mode,
      success: msg.success,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      speed_mode: msg.speed_mode,
      success: msg.success,
    }
  }
}


// Corresponds to dsr_msgs2__srv__GetCurrentPose_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetCurrentPose_Request {
    /// 0=ROBOT_SPACE_JOINT, 1=ROBOT_SPACE_TASK
    pub space_type: i8,

}



impl Default for GetCurrentPose_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::GetCurrentPose_Request::default())
  }
}

impl rosidl_runtime_rs::Message for GetCurrentPose_Request {
  type RmwMsg = super::srv::rmw::GetCurrentPose_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        space_type: msg.space_type,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      space_type: msg.space_type,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      space_type: msg.space_type,
    }
  }
}


// Corresponds to dsr_msgs2__srv__GetCurrentPose_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetCurrentPose_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub pos: [f64; 6],


    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,

}



impl Default for GetCurrentPose_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::GetCurrentPose_Response::default())
  }
}

impl rosidl_runtime_rs::Message for GetCurrentPose_Response {
  type RmwMsg = super::srv::rmw::GetCurrentPose_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        pos: msg.pos,
        success: msg.success,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        pos: msg.pos,
      success: msg.success,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      pos: msg.pos,
      success: msg.success,
    }
  }
}


// Corresponds to dsr_msgs2__srv__SetSafeStopResetType_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SetSafeStopResetType_Request {
    /// 0=SAFE_STOP_RESET_TYPE_DEFAULT = SAFE_STOP_RESET_TYPE_PROGRAM_STOP , 1= SAFE_STOP_RESET_TYPE_PROGRAM_RESUME
    pub reset_type: i8,

}



impl Default for SetSafeStopResetType_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::SetSafeStopResetType_Request::default())
  }
}

impl rosidl_runtime_rs::Message for SetSafeStopResetType_Request {
  type RmwMsg = super::srv::rmw::SetSafeStopResetType_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        reset_type: msg.reset_type,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      reset_type: msg.reset_type,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      reset_type: msg.reset_type,
    }
  }
}


// Corresponds to dsr_msgs2__srv__SetSafeStopResetType_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SetSafeStopResetType_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,

}



impl Default for SetSafeStopResetType_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::SetSafeStopResetType_Response::default())
  }
}

impl rosidl_runtime_rs::Message for SetSafeStopResetType_Response {
  type RmwMsg = super::srv::rmw::SetSafeStopResetType_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        success: msg.success,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      success: msg.success,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      success: msg.success,
    }
  }
}


// Corresponds to dsr_msgs2__srv__GetLastAlarm_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetLastAlarm_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub structure_needs_at_least_one_member: u8,

}



impl Default for GetLastAlarm_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::GetLastAlarm_Request::default())
  }
}

impl rosidl_runtime_rs::Message for GetLastAlarm_Request {
  type RmwMsg = super::srv::rmw::GetLastAlarm_Request;

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


// Corresponds to dsr_msgs2__srv__GetLastAlarm_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetLastAlarm_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub log_alarm: super::msg::LogAlarm,


    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,

}



impl Default for GetLastAlarm_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::GetLastAlarm_Response::default())
  }
}

impl rosidl_runtime_rs::Message for GetLastAlarm_Response {
  type RmwMsg = super::srv::rmw::GetLastAlarm_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        log_alarm: super::msg::LogAlarm::into_rmw_message(std::borrow::Cow::Owned(msg.log_alarm)).into_owned(),
        success: msg.success,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        log_alarm: super::msg::LogAlarm::into_rmw_message(std::borrow::Cow::Borrowed(&msg.log_alarm)).into_owned(),
      success: msg.success,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      log_alarm: super::msg::LogAlarm::from_rmw_message(msg.log_alarm),
      success: msg.success,
    }
  }
}


// Corresponds to dsr_msgs2__srv__GetRobotState_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetRobotState_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub structure_needs_at_least_one_member: u8,

}



impl Default for GetRobotState_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::GetRobotState_Request::default())
  }
}

impl rosidl_runtime_rs::Message for GetRobotState_Request {
  type RmwMsg = super::srv::rmw::GetRobotState_Request;

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


// Corresponds to dsr_msgs2__srv__GetRobotState_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetRobotState_Response {
    /// 0 : STATE_INITIALIZING
    /// 1 : STATE_STANDBY
    /// 2 : STATE_MOVING
    /// 3 : STATE_SAFE_OFF
    /// 4 : STATE_TEACHING
    /// 5 : STATE_SAFE_STOP
    /// 6 : STATE_EMERGENCY_STOP:
    /// 7 : STATE_HOMMING
    /// 8 : STATE_RECOVERY
    /// 9 : eSTATE_SAFE_STOP2
    /// 10: STATE_SAFE_OFF2
    /// 11: STATE_RESERVED1
    /// 12: STATE_RESERVED2
    /// 13: STATE_RESERVED3
    /// 14: STATE_RESERVED4
    /// 15: STATE_NOT_READY
    pub robot_state: i8,


    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,

}



impl Default for GetRobotState_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::GetRobotState_Response::default())
  }
}

impl rosidl_runtime_rs::Message for GetRobotState_Response {
  type RmwMsg = super::srv::rmw::GetRobotState_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        robot_state: msg.robot_state,
        success: msg.success,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      robot_state: msg.robot_state,
      success: msg.success,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      robot_state: msg.robot_state,
      success: msg.success,
    }
  }
}


// Corresponds to dsr_msgs2__srv__ServoOff_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ServoOff_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub stop_type: i8,

}

impl ServoOff_Request {

    // This constant is not documented.
    #[allow(missing_docs)]
    pub const STOP_TYPE_QUICK_STO: i8 = 0;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const STOP_TYPE_QUICK: i8 = 1;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const STOP_TYPE_SLOW: i8 = 2;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const STOP_TYPE_HOLD: i8 = 3;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const STOP_TYPE_EMERGENCY: i8 = 3;

}


impl Default for ServoOff_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::ServoOff_Request::default())
  }
}

impl rosidl_runtime_rs::Message for ServoOff_Request {
  type RmwMsg = super::srv::rmw::ServoOff_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        stop_type: msg.stop_type,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      stop_type: msg.stop_type,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      stop_type: msg.stop_type,
    }
  }
}


// Corresponds to dsr_msgs2__srv__ServoOff_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ServoOff_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,

}



impl Default for ServoOff_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::ServoOff_Response::default())
  }
}

impl rosidl_runtime_rs::Message for ServoOff_Response {
  type RmwMsg = super::srv::rmw::ServoOff_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        success: msg.success,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      success: msg.success,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      success: msg.success,
    }
  }
}


// Corresponds to dsr_msgs2__srv__SetRobotControl_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SetRobotControl_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub robot_control: i8,

}



impl Default for SetRobotControl_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::SetRobotControl_Request::default())
  }
}

impl rosidl_runtime_rs::Message for SetRobotControl_Request {
  type RmwMsg = super::srv::rmw::SetRobotControl_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        robot_control: msg.robot_control,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      robot_control: msg.robot_control,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      robot_control: msg.robot_control,
    }
  }
}


// Corresponds to dsr_msgs2__srv__SetRobotControl_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SetRobotControl_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,

}



impl Default for SetRobotControl_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::SetRobotControl_Response::default())
  }
}

impl rosidl_runtime_rs::Message for SetRobotControl_Response {
  type RmwMsg = super::srv::rmw::SetRobotControl_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        success: msg.success,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      success: msg.success,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      success: msg.success,
    }
  }
}


// Corresponds to dsr_msgs2__srv__ChangeCollisionSensitivity_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ChangeCollisionSensitivity_Request {
    /// 0 ~ 100
    pub sensitivity: i8,

}



impl Default for ChangeCollisionSensitivity_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::ChangeCollisionSensitivity_Request::default())
  }
}

impl rosidl_runtime_rs::Message for ChangeCollisionSensitivity_Request {
  type RmwMsg = super::srv::rmw::ChangeCollisionSensitivity_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        sensitivity: msg.sensitivity,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      sensitivity: msg.sensitivity,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      sensitivity: msg.sensitivity,
    }
  }
}


// Corresponds to dsr_msgs2__srv__ChangeCollisionSensitivity_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ChangeCollisionSensitivity_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,

}



impl Default for ChangeCollisionSensitivity_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::ChangeCollisionSensitivity_Response::default())
  }
}

impl rosidl_runtime_rs::Message for ChangeCollisionSensitivity_Response {
  type RmwMsg = super::srv::rmw::ChangeCollisionSensitivity_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        success: msg.success,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      success: msg.success,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      success: msg.success,
    }
  }
}


// Corresponds to dsr_msgs2__srv__SetSafetyMode_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SetSafetyMode_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub safety_mode: i8,


    // This member is not documented.
    #[allow(missing_docs)]
    pub safety_event: i8,

}



impl Default for SetSafetyMode_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::SetSafetyMode_Request::default())
  }
}

impl rosidl_runtime_rs::Message for SetSafetyMode_Request {
  type RmwMsg = super::srv::rmw::SetSafetyMode_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        safety_mode: msg.safety_mode,
        safety_event: msg.safety_event,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      safety_mode: msg.safety_mode,
      safety_event: msg.safety_event,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      safety_mode: msg.safety_mode,
      safety_event: msg.safety_event,
    }
  }
}


// Corresponds to dsr_msgs2__srv__SetSafetyMode_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SetSafetyMode_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,

}



impl Default for SetSafetyMode_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::SetSafetyMode_Response::default())
  }
}

impl rosidl_runtime_rs::Message for SetSafetyMode_Response {
  type RmwMsg = super::srv::rmw::SetSafetyMode_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        success: msg.success,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      success: msg.success,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      success: msg.success,
    }
  }
}


// Corresponds to dsr_msgs2__srv__GetRobotLinkInfo_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetRobotLinkInfo_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub structure_needs_at_least_one_member: u8,

}



impl Default for GetRobotLinkInfo_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::GetRobotLinkInfo_Request::default())
  }
}

impl rosidl_runtime_rs::Message for GetRobotLinkInfo_Request {
  type RmwMsg = super::srv::rmw::GetRobotLinkInfo_Request;

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


// Corresponds to dsr_msgs2__srv__GetRobotLinkInfo_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetRobotLinkInfo_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub d: [f32; 6],


    // This member is not documented.
    #[allow(missing_docs)]
    pub a: [f32; 6],


    // This member is not documented.
    #[allow(missing_docs)]
    pub alpha: [f32; 6],


    // This member is not documented.
    #[allow(missing_docs)]
    pub theta: [f32; 6],


    // This member is not documented.
    #[allow(missing_docs)]
    pub offset: [f32; 6],


    // This member is not documented.
    #[allow(missing_docs)]
    pub gradient: f32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub rotation: f32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,

}



impl Default for GetRobotLinkInfo_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::GetRobotLinkInfo_Response::default())
  }
}

impl rosidl_runtime_rs::Message for GetRobotLinkInfo_Response {
  type RmwMsg = super::srv::rmw::GetRobotLinkInfo_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        d: msg.d,
        a: msg.a,
        alpha: msg.alpha,
        theta: msg.theta,
        offset: msg.offset,
        gradient: msg.gradient,
        rotation: msg.rotation,
        success: msg.success,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        d: msg.d,
        a: msg.a,
        alpha: msg.alpha,
        theta: msg.theta,
        offset: msg.offset,
      gradient: msg.gradient,
      rotation: msg.rotation,
      success: msg.success,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      d: msg.d,
      a: msg.a,
      alpha: msg.alpha,
      theta: msg.theta,
      offset: msg.offset,
      gradient: msg.gradient,
      rotation: msg.rotation,
      success: msg.success,
    }
  }
}


// Corresponds to dsr_msgs2__srv__MoveJoint_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct MoveJoint_Request {
    /// target joint angle list
    pub pos: [f64; 6],

    /// set velocity:
    pub vel: f64,

    /// set acceleration:
    pub acc: f64,

    /// = 0.0       # Time
    pub time: f64,

    /// =0.0      # Radius under blending mode
    pub radius: f64,

    /// = 0         # MOVE_MODE_ABSOLUTE=0, MOVE_MODE_RELATIVE=1
    pub mode: i8,

    /// = 0    # BLENDING_SPEED_TYPE_DUPLICATE=0, BLENDING_SPEED_TYPE_OVERRIDE=1
    pub blend_type: i8,

    /// =0      # SYNC = 0, ASYNC = 1
    pub sync_type: i8,

}



impl Default for MoveJoint_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::MoveJoint_Request::default())
  }
}

impl rosidl_runtime_rs::Message for MoveJoint_Request {
  type RmwMsg = super::srv::rmw::MoveJoint_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        pos: msg.pos,
        vel: msg.vel,
        acc: msg.acc,
        time: msg.time,
        radius: msg.radius,
        mode: msg.mode,
        blend_type: msg.blend_type,
        sync_type: msg.sync_type,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        pos: msg.pos,
      vel: msg.vel,
      acc: msg.acc,
      time: msg.time,
      radius: msg.radius,
      mode: msg.mode,
      blend_type: msg.blend_type,
      sync_type: msg.sync_type,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      pos: msg.pos,
      vel: msg.vel,
      acc: msg.acc,
      time: msg.time,
      radius: msg.radius,
      mode: msg.mode,
      blend_type: msg.blend_type,
      sync_type: msg.sync_type,
    }
  }
}


// Corresponds to dsr_msgs2__srv__MoveJoint_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct MoveJoint_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,

}



impl Default for MoveJoint_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::MoveJoint_Response::default())
  }
}

impl rosidl_runtime_rs::Message for MoveJoint_Response {
  type RmwMsg = super::srv::rmw::MoveJoint_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        success: msg.success,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      success: msg.success,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      success: msg.success,
    }
  }
}


// Corresponds to dsr_msgs2__srv__MoveLine_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct MoveLine_Request {
    /// target
    pub pos: [f64; 6],

    /// set velocity: [mm/sec], [deg/sec]
    pub vel: [f64; 2],

    /// set acceleration: [mm/sec2], [deg/sec2]
    pub acc: [f64; 2],

    /// = 0.0       # Time
    pub time: f64,

    /// =0.0      # Radius under blending mode
    pub radius: f64,

    /// DR_BASE(0), DR_TOOL(1), DR_WORLD(2)
    /// <DR_WORLD is only available in M2.40 or later>
    pub ref_: i8,

    /// = 0         # DR_MV_MOD_ABS(0), DR_MV_MOD_REL(1)
    pub mode: i8,

    /// = 0    # BLENDING_SPEED_TYPE_DUPLICATE=0, BLENDING_SPEED_TYPE_OVERRIDE=1
    pub blend_type: i8,

    /// =0      # SYNC = 0, ASYNC = 1
    pub sync_type: i8,

}



impl Default for MoveLine_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::MoveLine_Request::default())
  }
}

impl rosidl_runtime_rs::Message for MoveLine_Request {
  type RmwMsg = super::srv::rmw::MoveLine_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        pos: msg.pos,
        vel: msg.vel,
        acc: msg.acc,
        time: msg.time,
        radius: msg.radius,
        ref_: msg.ref_,
        mode: msg.mode,
        blend_type: msg.blend_type,
        sync_type: msg.sync_type,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        pos: msg.pos,
        vel: msg.vel,
        acc: msg.acc,
      time: msg.time,
      radius: msg.radius,
      ref_: msg.ref_,
      mode: msg.mode,
      blend_type: msg.blend_type,
      sync_type: msg.sync_type,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      pos: msg.pos,
      vel: msg.vel,
      acc: msg.acc,
      time: msg.time,
      radius: msg.radius,
      ref_: msg.ref_,
      mode: msg.mode,
      blend_type: msg.blend_type,
      sync_type: msg.sync_type,
    }
  }
}


// Corresponds to dsr_msgs2__srv__MoveLine_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct MoveLine_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,

}



impl Default for MoveLine_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::MoveLine_Response::default())
  }
}

impl rosidl_runtime_rs::Message for MoveLine_Response {
  type RmwMsg = super::srv::rmw::MoveLine_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        success: msg.success,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      success: msg.success,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      success: msg.success,
    }
  }
}


// Corresponds to dsr_msgs2__srv__MoveJointx_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct MoveJointx_Request {
    /// target
    pub pos: [f64; 6],

    /// set velocity:
    pub vel: f64,

    /// set acceleration:
    pub acc: f64,

    /// = 0.0      # Time
    pub time: f64,

    /// =0.0     # Radius under blending mode
    pub radius: f64,

    /// DR_BASE(0), DR_TOOL(1), DR_WORLD(2)
    /// <DR_WORLD is only available in M2.40 or later>
    pub ref_: i8,

    /// = 0        # MOVE_MODE_ABSOLUTE=0, MOVE_MODE_RELATIVE=1
    pub mode: i8,

    /// = 0   # BLENDING_SPEED_TYPE_DUPLICATE=0, BLENDING_SPEED_TYPE_OVERRIDE=1
    pub blend_type: i8,

    /// SolutionSpace : 0~7
    pub sol: i8,

    /// =0     # SYNC = 0, ASYNC = 1
    pub sync_type: i8,

}



impl Default for MoveJointx_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::MoveJointx_Request::default())
  }
}

impl rosidl_runtime_rs::Message for MoveJointx_Request {
  type RmwMsg = super::srv::rmw::MoveJointx_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        pos: msg.pos,
        vel: msg.vel,
        acc: msg.acc,
        time: msg.time,
        radius: msg.radius,
        ref_: msg.ref_,
        mode: msg.mode,
        blend_type: msg.blend_type,
        sol: msg.sol,
        sync_type: msg.sync_type,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        pos: msg.pos,
      vel: msg.vel,
      acc: msg.acc,
      time: msg.time,
      radius: msg.radius,
      ref_: msg.ref_,
      mode: msg.mode,
      blend_type: msg.blend_type,
      sol: msg.sol,
      sync_type: msg.sync_type,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      pos: msg.pos,
      vel: msg.vel,
      acc: msg.acc,
      time: msg.time,
      radius: msg.radius,
      ref_: msg.ref_,
      mode: msg.mode,
      blend_type: msg.blend_type,
      sol: msg.sol,
      sync_type: msg.sync_type,
    }
  }
}


// Corresponds to dsr_msgs2__srv__MoveJointx_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct MoveJointx_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,

}



impl Default for MoveJointx_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::MoveJointx_Response::default())
  }
}

impl rosidl_runtime_rs::Message for MoveJointx_Response {
  type RmwMsg = super::srv::rmw::MoveJointx_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        success: msg.success,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      success: msg.success,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      success: msg.success,
    }
  }
}


// Corresponds to dsr_msgs2__srv__MoveCircle_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct MoveCircle_Request {
    /// target[2][6]
    pub pos: Vec<std_msgs::msg::Float64MultiArray>,

    /// set velocity: [mm/sec], [deg/sec]
    pub vel: [f64; 2],

    /// set acceleration: [mm/sec2], [deg/sec2]
    pub acc: [f64; 2],

    /// = 0.0       # Time
    pub time: f64,

    /// =0.0      # Radius under blending mode
    pub radius: f64,

    /// DR_BASE(0), DR_TOOL(1), DR_WORLD(2)
    /// <DR_WORLD is only available in M2.40 or later>
    pub ref_: i8,

    /// = 0         # MOVE_MODE_ABSOLUTE=0, MOVE_MODE_RELATIVE=1
    pub mode: i8,

    /// = 0.0     # angle1
    pub angle1: f64,

    /// = 0.0     # angle2
    pub angle2: f64,

    /// = 0    # BLENDING_SPEED_TYPE_DUPLICATE=0, BLENDING_SPEED_TYPE_OVERRIDE=1
    pub blend_type: i8,

    /// =0      # SYNC = 0, ASYNC = 1
    pub sync_type: i8,

}



impl Default for MoveCircle_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::MoveCircle_Request::default())
  }
}

impl rosidl_runtime_rs::Message for MoveCircle_Request {
  type RmwMsg = super::srv::rmw::MoveCircle_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        pos: msg.pos
          .into_iter()
          .map(|elem| std_msgs::msg::Float64MultiArray::into_rmw_message(std::borrow::Cow::Owned(elem)).into_owned())
          .collect(),
        vel: msg.vel,
        acc: msg.acc,
        time: msg.time,
        radius: msg.radius,
        ref_: msg.ref_,
        mode: msg.mode,
        angle1: msg.angle1,
        angle2: msg.angle2,
        blend_type: msg.blend_type,
        sync_type: msg.sync_type,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        pos: msg.pos
          .iter()
          .map(|elem| std_msgs::msg::Float64MultiArray::into_rmw_message(std::borrow::Cow::Borrowed(elem)).into_owned())
          .collect(),
        vel: msg.vel,
        acc: msg.acc,
      time: msg.time,
      radius: msg.radius,
      ref_: msg.ref_,
      mode: msg.mode,
      angle1: msg.angle1,
      angle2: msg.angle2,
      blend_type: msg.blend_type,
      sync_type: msg.sync_type,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      pos: msg.pos
          .into_iter()
          .map(std_msgs::msg::Float64MultiArray::from_rmw_message)
          .collect(),
      vel: msg.vel,
      acc: msg.acc,
      time: msg.time,
      radius: msg.radius,
      ref_: msg.ref_,
      mode: msg.mode,
      angle1: msg.angle1,
      angle2: msg.angle2,
      blend_type: msg.blend_type,
      sync_type: msg.sync_type,
    }
  }
}


// Corresponds to dsr_msgs2__srv__MoveCircle_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct MoveCircle_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,

}



impl Default for MoveCircle_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::MoveCircle_Response::default())
  }
}

impl rosidl_runtime_rs::Message for MoveCircle_Response {
  type RmwMsg = super::srv::rmw::MoveCircle_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        success: msg.success,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      success: msg.success,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      success: msg.success,
    }
  }
}


// Corresponds to dsr_msgs2__srv__MoveSplineJoint_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct MoveSplineJoint_Request {
    /// target [100][6] pos
    pub pos: Vec<std_msgs::msg::Float64MultiArray>,

    /// target cnt
    pub pos_cnt: i8,

    /// set joint velocity:
    pub vel: [f64; 6],

    /// set joint acceleration:
    pub acc: [f64; 6],

    /// = 0.0                   # Time
    pub time: f64,

    /// = 0                     # MOVE_MODE_ABSOLUTE=0, MOVE_MODE_RELATIVE=1
    pub mode: i8,

    /// =0                 # SYNC = 0, ASYNC = 1
    pub sync_type: i8,

}



impl Default for MoveSplineJoint_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::MoveSplineJoint_Request::default())
  }
}

impl rosidl_runtime_rs::Message for MoveSplineJoint_Request {
  type RmwMsg = super::srv::rmw::MoveSplineJoint_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        pos: msg.pos
          .into_iter()
          .map(|elem| std_msgs::msg::Float64MultiArray::into_rmw_message(std::borrow::Cow::Owned(elem)).into_owned())
          .collect(),
        pos_cnt: msg.pos_cnt,
        vel: msg.vel,
        acc: msg.acc,
        time: msg.time,
        mode: msg.mode,
        sync_type: msg.sync_type,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        pos: msg.pos
          .iter()
          .map(|elem| std_msgs::msg::Float64MultiArray::into_rmw_message(std::borrow::Cow::Borrowed(elem)).into_owned())
          .collect(),
      pos_cnt: msg.pos_cnt,
        vel: msg.vel,
        acc: msg.acc,
      time: msg.time,
      mode: msg.mode,
      sync_type: msg.sync_type,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      pos: msg.pos
          .into_iter()
          .map(std_msgs::msg::Float64MultiArray::from_rmw_message)
          .collect(),
      pos_cnt: msg.pos_cnt,
      vel: msg.vel,
      acc: msg.acc,
      time: msg.time,
      mode: msg.mode,
      sync_type: msg.sync_type,
    }
  }
}


// Corresponds to dsr_msgs2__srv__MoveSplineJoint_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct MoveSplineJoint_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,

}



impl Default for MoveSplineJoint_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::MoveSplineJoint_Response::default())
  }
}

impl rosidl_runtime_rs::Message for MoveSplineJoint_Response {
  type RmwMsg = super::srv::rmw::MoveSplineJoint_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        success: msg.success,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      success: msg.success,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      success: msg.success,
    }
  }
}


// Corresponds to dsr_msgs2__srv__MoveSplineTask_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct MoveSplineTask_Request {
    /// target
    pub pos: Vec<std_msgs::msg::Float64MultiArray>,

    /// target cnt
    pub pos_cnt: i8,

    /// set velocity: [mm/sec], [deg/sec]
    pub vel: [f64; 2],

    /// set acceleration: [mm/sec2], [deg/sec2]
    pub acc: [f64; 2],

    /// = 0.0       # Time
    pub time: f64,

    /// DR_BASE(0), DR_TOOL(1), DR_WORLD(2)
    /// <DR_WORLD is only available in M2.40 or later
    pub ref_: i8,

    /// = 0         # MOVE_MODE_ABSOLUTE=0, MOVE_MODE_RELATIVE=1
    pub mode: i8,

    /// = 0         # SPLINE_VELOCITY_OPTION_DEFAULT=0, SPLINE_VELOCITY_OPTION_CONST=1
    pub opt: i8,

    /// =0      # SYNC = 0, ASYNC = 1
    pub sync_type: i8,

}



impl Default for MoveSplineTask_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::MoveSplineTask_Request::default())
  }
}

impl rosidl_runtime_rs::Message for MoveSplineTask_Request {
  type RmwMsg = super::srv::rmw::MoveSplineTask_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        pos: msg.pos
          .into_iter()
          .map(|elem| std_msgs::msg::Float64MultiArray::into_rmw_message(std::borrow::Cow::Owned(elem)).into_owned())
          .collect(),
        pos_cnt: msg.pos_cnt,
        vel: msg.vel,
        acc: msg.acc,
        time: msg.time,
        ref_: msg.ref_,
        mode: msg.mode,
        opt: msg.opt,
        sync_type: msg.sync_type,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        pos: msg.pos
          .iter()
          .map(|elem| std_msgs::msg::Float64MultiArray::into_rmw_message(std::borrow::Cow::Borrowed(elem)).into_owned())
          .collect(),
      pos_cnt: msg.pos_cnt,
        vel: msg.vel,
        acc: msg.acc,
      time: msg.time,
      ref_: msg.ref_,
      mode: msg.mode,
      opt: msg.opt,
      sync_type: msg.sync_type,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      pos: msg.pos
          .into_iter()
          .map(std_msgs::msg::Float64MultiArray::from_rmw_message)
          .collect(),
      pos_cnt: msg.pos_cnt,
      vel: msg.vel,
      acc: msg.acc,
      time: msg.time,
      ref_: msg.ref_,
      mode: msg.mode,
      opt: msg.opt,
      sync_type: msg.sync_type,
    }
  }
}


// Corresponds to dsr_msgs2__srv__MoveSplineTask_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct MoveSplineTask_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,

}



impl Default for MoveSplineTask_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::MoveSplineTask_Response::default())
  }
}

impl rosidl_runtime_rs::Message for MoveSplineTask_Response {
  type RmwMsg = super::srv::rmw::MoveSplineTask_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        success: msg.success,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      success: msg.success,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      success: msg.success,
    }
  }
}


// Corresponds to dsr_msgs2__srv__MoveBlending_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct MoveBlending_Request {
    /// 50 x (pos1[6]:pos2[6]:type[1]:radius[1])
    pub segment: Vec<std_msgs::msg::Float64MultiArray>,

    /// target cnt
    pub pos_cnt: i8,

    /// set velocity: [mm/sec], [deg/sec]
    pub vel: [f64; 2],

    /// set acceleration: [mm/sec2], [deg/sec2]
    pub acc: [f64; 2],

    /// = 0.0          # Time
    pub time: f64,

    /// DR_BASE(0), DR_TOOL(1), DR_WORLD(2)
    /// <DR_WORLD is only available in M2.40 or later
    pub ref_: i8,

    /// = 0            # MOVE_MODE_ABSOLUTE=0, MOVE_MODE_RELATIVE=1
    pub mode: i8,

    /// =0         # SYNC = 0, ASYNC = 1
    pub sync_type: i8,

}



impl Default for MoveBlending_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::MoveBlending_Request::default())
  }
}

impl rosidl_runtime_rs::Message for MoveBlending_Request {
  type RmwMsg = super::srv::rmw::MoveBlending_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        segment: msg.segment
          .into_iter()
          .map(|elem| std_msgs::msg::Float64MultiArray::into_rmw_message(std::borrow::Cow::Owned(elem)).into_owned())
          .collect(),
        pos_cnt: msg.pos_cnt,
        vel: msg.vel,
        acc: msg.acc,
        time: msg.time,
        ref_: msg.ref_,
        mode: msg.mode,
        sync_type: msg.sync_type,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        segment: msg.segment
          .iter()
          .map(|elem| std_msgs::msg::Float64MultiArray::into_rmw_message(std::borrow::Cow::Borrowed(elem)).into_owned())
          .collect(),
      pos_cnt: msg.pos_cnt,
        vel: msg.vel,
        acc: msg.acc,
      time: msg.time,
      ref_: msg.ref_,
      mode: msg.mode,
      sync_type: msg.sync_type,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      segment: msg.segment
          .into_iter()
          .map(std_msgs::msg::Float64MultiArray::from_rmw_message)
          .collect(),
      pos_cnt: msg.pos_cnt,
      vel: msg.vel,
      acc: msg.acc,
      time: msg.time,
      ref_: msg.ref_,
      mode: msg.mode,
      sync_type: msg.sync_type,
    }
  }
}


// Corresponds to dsr_msgs2__srv__MoveBlending_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct MoveBlending_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,

}



impl Default for MoveBlending_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::MoveBlending_Response::default())
  }
}

impl rosidl_runtime_rs::Message for MoveBlending_Response {
  type RmwMsg = super::srv::rmw::MoveBlending_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        success: msg.success,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      success: msg.success,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      success: msg.success,
    }
  }
}


// Corresponds to dsr_msgs2__srv__MoveSpiral_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct MoveSpiral_Request {
    /// Total number of revolutions
    pub revolution: f64,

    /// Final spiral radius
    pub max_radius: f64,

    /// Distance moved in the axis direction
    pub max_length: f64,

    /// Target position. If used, max_radius and max_length are ignored
    pub target_pos: [f64; 3],

    /// set velocity: [mm/sec], [deg/sec]
    pub vel: [f64; 2],

    /// set acceleration: [mm/sec2], [deg/sec2]
    pub acc: [f64; 2],

    /// = 0.0      # Total execution time <sec>
    pub time: f64,

    /// TASK_AXIS_X = 0, TASK_AXIS_Y = 1, TASK_AXIS_Z = 2
    pub task_axis: i8,

    /// = 1        # DR_BASE(0), DR_TOOL(1), DR_WORLD(2)
    ///  <DR_WORLD is only available in M2.40 or later
    pub ref_: i8,

    /// = 0        # MOVE_MODE_ABSOLUTE=0, MOVE_MODE_RELATIVE=1
    pub mode: i8,

    /// = 0  # MOVE_SPIRAL_OUTWARD=0, MOVE_SPIRAL_INWARD=1
    pub spiral_dir: i8,

    /// =0      # MOVE_SPIRAL_FORWARD=0, MOVE_SPIRAL_REVERSE=1
    pub rot_dir: i8,

    /// =0    # SYNC = 0, ASYNC = 1
    pub sync_type: i8,

}



impl Default for MoveSpiral_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::MoveSpiral_Request::default())
  }
}

impl rosidl_runtime_rs::Message for MoveSpiral_Request {
  type RmwMsg = super::srv::rmw::MoveSpiral_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        revolution: msg.revolution,
        max_radius: msg.max_radius,
        max_length: msg.max_length,
        target_pos: msg.target_pos,
        vel: msg.vel,
        acc: msg.acc,
        time: msg.time,
        task_axis: msg.task_axis,
        ref_: msg.ref_,
        mode: msg.mode,
        spiral_dir: msg.spiral_dir,
        rot_dir: msg.rot_dir,
        sync_type: msg.sync_type,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      revolution: msg.revolution,
      max_radius: msg.max_radius,
      max_length: msg.max_length,
        target_pos: msg.target_pos,
        vel: msg.vel,
        acc: msg.acc,
      time: msg.time,
      task_axis: msg.task_axis,
      ref_: msg.ref_,
      mode: msg.mode,
      spiral_dir: msg.spiral_dir,
      rot_dir: msg.rot_dir,
      sync_type: msg.sync_type,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      revolution: msg.revolution,
      max_radius: msg.max_radius,
      max_length: msg.max_length,
      target_pos: msg.target_pos,
      vel: msg.vel,
      acc: msg.acc,
      time: msg.time,
      task_axis: msg.task_axis,
      ref_: msg.ref_,
      mode: msg.mode,
      spiral_dir: msg.spiral_dir,
      rot_dir: msg.rot_dir,
      sync_type: msg.sync_type,
    }
  }
}


// Corresponds to dsr_msgs2__srv__MoveSpiral_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct MoveSpiral_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,

}



impl Default for MoveSpiral_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::MoveSpiral_Response::default())
  }
}

impl rosidl_runtime_rs::Message for MoveSpiral_Response {
  type RmwMsg = super::srv::rmw::MoveSpiral_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        success: msg.success,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      success: msg.success,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      success: msg.success,
    }
  }
}


// Corresponds to dsr_msgs2__srv__MovePeriodic_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct MovePeriodic_Request {
    /// Amplitude (motion between -amp and +amp) [mm] or [deg]
    pub amp: [f64; 6],

    /// Period (time for 1 cycle)
    pub periodic: [f64; 6],

    /// Acc-, dec- time
    pub acc: f64,

    /// Repetition count
    pub repeat: i8,

    /// = 1        # DR_BASE(0), DR_TOOL(1), DR_WORLD(2)
    ///  <DR_WORLD is only available in M2.40 or later
    pub ref_: i8,

    /// =0     # SYNC = 0, ASYNC = 1
    pub sync_type: i8,

}



impl Default for MovePeriodic_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::MovePeriodic_Request::default())
  }
}

impl rosidl_runtime_rs::Message for MovePeriodic_Request {
  type RmwMsg = super::srv::rmw::MovePeriodic_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        amp: msg.amp,
        periodic: msg.periodic,
        acc: msg.acc,
        repeat: msg.repeat,
        ref_: msg.ref_,
        sync_type: msg.sync_type,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        amp: msg.amp,
        periodic: msg.periodic,
      acc: msg.acc,
      repeat: msg.repeat,
      ref_: msg.ref_,
      sync_type: msg.sync_type,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      amp: msg.amp,
      periodic: msg.periodic,
      acc: msg.acc,
      repeat: msg.repeat,
      ref_: msg.ref_,
      sync_type: msg.sync_type,
    }
  }
}


// Corresponds to dsr_msgs2__srv__MovePeriodic_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct MovePeriodic_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,

}



impl Default for MovePeriodic_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::MovePeriodic_Response::default())
  }
}

impl rosidl_runtime_rs::Message for MovePeriodic_Response {
  type RmwMsg = super::srv::rmw::MovePeriodic_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        success: msg.success,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      success: msg.success,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      success: msg.success,
    }
  }
}


// Corresponds to dsr_msgs2__srv__MoveWait_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct MoveWait_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub structure_needs_at_least_one_member: u8,

}



impl Default for MoveWait_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::MoveWait_Request::default())
  }
}

impl rosidl_runtime_rs::Message for MoveWait_Request {
  type RmwMsg = super::srv::rmw::MoveWait_Request;

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


// Corresponds to dsr_msgs2__srv__MoveWait_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct MoveWait_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,

}



impl Default for MoveWait_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::MoveWait_Response::default())
  }
}

impl rosidl_runtime_rs::Message for MoveWait_Response {
  type RmwMsg = super::srv::rmw::MoveWait_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        success: msg.success,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      success: msg.success,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      success: msg.success,
    }
  }
}


// Corresponds to dsr_msgs2__srv__Jog_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct Jog_Request {
    /// 0 ~ 5 : JOINT 1 ~ 6
    /// 6 ~ 11: TASK 1 ~ 6 (X,Y,Z,rx,ry,rz)
    pub jog_axis: i8,

    /// 0 : MOVE_REFERENCE_BASE, 1 : MOVE_REFERENCE_TOOL
    pub move_reference: i8,

    /// jog speed : + forward , 0=stop, - backward
    pub speed: f64,

}



impl Default for Jog_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::Jog_Request::default())
  }
}

impl rosidl_runtime_rs::Message for Jog_Request {
  type RmwMsg = super::srv::rmw::Jog_Request;

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


// Corresponds to dsr_msgs2__srv__Jog_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct Jog_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,

}



impl Default for Jog_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::Jog_Response::default())
  }
}

impl rosidl_runtime_rs::Message for Jog_Response {
  type RmwMsg = super::srv::rmw::Jog_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        success: msg.success,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      success: msg.success,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      success: msg.success,
    }
  }
}


// Corresponds to dsr_msgs2__srv__JogMulti_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct JogMulti_Request {
    /// unit vecter of Task space [Tx, Ty, Tz, Rx, Ry, Rz] : -1.0 ~ +1.0
    pub jog_axis: [f64; 6],

    /// 0 : MOVE_REFERENCE_BASE, 1 : MOVE_REFERENCE_TOOL, 2 : MOVE_REFERENCE_WORLD
    pub move_reference: i8,

    /// jog speed
    pub speed: f64,

}



impl Default for JogMulti_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::JogMulti_Request::default())
  }
}

impl rosidl_runtime_rs::Message for JogMulti_Request {
  type RmwMsg = super::srv::rmw::JogMulti_Request;

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


// Corresponds to dsr_msgs2__srv__JogMulti_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct JogMulti_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,

}



impl Default for JogMulti_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::JogMulti_Response::default())
  }
}

impl rosidl_runtime_rs::Message for JogMulti_Response {
  type RmwMsg = super::srv::rmw::JogMulti_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        success: msg.success,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      success: msg.success,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      success: msg.success,
    }
  }
}


// Corresponds to dsr_msgs2__srv__MoveStop_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct MoveStop_Request {
    /// DR_QSTOP_STO(0) : Quick stop (Stop Category 1 without STO(Safe Torque Off)
    /// DR_QSTOP(1)     : Quick stop (Stop Category 2)
    /// DR_SSTO(2)      : Soft Stop
    /// DR_HOLD(3)      : HOLD stop
    pub stop_mode: i32,

}



impl Default for MoveStop_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::MoveStop_Request::default())
  }
}

impl rosidl_runtime_rs::Message for MoveStop_Request {
  type RmwMsg = super::srv::rmw::MoveStop_Request;

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


// Corresponds to dsr_msgs2__srv__MoveStop_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct MoveStop_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,

}



impl Default for MoveStop_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::MoveStop_Response::default())
  }
}

impl rosidl_runtime_rs::Message for MoveStop_Response {
  type RmwMsg = super::srv::rmw::MoveStop_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        success: msg.success,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      success: msg.success,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      success: msg.success,
    }
  }
}


// Corresponds to dsr_msgs2__srv__MovePause_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct MovePause_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub structure_needs_at_least_one_member: u8,

}



impl Default for MovePause_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::MovePause_Request::default())
  }
}

impl rosidl_runtime_rs::Message for MovePause_Request {
  type RmwMsg = super::srv::rmw::MovePause_Request;

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


// Corresponds to dsr_msgs2__srv__MovePause_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct MovePause_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,

}



impl Default for MovePause_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::MovePause_Response::default())
  }
}

impl rosidl_runtime_rs::Message for MovePause_Response {
  type RmwMsg = super::srv::rmw::MovePause_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        success: msg.success,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      success: msg.success,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      success: msg.success,
    }
  }
}


// Corresponds to dsr_msgs2__srv__MoveResume_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct MoveResume_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub structure_needs_at_least_one_member: u8,

}



impl Default for MoveResume_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::MoveResume_Request::default())
  }
}

impl rosidl_runtime_rs::Message for MoveResume_Request {
  type RmwMsg = super::srv::rmw::MoveResume_Request;

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


// Corresponds to dsr_msgs2__srv__MoveResume_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct MoveResume_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,

}



impl Default for MoveResume_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::MoveResume_Response::default())
  }
}

impl rosidl_runtime_rs::Message for MoveResume_Response {
  type RmwMsg = super::srv::rmw::MoveResume_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        success: msg.success,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      success: msg.success,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      success: msg.success,
    }
  }
}


// Corresponds to dsr_msgs2__srv__Trans_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct Trans_Request {
    /// task pos(posx)
    pub pos: [f64; 6],

    /// delta (posx)
    pub delta: [f64; 6],

    /// = 0      # DR_BASE(0), DR_TOOL(1), DR_WORLD(2)
    ///  <DR_WORLD is only available in M2.40 or later>
    pub ref_: i8,

    /// = 0      # DR_BASE(0), DR_WORLD(2)
    ///  <ref_out is only available in M2.40 or later>
    pub ref_out: i8,

}



impl Default for Trans_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::Trans_Request::default())
  }
}

impl rosidl_runtime_rs::Message for Trans_Request {
  type RmwMsg = super::srv::rmw::Trans_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        pos: msg.pos,
        delta: msg.delta,
        ref_: msg.ref_,
        ref_out: msg.ref_out,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        pos: msg.pos,
        delta: msg.delta,
      ref_: msg.ref_,
      ref_out: msg.ref_out,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      pos: msg.pos,
      delta: msg.delta,
      ref_: msg.ref_,
      ref_out: msg.ref_out,
    }
  }
}


// Corresponds to dsr_msgs2__srv__Trans_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct Trans_Response {
    /// trans pos(posx)
    pub trans_pos: [f64; 6],


    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,

}



impl Default for Trans_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::Trans_Response::default())
  }
}

impl rosidl_runtime_rs::Message for Trans_Response {
  type RmwMsg = super::srv::rmw::Trans_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        trans_pos: msg.trans_pos,
        success: msg.success,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        trans_pos: msg.trans_pos,
      success: msg.success,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      trans_pos: msg.trans_pos,
      success: msg.success,
    }
  }
}


// Corresponds to dsr_msgs2__srv__Fkin_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct Fkin_Request {
    /// joint pos(posj)
    pub pos: [f64; 6],

    /// = 0      # DR_BASE(0), DR_WORLD(2)
    ///  <ref is only available in M2.40 or later>
    pub ref_: i8,

}



impl Default for Fkin_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::Fkin_Request::default())
  }
}

impl rosidl_runtime_rs::Message for Fkin_Request {
  type RmwMsg = super::srv::rmw::Fkin_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        pos: msg.pos,
        ref_: msg.ref_,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        pos: msg.pos,
      ref_: msg.ref_,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      pos: msg.pos,
      ref_: msg.ref_,
    }
  }
}


// Corresponds to dsr_msgs2__srv__Fkin_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct Fkin_Response {
    /// task pos(posx)
    pub conv_posx: [f64; 6],


    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,

}



impl Default for Fkin_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::Fkin_Response::default())
  }
}

impl rosidl_runtime_rs::Message for Fkin_Response {
  type RmwMsg = super::srv::rmw::Fkin_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        conv_posx: msg.conv_posx,
        success: msg.success,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        conv_posx: msg.conv_posx,
      success: msg.success,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      conv_posx: msg.conv_posx,
      success: msg.success,
    }
  }
}


// Corresponds to dsr_msgs2__srv__Ikin_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct Ikin_Request {
    /// task pos(posx)
    pub pos: [f64; 6],

    /// solution space : 0 ~ 7
    pub sol_space: i8,

    /// = 0      # DR_BASE(0), DR_WORLD(2)
    ///  <ref is only available in M2.40 or later>
    pub ref_: i8,

}



impl Default for Ikin_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::Ikin_Request::default())
  }
}

impl rosidl_runtime_rs::Message for Ikin_Request {
  type RmwMsg = super::srv::rmw::Ikin_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        pos: msg.pos,
        sol_space: msg.sol_space,
        ref_: msg.ref_,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        pos: msg.pos,
      sol_space: msg.sol_space,
      ref_: msg.ref_,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      pos: msg.pos,
      sol_space: msg.sol_space,
      ref_: msg.ref_,
    }
  }
}


// Corresponds to dsr_msgs2__srv__Ikin_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct Ikin_Response {
    /// joint pos(posj)
    pub conv_posj: [f64; 6],


    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,

}



impl Default for Ikin_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::Ikin_Response::default())
  }
}

impl rosidl_runtime_rs::Message for Ikin_Response {
  type RmwMsg = super::srv::rmw::Ikin_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        conv_posj: msg.conv_posj,
        success: msg.success,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        conv_posj: msg.conv_posj,
      success: msg.success,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      conv_posj: msg.conv_posj,
      success: msg.success,
    }
  }
}


// Corresponds to dsr_msgs2__srv__SetRefCoord_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SetRefCoord_Request {
    /// DR_BASE(0), DR_TOOL(1), DR_WORLD(2), user coord(101~200)
    /// <DR_WORLD is only available in M2.40 or later>
    pub coord: i8,

}



impl Default for SetRefCoord_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::SetRefCoord_Request::default())
  }
}

impl rosidl_runtime_rs::Message for SetRefCoord_Request {
  type RmwMsg = super::srv::rmw::SetRefCoord_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        coord: msg.coord,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      coord: msg.coord,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      coord: msg.coord,
    }
  }
}


// Corresponds to dsr_msgs2__srv__SetRefCoord_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SetRefCoord_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,

}



impl Default for SetRefCoord_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::SetRefCoord_Response::default())
  }
}

impl rosidl_runtime_rs::Message for SetRefCoord_Response {
  type RmwMsg = super::srv::rmw::SetRefCoord_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        success: msg.success,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      success: msg.success,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      success: msg.success,
    }
  }
}


// Corresponds to dsr_msgs2__srv__MoveHome_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct MoveHome_Request {
    /// DR_HOME_TARGET_MECHANIC(0) : Mechanical home, joint angle (0,0,0,0,0,0)
    /// DR_HOME_TARGET_USER(1)     : user home
    pub target: i8,

}



impl Default for MoveHome_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::MoveHome_Request::default())
  }
}

impl rosidl_runtime_rs::Message for MoveHome_Request {
  type RmwMsg = super::srv::rmw::MoveHome_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        target: msg.target,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      target: msg.target,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      target: msg.target,
    }
  }
}


// Corresponds to dsr_msgs2__srv__MoveHome_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct MoveHome_Response {
    /// 0=success, otherwise fail
    pub res: i8,


    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,

}



impl Default for MoveHome_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::MoveHome_Response::default())
  }
}

impl rosidl_runtime_rs::Message for MoveHome_Response {
  type RmwMsg = super::srv::rmw::MoveHome_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        res: msg.res,
        success: msg.success,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      res: msg.res,
      success: msg.success,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      res: msg.res,
      success: msg.success,
    }
  }
}


// Corresponds to dsr_msgs2__srv__CheckMotion_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct CheckMotion_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub structure_needs_at_least_one_member: u8,

}



impl Default for CheckMotion_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::CheckMotion_Request::default())
  }
}

impl rosidl_runtime_rs::Message for CheckMotion_Request {
  type RmwMsg = super::srv::rmw::CheckMotion_Request;

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


// Corresponds to dsr_msgs2__srv__CheckMotion_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct CheckMotion_Response {
    /// DR_STATE_IDLE(0) : no motion in action
    /// DR_STATE_INIT(1) : motion being calculated
    /// DR_STATE_BUSY(2) : motion in operation
    pub status: i8,


    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,

}



impl Default for CheckMotion_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::CheckMotion_Response::default())
  }
}

impl rosidl_runtime_rs::Message for CheckMotion_Response {
  type RmwMsg = super::srv::rmw::CheckMotion_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        status: msg.status,
        success: msg.success,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      status: msg.status,
      success: msg.success,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      status: msg.status,
      success: msg.success,
    }
  }
}


// Corresponds to dsr_msgs2__srv__ChangeOperationSpeed_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ChangeOperationSpeed_Request {
    /// operation speed: (1~100)
    pub speed: i8,

}



impl Default for ChangeOperationSpeed_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::ChangeOperationSpeed_Request::default())
  }
}

impl rosidl_runtime_rs::Message for ChangeOperationSpeed_Request {
  type RmwMsg = super::srv::rmw::ChangeOperationSpeed_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        speed: msg.speed,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      speed: msg.speed,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      speed: msg.speed,
    }
  }
}


// Corresponds to dsr_msgs2__srv__ChangeOperationSpeed_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ChangeOperationSpeed_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,

}



impl Default for ChangeOperationSpeed_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::ChangeOperationSpeed_Response::default())
  }
}

impl rosidl_runtime_rs::Message for ChangeOperationSpeed_Response {
  type RmwMsg = super::srv::rmw::ChangeOperationSpeed_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        success: msg.success,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      success: msg.success,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      success: msg.success,
    }
  }
}


// Corresponds to dsr_msgs2__srv__EnableAlterMotion_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct EnableAlterMotion_Request {
    /// Cycle time number
    pub n: i32,

    /// DR_DPOS(0) : accumulation amount, DR_DVEL(1) : increment amount
    pub mode: i8,

    /// DR_BASE(0), DR_TOOL(1), DR_WORLD(2), user coord(101~200)
    /// <ref is only available in M2.40 or later>
    pub ref_: i8,

    /// First value : limitation of position[mm], Second value : limitation of orientation[deg]
    pub limit_dpos: [f64; 2],

    /// First value : limitation of position[mm], Second value : limitation of orientation[deg]
    pub limit_dpos_per: [f64; 2],

}



impl Default for EnableAlterMotion_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::EnableAlterMotion_Request::default())
  }
}

impl rosidl_runtime_rs::Message for EnableAlterMotion_Request {
  type RmwMsg = super::srv::rmw::EnableAlterMotion_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        n: msg.n,
        mode: msg.mode,
        ref_: msg.ref_,
        limit_dpos: msg.limit_dpos,
        limit_dpos_per: msg.limit_dpos_per,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      n: msg.n,
      mode: msg.mode,
      ref_: msg.ref_,
        limit_dpos: msg.limit_dpos,
        limit_dpos_per: msg.limit_dpos_per,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      n: msg.n,
      mode: msg.mode,
      ref_: msg.ref_,
      limit_dpos: msg.limit_dpos,
      limit_dpos_per: msg.limit_dpos_per,
    }
  }
}


// Corresponds to dsr_msgs2__srv__EnableAlterMotion_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct EnableAlterMotion_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,

}



impl Default for EnableAlterMotion_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::EnableAlterMotion_Response::default())
  }
}

impl rosidl_runtime_rs::Message for EnableAlterMotion_Response {
  type RmwMsg = super::srv::rmw::EnableAlterMotion_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        success: msg.success,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      success: msg.success,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      success: msg.success,
    }
  }
}


// Corresponds to dsr_msgs2__srv__AlterMotion_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct AlterMotion_Request {
    /// position
    pub pos: [f64; 6],

}



impl Default for AlterMotion_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::AlterMotion_Request::default())
  }
}

impl rosidl_runtime_rs::Message for AlterMotion_Request {
  type RmwMsg = super::srv::rmw::AlterMotion_Request;

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


// Corresponds to dsr_msgs2__srv__AlterMotion_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct AlterMotion_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,

}



impl Default for AlterMotion_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::AlterMotion_Response::default())
  }
}

impl rosidl_runtime_rs::Message for AlterMotion_Response {
  type RmwMsg = super::srv::rmw::AlterMotion_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        success: msg.success,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      success: msg.success,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      success: msg.success,
    }
  }
}


// Corresponds to dsr_msgs2__srv__DisableAlterMotion_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct DisableAlterMotion_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub structure_needs_at_least_one_member: u8,

}



impl Default for DisableAlterMotion_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::DisableAlterMotion_Request::default())
  }
}

impl rosidl_runtime_rs::Message for DisableAlterMotion_Request {
  type RmwMsg = super::srv::rmw::DisableAlterMotion_Request;

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


// Corresponds to dsr_msgs2__srv__DisableAlterMotion_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct DisableAlterMotion_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,

}



impl Default for DisableAlterMotion_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::DisableAlterMotion_Response::default())
  }
}

impl rosidl_runtime_rs::Message for DisableAlterMotion_Response {
  type RmwMsg = super::srv::rmw::DisableAlterMotion_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        success: msg.success,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      success: msg.success,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      success: msg.success,
    }
  }
}


// Corresponds to dsr_msgs2__srv__SetSingularityHandling_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SetSingularityHandling_Request {
    /// DR_AVOID(0)     : Automatic avoidance mode
    /// DR_TASK_STOP(1) : Deceleration/ Warning/ Task termination
    /// DR_VAR_VEL(2)   : Variable velocity mode
    pub mode: i8,

}



impl Default for SetSingularityHandling_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::SetSingularityHandling_Request::default())
  }
}

impl rosidl_runtime_rs::Message for SetSingularityHandling_Request {
  type RmwMsg = super::srv::rmw::SetSingularityHandling_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        mode: msg.mode,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      mode: msg.mode,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      mode: msg.mode,
    }
  }
}


// Corresponds to dsr_msgs2__srv__SetSingularityHandling_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SetSingularityHandling_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,

}



impl Default for SetSingularityHandling_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::SetSingularityHandling_Response::default())
  }
}

impl rosidl_runtime_rs::Message for SetSingularityHandling_Response {
  type RmwMsg = super::srv::rmw::SetSingularityHandling_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        success: msg.success,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      success: msg.success,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      success: msg.success,
    }
  }
}


// Corresponds to dsr_msgs2__srv__SetSingularHandlingForce_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SetSingularHandlingForce_Request {
    /// DR_SINGULARITY_ERROR(0)  : Return error when force control/compliance control is used
    ///                            within singularity area
    /// DR_SINGULARITY_IGNORE(1) : Ignore error processing
    pub mode: i8,

}



impl Default for SetSingularHandlingForce_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::SetSingularHandlingForce_Request::default())
  }
}

impl rosidl_runtime_rs::Message for SetSingularHandlingForce_Request {
  type RmwMsg = super::srv::rmw::SetSingularHandlingForce_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        mode: msg.mode,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      mode: msg.mode,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      mode: msg.mode,
    }
  }
}


// Corresponds to dsr_msgs2__srv__SetSingularHandlingForce_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SetSingularHandlingForce_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,

}



impl Default for SetSingularHandlingForce_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::SetSingularHandlingForce_Response::default())
  }
}

impl rosidl_runtime_rs::Message for SetSingularHandlingForce_Response {
  type RmwMsg = super::srv::rmw::SetSingularHandlingForce_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        success: msg.success,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      success: msg.success,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      success: msg.success,
    }
  }
}


// Corresponds to dsr_msgs2__srv__GetControlMode_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetControlMode_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub structure_needs_at_least_one_member: u8,

}



impl Default for GetControlMode_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::GetControlMode_Request::default())
  }
}

impl rosidl_runtime_rs::Message for GetControlMode_Request {
  type RmwMsg = super::srv::rmw::GetControlMode_Request;

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


// Corresponds to dsr_msgs2__srv__GetControlMode_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetControlMode_Response {
    /// Control mode : Position control mode(3), Torque control mode(4)
    pub control_mode: i8,


    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,

}



impl Default for GetControlMode_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::GetControlMode_Response::default())
  }
}

impl rosidl_runtime_rs::Message for GetControlMode_Response {
  type RmwMsg = super::srv::rmw::GetControlMode_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        control_mode: msg.control_mode,
        success: msg.success,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      control_mode: msg.control_mode,
      success: msg.success,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      control_mode: msg.control_mode,
      success: msg.success,
    }
  }
}


// Corresponds to dsr_msgs2__srv__GetControlSpace_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetControlSpace_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub structure_needs_at_least_one_member: u8,

}



impl Default for GetControlSpace_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::GetControlSpace_Request::default())
  }
}

impl rosidl_runtime_rs::Message for GetControlSpace_Request {
  type RmwMsg = super::srv::rmw::GetControlSpace_Request;

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


// Corresponds to dsr_msgs2__srv__GetControlSpace_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetControlSpace_Response {
    /// Control mode : Joint space control(1), Task space control(2)
    pub space: i8,


    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,

}



impl Default for GetControlSpace_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::GetControlSpace_Response::default())
  }
}

impl rosidl_runtime_rs::Message for GetControlSpace_Response {
  type RmwMsg = super::srv::rmw::GetControlSpace_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        space: msg.space,
        success: msg.success,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      space: msg.space,
      success: msg.success,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      space: msg.space,
      success: msg.success,
    }
  }
}


// Corresponds to dsr_msgs2__srv__GetCurrentPosj_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetCurrentPosj_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub structure_needs_at_least_one_member: u8,

}



impl Default for GetCurrentPosj_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::GetCurrentPosj_Request::default())
  }
}

impl rosidl_runtime_rs::Message for GetCurrentPosj_Request {
  type RmwMsg = super::srv::rmw::GetCurrentPosj_Request;

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


// Corresponds to dsr_msgs2__srv__GetCurrentPosj_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetCurrentPosj_Response {
    /// joint pos(posj)
    pub pos: [f64; 6],


    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,

}



impl Default for GetCurrentPosj_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::GetCurrentPosj_Response::default())
  }
}

impl rosidl_runtime_rs::Message for GetCurrentPosj_Response {
  type RmwMsg = super::srv::rmw::GetCurrentPosj_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        pos: msg.pos,
        success: msg.success,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        pos: msg.pos,
      success: msg.success,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      pos: msg.pos,
      success: msg.success,
    }
  }
}


// Corresponds to dsr_msgs2__srv__GetDesiredPosj_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetDesiredPosj_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub structure_needs_at_least_one_member: u8,

}



impl Default for GetDesiredPosj_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::GetDesiredPosj_Request::default())
  }
}

impl rosidl_runtime_rs::Message for GetDesiredPosj_Request {
  type RmwMsg = super::srv::rmw::GetDesiredPosj_Request;

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


// Corresponds to dsr_msgs2__srv__GetDesiredPosj_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetDesiredPosj_Response {
    /// joint pos(posj)
    pub pos: [f64; 6],


    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,

}



impl Default for GetDesiredPosj_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::GetDesiredPosj_Response::default())
  }
}

impl rosidl_runtime_rs::Message for GetDesiredPosj_Response {
  type RmwMsg = super::srv::rmw::GetDesiredPosj_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        pos: msg.pos,
        success: msg.success,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        pos: msg.pos,
      success: msg.success,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      pos: msg.pos,
      success: msg.success,
    }
  }
}


// Corresponds to dsr_msgs2__srv__GetCurrentVelj_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetCurrentVelj_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub structure_needs_at_least_one_member: u8,

}



impl Default for GetCurrentVelj_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::GetCurrentVelj_Request::default())
  }
}

impl rosidl_runtime_rs::Message for GetCurrentVelj_Request {
  type RmwMsg = super::srv::rmw::GetCurrentVelj_Request;

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


// Corresponds to dsr_msgs2__srv__GetCurrentVelj_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetCurrentVelj_Response {
    /// joint speed
    pub joint_speed: [f64; 6],


    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,

}



impl Default for GetCurrentVelj_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::GetCurrentVelj_Response::default())
  }
}

impl rosidl_runtime_rs::Message for GetCurrentVelj_Response {
  type RmwMsg = super::srv::rmw::GetCurrentVelj_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        joint_speed: msg.joint_speed,
        success: msg.success,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        joint_speed: msg.joint_speed,
      success: msg.success,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      joint_speed: msg.joint_speed,
      success: msg.success,
    }
  }
}


// Corresponds to dsr_msgs2__srv__GetDesiredVelj_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetDesiredVelj_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub structure_needs_at_least_one_member: u8,

}



impl Default for GetDesiredVelj_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::GetDesiredVelj_Request::default())
  }
}

impl rosidl_runtime_rs::Message for GetDesiredVelj_Request {
  type RmwMsg = super::srv::rmw::GetDesiredVelj_Request;

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


// Corresponds to dsr_msgs2__srv__GetDesiredVelj_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetDesiredVelj_Response {
    /// Target joint velocity
    pub joint_vel: [f64; 6],


    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,

}



impl Default for GetDesiredVelj_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::GetDesiredVelj_Response::default())
  }
}

impl rosidl_runtime_rs::Message for GetDesiredVelj_Response {
  type RmwMsg = super::srv::rmw::GetDesiredVelj_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        joint_vel: msg.joint_vel,
        success: msg.success,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        joint_vel: msg.joint_vel,
      success: msg.success,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      joint_vel: msg.joint_vel,
      success: msg.success,
    }
  }
}


// Corresponds to dsr_msgs2__srv__GetCurrentPosx_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetCurrentPosx_Request {
    /// DR_BASE(0), DR_WORLD(2), user coord(101~200)
    /// <ref is only available in M2.40 or later>
    pub ref_: i8,

}



impl Default for GetCurrentPosx_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::GetCurrentPosx_Request::default())
  }
}

impl rosidl_runtime_rs::Message for GetCurrentPosx_Request {
  type RmwMsg = super::srv::rmw::GetCurrentPosx_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        ref_: msg.ref_,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      ref_: msg.ref_,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      ref_: msg.ref_,
    }
  }
}


// Corresponds to dsr_msgs2__srv__GetCurrentPosx_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetCurrentPosx_Response {
    /// task pos = task_pos_info[0][0:5], solution sapce = task_pos_info[0][6]
    pub task_pos_info: Vec<std_msgs::msg::Float64MultiArray>,


    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,

}



impl Default for GetCurrentPosx_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::GetCurrentPosx_Response::default())
  }
}

impl rosidl_runtime_rs::Message for GetCurrentPosx_Response {
  type RmwMsg = super::srv::rmw::GetCurrentPosx_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        task_pos_info: msg.task_pos_info
          .into_iter()
          .map(|elem| std_msgs::msg::Float64MultiArray::into_rmw_message(std::borrow::Cow::Owned(elem)).into_owned())
          .collect(),
        success: msg.success,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        task_pos_info: msg.task_pos_info
          .iter()
          .map(|elem| std_msgs::msg::Float64MultiArray::into_rmw_message(std::borrow::Cow::Borrowed(elem)).into_owned())
          .collect(),
      success: msg.success,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      task_pos_info: msg.task_pos_info
          .into_iter()
          .map(std_msgs::msg::Float64MultiArray::from_rmw_message)
          .collect(),
      success: msg.success,
    }
  }
}


// Corresponds to dsr_msgs2__srv__GetCurrentToolFlangePosx_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetCurrentToolFlangePosx_Request {
    /// DR_BASE(0), DR_WORLD(2)
    pub ref_: i8,

}



impl Default for GetCurrentToolFlangePosx_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::GetCurrentToolFlangePosx_Request::default())
  }
}

impl rosidl_runtime_rs::Message for GetCurrentToolFlangePosx_Request {
  type RmwMsg = super::srv::rmw::GetCurrentToolFlangePosx_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        ref_: msg.ref_,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      ref_: msg.ref_,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      ref_: msg.ref_,
    }
  }
}


// Corresponds to dsr_msgs2__srv__GetCurrentToolFlangePosx_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetCurrentToolFlangePosx_Response {
    /// Pose of tool flange(posx)
    pub pos: [f64; 6],


    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,

}



impl Default for GetCurrentToolFlangePosx_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::GetCurrentToolFlangePosx_Response::default())
  }
}

impl rosidl_runtime_rs::Message for GetCurrentToolFlangePosx_Response {
  type RmwMsg = super::srv::rmw::GetCurrentToolFlangePosx_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        pos: msg.pos,
        success: msg.success,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        pos: msg.pos,
      success: msg.success,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      pos: msg.pos,
      success: msg.success,
    }
  }
}


// Corresponds to dsr_msgs2__srv__GetCurrentVelx_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetCurrentVelx_Request {
    /// DR_BASE(0), DR_WORLD(2)
    pub ref_: i8,

}



impl Default for GetCurrentVelx_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::GetCurrentVelx_Request::default())
  }
}

impl rosidl_runtime_rs::Message for GetCurrentVelx_Request {
  type RmwMsg = super::srv::rmw::GetCurrentVelx_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        ref_: msg.ref_,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      ref_: msg.ref_,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      ref_: msg.ref_,
    }
  }
}


// Corresponds to dsr_msgs2__srv__GetCurrentVelx_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetCurrentVelx_Response {
    /// Tool velocity
    pub vel: [f64; 6],


    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,

}



impl Default for GetCurrentVelx_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::GetCurrentVelx_Response::default())
  }
}

impl rosidl_runtime_rs::Message for GetCurrentVelx_Response {
  type RmwMsg = super::srv::rmw::GetCurrentVelx_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        vel: msg.vel,
        success: msg.success,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        vel: msg.vel,
      success: msg.success,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      vel: msg.vel,
      success: msg.success,
    }
  }
}


// Corresponds to dsr_msgs2__srv__GetDesiredPosx_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetDesiredPosx_Request {
    /// = 0   # DR_BASE(0), DR_WORLD(2), user coord(101~200)
    ///  <ref is only available in M2.40 or later>
    pub ref_: i8,

}



impl Default for GetDesiredPosx_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::GetDesiredPosx_Request::default())
  }
}

impl rosidl_runtime_rs::Message for GetDesiredPosx_Request {
  type RmwMsg = super::srv::rmw::GetDesiredPosx_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        ref_: msg.ref_,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      ref_: msg.ref_,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      ref_: msg.ref_,
    }
  }
}


// Corresponds to dsr_msgs2__srv__GetDesiredPosx_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetDesiredPosx_Response {
    /// task pos(posx)
    pub pos: [f64; 6],


    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,

}



impl Default for GetDesiredPosx_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::GetDesiredPosx_Response::default())
  }
}

impl rosidl_runtime_rs::Message for GetDesiredPosx_Response {
  type RmwMsg = super::srv::rmw::GetDesiredPosx_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        pos: msg.pos,
        success: msg.success,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        pos: msg.pos,
      success: msg.success,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      pos: msg.pos,
      success: msg.success,
    }
  }
}


// Corresponds to dsr_msgs2__srv__GetDesiredVelx_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetDesiredVelx_Request {
    /// DR_BASE(0), DR_WORLD(2)
    pub ref_: i8,

}



impl Default for GetDesiredVelx_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::GetDesiredVelx_Request::default())
  }
}

impl rosidl_runtime_rs::Message for GetDesiredVelx_Request {
  type RmwMsg = super::srv::rmw::GetDesiredVelx_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        ref_: msg.ref_,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      ref_: msg.ref_,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      ref_: msg.ref_,
    }
  }
}


// Corresponds to dsr_msgs2__srv__GetDesiredVelx_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetDesiredVelx_Response {
    /// Tool velocity
    pub vel: [f64; 6],


    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,

}



impl Default for GetDesiredVelx_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::GetDesiredVelx_Response::default())
  }
}

impl rosidl_runtime_rs::Message for GetDesiredVelx_Response {
  type RmwMsg = super::srv::rmw::GetDesiredVelx_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        vel: msg.vel,
        success: msg.success,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        vel: msg.vel,
      success: msg.success,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      vel: msg.vel,
      success: msg.success,
    }
  }
}


// Corresponds to dsr_msgs2__srv__GetCurrentSolutionSpace_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetCurrentSolutionSpace_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub structure_needs_at_least_one_member: u8,

}



impl Default for GetCurrentSolutionSpace_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::GetCurrentSolutionSpace_Request::default())
  }
}

impl rosidl_runtime_rs::Message for GetCurrentSolutionSpace_Request {
  type RmwMsg = super::srv::rmw::GetCurrentSolutionSpace_Request;

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


// Corresponds to dsr_msgs2__srv__GetCurrentSolutionSpace_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetCurrentSolutionSpace_Response {
    /// solution space : 0 ~ 7
    pub sol_space: i8,


    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,

}



impl Default for GetCurrentSolutionSpace_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::GetCurrentSolutionSpace_Response::default())
  }
}

impl rosidl_runtime_rs::Message for GetCurrentSolutionSpace_Response {
  type RmwMsg = super::srv::rmw::GetCurrentSolutionSpace_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        sol_space: msg.sol_space,
        success: msg.success,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      sol_space: msg.sol_space,
      success: msg.success,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      sol_space: msg.sol_space,
      success: msg.success,
    }
  }
}


// Corresponds to dsr_msgs2__srv__GetCurrentRotm_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetCurrentRotm_Request {
    /// DR_BASE(0), DR_WORLD(2)
    pub ref_: i8,

}



impl Default for GetCurrentRotm_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::GetCurrentRotm_Request::default())
  }
}

impl rosidl_runtime_rs::Message for GetCurrentRotm_Request {
  type RmwMsg = super::srv::rmw::GetCurrentRotm_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        ref_: msg.ref_,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      ref_: msg.ref_,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      ref_: msg.ref_,
    }
  }
}


// Corresponds to dsr_msgs2__srv__GetCurrentRotm_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetCurrentRotm_Response {
    /// target[3][3] Rotation matrix
    pub rot_matrix: Vec<std_msgs::msg::Float64MultiArray>,


    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,

}



impl Default for GetCurrentRotm_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::GetCurrentRotm_Response::default())
  }
}

impl rosidl_runtime_rs::Message for GetCurrentRotm_Response {
  type RmwMsg = super::srv::rmw::GetCurrentRotm_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        rot_matrix: msg.rot_matrix
          .into_iter()
          .map(|elem| std_msgs::msg::Float64MultiArray::into_rmw_message(std::borrow::Cow::Owned(elem)).into_owned())
          .collect(),
        success: msg.success,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        rot_matrix: msg.rot_matrix
          .iter()
          .map(|elem| std_msgs::msg::Float64MultiArray::into_rmw_message(std::borrow::Cow::Borrowed(elem)).into_owned())
          .collect(),
      success: msg.success,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      rot_matrix: msg.rot_matrix
          .into_iter()
          .map(std_msgs::msg::Float64MultiArray::from_rmw_message)
          .collect(),
      success: msg.success,
    }
  }
}


// Corresponds to dsr_msgs2__srv__GetJointTorque_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetJointTorque_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub structure_needs_at_least_one_member: u8,

}



impl Default for GetJointTorque_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::GetJointTorque_Request::default())
  }
}

impl rosidl_runtime_rs::Message for GetJointTorque_Request {
  type RmwMsg = super::srv::rmw::GetJointTorque_Request;

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


// Corresponds to dsr_msgs2__srv__GetJointTorque_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetJointTorque_Response {
    /// value of JTS(Joint Torque Sensor)
    pub jts: [f64; 6],


    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,

}



impl Default for GetJointTorque_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::GetJointTorque_Response::default())
  }
}

impl rosidl_runtime_rs::Message for GetJointTorque_Response {
  type RmwMsg = super::srv::rmw::GetJointTorque_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        jts: msg.jts,
        success: msg.success,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        jts: msg.jts,
      success: msg.success,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      jts: msg.jts,
      success: msg.success,
    }
  }
}


// Corresponds to dsr_msgs2__srv__GetExternalTorque_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetExternalTorque_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub structure_needs_at_least_one_member: u8,

}



impl Default for GetExternalTorque_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::GetExternalTorque_Request::default())
  }
}

impl rosidl_runtime_rs::Message for GetExternalTorque_Request {
  type RmwMsg = super::srv::rmw::GetExternalTorque_Request;

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


// Corresponds to dsr_msgs2__srv__GetExternalTorque_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetExternalTorque_Response {
    /// Torque value generated by an external force
    pub ext_torque: [f64; 6],


    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,

}



impl Default for GetExternalTorque_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::GetExternalTorque_Response::default())
  }
}

impl rosidl_runtime_rs::Message for GetExternalTorque_Response {
  type RmwMsg = super::srv::rmw::GetExternalTorque_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        ext_torque: msg.ext_torque,
        success: msg.success,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        ext_torque: msg.ext_torque,
      success: msg.success,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      ext_torque: msg.ext_torque,
      success: msg.success,
    }
  }
}


// Corresponds to dsr_msgs2__srv__GetToolForce_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetToolForce_Request {
    /// DR_BASE(0), DR_TOOL(1), DR_WORLD(2)
    pub ref_: i8,

}



impl Default for GetToolForce_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::GetToolForce_Request::default())
  }
}

impl rosidl_runtime_rs::Message for GetToolForce_Request {
  type RmwMsg = super::srv::rmw::GetToolForce_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        ref_: msg.ref_,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      ref_: msg.ref_,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      ref_: msg.ref_,
    }
  }
}


// Corresponds to dsr_msgs2__srv__GetToolForce_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetToolForce_Response {
    /// External force applied to the tool
    pub tool_force: [f64; 6],


    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,

}



impl Default for GetToolForce_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::GetToolForce_Response::default())
  }
}

impl rosidl_runtime_rs::Message for GetToolForce_Response {
  type RmwMsg = super::srv::rmw::GetToolForce_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        tool_force: msg.tool_force,
        success: msg.success,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        tool_force: msg.tool_force,
      success: msg.success,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      tool_force: msg.tool_force,
      success: msg.success,
    }
  }
}


// Corresponds to dsr_msgs2__srv__GetSolutionSpace_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetSolutionSpace_Request {
    /// joint angle list
    pub pos: [f64; 6],

}



impl Default for GetSolutionSpace_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::GetSolutionSpace_Request::default())
  }
}

impl rosidl_runtime_rs::Message for GetSolutionSpace_Request {
  type RmwMsg = super::srv::rmw::GetSolutionSpace_Request;

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


// Corresponds to dsr_msgs2__srv__GetSolutionSpace_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetSolutionSpace_Response {
    /// solution space : 0 ~ 7
    pub sol_space: i8,


    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,

}



impl Default for GetSolutionSpace_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::GetSolutionSpace_Response::default())
  }
}

impl rosidl_runtime_rs::Message for GetSolutionSpace_Response {
  type RmwMsg = super::srv::rmw::GetSolutionSpace_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        sol_space: msg.sol_space,
        success: msg.success,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      sol_space: msg.sol_space,
      success: msg.success,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      sol_space: msg.sol_space,
      success: msg.success,
    }
  }
}


// Corresponds to dsr_msgs2__srv__GetOrientationError_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetOrientationError_Request {
    /// task pos(posx)
    pub xd: [f64; 6],

    /// task pos(posx)
    pub xc: [f64; 6],

    /// DR_AXIS_X(0), DR_AXIS_Y(1), DR_AXIS_Z(2)
    pub axis: i8,

}



impl Default for GetOrientationError_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::GetOrientationError_Request::default())
  }
}

impl rosidl_runtime_rs::Message for GetOrientationError_Request {
  type RmwMsg = super::srv::rmw::GetOrientationError_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        xd: msg.xd,
        xc: msg.xc,
        axis: msg.axis,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        xd: msg.xd,
        xc: msg.xc,
      axis: msg.axis,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      xd: msg.xd,
      xc: msg.xc,
      axis: msg.axis,
    }
  }
}


// Corresponds to dsr_msgs2__srv__GetOrientationError_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetOrientationError_Response {
    /// orientation error
    pub ori_error: f32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,

}



impl Default for GetOrientationError_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::GetOrientationError_Response::default())
  }
}

impl rosidl_runtime_rs::Message for GetOrientationError_Response {
  type RmwMsg = super::srv::rmw::GetOrientationError_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        ori_error: msg.ori_error,
        success: msg.success,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      ori_error: msg.ori_error,
      success: msg.success,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      ori_error: msg.ori_error,
      success: msg.success,
    }
  }
}


// Corresponds to dsr_msgs2__srv__ParallelAxis1_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ParallelAxis1_Request {
    /// task pos(posx)
    pub x1: [f64; 6],

    /// task pos(posx)
    pub x2: [f64; 6],

    /// task pos(posx)
    pub x3: [f64; 6],

    /// DR_AXIS_X(0), DR_AXIS_Y(1), DR_AXIS_Z(2)
    pub axis: i8,

    /// = 0   # DR_BASE(0), DR_WORLD(2), user coord(101~200)
    ///  <ref is only available in M2.40 or later>
    pub ref_: i8,

}



impl Default for ParallelAxis1_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::ParallelAxis1_Request::default())
  }
}

impl rosidl_runtime_rs::Message for ParallelAxis1_Request {
  type RmwMsg = super::srv::rmw::ParallelAxis1_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        x1: msg.x1,
        x2: msg.x2,
        x3: msg.x3,
        axis: msg.axis,
        ref_: msg.ref_,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        x1: msg.x1,
        x2: msg.x2,
        x3: msg.x3,
      axis: msg.axis,
      ref_: msg.ref_,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      x1: msg.x1,
      x2: msg.x2,
      x3: msg.x3,
      axis: msg.axis,
      ref_: msg.ref_,
    }
  }
}


// Corresponds to dsr_msgs2__srv__ParallelAxis1_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ParallelAxis1_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,

}



impl Default for ParallelAxis1_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::ParallelAxis1_Response::default())
  }
}

impl rosidl_runtime_rs::Message for ParallelAxis1_Response {
  type RmwMsg = super::srv::rmw::ParallelAxis1_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        success: msg.success,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      success: msg.success,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      success: msg.success,
    }
  }
}


// Corresponds to dsr_msgs2__srv__ParallelAxis2_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ParallelAxis2_Request {
    /// vector
    pub vect: [f64; 3],

    /// DR_AXIS_X(0), DR_AXIS_Y(1), DR_AXIS_Z(2)
    pub axis: i8,

    /// = 0   # DR_BASE(0), DR_WORLD(2), user coord(101~200)
    ///  <ref is only available in M2.40 or later>
    pub ref_: i8,

}



impl Default for ParallelAxis2_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::ParallelAxis2_Request::default())
  }
}

impl rosidl_runtime_rs::Message for ParallelAxis2_Request {
  type RmwMsg = super::srv::rmw::ParallelAxis2_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        vect: msg.vect,
        axis: msg.axis,
        ref_: msg.ref_,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        vect: msg.vect,
      axis: msg.axis,
      ref_: msg.ref_,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      vect: msg.vect,
      axis: msg.axis,
      ref_: msg.ref_,
    }
  }
}


// Corresponds to dsr_msgs2__srv__ParallelAxis2_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ParallelAxis2_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,

}



impl Default for ParallelAxis2_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::ParallelAxis2_Response::default())
  }
}

impl rosidl_runtime_rs::Message for ParallelAxis2_Response {
  type RmwMsg = super::srv::rmw::ParallelAxis2_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        success: msg.success,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      success: msg.success,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      success: msg.success,
    }
  }
}


// Corresponds to dsr_msgs2__srv__AlignAxis1_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct AlignAxis1_Request {
    /// task pos(posx)
    pub x1: [f64; 6],

    /// task pos(posx)
    pub x2: [f64; 6],

    /// task pos(posx)
    pub x3: [f64; 6],

    /// source vector
    pub source_vect: [f64; 3],

    /// DR_AXIS_X(0), DR_AXIS_Y(1), DR_AXIS_Z(2)
    pub axis: i8,

    /// DR_BASE(0), DR_WORLD(2), user coord(101~200)
    /// <ref is only available in M2.40 or later>
    pub ref_: i8,

}



impl Default for AlignAxis1_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::AlignAxis1_Request::default())
  }
}

impl rosidl_runtime_rs::Message for AlignAxis1_Request {
  type RmwMsg = super::srv::rmw::AlignAxis1_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        x1: msg.x1,
        x2: msg.x2,
        x3: msg.x3,
        source_vect: msg.source_vect,
        axis: msg.axis,
        ref_: msg.ref_,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        x1: msg.x1,
        x2: msg.x2,
        x3: msg.x3,
        source_vect: msg.source_vect,
      axis: msg.axis,
      ref_: msg.ref_,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      x1: msg.x1,
      x2: msg.x2,
      x3: msg.x3,
      source_vect: msg.source_vect,
      axis: msg.axis,
      ref_: msg.ref_,
    }
  }
}


// Corresponds to dsr_msgs2__srv__AlignAxis1_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct AlignAxis1_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,

}



impl Default for AlignAxis1_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::AlignAxis1_Response::default())
  }
}

impl rosidl_runtime_rs::Message for AlignAxis1_Response {
  type RmwMsg = super::srv::rmw::AlignAxis1_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        success: msg.success,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      success: msg.success,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      success: msg.success,
    }
  }
}


// Corresponds to dsr_msgs2__srv__AlignAxis2_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct AlignAxis2_Request {
    /// target vector
    pub target_vect: [f64; 3],

    /// source vector
    pub source_vect: [f64; 3],

    /// DR_AXIS_X(0), DR_AXIS_Y(1), DR_AXIS_Z(2)
    pub axis: i8,

    /// DR_BASE(0), DR_WORLD(2), user coord(101~200)
    /// <ref is only available in M2.40 or later>
    pub ref_: i8,

}



impl Default for AlignAxis2_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::AlignAxis2_Request::default())
  }
}

impl rosidl_runtime_rs::Message for AlignAxis2_Request {
  type RmwMsg = super::srv::rmw::AlignAxis2_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        target_vect: msg.target_vect,
        source_vect: msg.source_vect,
        axis: msg.axis,
        ref_: msg.ref_,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        target_vect: msg.target_vect,
        source_vect: msg.source_vect,
      axis: msg.axis,
      ref_: msg.ref_,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      target_vect: msg.target_vect,
      source_vect: msg.source_vect,
      axis: msg.axis,
      ref_: msg.ref_,
    }
  }
}


// Corresponds to dsr_msgs2__srv__AlignAxis2_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct AlignAxis2_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,

}



impl Default for AlignAxis2_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::AlignAxis2_Response::default())
  }
}

impl rosidl_runtime_rs::Message for AlignAxis2_Response {
  type RmwMsg = super::srv::rmw::AlignAxis2_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        success: msg.success,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      success: msg.success,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      success: msg.success,
    }
  }
}


// Corresponds to dsr_msgs2__srv__IsDoneBoltTightening_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct IsDoneBoltTightening_Request {
    /// Target torque
    pub m: f64,

    /// Monitoring duration
    pub timeout: f64,

    /// DR_AXIS_X(0), DR_AXIS_Y(1), DR_AXIS_Z(2)
    pub axis: i8,

}



impl Default for IsDoneBoltTightening_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::IsDoneBoltTightening_Request::default())
  }
}

impl rosidl_runtime_rs::Message for IsDoneBoltTightening_Request {
  type RmwMsg = super::srv::rmw::IsDoneBoltTightening_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        m: msg.m,
        timeout: msg.timeout,
        axis: msg.axis,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      m: msg.m,
      timeout: msg.timeout,
      axis: msg.axis,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      m: msg.m,
      timeout: msg.timeout,
      axis: msg.axis,
    }
  }
}


// Corresponds to dsr_msgs2__srv__IsDoneBoltTightening_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct IsDoneBoltTightening_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,

}



impl Default for IsDoneBoltTightening_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::IsDoneBoltTightening_Response::default())
  }
}

impl rosidl_runtime_rs::Message for IsDoneBoltTightening_Response {
  type RmwMsg = super::srv::rmw::IsDoneBoltTightening_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        success: msg.success,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      success: msg.success,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      success: msg.success,
    }
  }
}


// Corresponds to dsr_msgs2__srv__ReleaseComplianceCtrl_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ReleaseComplianceCtrl_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub structure_needs_at_least_one_member: u8,

}



impl Default for ReleaseComplianceCtrl_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::ReleaseComplianceCtrl_Request::default())
  }
}

impl rosidl_runtime_rs::Message for ReleaseComplianceCtrl_Request {
  type RmwMsg = super::srv::rmw::ReleaseComplianceCtrl_Request;

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


// Corresponds to dsr_msgs2__srv__ReleaseComplianceCtrl_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ReleaseComplianceCtrl_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,

}



impl Default for ReleaseComplianceCtrl_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::ReleaseComplianceCtrl_Response::default())
  }
}

impl rosidl_runtime_rs::Message for ReleaseComplianceCtrl_Response {
  type RmwMsg = super::srv::rmw::ReleaseComplianceCtrl_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        success: msg.success,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      success: msg.success,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      success: msg.success,
    }
  }
}


// Corresponds to dsr_msgs2__srv__TaskComplianceCtrl_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct TaskComplianceCtrl_Request {
    /// Three translational stiffnesses + Three rotational stiffnesses
    /// default  [3000, 3000, 3000, 200, 200, 200]
    pub stx: [f64; 6],

    /// the preset reference coordinate system.
    pub ref_: i8,

    /// Stiffness varying time, Linear transition during the specified time
    pub time: f64,

}



impl Default for TaskComplianceCtrl_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::TaskComplianceCtrl_Request::default())
  }
}

impl rosidl_runtime_rs::Message for TaskComplianceCtrl_Request {
  type RmwMsg = super::srv::rmw::TaskComplianceCtrl_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        stx: msg.stx,
        ref_: msg.ref_,
        time: msg.time,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        stx: msg.stx,
      ref_: msg.ref_,
      time: msg.time,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      stx: msg.stx,
      ref_: msg.ref_,
      time: msg.time,
    }
  }
}


// Corresponds to dsr_msgs2__srv__TaskComplianceCtrl_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct TaskComplianceCtrl_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,

}



impl Default for TaskComplianceCtrl_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::TaskComplianceCtrl_Response::default())
  }
}

impl rosidl_runtime_rs::Message for TaskComplianceCtrl_Response {
  type RmwMsg = super::srv::rmw::TaskComplianceCtrl_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        success: msg.success,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      success: msg.success,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      success: msg.success,
    }
  }
}


// Corresponds to dsr_msgs2__srv__SetStiffnessx_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SetStiffnessx_Request {
    /// default[500, 500, 500, 100, 100, 100], Three translational stiffnesses + Three rotational stiffnesses
    pub stx: [f64; 6],

    /// the preset reference coordinate system.
    pub ref_: i8,

    /// Stiffness varying time(0 ~ 1.0), Linear transition during the specified time
    pub time: f64,

}



impl Default for SetStiffnessx_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::SetStiffnessx_Request::default())
  }
}

impl rosidl_runtime_rs::Message for SetStiffnessx_Request {
  type RmwMsg = super::srv::rmw::SetStiffnessx_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        stx: msg.stx,
        ref_: msg.ref_,
        time: msg.time,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        stx: msg.stx,
      ref_: msg.ref_,
      time: msg.time,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      stx: msg.stx,
      ref_: msg.ref_,
      time: msg.time,
    }
  }
}


// Corresponds to dsr_msgs2__srv__SetStiffnessx_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SetStiffnessx_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,

}



impl Default for SetStiffnessx_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::SetStiffnessx_Response::default())
  }
}

impl rosidl_runtime_rs::Message for SetStiffnessx_Response {
  type RmwMsg = super::srv::rmw::SetStiffnessx_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        success: msg.success,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      success: msg.success,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      success: msg.success,
    }
  }
}


// Corresponds to dsr_msgs2__srv__CalcCoord_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct CalcCoord_Request {
    /// input_pos_cnt
    pub input_pos_cnt: i8,

    /// task pos(posx)
    pub x1: [f64; 6],

    /// task pos(posx)
    pub x2: [f64; 6],

    /// task pos(posx)
    pub x3: [f64; 6],

    /// task pos(posx)
    pub x4: [f64; 6],

    /// DR_BASE(0), DR_WORLD(2)
    pub ref_: i8,

    /// input mode(only valid when the number of input poses is 2)
    /// 0: defining z-axis based on the current Tool-z direction
    /// 1: defining z-axis based on the z direction of x1
    pub mod_: i8,

}



impl Default for CalcCoord_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::CalcCoord_Request::default())
  }
}

impl rosidl_runtime_rs::Message for CalcCoord_Request {
  type RmwMsg = super::srv::rmw::CalcCoord_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        input_pos_cnt: msg.input_pos_cnt,
        x1: msg.x1,
        x2: msg.x2,
        x3: msg.x3,
        x4: msg.x4,
        ref_: msg.ref_,
        mod_: msg.mod_,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      input_pos_cnt: msg.input_pos_cnt,
        x1: msg.x1,
        x2: msg.x2,
        x3: msg.x3,
        x4: msg.x4,
      ref_: msg.ref_,
      mod_: msg.mod_,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      input_pos_cnt: msg.input_pos_cnt,
      x1: msg.x1,
      x2: msg.x2,
      x3: msg.x3,
      x4: msg.x4,
      ref_: msg.ref_,
      mod_: msg.mod_,
    }
  }
}


// Corresponds to dsr_msgs2__srv__CalcCoord_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct CalcCoord_Response {
    /// task pos(posx)
    pub conv_posx: [f64; 6],


    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,

}



impl Default for CalcCoord_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::CalcCoord_Response::default())
  }
}

impl rosidl_runtime_rs::Message for CalcCoord_Response {
  type RmwMsg = super::srv::rmw::CalcCoord_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        conv_posx: msg.conv_posx,
        success: msg.success,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        conv_posx: msg.conv_posx,
      success: msg.success,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      conv_posx: msg.conv_posx,
      success: msg.success,
    }
  }
}


// Corresponds to dsr_msgs2__srv__SetUserCartCoord1_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SetUserCartCoord1_Request {
    /// task pos(posx)
    pub pos: [f64; 6],

    /// DR_BASE(0), DR_WORLD(2)
    /// <ref is only available in M2.40 or later>
    pub ref_: i8,

}



impl Default for SetUserCartCoord1_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::SetUserCartCoord1_Request::default())
  }
}

impl rosidl_runtime_rs::Message for SetUserCartCoord1_Request {
  type RmwMsg = super::srv::rmw::SetUserCartCoord1_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        pos: msg.pos,
        ref_: msg.ref_,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        pos: msg.pos,
      ref_: msg.ref_,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      pos: msg.pos,
      ref_: msg.ref_,
    }
  }
}


// Corresponds to dsr_msgs2__srv__SetUserCartCoord1_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SetUserCartCoord1_Response {
    /// set user coord (101~120) or fail(-1)
    pub id: i8,


    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,

}



impl Default for SetUserCartCoord1_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::SetUserCartCoord1_Response::default())
  }
}

impl rosidl_runtime_rs::Message for SetUserCartCoord1_Response {
  type RmwMsg = super::srv::rmw::SetUserCartCoord1_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        id: msg.id,
        success: msg.success,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      id: msg.id,
      success: msg.success,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      id: msg.id,
      success: msg.success,
    }
  }
}


// Corresponds to dsr_msgs2__srv__SetUserCartCoord2_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SetUserCartCoord2_Request {
    /// task pos(posx)
    pub x1: [f64; 6],

    /// task pos(posx)
    pub x2: [f64; 6],

    /// task pos(posx)
    pub x3: [f64; 6],

    /// pos(posx)
    pub pos: [f64; 6],

    /// DR_BASE(0), DR_WORLD(2)
    /// <ref is only available in M2.40 or later>
    pub ref_: i8,

}



impl Default for SetUserCartCoord2_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::SetUserCartCoord2_Request::default())
  }
}

impl rosidl_runtime_rs::Message for SetUserCartCoord2_Request {
  type RmwMsg = super::srv::rmw::SetUserCartCoord2_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        x1: msg.x1,
        x2: msg.x2,
        x3: msg.x3,
        pos: msg.pos,
        ref_: msg.ref_,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        x1: msg.x1,
        x2: msg.x2,
        x3: msg.x3,
        pos: msg.pos,
      ref_: msg.ref_,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      x1: msg.x1,
      x2: msg.x2,
      x3: msg.x3,
      pos: msg.pos,
      ref_: msg.ref_,
    }
  }
}


// Corresponds to dsr_msgs2__srv__SetUserCartCoord2_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SetUserCartCoord2_Response {
    /// set user coord (101~200) or fail(-1)
    pub id: i8,


    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,

}



impl Default for SetUserCartCoord2_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::SetUserCartCoord2_Response::default())
  }
}

impl rosidl_runtime_rs::Message for SetUserCartCoord2_Response {
  type RmwMsg = super::srv::rmw::SetUserCartCoord2_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        id: msg.id,
        success: msg.success,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      id: msg.id,
      success: msg.success,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      id: msg.id,
      success: msg.success,
    }
  }
}


// Corresponds to dsr_msgs2__srv__SetUserCartCoord3_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SetUserCartCoord3_Request {
    /// X-axis unit vector
    pub u1: [f64; 3],

    /// Y-axis unit vector
    pub v1: [f64; 3],

    /// task pos(posx)
    pub pos: [f64; 6],

    /// DR_BASE(0), DR_WORLD(2)
    /// <ref is only available in M2.40 or later>
    pub ref_: i8,

}



impl Default for SetUserCartCoord3_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::SetUserCartCoord3_Request::default())
  }
}

impl rosidl_runtime_rs::Message for SetUserCartCoord3_Request {
  type RmwMsg = super::srv::rmw::SetUserCartCoord3_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        u1: msg.u1,
        v1: msg.v1,
        pos: msg.pos,
        ref_: msg.ref_,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        u1: msg.u1,
        v1: msg.v1,
        pos: msg.pos,
      ref_: msg.ref_,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      u1: msg.u1,
      v1: msg.v1,
      pos: msg.pos,
      ref_: msg.ref_,
    }
  }
}


// Corresponds to dsr_msgs2__srv__SetUserCartCoord3_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SetUserCartCoord3_Response {
    /// set user coord (101~120) or fail(-1)
    pub id: i8,


    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,

}



impl Default for SetUserCartCoord3_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::SetUserCartCoord3_Response::default())
  }
}

impl rosidl_runtime_rs::Message for SetUserCartCoord3_Response {
  type RmwMsg = super::srv::rmw::SetUserCartCoord3_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        id: msg.id,
        success: msg.success,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      id: msg.id,
      success: msg.success,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      id: msg.id,
      success: msg.success,
    }
  }
}


// Corresponds to dsr_msgs2__srv__OverwriteUserCartCoord_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct OverwriteUserCartCoord_Request {
    /// ID of user coord
    pub id: i8,

    /// task pos(posx)
    pub pos: [f64; 6],

    /// = 0   # DR_BASE(0), DR_WORLD(2)
    pub ref_: i8,

}



impl Default for OverwriteUserCartCoord_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::OverwriteUserCartCoord_Request::default())
  }
}

impl rosidl_runtime_rs::Message for OverwriteUserCartCoord_Request {
  type RmwMsg = super::srv::rmw::OverwriteUserCartCoord_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        id: msg.id,
        pos: msg.pos,
        ref_: msg.ref_,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      id: msg.id,
        pos: msg.pos,
      ref_: msg.ref_,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      id: msg.id,
      pos: msg.pos,
      ref_: msg.ref_,
    }
  }
}


// Corresponds to dsr_msgs2__srv__OverwriteUserCartCoord_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct OverwriteUserCartCoord_Response {
    /// Successful coordinate setting, Set user coordinate ID (101 - 200)
    /// (-1) Failed coordinate setting
    pub id: i8,


    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,

}



impl Default for OverwriteUserCartCoord_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::OverwriteUserCartCoord_Response::default())
  }
}

impl rosidl_runtime_rs::Message for OverwriteUserCartCoord_Response {
  type RmwMsg = super::srv::rmw::OverwriteUserCartCoord_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        id: msg.id,
        success: msg.success,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      id: msg.id,
      success: msg.success,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      id: msg.id,
      success: msg.success,
    }
  }
}


// Corresponds to dsr_msgs2__srv__GetUserCartCoord_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetUserCartCoord_Request {
    /// ID of user coord
    pub id: i8,

}



impl Default for GetUserCartCoord_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::GetUserCartCoord_Request::default())
  }
}

impl rosidl_runtime_rs::Message for GetUserCartCoord_Request {
  type RmwMsg = super::srv::rmw::GetUserCartCoord_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        id: msg.id,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      id: msg.id,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      id: msg.id,
    }
  }
}


// Corresponds to dsr_msgs2__srv__GetUserCartCoord_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetUserCartCoord_Response {
    /// task pos(posx)
    pub conv_posx: [f64; 6],

    /// Reference coordinate of the coordinate to get
    pub ref_: i8,


    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,

}



impl Default for GetUserCartCoord_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::GetUserCartCoord_Response::default())
  }
}

impl rosidl_runtime_rs::Message for GetUserCartCoord_Response {
  type RmwMsg = super::srv::rmw::GetUserCartCoord_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        conv_posx: msg.conv_posx,
        ref_: msg.ref_,
        success: msg.success,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        conv_posx: msg.conv_posx,
      ref_: msg.ref_,
      success: msg.success,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      conv_posx: msg.conv_posx,
      ref_: msg.ref_,
      success: msg.success,
    }
  }
}


// Corresponds to dsr_msgs2__srv__SetDesiredForce_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SetDesiredForce_Request {
    /// Three translational target forces + Three rotational target moments
    pub fd: [f64; 6],

    /// Force control in the corresponding direction if 1, Compliance control in the corresponding direction if 0
    pub dir: [i8; 6],

    /// Reference coordinate of the coordinate to get
    pub ref_: i8,

    /// 0          # Transition time of target force to take effect (0 ~ 1.0 sec)
    pub time: f64,

    /// DR_FC_MOD_ABS(0): force control with absolute value,
    /// DR_FC_MOD_REL(1): force control with relative value to initial state (the instance when this function is called)
    pub mod_: i8,

}



impl Default for SetDesiredForce_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::SetDesiredForce_Request::default())
  }
}

impl rosidl_runtime_rs::Message for SetDesiredForce_Request {
  type RmwMsg = super::srv::rmw::SetDesiredForce_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        fd: msg.fd,
        dir: msg.dir,
        ref_: msg.ref_,
        time: msg.time,
        mod_: msg.mod_,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        fd: msg.fd,
        dir: msg.dir,
      ref_: msg.ref_,
      time: msg.time,
      mod_: msg.mod_,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      fd: msg.fd,
      dir: msg.dir,
      ref_: msg.ref_,
      time: msg.time,
      mod_: msg.mod_,
    }
  }
}


// Corresponds to dsr_msgs2__srv__SetDesiredForce_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SetDesiredForce_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,

}



impl Default for SetDesiredForce_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::SetDesiredForce_Response::default())
  }
}

impl rosidl_runtime_rs::Message for SetDesiredForce_Response {
  type RmwMsg = super::srv::rmw::SetDesiredForce_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        success: msg.success,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      success: msg.success,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      success: msg.success,
    }
  }
}


// Corresponds to dsr_msgs2__srv__ReleaseForce_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ReleaseForce_Request {
    /// 0          # Time needed to reduce the force (0 ~ 1.0)
    pub time: f64,

}



impl Default for ReleaseForce_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::ReleaseForce_Request::default())
  }
}

impl rosidl_runtime_rs::Message for ReleaseForce_Request {
  type RmwMsg = super::srv::rmw::ReleaseForce_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        time: msg.time,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      time: msg.time,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      time: msg.time,
    }
  }
}


// Corresponds to dsr_msgs2__srv__ReleaseForce_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ReleaseForce_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,

}



impl Default for ReleaseForce_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::ReleaseForce_Response::default())
  }
}

impl rosidl_runtime_rs::Message for ReleaseForce_Response {
  type RmwMsg = super::srv::rmw::ReleaseForce_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        success: msg.success,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      success: msg.success,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      success: msg.success,
    }
  }
}


// Corresponds to dsr_msgs2__srv__CheckPositionCondition_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct CheckPositionCondition_Request {
    /// DR_AXIS_X(0), DR_AXIS_Y(1), DR_AXIS_Z(2)
    pub axis: i8,

    /// min
    pub min: f64,

    /// max
    pub max: f64,

    /// = 0      # DR_BASE(0), DR_TOOL(1), DR_WORLD(2), user_coordinate(101~200)
    ///  <DR_WORLD is only available in M2.40 or later>
    pub ref_: i8,

    /// = 0         # DR_MV_MOD_ABS(0), DR_MV_MOD_REL(1)
    pub mode: i8,

    /// task pos(posx)
    pub pos: [f64; 6],

}



impl Default for CheckPositionCondition_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::CheckPositionCondition_Request::default())
  }
}

impl rosidl_runtime_rs::Message for CheckPositionCondition_Request {
  type RmwMsg = super::srv::rmw::CheckPositionCondition_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        axis: msg.axis,
        min: msg.min,
        max: msg.max,
        ref_: msg.ref_,
        mode: msg.mode,
        pos: msg.pos,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      axis: msg.axis,
      min: msg.min,
      max: msg.max,
      ref_: msg.ref_,
      mode: msg.mode,
        pos: msg.pos,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      axis: msg.axis,
      min: msg.min,
      max: msg.max,
      ref_: msg.ref_,
      mode: msg.mode,
      pos: msg.pos,
    }
  }
}


// Corresponds to dsr_msgs2__srv__CheckPositionCondition_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct CheckPositionCondition_Response {
    /// True or False
    pub success: bool,

}



impl Default for CheckPositionCondition_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::CheckPositionCondition_Response::default())
  }
}

impl rosidl_runtime_rs::Message for CheckPositionCondition_Response {
  type RmwMsg = super::srv::rmw::CheckPositionCondition_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        success: msg.success,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      success: msg.success,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      success: msg.success,
    }
  }
}


// Corresponds to dsr_msgs2__srv__CheckForceCondition_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct CheckForceCondition_Request {
    /// DR_AXIS_X(0), DR_AXIS_Y(1), DR_AXIS_Z(2), DR_AXIS_A(10), DR_AXIS_B(11), DR_AXIS_C(12)
    pub axis: i8,

    /// min >=0.0
    pub min: f64,

    /// max >=0.0
    pub max: f64,

    /// = 0      # DR_BASE(0), DR_TOOL(1), DR_WORLD(2), user coord(101~200)
    ///  <DR_WORLD is only available in M2.40 or later>
    pub ref_: i8,

}



impl Default for CheckForceCondition_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::CheckForceCondition_Request::default())
  }
}

impl rosidl_runtime_rs::Message for CheckForceCondition_Request {
  type RmwMsg = super::srv::rmw::CheckForceCondition_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        axis: msg.axis,
        min: msg.min,
        max: msg.max,
        ref_: msg.ref_,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      axis: msg.axis,
      min: msg.min,
      max: msg.max,
      ref_: msg.ref_,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      axis: msg.axis,
      min: msg.min,
      max: msg.max,
      ref_: msg.ref_,
    }
  }
}


// Corresponds to dsr_msgs2__srv__CheckForceCondition_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct CheckForceCondition_Response {
    /// True or False
    pub success: bool,

}



impl Default for CheckForceCondition_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::CheckForceCondition_Response::default())
  }
}

impl rosidl_runtime_rs::Message for CheckForceCondition_Response {
  type RmwMsg = super::srv::rmw::CheckForceCondition_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        success: msg.success,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      success: msg.success,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      success: msg.success,
    }
  }
}


// Corresponds to dsr_msgs2__srv__CheckOrientationCondition1_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct CheckOrientationCondition1_Request {
    /// DR_AXIS_A(10), DR_AXIS_B(11), DR_AXIS_C(12)
    pub axis: i8,

    /// task pos(posx)
    pub min: [f64; 6],

    /// task pos(posx)
    pub max: [f64; 6],

    /// = 0         # DR_BASE(0), DR_TOOL(1), DR_WORLD(2), user_coordinate(101~200)
    ///  <DR_WORLD is only available in M2.40 or later>
    pub ref_: i8,

    /// = 0         # DR_MV_MOD_ABS(0)
    pub mode: i8,

}



impl Default for CheckOrientationCondition1_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::CheckOrientationCondition1_Request::default())
  }
}

impl rosidl_runtime_rs::Message for CheckOrientationCondition1_Request {
  type RmwMsg = super::srv::rmw::CheckOrientationCondition1_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        axis: msg.axis,
        min: msg.min,
        max: msg.max,
        ref_: msg.ref_,
        mode: msg.mode,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      axis: msg.axis,
        min: msg.min,
        max: msg.max,
      ref_: msg.ref_,
      mode: msg.mode,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      axis: msg.axis,
      min: msg.min,
      max: msg.max,
      ref_: msg.ref_,
      mode: msg.mode,
    }
  }
}


// Corresponds to dsr_msgs2__srv__CheckOrientationCondition1_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct CheckOrientationCondition1_Response {
    /// True or False
    pub success: bool,

}



impl Default for CheckOrientationCondition1_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::CheckOrientationCondition1_Response::default())
  }
}

impl rosidl_runtime_rs::Message for CheckOrientationCondition1_Response {
  type RmwMsg = super::srv::rmw::CheckOrientationCondition1_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        success: msg.success,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      success: msg.success,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      success: msg.success,
    }
  }
}


// Corresponds to dsr_msgs2__srv__CheckOrientationCondition2_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct CheckOrientationCondition2_Request {
    /// DR_AXIS_A(10), DR_AXIS_B(11), DR_AXIS_C(12)
    pub axis: i8,

    /// minimum value
    pub min: f64,

    /// maximum value
    pub max: f64,

    /// = 0         # DR_BASE(0), DR_TOOL(1), DR_WORLD(2), user_coordinate(101~200)
    ///  <DR_WORLD is only available in M2.40 or later>
    pub ref_: i8,

    /// = 1         # DR_MV_MOD_REL(1)
    pub mode: i8,

    /// task pos(pos)
    pub pos: [f64; 6],

}



impl Default for CheckOrientationCondition2_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::CheckOrientationCondition2_Request::default())
  }
}

impl rosidl_runtime_rs::Message for CheckOrientationCondition2_Request {
  type RmwMsg = super::srv::rmw::CheckOrientationCondition2_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        axis: msg.axis,
        min: msg.min,
        max: msg.max,
        ref_: msg.ref_,
        mode: msg.mode,
        pos: msg.pos,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      axis: msg.axis,
      min: msg.min,
      max: msg.max,
      ref_: msg.ref_,
      mode: msg.mode,
        pos: msg.pos,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      axis: msg.axis,
      min: msg.min,
      max: msg.max,
      ref_: msg.ref_,
      mode: msg.mode,
      pos: msg.pos,
    }
  }
}


// Corresponds to dsr_msgs2__srv__CheckOrientationCondition2_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct CheckOrientationCondition2_Response {
    /// True or False
    pub success: bool,

}



impl Default for CheckOrientationCondition2_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::CheckOrientationCondition2_Response::default())
  }
}

impl rosidl_runtime_rs::Message for CheckOrientationCondition2_Response {
  type RmwMsg = super::srv::rmw::CheckOrientationCondition2_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        success: msg.success,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      success: msg.success,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      success: msg.success,
    }
  }
}


// Corresponds to dsr_msgs2__srv__CoordTransform_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct CoordTransform_Request {
    /// task pos(posx)
    pub pos_in: [f64; 6],

    /// DR_BASE(0), DR_TOOL(1), DR_WORLD(2), user coord(101~200)
    /// <ref is only available in M2.40 or later>
    pub ref_in: i8,

    /// DR_BASE(0), DR_TOOL(1), DR_WORLD(2), user coord(101~200)
    /// <ref is only available in M2.40 or later>
    pub ref_out: i8,

}



impl Default for CoordTransform_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::CoordTransform_Request::default())
  }
}

impl rosidl_runtime_rs::Message for CoordTransform_Request {
  type RmwMsg = super::srv::rmw::CoordTransform_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        pos_in: msg.pos_in,
        ref_in: msg.ref_in,
        ref_out: msg.ref_out,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        pos_in: msg.pos_in,
      ref_in: msg.ref_in,
      ref_out: msg.ref_out,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      pos_in: msg.pos_in,
      ref_in: msg.ref_in,
      ref_out: msg.ref_out,
    }
  }
}


// Corresponds to dsr_msgs2__srv__CoordTransform_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct CoordTransform_Response {
    /// task pos(posx)
    pub conv_posx: [f64; 6],


    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,

}



impl Default for CoordTransform_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::CoordTransform_Response::default())
  }
}

impl rosidl_runtime_rs::Message for CoordTransform_Response {
  type RmwMsg = super::srv::rmw::CoordTransform_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        conv_posx: msg.conv_posx,
        success: msg.success,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        conv_posx: msg.conv_posx,
      success: msg.success,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      conv_posx: msg.conv_posx,
      success: msg.success,
    }
  }
}


// Corresponds to dsr_msgs2__srv__GetWorkpieceWeight_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetWorkpieceWeight_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub structure_needs_at_least_one_member: u8,

}



impl Default for GetWorkpieceWeight_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::GetWorkpieceWeight_Request::default())
  }
}

impl rosidl_runtime_rs::Message for GetWorkpieceWeight_Request {
  type RmwMsg = super::srv::rmw::GetWorkpieceWeight_Request;

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


// Corresponds to dsr_msgs2__srv__GetWorkpieceWeight_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetWorkpieceWeight_Response {
    /// Measured weight, Negative value if error
    pub weight: f32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,

}



impl Default for GetWorkpieceWeight_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::GetWorkpieceWeight_Response::default())
  }
}

impl rosidl_runtime_rs::Message for GetWorkpieceWeight_Response {
  type RmwMsg = super::srv::rmw::GetWorkpieceWeight_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        weight: msg.weight,
        success: msg.success,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      weight: msg.weight,
      success: msg.success,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      weight: msg.weight,
      success: msg.success,
    }
  }
}


// Corresponds to dsr_msgs2__srv__ResetWorkpieceWeight_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ResetWorkpieceWeight_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub structure_needs_at_least_one_member: u8,

}



impl Default for ResetWorkpieceWeight_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::ResetWorkpieceWeight_Request::default())
  }
}

impl rosidl_runtime_rs::Message for ResetWorkpieceWeight_Request {
  type RmwMsg = super::srv::rmw::ResetWorkpieceWeight_Request;

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


// Corresponds to dsr_msgs2__srv__ResetWorkpieceWeight_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ResetWorkpieceWeight_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,

}



impl Default for ResetWorkpieceWeight_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::ResetWorkpieceWeight_Response::default())
  }
}

impl rosidl_runtime_rs::Message for ResetWorkpieceWeight_Response {
  type RmwMsg = super::srv::rmw::ResetWorkpieceWeight_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        success: msg.success,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      success: msg.success,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      success: msg.success,
    }
  }
}


// Corresponds to dsr_msgs2__srv__ConfigCreateTool_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ConfigCreateTool_Request {
    /// tool name
    pub name: std::string::String,

    /// tool weight
    pub weight: f64,

    /// Center of gravity
    pub cog: [f64; 3],

    /// tool inertia
    pub inertia: [f64; 6],

}



impl Default for ConfigCreateTool_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::ConfigCreateTool_Request::default())
  }
}

impl rosidl_runtime_rs::Message for ConfigCreateTool_Request {
  type RmwMsg = super::srv::rmw::ConfigCreateTool_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        name: msg.name.as_str().into(),
        weight: msg.weight,
        cog: msg.cog,
        inertia: msg.inertia,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        name: msg.name.as_str().into(),
      weight: msg.weight,
        cog: msg.cog,
        inertia: msg.inertia,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      name: msg.name.to_string(),
      weight: msg.weight,
      cog: msg.cog,
      inertia: msg.inertia,
    }
  }
}


// Corresponds to dsr_msgs2__srv__ConfigCreateTool_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ConfigCreateTool_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,

}



impl Default for ConfigCreateTool_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::ConfigCreateTool_Response::default())
  }
}

impl rosidl_runtime_rs::Message for ConfigCreateTool_Response {
  type RmwMsg = super::srv::rmw::ConfigCreateTool_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        success: msg.success,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      success: msg.success,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      success: msg.success,
    }
  }
}


// Corresponds to dsr_msgs2__srv__ConfigDeleteTool_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ConfigDeleteTool_Request {
    /// tool name
    pub name: std::string::String,

}



impl Default for ConfigDeleteTool_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::ConfigDeleteTool_Request::default())
  }
}

impl rosidl_runtime_rs::Message for ConfigDeleteTool_Request {
  type RmwMsg = super::srv::rmw::ConfigDeleteTool_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        name: msg.name.as_str().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        name: msg.name.as_str().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      name: msg.name.to_string(),
    }
  }
}


// Corresponds to dsr_msgs2__srv__ConfigDeleteTool_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ConfigDeleteTool_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,

}



impl Default for ConfigDeleteTool_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::ConfigDeleteTool_Response::default())
  }
}

impl rosidl_runtime_rs::Message for ConfigDeleteTool_Response {
  type RmwMsg = super::srv::rmw::ConfigDeleteTool_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        success: msg.success,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      success: msg.success,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      success: msg.success,
    }
  }
}


// Corresponds to dsr_msgs2__srv__SetCurrentTool_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SetCurrentTool_Request {
    /// tool name
    pub name: std::string::String,

}



impl Default for SetCurrentTool_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::SetCurrentTool_Request::default())
  }
}

impl rosidl_runtime_rs::Message for SetCurrentTool_Request {
  type RmwMsg = super::srv::rmw::SetCurrentTool_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        name: msg.name.as_str().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        name: msg.name.as_str().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      name: msg.name.to_string(),
    }
  }
}


// Corresponds to dsr_msgs2__srv__SetCurrentTool_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SetCurrentTool_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,

}



impl Default for SetCurrentTool_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::SetCurrentTool_Response::default())
  }
}

impl rosidl_runtime_rs::Message for SetCurrentTool_Response {
  type RmwMsg = super::srv::rmw::SetCurrentTool_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        success: msg.success,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      success: msg.success,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      success: msg.success,
    }
  }
}


// Corresponds to dsr_msgs2__srv__GetCurrentTool_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetCurrentTool_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub structure_needs_at_least_one_member: u8,

}



impl Default for GetCurrentTool_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::GetCurrentTool_Request::default())
  }
}

impl rosidl_runtime_rs::Message for GetCurrentTool_Request {
  type RmwMsg = super::srv::rmw::GetCurrentTool_Request;

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


// Corresponds to dsr_msgs2__srv__GetCurrentTool_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetCurrentTool_Response {
    /// tool name
    pub info: std::string::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,

}



impl Default for GetCurrentTool_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::GetCurrentTool_Response::default())
  }
}

impl rosidl_runtime_rs::Message for GetCurrentTool_Response {
  type RmwMsg = super::srv::rmw::GetCurrentTool_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        info: msg.info.as_str().into(),
        success: msg.success,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        info: msg.info.as_str().into(),
      success: msg.success,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      info: msg.info.to_string(),
      success: msg.success,
    }
  }
}


// Corresponds to dsr_msgs2__srv__SetToolShape_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SetToolShape_Request {
    /// Tool name registered in the Teach Pendant
    pub name: std::string::String,

}



impl Default for SetToolShape_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::SetToolShape_Request::default())
  }
}

impl rosidl_runtime_rs::Message for SetToolShape_Request {
  type RmwMsg = super::srv::rmw::SetToolShape_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        name: msg.name.as_str().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        name: msg.name.as_str().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      name: msg.name.to_string(),
    }
  }
}


// Corresponds to dsr_msgs2__srv__SetToolShape_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SetToolShape_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,

}



impl Default for SetToolShape_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::SetToolShape_Response::default())
  }
}

impl rosidl_runtime_rs::Message for SetToolShape_Response {
  type RmwMsg = super::srv::rmw::SetToolShape_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        success: msg.success,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      success: msg.success,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      success: msg.success,
    }
  }
}


// Corresponds to dsr_msgs2__srv__ConfigCreateTcp_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ConfigCreateTcp_Request {
    /// tcp name
    pub name: std::string::String,

    /// coordinates of the TCP
    pub pos: [f64; 6],

}



impl Default for ConfigCreateTcp_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::ConfigCreateTcp_Request::default())
  }
}

impl rosidl_runtime_rs::Message for ConfigCreateTcp_Request {
  type RmwMsg = super::srv::rmw::ConfigCreateTcp_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        name: msg.name.as_str().into(),
        pos: msg.pos,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        name: msg.name.as_str().into(),
        pos: msg.pos,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      name: msg.name.to_string(),
      pos: msg.pos,
    }
  }
}


// Corresponds to dsr_msgs2__srv__ConfigCreateTcp_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ConfigCreateTcp_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,

}



impl Default for ConfigCreateTcp_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::ConfigCreateTcp_Response::default())
  }
}

impl rosidl_runtime_rs::Message for ConfigCreateTcp_Response {
  type RmwMsg = super::srv::rmw::ConfigCreateTcp_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        success: msg.success,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      success: msg.success,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      success: msg.success,
    }
  }
}


// Corresponds to dsr_msgs2__srv__ConfigDeleteTcp_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ConfigDeleteTcp_Request {
    /// tcp name
    pub name: std::string::String,

}



impl Default for ConfigDeleteTcp_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::ConfigDeleteTcp_Request::default())
  }
}

impl rosidl_runtime_rs::Message for ConfigDeleteTcp_Request {
  type RmwMsg = super::srv::rmw::ConfigDeleteTcp_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        name: msg.name.as_str().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        name: msg.name.as_str().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      name: msg.name.to_string(),
    }
  }
}


// Corresponds to dsr_msgs2__srv__ConfigDeleteTcp_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ConfigDeleteTcp_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,

}



impl Default for ConfigDeleteTcp_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::ConfigDeleteTcp_Response::default())
  }
}

impl rosidl_runtime_rs::Message for ConfigDeleteTcp_Response {
  type RmwMsg = super::srv::rmw::ConfigDeleteTcp_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        success: msg.success,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      success: msg.success,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      success: msg.success,
    }
  }
}


// Corresponds to dsr_msgs2__srv__SetCurrentTcp_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SetCurrentTcp_Request {
    /// tcp name
    pub name: std::string::String,

}



impl Default for SetCurrentTcp_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::SetCurrentTcp_Request::default())
  }
}

impl rosidl_runtime_rs::Message for SetCurrentTcp_Request {
  type RmwMsg = super::srv::rmw::SetCurrentTcp_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        name: msg.name.as_str().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        name: msg.name.as_str().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      name: msg.name.to_string(),
    }
  }
}


// Corresponds to dsr_msgs2__srv__SetCurrentTcp_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SetCurrentTcp_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,

}



impl Default for SetCurrentTcp_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::SetCurrentTcp_Response::default())
  }
}

impl rosidl_runtime_rs::Message for SetCurrentTcp_Response {
  type RmwMsg = super::srv::rmw::SetCurrentTcp_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        success: msg.success,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      success: msg.success,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      success: msg.success,
    }
  }
}


// Corresponds to dsr_msgs2__srv__GetCurrentTcp_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetCurrentTcp_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub structure_needs_at_least_one_member: u8,

}



impl Default for GetCurrentTcp_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::GetCurrentTcp_Request::default())
  }
}

impl rosidl_runtime_rs::Message for GetCurrentTcp_Request {
  type RmwMsg = super::srv::rmw::GetCurrentTcp_Request;

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


// Corresponds to dsr_msgs2__srv__GetCurrentTcp_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetCurrentTcp_Response {
    /// tcp name
    pub info: std::string::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,

}



impl Default for GetCurrentTcp_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::GetCurrentTcp_Response::default())
  }
}

impl rosidl_runtime_rs::Message for GetCurrentTcp_Response {
  type RmwMsg = super::srv::rmw::GetCurrentTcp_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        info: msg.info.as_str().into(),
        success: msg.success,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        info: msg.info.as_str().into(),
      success: msg.success,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      info: msg.info.to_string(),
      success: msg.success,
    }
  }
}


// Corresponds to dsr_msgs2__srv__SetToolDigitalOutput_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SetToolDigitalOutput_Request {
    /// flange digital output port(1 ~ 6)
    pub index: i8,

    /// 0 : ON, 1 : OFF
    pub value: i8,

}



impl Default for SetToolDigitalOutput_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::SetToolDigitalOutput_Request::default())
  }
}

impl rosidl_runtime_rs::Message for SetToolDigitalOutput_Request {
  type RmwMsg = super::srv::rmw::SetToolDigitalOutput_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        index: msg.index,
        value: msg.value,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      index: msg.index,
      value: msg.value,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      index: msg.index,
      value: msg.value,
    }
  }
}


// Corresponds to dsr_msgs2__srv__SetToolDigitalOutput_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SetToolDigitalOutput_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,

}



impl Default for SetToolDigitalOutput_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::SetToolDigitalOutput_Response::default())
  }
}

impl rosidl_runtime_rs::Message for SetToolDigitalOutput_Response {
  type RmwMsg = super::srv::rmw::SetToolDigitalOutput_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        success: msg.success,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      success: msg.success,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      success: msg.success,
    }
  }
}


// Corresponds to dsr_msgs2__srv__GetToolDigitalOutput_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetToolDigitalOutput_Request {
    /// flange digital output port(1 ~ 6)
    pub index: i8,

}



impl Default for GetToolDigitalOutput_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::GetToolDigitalOutput_Request::default())
  }
}

impl rosidl_runtime_rs::Message for GetToolDigitalOutput_Request {
  type RmwMsg = super::srv::rmw::GetToolDigitalOutput_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        index: msg.index,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      index: msg.index,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      index: msg.index,
    }
  }
}


// Corresponds to dsr_msgs2__srv__GetToolDigitalOutput_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetToolDigitalOutput_Response {
    /// Current output status (0 : ON, 1 : OFF)
    pub value: i8,


    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,

}



impl Default for GetToolDigitalOutput_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::GetToolDigitalOutput_Response::default())
  }
}

impl rosidl_runtime_rs::Message for GetToolDigitalOutput_Response {
  type RmwMsg = super::srv::rmw::GetToolDigitalOutput_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        value: msg.value,
        success: msg.success,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      value: msg.value,
      success: msg.success,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      value: msg.value,
      success: msg.success,
    }
  }
}


// Corresponds to dsr_msgs2__srv__GetToolDigitalInput_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetToolDigitalInput_Request {
    /// Digital Input in Flange(1 ~ 6)
    /// <GPIO_TOOL_DIGITAL_INDEX>
    pub index: i8,

}



impl Default for GetToolDigitalInput_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::GetToolDigitalInput_Request::default())
  }
}

impl rosidl_runtime_rs::Message for GetToolDigitalInput_Request {
  type RmwMsg = super::srv::rmw::GetToolDigitalInput_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        index: msg.index,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      index: msg.index,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      index: msg.index,
    }
  }
}


// Corresponds to dsr_msgs2__srv__GetToolDigitalInput_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetToolDigitalInput_Response {
    /// 0=OFF, 1=ON
    pub value: i8,


    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,

}



impl Default for GetToolDigitalInput_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::GetToolDigitalInput_Response::default())
  }
}

impl rosidl_runtime_rs::Message for GetToolDigitalInput_Response {
  type RmwMsg = super::srv::rmw::GetToolDigitalInput_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        value: msg.value,
        success: msg.success,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      value: msg.value,
      success: msg.success,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      value: msg.value,
      success: msg.success,
    }
  }
}


// Corresponds to dsr_msgs2__srv__SetCtrlBoxDigitalOutput_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SetCtrlBoxDigitalOutput_Request {
    /// ctrlbox digital output port(1 ~ 16)
    pub index: i8,

    /// 0 : ON, 1 : OFF
    pub value: i8,

}



impl Default for SetCtrlBoxDigitalOutput_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::SetCtrlBoxDigitalOutput_Request::default())
  }
}

impl rosidl_runtime_rs::Message for SetCtrlBoxDigitalOutput_Request {
  type RmwMsg = super::srv::rmw::SetCtrlBoxDigitalOutput_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        index: msg.index,
        value: msg.value,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      index: msg.index,
      value: msg.value,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      index: msg.index,
      value: msg.value,
    }
  }
}


// Corresponds to dsr_msgs2__srv__SetCtrlBoxDigitalOutput_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SetCtrlBoxDigitalOutput_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,

}



impl Default for SetCtrlBoxDigitalOutput_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::SetCtrlBoxDigitalOutput_Response::default())
  }
}

impl rosidl_runtime_rs::Message for SetCtrlBoxDigitalOutput_Response {
  type RmwMsg = super::srv::rmw::SetCtrlBoxDigitalOutput_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        success: msg.success,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      success: msg.success,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      success: msg.success,
    }
  }
}


// Corresponds to dsr_msgs2__srv__GetCtrlBoxDigitalOutput_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetCtrlBoxDigitalOutput_Request {
    /// ctrlbox digital output port(1 ~ 16)
    pub index: i8,

}



impl Default for GetCtrlBoxDigitalOutput_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::GetCtrlBoxDigitalOutput_Request::default())
  }
}

impl rosidl_runtime_rs::Message for GetCtrlBoxDigitalOutput_Request {
  type RmwMsg = super::srv::rmw::GetCtrlBoxDigitalOutput_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        index: msg.index,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      index: msg.index,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      index: msg.index,
    }
  }
}


// Corresponds to dsr_msgs2__srv__GetCtrlBoxDigitalOutput_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetCtrlBoxDigitalOutput_Response {
    /// Current output status (0 : ON, 1 : OFF)
    pub value: i8,


    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,

}



impl Default for GetCtrlBoxDigitalOutput_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::GetCtrlBoxDigitalOutput_Response::default())
  }
}

impl rosidl_runtime_rs::Message for GetCtrlBoxDigitalOutput_Response {
  type RmwMsg = super::srv::rmw::GetCtrlBoxDigitalOutput_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        value: msg.value,
        success: msg.success,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      value: msg.value,
      success: msg.success,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      value: msg.value,
      success: msg.success,
    }
  }
}


// Corresponds to dsr_msgs2__srv__GetCtrlBoxDigitalInput_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetCtrlBoxDigitalInput_Request {
    /// Digital Input in Control Box(1 ~ 16)
    /// <GPIO_CTRLBOX_DIGITAL_INDEX>
    pub index: i8,

}



impl Default for GetCtrlBoxDigitalInput_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::GetCtrlBoxDigitalInput_Request::default())
  }
}

impl rosidl_runtime_rs::Message for GetCtrlBoxDigitalInput_Request {
  type RmwMsg = super::srv::rmw::GetCtrlBoxDigitalInput_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        index: msg.index,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      index: msg.index,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      index: msg.index,
    }
  }
}


// Corresponds to dsr_msgs2__srv__GetCtrlBoxDigitalInput_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetCtrlBoxDigitalInput_Response {
    /// 0=OFF, 1=ON
    pub value: i8,


    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,

}



impl Default for GetCtrlBoxDigitalInput_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::GetCtrlBoxDigitalInput_Response::default())
  }
}

impl rosidl_runtime_rs::Message for GetCtrlBoxDigitalInput_Response {
  type RmwMsg = super::srv::rmw::GetCtrlBoxDigitalInput_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        value: msg.value,
        success: msg.success,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      value: msg.value,
      success: msg.success,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      value: msg.value,
      success: msg.success,
    }
  }
}


// Corresponds to dsr_msgs2__srv__SetCtrlBoxAnalogInputType_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SetCtrlBoxAnalogInputType_Request {
    /// 1 = ch1, 2= ch2
    pub channel: i8,

    /// 0 = current, 1 = voltage
    pub mode: i8,

}



impl Default for SetCtrlBoxAnalogInputType_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::SetCtrlBoxAnalogInputType_Request::default())
  }
}

impl rosidl_runtime_rs::Message for SetCtrlBoxAnalogInputType_Request {
  type RmwMsg = super::srv::rmw::SetCtrlBoxAnalogInputType_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        channel: msg.channel,
        mode: msg.mode,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      channel: msg.channel,
      mode: msg.mode,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      channel: msg.channel,
      mode: msg.mode,
    }
  }
}


// Corresponds to dsr_msgs2__srv__SetCtrlBoxAnalogInputType_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SetCtrlBoxAnalogInputType_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,

}



impl Default for SetCtrlBoxAnalogInputType_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::SetCtrlBoxAnalogInputType_Response::default())
  }
}

impl rosidl_runtime_rs::Message for SetCtrlBoxAnalogInputType_Response {
  type RmwMsg = super::srv::rmw::SetCtrlBoxAnalogInputType_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        success: msg.success,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      success: msg.success,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      success: msg.success,
    }
  }
}


// Corresponds to dsr_msgs2__srv__SetCtrlBoxAnalogOutputType_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SetCtrlBoxAnalogOutputType_Request {
    /// 1 = ch1, 2= ch2
    pub channel: i8,

    /// 0 = current, 1 = voltage
    pub mode: i8,

}



impl Default for SetCtrlBoxAnalogOutputType_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::SetCtrlBoxAnalogOutputType_Request::default())
  }
}

impl rosidl_runtime_rs::Message for SetCtrlBoxAnalogOutputType_Request {
  type RmwMsg = super::srv::rmw::SetCtrlBoxAnalogOutputType_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        channel: msg.channel,
        mode: msg.mode,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      channel: msg.channel,
      mode: msg.mode,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      channel: msg.channel,
      mode: msg.mode,
    }
  }
}


// Corresponds to dsr_msgs2__srv__SetCtrlBoxAnalogOutputType_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SetCtrlBoxAnalogOutputType_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,

}



impl Default for SetCtrlBoxAnalogOutputType_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::SetCtrlBoxAnalogOutputType_Response::default())
  }
}

impl rosidl_runtime_rs::Message for SetCtrlBoxAnalogOutputType_Response {
  type RmwMsg = super::srv::rmw::SetCtrlBoxAnalogOutputType_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        success: msg.success,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      success: msg.success,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      success: msg.success,
    }
  }
}


// Corresponds to dsr_msgs2__srv__SetCtrlBoxAnalogOutput_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SetCtrlBoxAnalogOutput_Request {
    /// 1 = ch1, 2= ch2
    pub channel: i8,


    // This member is not documented.
    #[allow(missing_docs)]
    pub value: f64,

}



impl Default for SetCtrlBoxAnalogOutput_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::SetCtrlBoxAnalogOutput_Request::default())
  }
}

impl rosidl_runtime_rs::Message for SetCtrlBoxAnalogOutput_Request {
  type RmwMsg = super::srv::rmw::SetCtrlBoxAnalogOutput_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        channel: msg.channel,
        value: msg.value,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      channel: msg.channel,
      value: msg.value,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      channel: msg.channel,
      value: msg.value,
    }
  }
}


// Corresponds to dsr_msgs2__srv__SetCtrlBoxAnalogOutput_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SetCtrlBoxAnalogOutput_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,

}



impl Default for SetCtrlBoxAnalogOutput_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::SetCtrlBoxAnalogOutput_Response::default())
  }
}

impl rosidl_runtime_rs::Message for SetCtrlBoxAnalogOutput_Response {
  type RmwMsg = super::srv::rmw::SetCtrlBoxAnalogOutput_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        success: msg.success,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      success: msg.success,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      success: msg.success,
    }
  }
}


// Corresponds to dsr_msgs2__srv__GetCtrlBoxAnalogInput_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetCtrlBoxAnalogInput_Request {
    /// 1 = ch1, 2= ch2
    pub channel: i8,

}



impl Default for GetCtrlBoxAnalogInput_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::GetCtrlBoxAnalogInput_Request::default())
  }
}

impl rosidl_runtime_rs::Message for GetCtrlBoxAnalogInput_Request {
  type RmwMsg = super::srv::rmw::GetCtrlBoxAnalogInput_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        channel: msg.channel,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      channel: msg.channel,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      channel: msg.channel,
    }
  }
}


// Corresponds to dsr_msgs2__srv__GetCtrlBoxAnalogInput_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetCtrlBoxAnalogInput_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub value: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,

}



impl Default for GetCtrlBoxAnalogInput_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::GetCtrlBoxAnalogInput_Response::default())
  }
}

impl rosidl_runtime_rs::Message for GetCtrlBoxAnalogInput_Response {
  type RmwMsg = super::srv::rmw::GetCtrlBoxAnalogInput_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        value: msg.value,
        success: msg.success,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      value: msg.value,
      success: msg.success,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      value: msg.value,
      success: msg.success,
    }
  }
}


// Corresponds to dsr_msgs2__srv__GetInputRegisterBit_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetInputRegisterBit_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub address: u16,


    // This member is not documented.
    #[allow(missing_docs)]
    pub timeout_ms: u32,

}



impl Default for GetInputRegisterBit_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::GetInputRegisterBit_Request::default())
  }
}

impl rosidl_runtime_rs::Message for GetInputRegisterBit_Request {
  type RmwMsg = super::srv::rmw::GetInputRegisterBit_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        address: msg.address,
        timeout_ms: msg.timeout_ms,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      address: msg.address,
      timeout_ms: msg.timeout_ms,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      address: msg.address,
      timeout_ms: msg.timeout_ms,
    }
  }
}


// Corresponds to dsr_msgs2__srv__GetInputRegisterBit_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetInputRegisterBit_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub value: i32,

}



impl Default for GetInputRegisterBit_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::GetInputRegisterBit_Response::default())
  }
}

impl rosidl_runtime_rs::Message for GetInputRegisterBit_Response {
  type RmwMsg = super::srv::rmw::GetInputRegisterBit_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        success: msg.success,
        value: msg.value,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      success: msg.success,
      value: msg.value,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      success: msg.success,
      value: msg.value,
    }
  }
}


// Corresponds to dsr_msgs2__srv__GetInputRegisterInt_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetInputRegisterInt_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub address: u16,


    // This member is not documented.
    #[allow(missing_docs)]
    pub timeout_ms: u32,

}



impl Default for GetInputRegisterInt_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::GetInputRegisterInt_Request::default())
  }
}

impl rosidl_runtime_rs::Message for GetInputRegisterInt_Request {
  type RmwMsg = super::srv::rmw::GetInputRegisterInt_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        address: msg.address,
        timeout_ms: msg.timeout_ms,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      address: msg.address,
      timeout_ms: msg.timeout_ms,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      address: msg.address,
      timeout_ms: msg.timeout_ms,
    }
  }
}


// Corresponds to dsr_msgs2__srv__GetInputRegisterInt_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetInputRegisterInt_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub value: i32,

}



impl Default for GetInputRegisterInt_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::GetInputRegisterInt_Response::default())
  }
}

impl rosidl_runtime_rs::Message for GetInputRegisterInt_Response {
  type RmwMsg = super::srv::rmw::GetInputRegisterInt_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        success: msg.success,
        value: msg.value,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      success: msg.success,
      value: msg.value,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      success: msg.success,
      value: msg.value,
    }
  }
}


// Corresponds to dsr_msgs2__srv__GetInputRegisterFloat_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetInputRegisterFloat_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub address: u16,


    // This member is not documented.
    #[allow(missing_docs)]
    pub timeout_ms: u32,

}



impl Default for GetInputRegisterFloat_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::GetInputRegisterFloat_Request::default())
  }
}

impl rosidl_runtime_rs::Message for GetInputRegisterFloat_Request {
  type RmwMsg = super::srv::rmw::GetInputRegisterFloat_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        address: msg.address,
        timeout_ms: msg.timeout_ms,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      address: msg.address,
      timeout_ms: msg.timeout_ms,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      address: msg.address,
      timeout_ms: msg.timeout_ms,
    }
  }
}


// Corresponds to dsr_msgs2__srv__GetInputRegisterFloat_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetInputRegisterFloat_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub value: f64,

}



impl Default for GetInputRegisterFloat_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::GetInputRegisterFloat_Response::default())
  }
}

impl rosidl_runtime_rs::Message for GetInputRegisterFloat_Response {
  type RmwMsg = super::srv::rmw::GetInputRegisterFloat_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        success: msg.success,
        value: msg.value,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      success: msg.success,
      value: msg.value,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      success: msg.success,
      value: msg.value,
    }
  }
}


// Corresponds to dsr_msgs2__srv__GetOutputRegisterBit_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetOutputRegisterBit_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub address: u16,


    // This member is not documented.
    #[allow(missing_docs)]
    pub timeout_ms: u32,

}



impl Default for GetOutputRegisterBit_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::GetOutputRegisterBit_Request::default())
  }
}

impl rosidl_runtime_rs::Message for GetOutputRegisterBit_Request {
  type RmwMsg = super::srv::rmw::GetOutputRegisterBit_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        address: msg.address,
        timeout_ms: msg.timeout_ms,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      address: msg.address,
      timeout_ms: msg.timeout_ms,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      address: msg.address,
      timeout_ms: msg.timeout_ms,
    }
  }
}


// Corresponds to dsr_msgs2__srv__GetOutputRegisterBit_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetOutputRegisterBit_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub value: i32,

}



impl Default for GetOutputRegisterBit_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::GetOutputRegisterBit_Response::default())
  }
}

impl rosidl_runtime_rs::Message for GetOutputRegisterBit_Response {
  type RmwMsg = super::srv::rmw::GetOutputRegisterBit_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        success: msg.success,
        value: msg.value,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      success: msg.success,
      value: msg.value,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      success: msg.success,
      value: msg.value,
    }
  }
}


// Corresponds to dsr_msgs2__srv__GetOutputRegisterInt_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetOutputRegisterInt_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub address: u16,


    // This member is not documented.
    #[allow(missing_docs)]
    pub timeout_ms: u32,

}



impl Default for GetOutputRegisterInt_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::GetOutputRegisterInt_Request::default())
  }
}

impl rosidl_runtime_rs::Message for GetOutputRegisterInt_Request {
  type RmwMsg = super::srv::rmw::GetOutputRegisterInt_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        address: msg.address,
        timeout_ms: msg.timeout_ms,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      address: msg.address,
      timeout_ms: msg.timeout_ms,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      address: msg.address,
      timeout_ms: msg.timeout_ms,
    }
  }
}


// Corresponds to dsr_msgs2__srv__GetOutputRegisterInt_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetOutputRegisterInt_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub value: i32,

}



impl Default for GetOutputRegisterInt_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::GetOutputRegisterInt_Response::default())
  }
}

impl rosidl_runtime_rs::Message for GetOutputRegisterInt_Response {
  type RmwMsg = super::srv::rmw::GetOutputRegisterInt_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        success: msg.success,
        value: msg.value,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      success: msg.success,
      value: msg.value,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      success: msg.success,
      value: msg.value,
    }
  }
}


// Corresponds to dsr_msgs2__srv__GetOutputRegisterFloat_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetOutputRegisterFloat_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub address: u16,


    // This member is not documented.
    #[allow(missing_docs)]
    pub timeout_ms: u32,

}



impl Default for GetOutputRegisterFloat_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::GetOutputRegisterFloat_Request::default())
  }
}

impl rosidl_runtime_rs::Message for GetOutputRegisterFloat_Request {
  type RmwMsg = super::srv::rmw::GetOutputRegisterFloat_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        address: msg.address,
        timeout_ms: msg.timeout_ms,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      address: msg.address,
      timeout_ms: msg.timeout_ms,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      address: msg.address,
      timeout_ms: msg.timeout_ms,
    }
  }
}


// Corresponds to dsr_msgs2__srv__GetOutputRegisterFloat_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetOutputRegisterFloat_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub value: f64,

}



impl Default for GetOutputRegisterFloat_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::GetOutputRegisterFloat_Response::default())
  }
}

impl rosidl_runtime_rs::Message for GetOutputRegisterFloat_Response {
  type RmwMsg = super::srv::rmw::GetOutputRegisterFloat_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        success: msg.success,
        value: msg.value,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      success: msg.success,
      value: msg.value,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      success: msg.success,
      value: msg.value,
    }
  }
}


// Corresponds to dsr_msgs2__srv__SetOutputRegisterBit_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SetOutputRegisterBit_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub address: u16,


    // This member is not documented.
    #[allow(missing_docs)]
    pub value: i32,

}



impl Default for SetOutputRegisterBit_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::SetOutputRegisterBit_Request::default())
  }
}

impl rosidl_runtime_rs::Message for SetOutputRegisterBit_Request {
  type RmwMsg = super::srv::rmw::SetOutputRegisterBit_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        address: msg.address,
        value: msg.value,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      address: msg.address,
      value: msg.value,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      address: msg.address,
      value: msg.value,
    }
  }
}


// Corresponds to dsr_msgs2__srv__SetOutputRegisterBit_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SetOutputRegisterBit_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,

}



impl Default for SetOutputRegisterBit_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::SetOutputRegisterBit_Response::default())
  }
}

impl rosidl_runtime_rs::Message for SetOutputRegisterBit_Response {
  type RmwMsg = super::srv::rmw::SetOutputRegisterBit_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        success: msg.success,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      success: msg.success,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      success: msg.success,
    }
  }
}


// Corresponds to dsr_msgs2__srv__SetOutputRegisterInt_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SetOutputRegisterInt_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub address: u16,


    // This member is not documented.
    #[allow(missing_docs)]
    pub value: i32,

}



impl Default for SetOutputRegisterInt_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::SetOutputRegisterInt_Request::default())
  }
}

impl rosidl_runtime_rs::Message for SetOutputRegisterInt_Request {
  type RmwMsg = super::srv::rmw::SetOutputRegisterInt_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        address: msg.address,
        value: msg.value,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      address: msg.address,
      value: msg.value,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      address: msg.address,
      value: msg.value,
    }
  }
}


// Corresponds to dsr_msgs2__srv__SetOutputRegisterInt_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SetOutputRegisterInt_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,

}



impl Default for SetOutputRegisterInt_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::SetOutputRegisterInt_Response::default())
  }
}

impl rosidl_runtime_rs::Message for SetOutputRegisterInt_Response {
  type RmwMsg = super::srv::rmw::SetOutputRegisterInt_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        success: msg.success,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      success: msg.success,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      success: msg.success,
    }
  }
}


// Corresponds to dsr_msgs2__srv__SetOutputRegisterFloat_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SetOutputRegisterFloat_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub address: u16,


    // This member is not documented.
    #[allow(missing_docs)]
    pub value: f64,

}



impl Default for SetOutputRegisterFloat_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::SetOutputRegisterFloat_Request::default())
  }
}

impl rosidl_runtime_rs::Message for SetOutputRegisterFloat_Request {
  type RmwMsg = super::srv::rmw::SetOutputRegisterFloat_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        address: msg.address,
        value: msg.value,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      address: msg.address,
      value: msg.value,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      address: msg.address,
      value: msg.value,
    }
  }
}


// Corresponds to dsr_msgs2__srv__SetOutputRegisterFloat_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SetOutputRegisterFloat_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,

}



impl Default for SetOutputRegisterFloat_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::SetOutputRegisterFloat_Response::default())
  }
}

impl rosidl_runtime_rs::Message for SetOutputRegisterFloat_Response {
  type RmwMsg = super::srv::rmw::SetOutputRegisterFloat_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        success: msg.success,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      success: msg.success,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      success: msg.success,
    }
  }
}


// Corresponds to dsr_msgs2__srv__ConfigCreateModbus_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ConfigCreateModbus_Request {
    /// modbus signal symbol
    pub name: std::string::String,

    /// external device ip
    pub ip: std::string::String,

    /// external device port
    pub port: i32,

    /// <MODBUS_REGISTER_TYPE>(0: discrete input, 1: coil, 2: input register, 3: holding register)
    pub reg_type: i8,

    /// modbus signal index(0 ~ 9999)
    pub index: i8,

    /// modbus singla value(unsigned value ; 0 ~ 65535)
    pub value: i8,

    /// Slave ID of the ModbusTCP(0: Broadcase address or 1-247 or 255: Default value for ModbusTCP)
    /// <slave_id is only available in M2.40 or later versions>
    pub slave_id: i32,

}



impl Default for ConfigCreateModbus_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::ConfigCreateModbus_Request::default())
  }
}

impl rosidl_runtime_rs::Message for ConfigCreateModbus_Request {
  type RmwMsg = super::srv::rmw::ConfigCreateModbus_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        name: msg.name.as_str().into(),
        ip: msg.ip.as_str().into(),
        port: msg.port,
        reg_type: msg.reg_type,
        index: msg.index,
        value: msg.value,
        slave_id: msg.slave_id,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        name: msg.name.as_str().into(),
        ip: msg.ip.as_str().into(),
      port: msg.port,
      reg_type: msg.reg_type,
      index: msg.index,
      value: msg.value,
      slave_id: msg.slave_id,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      name: msg.name.to_string(),
      ip: msg.ip.to_string(),
      port: msg.port,
      reg_type: msg.reg_type,
      index: msg.index,
      value: msg.value,
      slave_id: msg.slave_id,
    }
  }
}


// Corresponds to dsr_msgs2__srv__ConfigCreateModbus_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ConfigCreateModbus_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,

}



impl Default for ConfigCreateModbus_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::ConfigCreateModbus_Response::default())
  }
}

impl rosidl_runtime_rs::Message for ConfigCreateModbus_Response {
  type RmwMsg = super::srv::rmw::ConfigCreateModbus_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        success: msg.success,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      success: msg.success,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      success: msg.success,
    }
  }
}


// Corresponds to dsr_msgs2__srv__ConfigDeleteModbus_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ConfigDeleteModbus_Request {
    /// modbus signal symbol
    pub name: std::string::String,

}



impl Default for ConfigDeleteModbus_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::ConfigDeleteModbus_Request::default())
  }
}

impl rosidl_runtime_rs::Message for ConfigDeleteModbus_Request {
  type RmwMsg = super::srv::rmw::ConfigDeleteModbus_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        name: msg.name.as_str().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        name: msg.name.as_str().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      name: msg.name.to_string(),
    }
  }
}


// Corresponds to dsr_msgs2__srv__ConfigDeleteModbus_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ConfigDeleteModbus_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,

}



impl Default for ConfigDeleteModbus_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::ConfigDeleteModbus_Response::default())
  }
}

impl rosidl_runtime_rs::Message for ConfigDeleteModbus_Response {
  type RmwMsg = super::srv::rmw::ConfigDeleteModbus_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        success: msg.success,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      success: msg.success,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      success: msg.success,
    }
  }
}


// Corresponds to dsr_msgs2__srv__SetModbusOutput_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SetModbusOutput_Request {
    /// modbus signal symbol
    pub name: std::string::String,

    /// modbus register value
    pub value: i32,

}



impl Default for SetModbusOutput_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::SetModbusOutput_Request::default())
  }
}

impl rosidl_runtime_rs::Message for SetModbusOutput_Request {
  type RmwMsg = super::srv::rmw::SetModbusOutput_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        name: msg.name.as_str().into(),
        value: msg.value,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        name: msg.name.as_str().into(),
      value: msg.value,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      name: msg.name.to_string(),
      value: msg.value,
    }
  }
}


// Corresponds to dsr_msgs2__srv__SetModbusOutput_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SetModbusOutput_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,

}



impl Default for SetModbusOutput_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::SetModbusOutput_Response::default())
  }
}

impl rosidl_runtime_rs::Message for SetModbusOutput_Response {
  type RmwMsg = super::srv::rmw::SetModbusOutput_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        success: msg.success,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      success: msg.success,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      success: msg.success,
    }
  }
}


// Corresponds to dsr_msgs2__srv__GetModbusInput_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetModbusInput_Request {
    /// modbus signal symbol
    pub name: std::string::String,

}



impl Default for GetModbusInput_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::GetModbusInput_Request::default())
  }
}

impl rosidl_runtime_rs::Message for GetModbusInput_Request {
  type RmwMsg = super::srv::rmw::GetModbusInput_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        name: msg.name.as_str().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        name: msg.name.as_str().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      name: msg.name.to_string(),
    }
  }
}


// Corresponds to dsr_msgs2__srv__GetModbusInput_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetModbusInput_Response {
    /// modbus signal value
    pub value: i32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,

}



impl Default for GetModbusInput_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::GetModbusInput_Response::default())
  }
}

impl rosidl_runtime_rs::Message for GetModbusInput_Response {
  type RmwMsg = super::srv::rmw::GetModbusInput_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        value: msg.value,
        success: msg.success,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      value: msg.value,
      success: msg.success,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      value: msg.value,
      success: msg.success,
    }
  }
}


// Corresponds to dsr_msgs2__srv__DrlStart_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct DrlStart_Request {
    /// Robot System Mode 0 : Real, 1 : virtual
    pub robot_system: i8,

    /// drl code
    pub code: std::string::String,

}



impl Default for DrlStart_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::DrlStart_Request::default())
  }
}

impl rosidl_runtime_rs::Message for DrlStart_Request {
  type RmwMsg = super::srv::rmw::DrlStart_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        robot_system: msg.robot_system,
        code: msg.code.as_str().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      robot_system: msg.robot_system,
        code: msg.code.as_str().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      robot_system: msg.robot_system,
      code: msg.code.to_string(),
    }
  }
}


// Corresponds to dsr_msgs2__srv__DrlStart_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct DrlStart_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,

}



impl Default for DrlStart_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::DrlStart_Response::default())
  }
}

impl rosidl_runtime_rs::Message for DrlStart_Response {
  type RmwMsg = super::srv::rmw::DrlStart_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        success: msg.success,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      success: msg.success,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      success: msg.success,
    }
  }
}


// Corresponds to dsr_msgs2__srv__DrlStop_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct DrlStop_Request {
    /// <STOP_TYPE> stop_mode
    pub stop_mode: i8,

}



impl Default for DrlStop_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::DrlStop_Request::default())
  }
}

impl rosidl_runtime_rs::Message for DrlStop_Request {
  type RmwMsg = super::srv::rmw::DrlStop_Request;

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


// Corresponds to dsr_msgs2__srv__DrlStop_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct DrlStop_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,

}



impl Default for DrlStop_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::DrlStop_Response::default())
  }
}

impl rosidl_runtime_rs::Message for DrlStop_Response {
  type RmwMsg = super::srv::rmw::DrlStop_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        success: msg.success,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      success: msg.success,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      success: msg.success,
    }
  }
}


// Corresponds to dsr_msgs2__srv__DrlPause_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct DrlPause_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub structure_needs_at_least_one_member: u8,

}



impl Default for DrlPause_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::DrlPause_Request::default())
  }
}

impl rosidl_runtime_rs::Message for DrlPause_Request {
  type RmwMsg = super::srv::rmw::DrlPause_Request;

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


// Corresponds to dsr_msgs2__srv__DrlPause_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct DrlPause_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,

}



impl Default for DrlPause_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::DrlPause_Response::default())
  }
}

impl rosidl_runtime_rs::Message for DrlPause_Response {
  type RmwMsg = super::srv::rmw::DrlPause_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        success: msg.success,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      success: msg.success,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      success: msg.success,
    }
  }
}


// Corresponds to dsr_msgs2__srv__DrlResume_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct DrlResume_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub structure_needs_at_least_one_member: u8,

}



impl Default for DrlResume_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::DrlResume_Request::default())
  }
}

impl rosidl_runtime_rs::Message for DrlResume_Request {
  type RmwMsg = super::srv::rmw::DrlResume_Request;

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


// Corresponds to dsr_msgs2__srv__DrlResume_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct DrlResume_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,

}



impl Default for DrlResume_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::DrlResume_Response::default())
  }
}

impl rosidl_runtime_rs::Message for DrlResume_Response {
  type RmwMsg = super::srv::rmw::DrlResume_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        success: msg.success,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      success: msg.success,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      success: msg.success,
    }
  }
}


// Corresponds to dsr_msgs2__srv__GetDrlState_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetDrlState_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub structure_needs_at_least_one_member: u8,

}



impl Default for GetDrlState_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::GetDrlState_Request::default())
  }
}

impl rosidl_runtime_rs::Message for GetDrlState_Request {
  type RmwMsg = super::srv::rmw::GetDrlState_Request;

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


// Corresponds to dsr_msgs2__srv__GetDrlState_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetDrlState_Response {
    /// <DRL_PROGRAM_STATE>
    pub drl_state: i8,


    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,

}



impl Default for GetDrlState_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::GetDrlState_Response::default())
  }
}

impl rosidl_runtime_rs::Message for GetDrlState_Response {
  type RmwMsg = super::srv::rmw::GetDrlState_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        drl_state: msg.drl_state,
        success: msg.success,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      drl_state: msg.drl_state,
      success: msg.success,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      drl_state: msg.drl_state,
      success: msg.success,
    }
  }
}


// Corresponds to dsr_msgs2__srv__Robotiq2FClose_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct Robotiq2FClose_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub structure_needs_at_least_one_member: u8,

}



impl Default for Robotiq2FClose_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::Robotiq2FClose_Request::default())
  }
}

impl rosidl_runtime_rs::Message for Robotiq2FClose_Request {
  type RmwMsg = super::srv::rmw::Robotiq2FClose_Request;

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


// Corresponds to dsr_msgs2__srv__Robotiq2FClose_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct Robotiq2FClose_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,

}



impl Default for Robotiq2FClose_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::Robotiq2FClose_Response::default())
  }
}

impl rosidl_runtime_rs::Message for Robotiq2FClose_Response {
  type RmwMsg = super::srv::rmw::Robotiq2FClose_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        success: msg.success,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      success: msg.success,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      success: msg.success,
    }
  }
}


// Corresponds to dsr_msgs2__srv__Robotiq2FOpen_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct Robotiq2FOpen_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub structure_needs_at_least_one_member: u8,

}



impl Default for Robotiq2FOpen_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::Robotiq2FOpen_Request::default())
  }
}

impl rosidl_runtime_rs::Message for Robotiq2FOpen_Request {
  type RmwMsg = super::srv::rmw::Robotiq2FOpen_Request;

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


// Corresponds to dsr_msgs2__srv__Robotiq2FOpen_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct Robotiq2FOpen_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,

}



impl Default for Robotiq2FOpen_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::Robotiq2FOpen_Response::default())
  }
}

impl rosidl_runtime_rs::Message for Robotiq2FOpen_Response {
  type RmwMsg = super::srv::rmw::Robotiq2FOpen_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        success: msg.success,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      success: msg.success,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      success: msg.success,
    }
  }
}


// Corresponds to dsr_msgs2__srv__Robotiq2FMove_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct Robotiq2FMove_Request {
    /// 0.0(open) ~ 0.8(close)
    pub width: f64,

}



impl Default for Robotiq2FMove_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::Robotiq2FMove_Request::default())
  }
}

impl rosidl_runtime_rs::Message for Robotiq2FMove_Request {
  type RmwMsg = super::srv::rmw::Robotiq2FMove_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        width: msg.width,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      width: msg.width,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      width: msg.width,
    }
  }
}


// Corresponds to dsr_msgs2__srv__Robotiq2FMove_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct Robotiq2FMove_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,

}



impl Default for Robotiq2FMove_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::Robotiq2FMove_Response::default())
  }
}

impl rosidl_runtime_rs::Message for Robotiq2FMove_Response {
  type RmwMsg = super::srv::rmw::Robotiq2FMove_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        success: msg.success,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      success: msg.success,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      success: msg.success,
    }
  }
}


// Corresponds to dsr_msgs2__srv__SerialSendData_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SerialSendData_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub data: std::string::String,

}



impl Default for SerialSendData_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::SerialSendData_Request::default())
  }
}

impl rosidl_runtime_rs::Message for SerialSendData_Request {
  type RmwMsg = super::srv::rmw::SerialSendData_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        data: msg.data.as_str().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        data: msg.data.as_str().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      data: msg.data.to_string(),
    }
  }
}


// Corresponds to dsr_msgs2__srv__SerialSendData_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SerialSendData_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,

}



impl Default for SerialSendData_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::SerialSendData_Response::default())
  }
}

impl rosidl_runtime_rs::Message for SerialSendData_Response {
  type RmwMsg = super::srv::rmw::SerialSendData_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        success: msg.success,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      success: msg.success,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      success: msg.success,
    }
  }
}


// Corresponds to dsr_msgs2__srv__FlangeSerialOpen_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct FlangeSerialOpen_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub port: i32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub baudrate: i32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub bytesize: i32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub parity: i32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub stopbits: i32,

}



impl Default for FlangeSerialOpen_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::FlangeSerialOpen_Request::default())
  }
}

impl rosidl_runtime_rs::Message for FlangeSerialOpen_Request {
  type RmwMsg = super::srv::rmw::FlangeSerialOpen_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        port: msg.port,
        baudrate: msg.baudrate,
        bytesize: msg.bytesize,
        parity: msg.parity,
        stopbits: msg.stopbits,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      port: msg.port,
      baudrate: msg.baudrate,
      bytesize: msg.bytesize,
      parity: msg.parity,
      stopbits: msg.stopbits,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      port: msg.port,
      baudrate: msg.baudrate,
      bytesize: msg.bytesize,
      parity: msg.parity,
      stopbits: msg.stopbits,
    }
  }
}


// Corresponds to dsr_msgs2__srv__FlangeSerialOpen_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct FlangeSerialOpen_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,

}



impl Default for FlangeSerialOpen_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::FlangeSerialOpen_Response::default())
  }
}

impl rosidl_runtime_rs::Message for FlangeSerialOpen_Response {
  type RmwMsg = super::srv::rmw::FlangeSerialOpen_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        success: msg.success,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      success: msg.success,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      success: msg.success,
    }
  }
}


// Corresponds to dsr_msgs2__srv__FlangeSerialClose_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct FlangeSerialClose_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub port: i32,

}



impl Default for FlangeSerialClose_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::FlangeSerialClose_Request::default())
  }
}

impl rosidl_runtime_rs::Message for FlangeSerialClose_Request {
  type RmwMsg = super::srv::rmw::FlangeSerialClose_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        port: msg.port,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      port: msg.port,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      port: msg.port,
    }
  }
}


// Corresponds to dsr_msgs2__srv__FlangeSerialClose_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct FlangeSerialClose_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,

}



impl Default for FlangeSerialClose_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::FlangeSerialClose_Response::default())
  }
}

impl rosidl_runtime_rs::Message for FlangeSerialClose_Response {
  type RmwMsg = super::srv::rmw::FlangeSerialClose_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        success: msg.success,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      success: msg.success,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      success: msg.success,
    }
  }
}


// Corresponds to dsr_msgs2__srv__FlangeSerialWrite_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct FlangeSerialWrite_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub port: i32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub data: Vec<u8>,

}



impl Default for FlangeSerialWrite_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::FlangeSerialWrite_Request::default())
  }
}

impl rosidl_runtime_rs::Message for FlangeSerialWrite_Request {
  type RmwMsg = super::srv::rmw::FlangeSerialWrite_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        port: msg.port,
        data: msg.data.into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      port: msg.port,
        data: msg.data.as_slice().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      port: msg.port,
      data: msg.data
          .into_iter()
          .collect(),
    }
  }
}


// Corresponds to dsr_msgs2__srv__FlangeSerialWrite_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct FlangeSerialWrite_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,

}



impl Default for FlangeSerialWrite_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::FlangeSerialWrite_Response::default())
  }
}

impl rosidl_runtime_rs::Message for FlangeSerialWrite_Response {
  type RmwMsg = super::srv::rmw::FlangeSerialWrite_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        success: msg.success,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      success: msg.success,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      success: msg.success,
    }
  }
}


// Corresponds to dsr_msgs2__srv__FlangeSerialRead_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct FlangeSerialRead_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub port: i32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub timeout: f32,

}



impl Default for FlangeSerialRead_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::FlangeSerialRead_Request::default())
  }
}

impl rosidl_runtime_rs::Message for FlangeSerialRead_Request {
  type RmwMsg = super::srv::rmw::FlangeSerialRead_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        port: msg.port,
        timeout: msg.timeout,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      port: msg.port,
      timeout: msg.timeout,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      port: msg.port,
      timeout: msg.timeout,
    }
  }
}


// Corresponds to dsr_msgs2__srv__FlangeSerialRead_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct FlangeSerialRead_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub size: i32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub data: Vec<u8>,

}



impl Default for FlangeSerialRead_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::FlangeSerialRead_Response::default())
  }
}

impl rosidl_runtime_rs::Message for FlangeSerialRead_Response {
  type RmwMsg = super::srv::rmw::FlangeSerialRead_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        success: msg.success,
        size: msg.size,
        data: msg.data.into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      success: msg.success,
      size: msg.size,
        data: msg.data.as_slice().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      success: msg.success,
      size: msg.size,
      data: msg.data
          .into_iter()
          .collect(),
    }
  }
}


// Corresponds to dsr_msgs2__srv__ConnectRtControl_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ConnectRtControl_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub ip_address: std::string::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub port: u32,

}



impl Default for ConnectRtControl_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::ConnectRtControl_Request::default())
  }
}

impl rosidl_runtime_rs::Message for ConnectRtControl_Request {
  type RmwMsg = super::srv::rmw::ConnectRtControl_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        ip_address: msg.ip_address.as_str().into(),
        port: msg.port,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        ip_address: msg.ip_address.as_str().into(),
      port: msg.port,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      ip_address: msg.ip_address.to_string(),
      port: msg.port,
    }
  }
}


// Corresponds to dsr_msgs2__srv__ConnectRtControl_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ConnectRtControl_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,

}



impl Default for ConnectRtControl_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::ConnectRtControl_Response::default())
  }
}

impl rosidl_runtime_rs::Message for ConnectRtControl_Response {
  type RmwMsg = super::srv::rmw::ConnectRtControl_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        success: msg.success,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      success: msg.success,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      success: msg.success,
    }
  }
}


// Corresponds to dsr_msgs2__srv__DisconnectRtControl_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct DisconnectRtControl_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub structure_needs_at_least_one_member: u8,

}



impl Default for DisconnectRtControl_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::DisconnectRtControl_Request::default())
  }
}

impl rosidl_runtime_rs::Message for DisconnectRtControl_Request {
  type RmwMsg = super::srv::rmw::DisconnectRtControl_Request;

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


// Corresponds to dsr_msgs2__srv__DisconnectRtControl_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct DisconnectRtControl_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,

}



impl Default for DisconnectRtControl_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::DisconnectRtControl_Response::default())
  }
}

impl rosidl_runtime_rs::Message for DisconnectRtControl_Response {
  type RmwMsg = super::srv::rmw::DisconnectRtControl_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        success: msg.success,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      success: msg.success,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      success: msg.success,
    }
  }
}


// Corresponds to dsr_msgs2__srv__GetRtControlInputDataList_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetRtControlInputDataList_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub version: std::string::String,

}



impl Default for GetRtControlInputDataList_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::GetRtControlInputDataList_Request::default())
  }
}

impl rosidl_runtime_rs::Message for GetRtControlInputDataList_Request {
  type RmwMsg = super::srv::rmw::GetRtControlInputDataList_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        version: msg.version.as_str().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        version: msg.version.as_str().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      version: msg.version.to_string(),
    }
  }
}


// Corresponds to dsr_msgs2__srv__GetRtControlInputDataList_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetRtControlInputDataList_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub data: std::string::String,

}



impl Default for GetRtControlInputDataList_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::GetRtControlInputDataList_Response::default())
  }
}

impl rosidl_runtime_rs::Message for GetRtControlInputDataList_Response {
  type RmwMsg = super::srv::rmw::GetRtControlInputDataList_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        success: msg.success,
        data: msg.data.as_str().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      success: msg.success,
        data: msg.data.as_str().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      success: msg.success,
      data: msg.data.to_string(),
    }
  }
}


// Corresponds to dsr_msgs2__srv__GetRtControlInputVersionList_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetRtControlInputVersionList_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub structure_needs_at_least_one_member: u8,

}



impl Default for GetRtControlInputVersionList_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::GetRtControlInputVersionList_Request::default())
  }
}

impl rosidl_runtime_rs::Message for GetRtControlInputVersionList_Request {
  type RmwMsg = super::srv::rmw::GetRtControlInputVersionList_Request;

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


// Corresponds to dsr_msgs2__srv__GetRtControlInputVersionList_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetRtControlInputVersionList_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub version: std::string::String,

}



impl Default for GetRtControlInputVersionList_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::GetRtControlInputVersionList_Response::default())
  }
}

impl rosidl_runtime_rs::Message for GetRtControlInputVersionList_Response {
  type RmwMsg = super::srv::rmw::GetRtControlInputVersionList_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        success: msg.success,
        version: msg.version.as_str().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      success: msg.success,
        version: msg.version.as_str().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      success: msg.success,
      version: msg.version.to_string(),
    }
  }
}


// Corresponds to dsr_msgs2__srv__GetRtControlOutputDataList_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetRtControlOutputDataList_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub version: std::string::String,

}



impl Default for GetRtControlOutputDataList_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::GetRtControlOutputDataList_Request::default())
  }
}

impl rosidl_runtime_rs::Message for GetRtControlOutputDataList_Request {
  type RmwMsg = super::srv::rmw::GetRtControlOutputDataList_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        version: msg.version.as_str().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        version: msg.version.as_str().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      version: msg.version.to_string(),
    }
  }
}


// Corresponds to dsr_msgs2__srv__GetRtControlOutputDataList_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetRtControlOutputDataList_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub data: std::string::String,

}



impl Default for GetRtControlOutputDataList_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::GetRtControlOutputDataList_Response::default())
  }
}

impl rosidl_runtime_rs::Message for GetRtControlOutputDataList_Response {
  type RmwMsg = super::srv::rmw::GetRtControlOutputDataList_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        success: msg.success,
        data: msg.data.as_str().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      success: msg.success,
        data: msg.data.as_str().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      success: msg.success,
      data: msg.data.to_string(),
    }
  }
}


// Corresponds to dsr_msgs2__srv__GetRtControlOutputVersionList_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetRtControlOutputVersionList_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub structure_needs_at_least_one_member: u8,

}



impl Default for GetRtControlOutputVersionList_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::GetRtControlOutputVersionList_Request::default())
  }
}

impl rosidl_runtime_rs::Message for GetRtControlOutputVersionList_Request {
  type RmwMsg = super::srv::rmw::GetRtControlOutputVersionList_Request;

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


// Corresponds to dsr_msgs2__srv__GetRtControlOutputVersionList_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetRtControlOutputVersionList_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub version: std::string::String,

}



impl Default for GetRtControlOutputVersionList_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::GetRtControlOutputVersionList_Response::default())
  }
}

impl rosidl_runtime_rs::Message for GetRtControlOutputVersionList_Response {
  type RmwMsg = super::srv::rmw::GetRtControlOutputVersionList_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        success: msg.success,
        version: msg.version.as_str().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      success: msg.success,
        version: msg.version.as_str().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      success: msg.success,
      version: msg.version.to_string(),
    }
  }
}


// Corresponds to dsr_msgs2__srv__ReadDataRt_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ReadDataRt_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub structure_needs_at_least_one_member: u8,

}



impl Default for ReadDataRt_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::ReadDataRt_Request::default())
  }
}

impl rosidl_runtime_rs::Message for ReadDataRt_Request {
  type RmwMsg = super::srv::rmw::ReadDataRt_Request;

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


// Corresponds to dsr_msgs2__srv__ReadDataRt_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ReadDataRt_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub data: super::msg::RobotStateRt,

}



impl Default for ReadDataRt_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::ReadDataRt_Response::default())
  }
}

impl rosidl_runtime_rs::Message for ReadDataRt_Response {
  type RmwMsg = super::srv::rmw::ReadDataRt_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        data: super::msg::RobotStateRt::into_rmw_message(std::borrow::Cow::Owned(msg.data)).into_owned(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        data: super::msg::RobotStateRt::into_rmw_message(std::borrow::Cow::Borrowed(&msg.data)).into_owned(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      data: super::msg::RobotStateRt::from_rmw_message(msg.data),
    }
  }
}


// Corresponds to dsr_msgs2__srv__SetAccjRt_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SetAccjRt_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub acc: [f64; 6],

}



impl Default for SetAccjRt_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::SetAccjRt_Request::default())
  }
}

impl rosidl_runtime_rs::Message for SetAccjRt_Request {
  type RmwMsg = super::srv::rmw::SetAccjRt_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        acc: msg.acc,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        acc: msg.acc,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      acc: msg.acc,
    }
  }
}


// Corresponds to dsr_msgs2__srv__SetAccjRt_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SetAccjRt_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,

}



impl Default for SetAccjRt_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::SetAccjRt_Response::default())
  }
}

impl rosidl_runtime_rs::Message for SetAccjRt_Response {
  type RmwMsg = super::srv::rmw::SetAccjRt_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        success: msg.success,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      success: msg.success,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      success: msg.success,
    }
  }
}


// Corresponds to dsr_msgs2__srv__SetAccxRt_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SetAccxRt_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub trans: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub rotation: f64,

}



impl Default for SetAccxRt_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::SetAccxRt_Request::default())
  }
}

impl rosidl_runtime_rs::Message for SetAccxRt_Request {
  type RmwMsg = super::srv::rmw::SetAccxRt_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        trans: msg.trans,
        rotation: msg.rotation,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      trans: msg.trans,
      rotation: msg.rotation,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      trans: msg.trans,
      rotation: msg.rotation,
    }
  }
}


// Corresponds to dsr_msgs2__srv__SetAccxRt_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SetAccxRt_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,

}



impl Default for SetAccxRt_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::SetAccxRt_Response::default())
  }
}

impl rosidl_runtime_rs::Message for SetAccxRt_Response {
  type RmwMsg = super::srv::rmw::SetAccxRt_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        success: msg.success,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      success: msg.success,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      success: msg.success,
    }
  }
}


// Corresponds to dsr_msgs2__srv__SetRtControlInput_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SetRtControlInput_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub version: std::string::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub period: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub loss: i32,

}



impl Default for SetRtControlInput_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::SetRtControlInput_Request::default())
  }
}

impl rosidl_runtime_rs::Message for SetRtControlInput_Request {
  type RmwMsg = super::srv::rmw::SetRtControlInput_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        version: msg.version.as_str().into(),
        period: msg.period,
        loss: msg.loss,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        version: msg.version.as_str().into(),
      period: msg.period,
      loss: msg.loss,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      version: msg.version.to_string(),
      period: msg.period,
      loss: msg.loss,
    }
  }
}


// Corresponds to dsr_msgs2__srv__SetRtControlInput_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SetRtControlInput_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,

}



impl Default for SetRtControlInput_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::SetRtControlInput_Response::default())
  }
}

impl rosidl_runtime_rs::Message for SetRtControlInput_Response {
  type RmwMsg = super::srv::rmw::SetRtControlInput_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        success: msg.success,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      success: msg.success,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      success: msg.success,
    }
  }
}


// Corresponds to dsr_msgs2__srv__SetRtControlOutput_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SetRtControlOutput_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub version: std::string::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub period: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub loss: i32,

}



impl Default for SetRtControlOutput_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::SetRtControlOutput_Request::default())
  }
}

impl rosidl_runtime_rs::Message for SetRtControlOutput_Request {
  type RmwMsg = super::srv::rmw::SetRtControlOutput_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        version: msg.version.as_str().into(),
        period: msg.period,
        loss: msg.loss,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        version: msg.version.as_str().into(),
      period: msg.period,
      loss: msg.loss,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      version: msg.version.to_string(),
      period: msg.period,
      loss: msg.loss,
    }
  }
}


// Corresponds to dsr_msgs2__srv__SetRtControlOutput_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SetRtControlOutput_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,

}



impl Default for SetRtControlOutput_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::SetRtControlOutput_Response::default())
  }
}

impl rosidl_runtime_rs::Message for SetRtControlOutput_Response {
  type RmwMsg = super::srv::rmw::SetRtControlOutput_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        success: msg.success,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      success: msg.success,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      success: msg.success,
    }
  }
}


// Corresponds to dsr_msgs2__srv__SetVeljRt_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SetVeljRt_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub vel: [f64; 6],

}



impl Default for SetVeljRt_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::SetVeljRt_Request::default())
  }
}

impl rosidl_runtime_rs::Message for SetVeljRt_Request {
  type RmwMsg = super::srv::rmw::SetVeljRt_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        vel: msg.vel,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        vel: msg.vel,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      vel: msg.vel,
    }
  }
}


// Corresponds to dsr_msgs2__srv__SetVeljRt_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SetVeljRt_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,

}



impl Default for SetVeljRt_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::SetVeljRt_Response::default())
  }
}

impl rosidl_runtime_rs::Message for SetVeljRt_Response {
  type RmwMsg = super::srv::rmw::SetVeljRt_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        success: msg.success,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      success: msg.success,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      success: msg.success,
    }
  }
}


// Corresponds to dsr_msgs2__srv__SetVelxRt_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SetVelxRt_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub trans: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub rotation: f64,

}



impl Default for SetVelxRt_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::SetVelxRt_Request::default())
  }
}

impl rosidl_runtime_rs::Message for SetVelxRt_Request {
  type RmwMsg = super::srv::rmw::SetVelxRt_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        trans: msg.trans,
        rotation: msg.rotation,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      trans: msg.trans,
      rotation: msg.rotation,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      trans: msg.trans,
      rotation: msg.rotation,
    }
  }
}


// Corresponds to dsr_msgs2__srv__SetVelxRt_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SetVelxRt_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,

}



impl Default for SetVelxRt_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::SetVelxRt_Response::default())
  }
}

impl rosidl_runtime_rs::Message for SetVelxRt_Response {
  type RmwMsg = super::srv::rmw::SetVelxRt_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        success: msg.success,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      success: msg.success,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      success: msg.success,
    }
  }
}


// Corresponds to dsr_msgs2__srv__StartRtControl_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct StartRtControl_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub structure_needs_at_least_one_member: u8,

}



impl Default for StartRtControl_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::StartRtControl_Request::default())
  }
}

impl rosidl_runtime_rs::Message for StartRtControl_Request {
  type RmwMsg = super::srv::rmw::StartRtControl_Request;

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


// Corresponds to dsr_msgs2__srv__StartRtControl_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct StartRtControl_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,

}



impl Default for StartRtControl_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::StartRtControl_Response::default())
  }
}

impl rosidl_runtime_rs::Message for StartRtControl_Response {
  type RmwMsg = super::srv::rmw::StartRtControl_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        success: msg.success,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      success: msg.success,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      success: msg.success,
    }
  }
}


// Corresponds to dsr_msgs2__srv__StopRtControl_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct StopRtControl_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub structure_needs_at_least_one_member: u8,

}



impl Default for StopRtControl_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::StopRtControl_Request::default())
  }
}

impl rosidl_runtime_rs::Message for StopRtControl_Request {
  type RmwMsg = super::srv::rmw::StopRtControl_Request;

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


// Corresponds to dsr_msgs2__srv__StopRtControl_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct StopRtControl_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,

}



impl Default for StopRtControl_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::StopRtControl_Response::default())
  }
}

impl rosidl_runtime_rs::Message for StopRtControl_Response {
  type RmwMsg = super::srv::rmw::StopRtControl_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        success: msg.success,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      success: msg.success,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      success: msg.success,
    }
  }
}


// Corresponds to dsr_msgs2__srv__WriteDataRt_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct WriteDataRt_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub external_force_torque: [f64; 6],


    // This member is not documented.
    #[allow(missing_docs)]
    pub external_digital_input: i32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub external_digital_output: i32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub external_analog_input: [f64; 6],


    // This member is not documented.
    #[allow(missing_docs)]
    pub external_analog_output: [f64; 6],

}



impl Default for WriteDataRt_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::WriteDataRt_Request::default())
  }
}

impl rosidl_runtime_rs::Message for WriteDataRt_Request {
  type RmwMsg = super::srv::rmw::WriteDataRt_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        external_force_torque: msg.external_force_torque,
        external_digital_input: msg.external_digital_input,
        external_digital_output: msg.external_digital_output,
        external_analog_input: msg.external_analog_input,
        external_analog_output: msg.external_analog_output,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        external_force_torque: msg.external_force_torque,
      external_digital_input: msg.external_digital_input,
      external_digital_output: msg.external_digital_output,
        external_analog_input: msg.external_analog_input,
        external_analog_output: msg.external_analog_output,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      external_force_torque: msg.external_force_torque,
      external_digital_input: msg.external_digital_input,
      external_digital_output: msg.external_digital_output,
      external_analog_input: msg.external_analog_input,
      external_analog_output: msg.external_analog_output,
    }
  }
}


// Corresponds to dsr_msgs2__srv__WriteDataRt_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct WriteDataRt_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,

}



impl Default for WriteDataRt_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::WriteDataRt_Response::default())
  }
}

impl rosidl_runtime_rs::Message for WriteDataRt_Response {
  type RmwMsg = super::srv::rmw::WriteDataRt_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        success: msg.success,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      success: msg.success,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      success: msg.success,
    }
  }
}






#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__SetRobotMode() -> *const std::ffi::c_void;
}

// Corresponds to dsr_msgs2__srv__SetRobotMode
#[allow(missing_docs, non_camel_case_types)]
pub struct SetRobotMode;

impl rosidl_runtime_rs::Service for SetRobotMode {
    type Request = SetRobotMode_Request;
    type Response = SetRobotMode_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__SetRobotMode() }
    }
}




#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__GetRobotMode() -> *const std::ffi::c_void;
}

// Corresponds to dsr_msgs2__srv__GetRobotMode
#[allow(missing_docs, non_camel_case_types)]
pub struct GetRobotMode;

impl rosidl_runtime_rs::Service for GetRobotMode {
    type Request = GetRobotMode_Request;
    type Response = GetRobotMode_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__GetRobotMode() }
    }
}




#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__SetRobotSystem() -> *const std::ffi::c_void;
}

// Corresponds to dsr_msgs2__srv__SetRobotSystem
#[allow(missing_docs, non_camel_case_types)]
pub struct SetRobotSystem;

impl rosidl_runtime_rs::Service for SetRobotSystem {
    type Request = SetRobotSystem_Request;
    type Response = SetRobotSystem_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__SetRobotSystem() }
    }
}




#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__GetRobotSystem() -> *const std::ffi::c_void;
}

// Corresponds to dsr_msgs2__srv__GetRobotSystem
#[allow(missing_docs, non_camel_case_types)]
pub struct GetRobotSystem;

impl rosidl_runtime_rs::Service for GetRobotSystem {
    type Request = GetRobotSystem_Request;
    type Response = GetRobotSystem_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__GetRobotSystem() }
    }
}




#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__SetRobotSpeedMode() -> *const std::ffi::c_void;
}

// Corresponds to dsr_msgs2__srv__SetRobotSpeedMode
#[allow(missing_docs, non_camel_case_types)]
pub struct SetRobotSpeedMode;

impl rosidl_runtime_rs::Service for SetRobotSpeedMode {
    type Request = SetRobotSpeedMode_Request;
    type Response = SetRobotSpeedMode_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__SetRobotSpeedMode() }
    }
}




#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__GetRobotSpeedMode() -> *const std::ffi::c_void;
}

// Corresponds to dsr_msgs2__srv__GetRobotSpeedMode
#[allow(missing_docs, non_camel_case_types)]
pub struct GetRobotSpeedMode;

impl rosidl_runtime_rs::Service for GetRobotSpeedMode {
    type Request = GetRobotSpeedMode_Request;
    type Response = GetRobotSpeedMode_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__GetRobotSpeedMode() }
    }
}




#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__GetCurrentPose() -> *const std::ffi::c_void;
}

// Corresponds to dsr_msgs2__srv__GetCurrentPose
#[allow(missing_docs, non_camel_case_types)]
pub struct GetCurrentPose;

impl rosidl_runtime_rs::Service for GetCurrentPose {
    type Request = GetCurrentPose_Request;
    type Response = GetCurrentPose_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__GetCurrentPose() }
    }
}




#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__SetSafeStopResetType() -> *const std::ffi::c_void;
}

// Corresponds to dsr_msgs2__srv__SetSafeStopResetType
#[allow(missing_docs, non_camel_case_types)]
pub struct SetSafeStopResetType;

impl rosidl_runtime_rs::Service for SetSafeStopResetType {
    type Request = SetSafeStopResetType_Request;
    type Response = SetSafeStopResetType_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__SetSafeStopResetType() }
    }
}




#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__GetLastAlarm() -> *const std::ffi::c_void;
}

// Corresponds to dsr_msgs2__srv__GetLastAlarm
#[allow(missing_docs, non_camel_case_types)]
pub struct GetLastAlarm;

impl rosidl_runtime_rs::Service for GetLastAlarm {
    type Request = GetLastAlarm_Request;
    type Response = GetLastAlarm_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__GetLastAlarm() }
    }
}




#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__GetRobotState() -> *const std::ffi::c_void;
}

// Corresponds to dsr_msgs2__srv__GetRobotState
#[allow(missing_docs, non_camel_case_types)]
pub struct GetRobotState;

impl rosidl_runtime_rs::Service for GetRobotState {
    type Request = GetRobotState_Request;
    type Response = GetRobotState_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__GetRobotState() }
    }
}




#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__ServoOff() -> *const std::ffi::c_void;
}

// Corresponds to dsr_msgs2__srv__ServoOff
#[allow(missing_docs, non_camel_case_types)]
pub struct ServoOff;

impl rosidl_runtime_rs::Service for ServoOff {
    type Request = ServoOff_Request;
    type Response = ServoOff_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__ServoOff() }
    }
}




#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__SetRobotControl() -> *const std::ffi::c_void;
}

// Corresponds to dsr_msgs2__srv__SetRobotControl
#[allow(missing_docs, non_camel_case_types)]
pub struct SetRobotControl;

impl rosidl_runtime_rs::Service for SetRobotControl {
    type Request = SetRobotControl_Request;
    type Response = SetRobotControl_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__SetRobotControl() }
    }
}




#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__ChangeCollisionSensitivity() -> *const std::ffi::c_void;
}

// Corresponds to dsr_msgs2__srv__ChangeCollisionSensitivity
#[allow(missing_docs, non_camel_case_types)]
pub struct ChangeCollisionSensitivity;

impl rosidl_runtime_rs::Service for ChangeCollisionSensitivity {
    type Request = ChangeCollisionSensitivity_Request;
    type Response = ChangeCollisionSensitivity_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__ChangeCollisionSensitivity() }
    }
}




#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__SetSafetyMode() -> *const std::ffi::c_void;
}

// Corresponds to dsr_msgs2__srv__SetSafetyMode
#[allow(missing_docs, non_camel_case_types)]
pub struct SetSafetyMode;

impl rosidl_runtime_rs::Service for SetSafetyMode {
    type Request = SetSafetyMode_Request;
    type Response = SetSafetyMode_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__SetSafetyMode() }
    }
}




#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__GetRobotLinkInfo() -> *const std::ffi::c_void;
}

// Corresponds to dsr_msgs2__srv__GetRobotLinkInfo
#[allow(missing_docs, non_camel_case_types)]
pub struct GetRobotLinkInfo;

impl rosidl_runtime_rs::Service for GetRobotLinkInfo {
    type Request = GetRobotLinkInfo_Request;
    type Response = GetRobotLinkInfo_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__GetRobotLinkInfo() }
    }
}




#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__MoveJoint() -> *const std::ffi::c_void;
}

// Corresponds to dsr_msgs2__srv__MoveJoint
#[allow(missing_docs, non_camel_case_types)]
pub struct MoveJoint;

impl rosidl_runtime_rs::Service for MoveJoint {
    type Request = MoveJoint_Request;
    type Response = MoveJoint_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__MoveJoint() }
    }
}




#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__MoveLine() -> *const std::ffi::c_void;
}

// Corresponds to dsr_msgs2__srv__MoveLine
#[allow(missing_docs, non_camel_case_types)]
pub struct MoveLine;

impl rosidl_runtime_rs::Service for MoveLine {
    type Request = MoveLine_Request;
    type Response = MoveLine_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__MoveLine() }
    }
}




#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__MoveJointx() -> *const std::ffi::c_void;
}

// Corresponds to dsr_msgs2__srv__MoveJointx
#[allow(missing_docs, non_camel_case_types)]
pub struct MoveJointx;

impl rosidl_runtime_rs::Service for MoveJointx {
    type Request = MoveJointx_Request;
    type Response = MoveJointx_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__MoveJointx() }
    }
}




#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__MoveCircle() -> *const std::ffi::c_void;
}

// Corresponds to dsr_msgs2__srv__MoveCircle
#[allow(missing_docs, non_camel_case_types)]
pub struct MoveCircle;

impl rosidl_runtime_rs::Service for MoveCircle {
    type Request = MoveCircle_Request;
    type Response = MoveCircle_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__MoveCircle() }
    }
}




#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__MoveSplineJoint() -> *const std::ffi::c_void;
}

// Corresponds to dsr_msgs2__srv__MoveSplineJoint
#[allow(missing_docs, non_camel_case_types)]
pub struct MoveSplineJoint;

impl rosidl_runtime_rs::Service for MoveSplineJoint {
    type Request = MoveSplineJoint_Request;
    type Response = MoveSplineJoint_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__MoveSplineJoint() }
    }
}




#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__MoveSplineTask() -> *const std::ffi::c_void;
}

// Corresponds to dsr_msgs2__srv__MoveSplineTask
#[allow(missing_docs, non_camel_case_types)]
pub struct MoveSplineTask;

impl rosidl_runtime_rs::Service for MoveSplineTask {
    type Request = MoveSplineTask_Request;
    type Response = MoveSplineTask_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__MoveSplineTask() }
    }
}




#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__MoveBlending() -> *const std::ffi::c_void;
}

// Corresponds to dsr_msgs2__srv__MoveBlending
#[allow(missing_docs, non_camel_case_types)]
pub struct MoveBlending;

impl rosidl_runtime_rs::Service for MoveBlending {
    type Request = MoveBlending_Request;
    type Response = MoveBlending_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__MoveBlending() }
    }
}




#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__MoveSpiral() -> *const std::ffi::c_void;
}

// Corresponds to dsr_msgs2__srv__MoveSpiral
#[allow(missing_docs, non_camel_case_types)]
pub struct MoveSpiral;

impl rosidl_runtime_rs::Service for MoveSpiral {
    type Request = MoveSpiral_Request;
    type Response = MoveSpiral_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__MoveSpiral() }
    }
}




#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__MovePeriodic() -> *const std::ffi::c_void;
}

// Corresponds to dsr_msgs2__srv__MovePeriodic
#[allow(missing_docs, non_camel_case_types)]
pub struct MovePeriodic;

impl rosidl_runtime_rs::Service for MovePeriodic {
    type Request = MovePeriodic_Request;
    type Response = MovePeriodic_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__MovePeriodic() }
    }
}




#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__MoveWait() -> *const std::ffi::c_void;
}

// Corresponds to dsr_msgs2__srv__MoveWait
#[allow(missing_docs, non_camel_case_types)]
pub struct MoveWait;

impl rosidl_runtime_rs::Service for MoveWait {
    type Request = MoveWait_Request;
    type Response = MoveWait_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__MoveWait() }
    }
}




#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__Jog() -> *const std::ffi::c_void;
}

// Corresponds to dsr_msgs2__srv__Jog
#[allow(missing_docs, non_camel_case_types)]
pub struct Jog;

impl rosidl_runtime_rs::Service for Jog {
    type Request = Jog_Request;
    type Response = Jog_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__Jog() }
    }
}




#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__JogMulti() -> *const std::ffi::c_void;
}

// Corresponds to dsr_msgs2__srv__JogMulti
#[allow(missing_docs, non_camel_case_types)]
pub struct JogMulti;

impl rosidl_runtime_rs::Service for JogMulti {
    type Request = JogMulti_Request;
    type Response = JogMulti_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__JogMulti() }
    }
}




#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__MoveStop() -> *const std::ffi::c_void;
}

// Corresponds to dsr_msgs2__srv__MoveStop
#[allow(missing_docs, non_camel_case_types)]
pub struct MoveStop;

impl rosidl_runtime_rs::Service for MoveStop {
    type Request = MoveStop_Request;
    type Response = MoveStop_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__MoveStop() }
    }
}




#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__MovePause() -> *const std::ffi::c_void;
}

// Corresponds to dsr_msgs2__srv__MovePause
#[allow(missing_docs, non_camel_case_types)]
pub struct MovePause;

impl rosidl_runtime_rs::Service for MovePause {
    type Request = MovePause_Request;
    type Response = MovePause_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__MovePause() }
    }
}




#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__MoveResume() -> *const std::ffi::c_void;
}

// Corresponds to dsr_msgs2__srv__MoveResume
#[allow(missing_docs, non_camel_case_types)]
pub struct MoveResume;

impl rosidl_runtime_rs::Service for MoveResume {
    type Request = MoveResume_Request;
    type Response = MoveResume_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__MoveResume() }
    }
}




#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__Trans() -> *const std::ffi::c_void;
}

// Corresponds to dsr_msgs2__srv__Trans
#[allow(missing_docs, non_camel_case_types)]
pub struct Trans;

impl rosidl_runtime_rs::Service for Trans {
    type Request = Trans_Request;
    type Response = Trans_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__Trans() }
    }
}




#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__Fkin() -> *const std::ffi::c_void;
}

// Corresponds to dsr_msgs2__srv__Fkin
#[allow(missing_docs, non_camel_case_types)]
pub struct Fkin;

impl rosidl_runtime_rs::Service for Fkin {
    type Request = Fkin_Request;
    type Response = Fkin_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__Fkin() }
    }
}




#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__Ikin() -> *const std::ffi::c_void;
}

// Corresponds to dsr_msgs2__srv__Ikin
#[allow(missing_docs, non_camel_case_types)]
pub struct Ikin;

impl rosidl_runtime_rs::Service for Ikin {
    type Request = Ikin_Request;
    type Response = Ikin_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__Ikin() }
    }
}




#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__SetRefCoord() -> *const std::ffi::c_void;
}

// Corresponds to dsr_msgs2__srv__SetRefCoord
#[allow(missing_docs, non_camel_case_types)]
pub struct SetRefCoord;

impl rosidl_runtime_rs::Service for SetRefCoord {
    type Request = SetRefCoord_Request;
    type Response = SetRefCoord_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__SetRefCoord() }
    }
}




#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__MoveHome() -> *const std::ffi::c_void;
}

// Corresponds to dsr_msgs2__srv__MoveHome
#[allow(missing_docs, non_camel_case_types)]
pub struct MoveHome;

impl rosidl_runtime_rs::Service for MoveHome {
    type Request = MoveHome_Request;
    type Response = MoveHome_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__MoveHome() }
    }
}




#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__CheckMotion() -> *const std::ffi::c_void;
}

// Corresponds to dsr_msgs2__srv__CheckMotion
#[allow(missing_docs, non_camel_case_types)]
pub struct CheckMotion;

impl rosidl_runtime_rs::Service for CheckMotion {
    type Request = CheckMotion_Request;
    type Response = CheckMotion_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__CheckMotion() }
    }
}




#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__ChangeOperationSpeed() -> *const std::ffi::c_void;
}

// Corresponds to dsr_msgs2__srv__ChangeOperationSpeed
#[allow(missing_docs, non_camel_case_types)]
pub struct ChangeOperationSpeed;

impl rosidl_runtime_rs::Service for ChangeOperationSpeed {
    type Request = ChangeOperationSpeed_Request;
    type Response = ChangeOperationSpeed_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__ChangeOperationSpeed() }
    }
}




#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__EnableAlterMotion() -> *const std::ffi::c_void;
}

// Corresponds to dsr_msgs2__srv__EnableAlterMotion
#[allow(missing_docs, non_camel_case_types)]
pub struct EnableAlterMotion;

impl rosidl_runtime_rs::Service for EnableAlterMotion {
    type Request = EnableAlterMotion_Request;
    type Response = EnableAlterMotion_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__EnableAlterMotion() }
    }
}




#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__AlterMotion() -> *const std::ffi::c_void;
}

// Corresponds to dsr_msgs2__srv__AlterMotion
#[allow(missing_docs, non_camel_case_types)]
pub struct AlterMotion;

impl rosidl_runtime_rs::Service for AlterMotion {
    type Request = AlterMotion_Request;
    type Response = AlterMotion_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__AlterMotion() }
    }
}




#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__DisableAlterMotion() -> *const std::ffi::c_void;
}

// Corresponds to dsr_msgs2__srv__DisableAlterMotion
#[allow(missing_docs, non_camel_case_types)]
pub struct DisableAlterMotion;

impl rosidl_runtime_rs::Service for DisableAlterMotion {
    type Request = DisableAlterMotion_Request;
    type Response = DisableAlterMotion_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__DisableAlterMotion() }
    }
}




#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__SetSingularityHandling() -> *const std::ffi::c_void;
}

// Corresponds to dsr_msgs2__srv__SetSingularityHandling
#[allow(missing_docs, non_camel_case_types)]
pub struct SetSingularityHandling;

impl rosidl_runtime_rs::Service for SetSingularityHandling {
    type Request = SetSingularityHandling_Request;
    type Response = SetSingularityHandling_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__SetSingularityHandling() }
    }
}




#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__SetSingularHandlingForce() -> *const std::ffi::c_void;
}

// Corresponds to dsr_msgs2__srv__SetSingularHandlingForce
#[allow(missing_docs, non_camel_case_types)]
pub struct SetSingularHandlingForce;

impl rosidl_runtime_rs::Service for SetSingularHandlingForce {
    type Request = SetSingularHandlingForce_Request;
    type Response = SetSingularHandlingForce_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__SetSingularHandlingForce() }
    }
}




#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__GetControlMode() -> *const std::ffi::c_void;
}

// Corresponds to dsr_msgs2__srv__GetControlMode
#[allow(missing_docs, non_camel_case_types)]
pub struct GetControlMode;

impl rosidl_runtime_rs::Service for GetControlMode {
    type Request = GetControlMode_Request;
    type Response = GetControlMode_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__GetControlMode() }
    }
}




#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__GetControlSpace() -> *const std::ffi::c_void;
}

// Corresponds to dsr_msgs2__srv__GetControlSpace
#[allow(missing_docs, non_camel_case_types)]
pub struct GetControlSpace;

impl rosidl_runtime_rs::Service for GetControlSpace {
    type Request = GetControlSpace_Request;
    type Response = GetControlSpace_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__GetControlSpace() }
    }
}




#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__GetCurrentPosj() -> *const std::ffi::c_void;
}

// Corresponds to dsr_msgs2__srv__GetCurrentPosj
#[allow(missing_docs, non_camel_case_types)]
pub struct GetCurrentPosj;

impl rosidl_runtime_rs::Service for GetCurrentPosj {
    type Request = GetCurrentPosj_Request;
    type Response = GetCurrentPosj_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__GetCurrentPosj() }
    }
}




#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__GetDesiredPosj() -> *const std::ffi::c_void;
}

// Corresponds to dsr_msgs2__srv__GetDesiredPosj
#[allow(missing_docs, non_camel_case_types)]
pub struct GetDesiredPosj;

impl rosidl_runtime_rs::Service for GetDesiredPosj {
    type Request = GetDesiredPosj_Request;
    type Response = GetDesiredPosj_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__GetDesiredPosj() }
    }
}




#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__GetCurrentVelj() -> *const std::ffi::c_void;
}

// Corresponds to dsr_msgs2__srv__GetCurrentVelj
#[allow(missing_docs, non_camel_case_types)]
pub struct GetCurrentVelj;

impl rosidl_runtime_rs::Service for GetCurrentVelj {
    type Request = GetCurrentVelj_Request;
    type Response = GetCurrentVelj_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__GetCurrentVelj() }
    }
}




#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__GetDesiredVelj() -> *const std::ffi::c_void;
}

// Corresponds to dsr_msgs2__srv__GetDesiredVelj
#[allow(missing_docs, non_camel_case_types)]
pub struct GetDesiredVelj;

impl rosidl_runtime_rs::Service for GetDesiredVelj {
    type Request = GetDesiredVelj_Request;
    type Response = GetDesiredVelj_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__GetDesiredVelj() }
    }
}




#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__GetCurrentPosx() -> *const std::ffi::c_void;
}

// Corresponds to dsr_msgs2__srv__GetCurrentPosx
#[allow(missing_docs, non_camel_case_types)]
pub struct GetCurrentPosx;

impl rosidl_runtime_rs::Service for GetCurrentPosx {
    type Request = GetCurrentPosx_Request;
    type Response = GetCurrentPosx_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__GetCurrentPosx() }
    }
}




#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__GetCurrentToolFlangePosx() -> *const std::ffi::c_void;
}

// Corresponds to dsr_msgs2__srv__GetCurrentToolFlangePosx
#[allow(missing_docs, non_camel_case_types)]
pub struct GetCurrentToolFlangePosx;

impl rosidl_runtime_rs::Service for GetCurrentToolFlangePosx {
    type Request = GetCurrentToolFlangePosx_Request;
    type Response = GetCurrentToolFlangePosx_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__GetCurrentToolFlangePosx() }
    }
}




#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__GetCurrentVelx() -> *const std::ffi::c_void;
}

// Corresponds to dsr_msgs2__srv__GetCurrentVelx
#[allow(missing_docs, non_camel_case_types)]
pub struct GetCurrentVelx;

impl rosidl_runtime_rs::Service for GetCurrentVelx {
    type Request = GetCurrentVelx_Request;
    type Response = GetCurrentVelx_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__GetCurrentVelx() }
    }
}




#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__GetDesiredPosx() -> *const std::ffi::c_void;
}

// Corresponds to dsr_msgs2__srv__GetDesiredPosx
#[allow(missing_docs, non_camel_case_types)]
pub struct GetDesiredPosx;

impl rosidl_runtime_rs::Service for GetDesiredPosx {
    type Request = GetDesiredPosx_Request;
    type Response = GetDesiredPosx_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__GetDesiredPosx() }
    }
}




#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__GetDesiredVelx() -> *const std::ffi::c_void;
}

// Corresponds to dsr_msgs2__srv__GetDesiredVelx
#[allow(missing_docs, non_camel_case_types)]
pub struct GetDesiredVelx;

impl rosidl_runtime_rs::Service for GetDesiredVelx {
    type Request = GetDesiredVelx_Request;
    type Response = GetDesiredVelx_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__GetDesiredVelx() }
    }
}




#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__GetCurrentSolutionSpace() -> *const std::ffi::c_void;
}

// Corresponds to dsr_msgs2__srv__GetCurrentSolutionSpace
#[allow(missing_docs, non_camel_case_types)]
pub struct GetCurrentSolutionSpace;

impl rosidl_runtime_rs::Service for GetCurrentSolutionSpace {
    type Request = GetCurrentSolutionSpace_Request;
    type Response = GetCurrentSolutionSpace_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__GetCurrentSolutionSpace() }
    }
}




#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__GetCurrentRotm() -> *const std::ffi::c_void;
}

// Corresponds to dsr_msgs2__srv__GetCurrentRotm
#[allow(missing_docs, non_camel_case_types)]
pub struct GetCurrentRotm;

impl rosidl_runtime_rs::Service for GetCurrentRotm {
    type Request = GetCurrentRotm_Request;
    type Response = GetCurrentRotm_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__GetCurrentRotm() }
    }
}




#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__GetJointTorque() -> *const std::ffi::c_void;
}

// Corresponds to dsr_msgs2__srv__GetJointTorque
#[allow(missing_docs, non_camel_case_types)]
pub struct GetJointTorque;

impl rosidl_runtime_rs::Service for GetJointTorque {
    type Request = GetJointTorque_Request;
    type Response = GetJointTorque_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__GetJointTorque() }
    }
}




#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__GetExternalTorque() -> *const std::ffi::c_void;
}

// Corresponds to dsr_msgs2__srv__GetExternalTorque
#[allow(missing_docs, non_camel_case_types)]
pub struct GetExternalTorque;

impl rosidl_runtime_rs::Service for GetExternalTorque {
    type Request = GetExternalTorque_Request;
    type Response = GetExternalTorque_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__GetExternalTorque() }
    }
}




#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__GetToolForce() -> *const std::ffi::c_void;
}

// Corresponds to dsr_msgs2__srv__GetToolForce
#[allow(missing_docs, non_camel_case_types)]
pub struct GetToolForce;

impl rosidl_runtime_rs::Service for GetToolForce {
    type Request = GetToolForce_Request;
    type Response = GetToolForce_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__GetToolForce() }
    }
}




#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__GetSolutionSpace() -> *const std::ffi::c_void;
}

// Corresponds to dsr_msgs2__srv__GetSolutionSpace
#[allow(missing_docs, non_camel_case_types)]
pub struct GetSolutionSpace;

impl rosidl_runtime_rs::Service for GetSolutionSpace {
    type Request = GetSolutionSpace_Request;
    type Response = GetSolutionSpace_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__GetSolutionSpace() }
    }
}




#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__GetOrientationError() -> *const std::ffi::c_void;
}

// Corresponds to dsr_msgs2__srv__GetOrientationError
#[allow(missing_docs, non_camel_case_types)]
pub struct GetOrientationError;

impl rosidl_runtime_rs::Service for GetOrientationError {
    type Request = GetOrientationError_Request;
    type Response = GetOrientationError_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__GetOrientationError() }
    }
}




#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__ParallelAxis1() -> *const std::ffi::c_void;
}

// Corresponds to dsr_msgs2__srv__ParallelAxis1
#[allow(missing_docs, non_camel_case_types)]
pub struct ParallelAxis1;

impl rosidl_runtime_rs::Service for ParallelAxis1 {
    type Request = ParallelAxis1_Request;
    type Response = ParallelAxis1_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__ParallelAxis1() }
    }
}




#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__ParallelAxis2() -> *const std::ffi::c_void;
}

// Corresponds to dsr_msgs2__srv__ParallelAxis2
#[allow(missing_docs, non_camel_case_types)]
pub struct ParallelAxis2;

impl rosidl_runtime_rs::Service for ParallelAxis2 {
    type Request = ParallelAxis2_Request;
    type Response = ParallelAxis2_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__ParallelAxis2() }
    }
}




#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__AlignAxis1() -> *const std::ffi::c_void;
}

// Corresponds to dsr_msgs2__srv__AlignAxis1
#[allow(missing_docs, non_camel_case_types)]
pub struct AlignAxis1;

impl rosidl_runtime_rs::Service for AlignAxis1 {
    type Request = AlignAxis1_Request;
    type Response = AlignAxis1_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__AlignAxis1() }
    }
}




#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__AlignAxis2() -> *const std::ffi::c_void;
}

// Corresponds to dsr_msgs2__srv__AlignAxis2
#[allow(missing_docs, non_camel_case_types)]
pub struct AlignAxis2;

impl rosidl_runtime_rs::Service for AlignAxis2 {
    type Request = AlignAxis2_Request;
    type Response = AlignAxis2_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__AlignAxis2() }
    }
}




#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__IsDoneBoltTightening() -> *const std::ffi::c_void;
}

// Corresponds to dsr_msgs2__srv__IsDoneBoltTightening
#[allow(missing_docs, non_camel_case_types)]
pub struct IsDoneBoltTightening;

impl rosidl_runtime_rs::Service for IsDoneBoltTightening {
    type Request = IsDoneBoltTightening_Request;
    type Response = IsDoneBoltTightening_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__IsDoneBoltTightening() }
    }
}




#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__ReleaseComplianceCtrl() -> *const std::ffi::c_void;
}

// Corresponds to dsr_msgs2__srv__ReleaseComplianceCtrl
#[allow(missing_docs, non_camel_case_types)]
pub struct ReleaseComplianceCtrl;

impl rosidl_runtime_rs::Service for ReleaseComplianceCtrl {
    type Request = ReleaseComplianceCtrl_Request;
    type Response = ReleaseComplianceCtrl_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__ReleaseComplianceCtrl() }
    }
}




#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__TaskComplianceCtrl() -> *const std::ffi::c_void;
}

// Corresponds to dsr_msgs2__srv__TaskComplianceCtrl
#[allow(missing_docs, non_camel_case_types)]
pub struct TaskComplianceCtrl;

impl rosidl_runtime_rs::Service for TaskComplianceCtrl {
    type Request = TaskComplianceCtrl_Request;
    type Response = TaskComplianceCtrl_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__TaskComplianceCtrl() }
    }
}




#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__SetStiffnessx() -> *const std::ffi::c_void;
}

// Corresponds to dsr_msgs2__srv__SetStiffnessx
#[allow(missing_docs, non_camel_case_types)]
pub struct SetStiffnessx;

impl rosidl_runtime_rs::Service for SetStiffnessx {
    type Request = SetStiffnessx_Request;
    type Response = SetStiffnessx_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__SetStiffnessx() }
    }
}




#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__CalcCoord() -> *const std::ffi::c_void;
}

// Corresponds to dsr_msgs2__srv__CalcCoord
#[allow(missing_docs, non_camel_case_types)]
pub struct CalcCoord;

impl rosidl_runtime_rs::Service for CalcCoord {
    type Request = CalcCoord_Request;
    type Response = CalcCoord_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__CalcCoord() }
    }
}




#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__SetUserCartCoord1() -> *const std::ffi::c_void;
}

// Corresponds to dsr_msgs2__srv__SetUserCartCoord1
#[allow(missing_docs, non_camel_case_types)]
pub struct SetUserCartCoord1;

impl rosidl_runtime_rs::Service for SetUserCartCoord1 {
    type Request = SetUserCartCoord1_Request;
    type Response = SetUserCartCoord1_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__SetUserCartCoord1() }
    }
}




#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__SetUserCartCoord2() -> *const std::ffi::c_void;
}

// Corresponds to dsr_msgs2__srv__SetUserCartCoord2
#[allow(missing_docs, non_camel_case_types)]
pub struct SetUserCartCoord2;

impl rosidl_runtime_rs::Service for SetUserCartCoord2 {
    type Request = SetUserCartCoord2_Request;
    type Response = SetUserCartCoord2_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__SetUserCartCoord2() }
    }
}




#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__SetUserCartCoord3() -> *const std::ffi::c_void;
}

// Corresponds to dsr_msgs2__srv__SetUserCartCoord3
#[allow(missing_docs, non_camel_case_types)]
pub struct SetUserCartCoord3;

impl rosidl_runtime_rs::Service for SetUserCartCoord3 {
    type Request = SetUserCartCoord3_Request;
    type Response = SetUserCartCoord3_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__SetUserCartCoord3() }
    }
}




#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__OverwriteUserCartCoord() -> *const std::ffi::c_void;
}

// Corresponds to dsr_msgs2__srv__OverwriteUserCartCoord
#[allow(missing_docs, non_camel_case_types)]
pub struct OverwriteUserCartCoord;

impl rosidl_runtime_rs::Service for OverwriteUserCartCoord {
    type Request = OverwriteUserCartCoord_Request;
    type Response = OverwriteUserCartCoord_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__OverwriteUserCartCoord() }
    }
}




#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__GetUserCartCoord() -> *const std::ffi::c_void;
}

// Corresponds to dsr_msgs2__srv__GetUserCartCoord
#[allow(missing_docs, non_camel_case_types)]
pub struct GetUserCartCoord;

impl rosidl_runtime_rs::Service for GetUserCartCoord {
    type Request = GetUserCartCoord_Request;
    type Response = GetUserCartCoord_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__GetUserCartCoord() }
    }
}




#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__SetDesiredForce() -> *const std::ffi::c_void;
}

// Corresponds to dsr_msgs2__srv__SetDesiredForce
#[allow(missing_docs, non_camel_case_types)]
pub struct SetDesiredForce;

impl rosidl_runtime_rs::Service for SetDesiredForce {
    type Request = SetDesiredForce_Request;
    type Response = SetDesiredForce_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__SetDesiredForce() }
    }
}




#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__ReleaseForce() -> *const std::ffi::c_void;
}

// Corresponds to dsr_msgs2__srv__ReleaseForce
#[allow(missing_docs, non_camel_case_types)]
pub struct ReleaseForce;

impl rosidl_runtime_rs::Service for ReleaseForce {
    type Request = ReleaseForce_Request;
    type Response = ReleaseForce_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__ReleaseForce() }
    }
}




#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__CheckPositionCondition() -> *const std::ffi::c_void;
}

// Corresponds to dsr_msgs2__srv__CheckPositionCondition
#[allow(missing_docs, non_camel_case_types)]
pub struct CheckPositionCondition;

impl rosidl_runtime_rs::Service for CheckPositionCondition {
    type Request = CheckPositionCondition_Request;
    type Response = CheckPositionCondition_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__CheckPositionCondition() }
    }
}




#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__CheckForceCondition() -> *const std::ffi::c_void;
}

// Corresponds to dsr_msgs2__srv__CheckForceCondition
#[allow(missing_docs, non_camel_case_types)]
pub struct CheckForceCondition;

impl rosidl_runtime_rs::Service for CheckForceCondition {
    type Request = CheckForceCondition_Request;
    type Response = CheckForceCondition_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__CheckForceCondition() }
    }
}




#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__CheckOrientationCondition1() -> *const std::ffi::c_void;
}

// Corresponds to dsr_msgs2__srv__CheckOrientationCondition1
#[allow(missing_docs, non_camel_case_types)]
pub struct CheckOrientationCondition1;

impl rosidl_runtime_rs::Service for CheckOrientationCondition1 {
    type Request = CheckOrientationCondition1_Request;
    type Response = CheckOrientationCondition1_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__CheckOrientationCondition1() }
    }
}




#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__CheckOrientationCondition2() -> *const std::ffi::c_void;
}

// Corresponds to dsr_msgs2__srv__CheckOrientationCondition2
#[allow(missing_docs, non_camel_case_types)]
pub struct CheckOrientationCondition2;

impl rosidl_runtime_rs::Service for CheckOrientationCondition2 {
    type Request = CheckOrientationCondition2_Request;
    type Response = CheckOrientationCondition2_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__CheckOrientationCondition2() }
    }
}




#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__CoordTransform() -> *const std::ffi::c_void;
}

// Corresponds to dsr_msgs2__srv__CoordTransform
#[allow(missing_docs, non_camel_case_types)]
pub struct CoordTransform;

impl rosidl_runtime_rs::Service for CoordTransform {
    type Request = CoordTransform_Request;
    type Response = CoordTransform_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__CoordTransform() }
    }
}




#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__GetWorkpieceWeight() -> *const std::ffi::c_void;
}

// Corresponds to dsr_msgs2__srv__GetWorkpieceWeight
#[allow(missing_docs, non_camel_case_types)]
pub struct GetWorkpieceWeight;

impl rosidl_runtime_rs::Service for GetWorkpieceWeight {
    type Request = GetWorkpieceWeight_Request;
    type Response = GetWorkpieceWeight_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__GetWorkpieceWeight() }
    }
}




#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__ResetWorkpieceWeight() -> *const std::ffi::c_void;
}

// Corresponds to dsr_msgs2__srv__ResetWorkpieceWeight
#[allow(missing_docs, non_camel_case_types)]
pub struct ResetWorkpieceWeight;

impl rosidl_runtime_rs::Service for ResetWorkpieceWeight {
    type Request = ResetWorkpieceWeight_Request;
    type Response = ResetWorkpieceWeight_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__ResetWorkpieceWeight() }
    }
}




#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__ConfigCreateTool() -> *const std::ffi::c_void;
}

// Corresponds to dsr_msgs2__srv__ConfigCreateTool
#[allow(missing_docs, non_camel_case_types)]
pub struct ConfigCreateTool;

impl rosidl_runtime_rs::Service for ConfigCreateTool {
    type Request = ConfigCreateTool_Request;
    type Response = ConfigCreateTool_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__ConfigCreateTool() }
    }
}




#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__ConfigDeleteTool() -> *const std::ffi::c_void;
}

// Corresponds to dsr_msgs2__srv__ConfigDeleteTool
#[allow(missing_docs, non_camel_case_types)]
pub struct ConfigDeleteTool;

impl rosidl_runtime_rs::Service for ConfigDeleteTool {
    type Request = ConfigDeleteTool_Request;
    type Response = ConfigDeleteTool_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__ConfigDeleteTool() }
    }
}




#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__SetCurrentTool() -> *const std::ffi::c_void;
}

// Corresponds to dsr_msgs2__srv__SetCurrentTool
#[allow(missing_docs, non_camel_case_types)]
pub struct SetCurrentTool;

impl rosidl_runtime_rs::Service for SetCurrentTool {
    type Request = SetCurrentTool_Request;
    type Response = SetCurrentTool_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__SetCurrentTool() }
    }
}




#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__GetCurrentTool() -> *const std::ffi::c_void;
}

// Corresponds to dsr_msgs2__srv__GetCurrentTool
#[allow(missing_docs, non_camel_case_types)]
pub struct GetCurrentTool;

impl rosidl_runtime_rs::Service for GetCurrentTool {
    type Request = GetCurrentTool_Request;
    type Response = GetCurrentTool_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__GetCurrentTool() }
    }
}




#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__SetToolShape() -> *const std::ffi::c_void;
}

// Corresponds to dsr_msgs2__srv__SetToolShape
#[allow(missing_docs, non_camel_case_types)]
pub struct SetToolShape;

impl rosidl_runtime_rs::Service for SetToolShape {
    type Request = SetToolShape_Request;
    type Response = SetToolShape_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__SetToolShape() }
    }
}




#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__ConfigCreateTcp() -> *const std::ffi::c_void;
}

// Corresponds to dsr_msgs2__srv__ConfigCreateTcp
#[allow(missing_docs, non_camel_case_types)]
pub struct ConfigCreateTcp;

impl rosidl_runtime_rs::Service for ConfigCreateTcp {
    type Request = ConfigCreateTcp_Request;
    type Response = ConfigCreateTcp_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__ConfigCreateTcp() }
    }
}




#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__ConfigDeleteTcp() -> *const std::ffi::c_void;
}

// Corresponds to dsr_msgs2__srv__ConfigDeleteTcp
#[allow(missing_docs, non_camel_case_types)]
pub struct ConfigDeleteTcp;

impl rosidl_runtime_rs::Service for ConfigDeleteTcp {
    type Request = ConfigDeleteTcp_Request;
    type Response = ConfigDeleteTcp_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__ConfigDeleteTcp() }
    }
}




#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__SetCurrentTcp() -> *const std::ffi::c_void;
}

// Corresponds to dsr_msgs2__srv__SetCurrentTcp
#[allow(missing_docs, non_camel_case_types)]
pub struct SetCurrentTcp;

impl rosidl_runtime_rs::Service for SetCurrentTcp {
    type Request = SetCurrentTcp_Request;
    type Response = SetCurrentTcp_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__SetCurrentTcp() }
    }
}




#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__GetCurrentTcp() -> *const std::ffi::c_void;
}

// Corresponds to dsr_msgs2__srv__GetCurrentTcp
#[allow(missing_docs, non_camel_case_types)]
pub struct GetCurrentTcp;

impl rosidl_runtime_rs::Service for GetCurrentTcp {
    type Request = GetCurrentTcp_Request;
    type Response = GetCurrentTcp_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__GetCurrentTcp() }
    }
}




#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__SetToolDigitalOutput() -> *const std::ffi::c_void;
}

// Corresponds to dsr_msgs2__srv__SetToolDigitalOutput
#[allow(missing_docs, non_camel_case_types)]
pub struct SetToolDigitalOutput;

impl rosidl_runtime_rs::Service for SetToolDigitalOutput {
    type Request = SetToolDigitalOutput_Request;
    type Response = SetToolDigitalOutput_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__SetToolDigitalOutput() }
    }
}




#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__GetToolDigitalOutput() -> *const std::ffi::c_void;
}

// Corresponds to dsr_msgs2__srv__GetToolDigitalOutput
#[allow(missing_docs, non_camel_case_types)]
pub struct GetToolDigitalOutput;

impl rosidl_runtime_rs::Service for GetToolDigitalOutput {
    type Request = GetToolDigitalOutput_Request;
    type Response = GetToolDigitalOutput_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__GetToolDigitalOutput() }
    }
}




#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__GetToolDigitalInput() -> *const std::ffi::c_void;
}

// Corresponds to dsr_msgs2__srv__GetToolDigitalInput
#[allow(missing_docs, non_camel_case_types)]
pub struct GetToolDigitalInput;

impl rosidl_runtime_rs::Service for GetToolDigitalInput {
    type Request = GetToolDigitalInput_Request;
    type Response = GetToolDigitalInput_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__GetToolDigitalInput() }
    }
}




#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__SetCtrlBoxDigitalOutput() -> *const std::ffi::c_void;
}

// Corresponds to dsr_msgs2__srv__SetCtrlBoxDigitalOutput
#[allow(missing_docs, non_camel_case_types)]
pub struct SetCtrlBoxDigitalOutput;

impl rosidl_runtime_rs::Service for SetCtrlBoxDigitalOutput {
    type Request = SetCtrlBoxDigitalOutput_Request;
    type Response = SetCtrlBoxDigitalOutput_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__SetCtrlBoxDigitalOutput() }
    }
}




#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__GetCtrlBoxDigitalOutput() -> *const std::ffi::c_void;
}

// Corresponds to dsr_msgs2__srv__GetCtrlBoxDigitalOutput
#[allow(missing_docs, non_camel_case_types)]
pub struct GetCtrlBoxDigitalOutput;

impl rosidl_runtime_rs::Service for GetCtrlBoxDigitalOutput {
    type Request = GetCtrlBoxDigitalOutput_Request;
    type Response = GetCtrlBoxDigitalOutput_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__GetCtrlBoxDigitalOutput() }
    }
}




#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__GetCtrlBoxDigitalInput() -> *const std::ffi::c_void;
}

// Corresponds to dsr_msgs2__srv__GetCtrlBoxDigitalInput
#[allow(missing_docs, non_camel_case_types)]
pub struct GetCtrlBoxDigitalInput;

impl rosidl_runtime_rs::Service for GetCtrlBoxDigitalInput {
    type Request = GetCtrlBoxDigitalInput_Request;
    type Response = GetCtrlBoxDigitalInput_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__GetCtrlBoxDigitalInput() }
    }
}




#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__SetCtrlBoxAnalogInputType() -> *const std::ffi::c_void;
}

// Corresponds to dsr_msgs2__srv__SetCtrlBoxAnalogInputType
#[allow(missing_docs, non_camel_case_types)]
pub struct SetCtrlBoxAnalogInputType;

impl rosidl_runtime_rs::Service for SetCtrlBoxAnalogInputType {
    type Request = SetCtrlBoxAnalogInputType_Request;
    type Response = SetCtrlBoxAnalogInputType_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__SetCtrlBoxAnalogInputType() }
    }
}




#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__SetCtrlBoxAnalogOutputType() -> *const std::ffi::c_void;
}

// Corresponds to dsr_msgs2__srv__SetCtrlBoxAnalogOutputType
#[allow(missing_docs, non_camel_case_types)]
pub struct SetCtrlBoxAnalogOutputType;

impl rosidl_runtime_rs::Service for SetCtrlBoxAnalogOutputType {
    type Request = SetCtrlBoxAnalogOutputType_Request;
    type Response = SetCtrlBoxAnalogOutputType_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__SetCtrlBoxAnalogOutputType() }
    }
}




#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__SetCtrlBoxAnalogOutput() -> *const std::ffi::c_void;
}

// Corresponds to dsr_msgs2__srv__SetCtrlBoxAnalogOutput
#[allow(missing_docs, non_camel_case_types)]
pub struct SetCtrlBoxAnalogOutput;

impl rosidl_runtime_rs::Service for SetCtrlBoxAnalogOutput {
    type Request = SetCtrlBoxAnalogOutput_Request;
    type Response = SetCtrlBoxAnalogOutput_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__SetCtrlBoxAnalogOutput() }
    }
}




#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__GetCtrlBoxAnalogInput() -> *const std::ffi::c_void;
}

// Corresponds to dsr_msgs2__srv__GetCtrlBoxAnalogInput
#[allow(missing_docs, non_camel_case_types)]
pub struct GetCtrlBoxAnalogInput;

impl rosidl_runtime_rs::Service for GetCtrlBoxAnalogInput {
    type Request = GetCtrlBoxAnalogInput_Request;
    type Response = GetCtrlBoxAnalogInput_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__GetCtrlBoxAnalogInput() }
    }
}




#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__GetInputRegisterBit() -> *const std::ffi::c_void;
}

// Corresponds to dsr_msgs2__srv__GetInputRegisterBit
#[allow(missing_docs, non_camel_case_types)]
pub struct GetInputRegisterBit;

impl rosidl_runtime_rs::Service for GetInputRegisterBit {
    type Request = GetInputRegisterBit_Request;
    type Response = GetInputRegisterBit_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__GetInputRegisterBit() }
    }
}




#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__GetInputRegisterInt() -> *const std::ffi::c_void;
}

// Corresponds to dsr_msgs2__srv__GetInputRegisterInt
#[allow(missing_docs, non_camel_case_types)]
pub struct GetInputRegisterInt;

impl rosidl_runtime_rs::Service for GetInputRegisterInt {
    type Request = GetInputRegisterInt_Request;
    type Response = GetInputRegisterInt_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__GetInputRegisterInt() }
    }
}




#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__GetInputRegisterFloat() -> *const std::ffi::c_void;
}

// Corresponds to dsr_msgs2__srv__GetInputRegisterFloat
#[allow(missing_docs, non_camel_case_types)]
pub struct GetInputRegisterFloat;

impl rosidl_runtime_rs::Service for GetInputRegisterFloat {
    type Request = GetInputRegisterFloat_Request;
    type Response = GetInputRegisterFloat_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__GetInputRegisterFloat() }
    }
}




#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__GetOutputRegisterBit() -> *const std::ffi::c_void;
}

// Corresponds to dsr_msgs2__srv__GetOutputRegisterBit
#[allow(missing_docs, non_camel_case_types)]
pub struct GetOutputRegisterBit;

impl rosidl_runtime_rs::Service for GetOutputRegisterBit {
    type Request = GetOutputRegisterBit_Request;
    type Response = GetOutputRegisterBit_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__GetOutputRegisterBit() }
    }
}




#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__GetOutputRegisterInt() -> *const std::ffi::c_void;
}

// Corresponds to dsr_msgs2__srv__GetOutputRegisterInt
#[allow(missing_docs, non_camel_case_types)]
pub struct GetOutputRegisterInt;

impl rosidl_runtime_rs::Service for GetOutputRegisterInt {
    type Request = GetOutputRegisterInt_Request;
    type Response = GetOutputRegisterInt_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__GetOutputRegisterInt() }
    }
}




#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__GetOutputRegisterFloat() -> *const std::ffi::c_void;
}

// Corresponds to dsr_msgs2__srv__GetOutputRegisterFloat
#[allow(missing_docs, non_camel_case_types)]
pub struct GetOutputRegisterFloat;

impl rosidl_runtime_rs::Service for GetOutputRegisterFloat {
    type Request = GetOutputRegisterFloat_Request;
    type Response = GetOutputRegisterFloat_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__GetOutputRegisterFloat() }
    }
}




#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__SetOutputRegisterBit() -> *const std::ffi::c_void;
}

// Corresponds to dsr_msgs2__srv__SetOutputRegisterBit
#[allow(missing_docs, non_camel_case_types)]
pub struct SetOutputRegisterBit;

impl rosidl_runtime_rs::Service for SetOutputRegisterBit {
    type Request = SetOutputRegisterBit_Request;
    type Response = SetOutputRegisterBit_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__SetOutputRegisterBit() }
    }
}




#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__SetOutputRegisterInt() -> *const std::ffi::c_void;
}

// Corresponds to dsr_msgs2__srv__SetOutputRegisterInt
#[allow(missing_docs, non_camel_case_types)]
pub struct SetOutputRegisterInt;

impl rosidl_runtime_rs::Service for SetOutputRegisterInt {
    type Request = SetOutputRegisterInt_Request;
    type Response = SetOutputRegisterInt_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__SetOutputRegisterInt() }
    }
}




#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__SetOutputRegisterFloat() -> *const std::ffi::c_void;
}

// Corresponds to dsr_msgs2__srv__SetOutputRegisterFloat
#[allow(missing_docs, non_camel_case_types)]
pub struct SetOutputRegisterFloat;

impl rosidl_runtime_rs::Service for SetOutputRegisterFloat {
    type Request = SetOutputRegisterFloat_Request;
    type Response = SetOutputRegisterFloat_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__SetOutputRegisterFloat() }
    }
}




#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__ConfigCreateModbus() -> *const std::ffi::c_void;
}

// Corresponds to dsr_msgs2__srv__ConfigCreateModbus
#[allow(missing_docs, non_camel_case_types)]
pub struct ConfigCreateModbus;

impl rosidl_runtime_rs::Service for ConfigCreateModbus {
    type Request = ConfigCreateModbus_Request;
    type Response = ConfigCreateModbus_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__ConfigCreateModbus() }
    }
}




#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__ConfigDeleteModbus() -> *const std::ffi::c_void;
}

// Corresponds to dsr_msgs2__srv__ConfigDeleteModbus
#[allow(missing_docs, non_camel_case_types)]
pub struct ConfigDeleteModbus;

impl rosidl_runtime_rs::Service for ConfigDeleteModbus {
    type Request = ConfigDeleteModbus_Request;
    type Response = ConfigDeleteModbus_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__ConfigDeleteModbus() }
    }
}




#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__SetModbusOutput() -> *const std::ffi::c_void;
}

// Corresponds to dsr_msgs2__srv__SetModbusOutput
#[allow(missing_docs, non_camel_case_types)]
pub struct SetModbusOutput;

impl rosidl_runtime_rs::Service for SetModbusOutput {
    type Request = SetModbusOutput_Request;
    type Response = SetModbusOutput_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__SetModbusOutput() }
    }
}




#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__GetModbusInput() -> *const std::ffi::c_void;
}

// Corresponds to dsr_msgs2__srv__GetModbusInput
#[allow(missing_docs, non_camel_case_types)]
pub struct GetModbusInput;

impl rosidl_runtime_rs::Service for GetModbusInput {
    type Request = GetModbusInput_Request;
    type Response = GetModbusInput_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__GetModbusInput() }
    }
}




#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__DrlStart() -> *const std::ffi::c_void;
}

// Corresponds to dsr_msgs2__srv__DrlStart
#[allow(missing_docs, non_camel_case_types)]
pub struct DrlStart;

impl rosidl_runtime_rs::Service for DrlStart {
    type Request = DrlStart_Request;
    type Response = DrlStart_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__DrlStart() }
    }
}




#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__DrlStop() -> *const std::ffi::c_void;
}

// Corresponds to dsr_msgs2__srv__DrlStop
#[allow(missing_docs, non_camel_case_types)]
pub struct DrlStop;

impl rosidl_runtime_rs::Service for DrlStop {
    type Request = DrlStop_Request;
    type Response = DrlStop_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__DrlStop() }
    }
}




#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__DrlPause() -> *const std::ffi::c_void;
}

// Corresponds to dsr_msgs2__srv__DrlPause
#[allow(missing_docs, non_camel_case_types)]
pub struct DrlPause;

impl rosidl_runtime_rs::Service for DrlPause {
    type Request = DrlPause_Request;
    type Response = DrlPause_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__DrlPause() }
    }
}




#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__DrlResume() -> *const std::ffi::c_void;
}

// Corresponds to dsr_msgs2__srv__DrlResume
#[allow(missing_docs, non_camel_case_types)]
pub struct DrlResume;

impl rosidl_runtime_rs::Service for DrlResume {
    type Request = DrlResume_Request;
    type Response = DrlResume_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__DrlResume() }
    }
}




#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__GetDrlState() -> *const std::ffi::c_void;
}

// Corresponds to dsr_msgs2__srv__GetDrlState
#[allow(missing_docs, non_camel_case_types)]
pub struct GetDrlState;

impl rosidl_runtime_rs::Service for GetDrlState {
    type Request = GetDrlState_Request;
    type Response = GetDrlState_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__GetDrlState() }
    }
}




#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__Robotiq2FClose() -> *const std::ffi::c_void;
}

// Corresponds to dsr_msgs2__srv__Robotiq2FClose
#[allow(missing_docs, non_camel_case_types)]
pub struct Robotiq2FClose;

impl rosidl_runtime_rs::Service for Robotiq2FClose {
    type Request = Robotiq2FClose_Request;
    type Response = Robotiq2FClose_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__Robotiq2FClose() }
    }
}




#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__Robotiq2FOpen() -> *const std::ffi::c_void;
}

// Corresponds to dsr_msgs2__srv__Robotiq2FOpen
#[allow(missing_docs, non_camel_case_types)]
pub struct Robotiq2FOpen;

impl rosidl_runtime_rs::Service for Robotiq2FOpen {
    type Request = Robotiq2FOpen_Request;
    type Response = Robotiq2FOpen_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__Robotiq2FOpen() }
    }
}




#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__Robotiq2FMove() -> *const std::ffi::c_void;
}

// Corresponds to dsr_msgs2__srv__Robotiq2FMove
#[allow(missing_docs, non_camel_case_types)]
pub struct Robotiq2FMove;

impl rosidl_runtime_rs::Service for Robotiq2FMove {
    type Request = Robotiq2FMove_Request;
    type Response = Robotiq2FMove_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__Robotiq2FMove() }
    }
}




#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__SerialSendData() -> *const std::ffi::c_void;
}

// Corresponds to dsr_msgs2__srv__SerialSendData
#[allow(missing_docs, non_camel_case_types)]
pub struct SerialSendData;

impl rosidl_runtime_rs::Service for SerialSendData {
    type Request = SerialSendData_Request;
    type Response = SerialSendData_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__SerialSendData() }
    }
}




#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__FlangeSerialOpen() -> *const std::ffi::c_void;
}

// Corresponds to dsr_msgs2__srv__FlangeSerialOpen
#[allow(missing_docs, non_camel_case_types)]
pub struct FlangeSerialOpen;

impl rosidl_runtime_rs::Service for FlangeSerialOpen {
    type Request = FlangeSerialOpen_Request;
    type Response = FlangeSerialOpen_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__FlangeSerialOpen() }
    }
}




#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__FlangeSerialClose() -> *const std::ffi::c_void;
}

// Corresponds to dsr_msgs2__srv__FlangeSerialClose
#[allow(missing_docs, non_camel_case_types)]
pub struct FlangeSerialClose;

impl rosidl_runtime_rs::Service for FlangeSerialClose {
    type Request = FlangeSerialClose_Request;
    type Response = FlangeSerialClose_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__FlangeSerialClose() }
    }
}




#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__FlangeSerialWrite() -> *const std::ffi::c_void;
}

// Corresponds to dsr_msgs2__srv__FlangeSerialWrite
#[allow(missing_docs, non_camel_case_types)]
pub struct FlangeSerialWrite;

impl rosidl_runtime_rs::Service for FlangeSerialWrite {
    type Request = FlangeSerialWrite_Request;
    type Response = FlangeSerialWrite_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__FlangeSerialWrite() }
    }
}




#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__FlangeSerialRead() -> *const std::ffi::c_void;
}

// Corresponds to dsr_msgs2__srv__FlangeSerialRead
#[allow(missing_docs, non_camel_case_types)]
pub struct FlangeSerialRead;

impl rosidl_runtime_rs::Service for FlangeSerialRead {
    type Request = FlangeSerialRead_Request;
    type Response = FlangeSerialRead_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__FlangeSerialRead() }
    }
}




#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__ConnectRtControl() -> *const std::ffi::c_void;
}

// Corresponds to dsr_msgs2__srv__ConnectRtControl
#[allow(missing_docs, non_camel_case_types)]
pub struct ConnectRtControl;

impl rosidl_runtime_rs::Service for ConnectRtControl {
    type Request = ConnectRtControl_Request;
    type Response = ConnectRtControl_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__ConnectRtControl() }
    }
}




#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__DisconnectRtControl() -> *const std::ffi::c_void;
}

// Corresponds to dsr_msgs2__srv__DisconnectRtControl
#[allow(missing_docs, non_camel_case_types)]
pub struct DisconnectRtControl;

impl rosidl_runtime_rs::Service for DisconnectRtControl {
    type Request = DisconnectRtControl_Request;
    type Response = DisconnectRtControl_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__DisconnectRtControl() }
    }
}




#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__GetRtControlInputDataList() -> *const std::ffi::c_void;
}

// Corresponds to dsr_msgs2__srv__GetRtControlInputDataList
#[allow(missing_docs, non_camel_case_types)]
pub struct GetRtControlInputDataList;

impl rosidl_runtime_rs::Service for GetRtControlInputDataList {
    type Request = GetRtControlInputDataList_Request;
    type Response = GetRtControlInputDataList_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__GetRtControlInputDataList() }
    }
}




#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__GetRtControlInputVersionList() -> *const std::ffi::c_void;
}

// Corresponds to dsr_msgs2__srv__GetRtControlInputVersionList
#[allow(missing_docs, non_camel_case_types)]
pub struct GetRtControlInputVersionList;

impl rosidl_runtime_rs::Service for GetRtControlInputVersionList {
    type Request = GetRtControlInputVersionList_Request;
    type Response = GetRtControlInputVersionList_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__GetRtControlInputVersionList() }
    }
}




#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__GetRtControlOutputDataList() -> *const std::ffi::c_void;
}

// Corresponds to dsr_msgs2__srv__GetRtControlOutputDataList
#[allow(missing_docs, non_camel_case_types)]
pub struct GetRtControlOutputDataList;

impl rosidl_runtime_rs::Service for GetRtControlOutputDataList {
    type Request = GetRtControlOutputDataList_Request;
    type Response = GetRtControlOutputDataList_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__GetRtControlOutputDataList() }
    }
}




#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__GetRtControlOutputVersionList() -> *const std::ffi::c_void;
}

// Corresponds to dsr_msgs2__srv__GetRtControlOutputVersionList
#[allow(missing_docs, non_camel_case_types)]
pub struct GetRtControlOutputVersionList;

impl rosidl_runtime_rs::Service for GetRtControlOutputVersionList {
    type Request = GetRtControlOutputVersionList_Request;
    type Response = GetRtControlOutputVersionList_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__GetRtControlOutputVersionList() }
    }
}




#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__ReadDataRt() -> *const std::ffi::c_void;
}

// Corresponds to dsr_msgs2__srv__ReadDataRt
#[allow(missing_docs, non_camel_case_types)]
pub struct ReadDataRt;

impl rosidl_runtime_rs::Service for ReadDataRt {
    type Request = ReadDataRt_Request;
    type Response = ReadDataRt_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__ReadDataRt() }
    }
}




#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__SetAccjRt() -> *const std::ffi::c_void;
}

// Corresponds to dsr_msgs2__srv__SetAccjRt
#[allow(missing_docs, non_camel_case_types)]
pub struct SetAccjRt;

impl rosidl_runtime_rs::Service for SetAccjRt {
    type Request = SetAccjRt_Request;
    type Response = SetAccjRt_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__SetAccjRt() }
    }
}




#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__SetAccxRt() -> *const std::ffi::c_void;
}

// Corresponds to dsr_msgs2__srv__SetAccxRt
#[allow(missing_docs, non_camel_case_types)]
pub struct SetAccxRt;

impl rosidl_runtime_rs::Service for SetAccxRt {
    type Request = SetAccxRt_Request;
    type Response = SetAccxRt_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__SetAccxRt() }
    }
}




#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__SetRtControlInput() -> *const std::ffi::c_void;
}

// Corresponds to dsr_msgs2__srv__SetRtControlInput
#[allow(missing_docs, non_camel_case_types)]
pub struct SetRtControlInput;

impl rosidl_runtime_rs::Service for SetRtControlInput {
    type Request = SetRtControlInput_Request;
    type Response = SetRtControlInput_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__SetRtControlInput() }
    }
}




#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__SetRtControlOutput() -> *const std::ffi::c_void;
}

// Corresponds to dsr_msgs2__srv__SetRtControlOutput
#[allow(missing_docs, non_camel_case_types)]
pub struct SetRtControlOutput;

impl rosidl_runtime_rs::Service for SetRtControlOutput {
    type Request = SetRtControlOutput_Request;
    type Response = SetRtControlOutput_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__SetRtControlOutput() }
    }
}




#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__SetVeljRt() -> *const std::ffi::c_void;
}

// Corresponds to dsr_msgs2__srv__SetVeljRt
#[allow(missing_docs, non_camel_case_types)]
pub struct SetVeljRt;

impl rosidl_runtime_rs::Service for SetVeljRt {
    type Request = SetVeljRt_Request;
    type Response = SetVeljRt_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__SetVeljRt() }
    }
}




#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__SetVelxRt() -> *const std::ffi::c_void;
}

// Corresponds to dsr_msgs2__srv__SetVelxRt
#[allow(missing_docs, non_camel_case_types)]
pub struct SetVelxRt;

impl rosidl_runtime_rs::Service for SetVelxRt {
    type Request = SetVelxRt_Request;
    type Response = SetVelxRt_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__SetVelxRt() }
    }
}




#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__StartRtControl() -> *const std::ffi::c_void;
}

// Corresponds to dsr_msgs2__srv__StartRtControl
#[allow(missing_docs, non_camel_case_types)]
pub struct StartRtControl;

impl rosidl_runtime_rs::Service for StartRtControl {
    type Request = StartRtControl_Request;
    type Response = StartRtControl_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__StartRtControl() }
    }
}




#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__StopRtControl() -> *const std::ffi::c_void;
}

// Corresponds to dsr_msgs2__srv__StopRtControl
#[allow(missing_docs, non_camel_case_types)]
pub struct StopRtControl;

impl rosidl_runtime_rs::Service for StopRtControl {
    type Request = StopRtControl_Request;
    type Response = StopRtControl_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__StopRtControl() }
    }
}




#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__WriteDataRt() -> *const std::ffi::c_void;
}

// Corresponds to dsr_msgs2__srv__WriteDataRt
#[allow(missing_docs, non_camel_case_types)]
pub struct WriteDataRt;

impl rosidl_runtime_rs::Service for WriteDataRt {
    type Request = WriteDataRt_Request;
    type Response = WriteDataRt_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__dsr_msgs2__srv__WriteDataRt() }
    }
}


