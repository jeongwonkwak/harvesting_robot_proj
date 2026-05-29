
#[cfg(feature = "serde")]
use serde::{Deserialize, Serialize};



// Corresponds to dsr_msgs2__action__JogH2r_Goal

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
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
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::action::rmw::JogH2r_Goal::default())
  }
}

impl rosidl_runtime_rs::Message for JogH2r_Goal {
  type RmwMsg = super::action::rmw::JogH2r_Goal;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        jog_axis: msg.jog_axis,
        move_reference: msg.move_reference,
        velocity: msg.velocity,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      jog_axis: msg.jog_axis,
      move_reference: msg.move_reference,
      velocity: msg.velocity,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      jog_axis: msg.jog_axis,
      move_reference: msg.move_reference,
      velocity: msg.velocity,
    }
  }
}


// Corresponds to dsr_msgs2__action__JogH2r_Result

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct JogH2r_Result {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,

}



impl Default for JogH2r_Result {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::action::rmw::JogH2r_Result::default())
  }
}

impl rosidl_runtime_rs::Message for JogH2r_Result {
  type RmwMsg = super::action::rmw::JogH2r_Result;

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


// Corresponds to dsr_msgs2__action__JogH2r_Feedback

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct JogH2r_Feedback {

    // This member is not documented.
    #[allow(missing_docs)]
    pub pos: [f64; 6],

}



impl Default for JogH2r_Feedback {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::action::rmw::JogH2r_Feedback::default())
  }
}

impl rosidl_runtime_rs::Message for JogH2r_Feedback {
  type RmwMsg = super::action::rmw::JogH2r_Feedback;

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


// Corresponds to dsr_msgs2__action__JogH2r_FeedbackMessage

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct JogH2r_FeedbackMessage {

    // This member is not documented.
    #[allow(missing_docs)]
    pub goal_id: unique_identifier_msgs::msg::UUID,


    // This member is not documented.
    #[allow(missing_docs)]
    pub feedback: super::action::JogH2r_Feedback,

}



impl Default for JogH2r_FeedbackMessage {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::action::rmw::JogH2r_FeedbackMessage::default())
  }
}

impl rosidl_runtime_rs::Message for JogH2r_FeedbackMessage {
  type RmwMsg = super::action::rmw::JogH2r_FeedbackMessage;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        goal_id: unique_identifier_msgs::msg::UUID::into_rmw_message(std::borrow::Cow::Owned(msg.goal_id)).into_owned(),
        feedback: super::action::JogH2r_Feedback::into_rmw_message(std::borrow::Cow::Owned(msg.feedback)).into_owned(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        goal_id: unique_identifier_msgs::msg::UUID::into_rmw_message(std::borrow::Cow::Borrowed(&msg.goal_id)).into_owned(),
        feedback: super::action::JogH2r_Feedback::into_rmw_message(std::borrow::Cow::Borrowed(&msg.feedback)).into_owned(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      goal_id: unique_identifier_msgs::msg::UUID::from_rmw_message(msg.goal_id),
      feedback: super::action::JogH2r_Feedback::from_rmw_message(msg.feedback),
    }
  }
}


// Corresponds to dsr_msgs2__action__MovejH2r_Goal

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
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
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::action::rmw::MovejH2r_Goal::default())
  }
}

impl rosidl_runtime_rs::Message for MovejH2r_Goal {
  type RmwMsg = super::action::rmw::MovejH2r_Goal;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        target_pos: msg.target_pos,
        target_vel: msg.target_vel,
        target_acc: msg.target_acc,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        target_pos: msg.target_pos,
        target_vel: msg.target_vel,
        target_acc: msg.target_acc,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      target_pos: msg.target_pos,
      target_vel: msg.target_vel,
      target_acc: msg.target_acc,
    }
  }
}


// Corresponds to dsr_msgs2__action__MovejH2r_Result

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct MovejH2r_Result {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,

}



impl Default for MovejH2r_Result {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::action::rmw::MovejH2r_Result::default())
  }
}

impl rosidl_runtime_rs::Message for MovejH2r_Result {
  type RmwMsg = super::action::rmw::MovejH2r_Result;

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


// Corresponds to dsr_msgs2__action__MovejH2r_Feedback

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct MovejH2r_Feedback {

    // This member is not documented.
    #[allow(missing_docs)]
    pub pos: [f64; 6],

}



impl Default for MovejH2r_Feedback {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::action::rmw::MovejH2r_Feedback::default())
  }
}

impl rosidl_runtime_rs::Message for MovejH2r_Feedback {
  type RmwMsg = super::action::rmw::MovejH2r_Feedback;

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


// Corresponds to dsr_msgs2__action__MovejH2r_FeedbackMessage

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct MovejH2r_FeedbackMessage {

    // This member is not documented.
    #[allow(missing_docs)]
    pub goal_id: unique_identifier_msgs::msg::UUID,


    // This member is not documented.
    #[allow(missing_docs)]
    pub feedback: super::action::MovejH2r_Feedback,

}



impl Default for MovejH2r_FeedbackMessage {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::action::rmw::MovejH2r_FeedbackMessage::default())
  }
}

impl rosidl_runtime_rs::Message for MovejH2r_FeedbackMessage {
  type RmwMsg = super::action::rmw::MovejH2r_FeedbackMessage;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        goal_id: unique_identifier_msgs::msg::UUID::into_rmw_message(std::borrow::Cow::Owned(msg.goal_id)).into_owned(),
        feedback: super::action::MovejH2r_Feedback::into_rmw_message(std::borrow::Cow::Owned(msg.feedback)).into_owned(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        goal_id: unique_identifier_msgs::msg::UUID::into_rmw_message(std::borrow::Cow::Borrowed(&msg.goal_id)).into_owned(),
        feedback: super::action::MovejH2r_Feedback::into_rmw_message(std::borrow::Cow::Borrowed(&msg.feedback)).into_owned(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      goal_id: unique_identifier_msgs::msg::UUID::from_rmw_message(msg.goal_id),
      feedback: super::action::MovejH2r_Feedback::from_rmw_message(msg.feedback),
    }
  }
}


// Corresponds to dsr_msgs2__action__MovelH2r_Goal

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
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
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::action::rmw::MovelH2r_Goal::default())
  }
}

impl rosidl_runtime_rs::Message for MovelH2r_Goal {
  type RmwMsg = super::action::rmw::MovelH2r_Goal;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        target_pos: msg.target_pos,
        target_vel: msg.target_vel,
        target_acc: msg.target_acc,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        target_pos: msg.target_pos,
        target_vel: msg.target_vel,
        target_acc: msg.target_acc,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      target_pos: msg.target_pos,
      target_vel: msg.target_vel,
      target_acc: msg.target_acc,
    }
  }
}


// Corresponds to dsr_msgs2__action__MovelH2r_Result

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct MovelH2r_Result {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,

}



impl Default for MovelH2r_Result {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::action::rmw::MovelH2r_Result::default())
  }
}

impl rosidl_runtime_rs::Message for MovelH2r_Result {
  type RmwMsg = super::action::rmw::MovelH2r_Result;

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


// Corresponds to dsr_msgs2__action__MovelH2r_Feedback

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct MovelH2r_Feedback {

    // This member is not documented.
    #[allow(missing_docs)]
    pub pos: [f64; 6],

}



impl Default for MovelH2r_Feedback {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::action::rmw::MovelH2r_Feedback::default())
  }
}

impl rosidl_runtime_rs::Message for MovelH2r_Feedback {
  type RmwMsg = super::action::rmw::MovelH2r_Feedback;

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


// Corresponds to dsr_msgs2__action__MovelH2r_FeedbackMessage

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct MovelH2r_FeedbackMessage {

    // This member is not documented.
    #[allow(missing_docs)]
    pub goal_id: unique_identifier_msgs::msg::UUID,


    // This member is not documented.
    #[allow(missing_docs)]
    pub feedback: super::action::MovelH2r_Feedback,

}



impl Default for MovelH2r_FeedbackMessage {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::action::rmw::MovelH2r_FeedbackMessage::default())
  }
}

impl rosidl_runtime_rs::Message for MovelH2r_FeedbackMessage {
  type RmwMsg = super::action::rmw::MovelH2r_FeedbackMessage;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        goal_id: unique_identifier_msgs::msg::UUID::into_rmw_message(std::borrow::Cow::Owned(msg.goal_id)).into_owned(),
        feedback: super::action::MovelH2r_Feedback::into_rmw_message(std::borrow::Cow::Owned(msg.feedback)).into_owned(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        goal_id: unique_identifier_msgs::msg::UUID::into_rmw_message(std::borrow::Cow::Borrowed(&msg.goal_id)).into_owned(),
        feedback: super::action::MovelH2r_Feedback::into_rmw_message(std::borrow::Cow::Borrowed(&msg.feedback)).into_owned(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      goal_id: unique_identifier_msgs::msg::UUID::from_rmw_message(msg.goal_id),
      feedback: super::action::MovelH2r_Feedback::from_rmw_message(msg.feedback),
    }
  }
}






// Corresponds to dsr_msgs2__action__JogH2r_SendGoal_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct JogH2r_SendGoal_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub goal_id: unique_identifier_msgs::msg::UUID,


    // This member is not documented.
    #[allow(missing_docs)]
    pub goal: super::action::JogH2r_Goal,

}



impl Default for JogH2r_SendGoal_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::action::rmw::JogH2r_SendGoal_Request::default())
  }
}

impl rosidl_runtime_rs::Message for JogH2r_SendGoal_Request {
  type RmwMsg = super::action::rmw::JogH2r_SendGoal_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        goal_id: unique_identifier_msgs::msg::UUID::into_rmw_message(std::borrow::Cow::Owned(msg.goal_id)).into_owned(),
        goal: super::action::JogH2r_Goal::into_rmw_message(std::borrow::Cow::Owned(msg.goal)).into_owned(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        goal_id: unique_identifier_msgs::msg::UUID::into_rmw_message(std::borrow::Cow::Borrowed(&msg.goal_id)).into_owned(),
        goal: super::action::JogH2r_Goal::into_rmw_message(std::borrow::Cow::Borrowed(&msg.goal)).into_owned(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      goal_id: unique_identifier_msgs::msg::UUID::from_rmw_message(msg.goal_id),
      goal: super::action::JogH2r_Goal::from_rmw_message(msg.goal),
    }
  }
}


// Corresponds to dsr_msgs2__action__JogH2r_SendGoal_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct JogH2r_SendGoal_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub accepted: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub stamp: builtin_interfaces::msg::Time,

}



impl Default for JogH2r_SendGoal_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::action::rmw::JogH2r_SendGoal_Response::default())
  }
}

impl rosidl_runtime_rs::Message for JogH2r_SendGoal_Response {
  type RmwMsg = super::action::rmw::JogH2r_SendGoal_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        accepted: msg.accepted,
        stamp: builtin_interfaces::msg::Time::into_rmw_message(std::borrow::Cow::Owned(msg.stamp)).into_owned(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      accepted: msg.accepted,
        stamp: builtin_interfaces::msg::Time::into_rmw_message(std::borrow::Cow::Borrowed(&msg.stamp)).into_owned(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      accepted: msg.accepted,
      stamp: builtin_interfaces::msg::Time::from_rmw_message(msg.stamp),
    }
  }
}


// Corresponds to dsr_msgs2__action__JogH2r_GetResult_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct JogH2r_GetResult_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub goal_id: unique_identifier_msgs::msg::UUID,

}



impl Default for JogH2r_GetResult_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::action::rmw::JogH2r_GetResult_Request::default())
  }
}

impl rosidl_runtime_rs::Message for JogH2r_GetResult_Request {
  type RmwMsg = super::action::rmw::JogH2r_GetResult_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        goal_id: unique_identifier_msgs::msg::UUID::into_rmw_message(std::borrow::Cow::Owned(msg.goal_id)).into_owned(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        goal_id: unique_identifier_msgs::msg::UUID::into_rmw_message(std::borrow::Cow::Borrowed(&msg.goal_id)).into_owned(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      goal_id: unique_identifier_msgs::msg::UUID::from_rmw_message(msg.goal_id),
    }
  }
}


// Corresponds to dsr_msgs2__action__JogH2r_GetResult_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct JogH2r_GetResult_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub status: i8,


    // This member is not documented.
    #[allow(missing_docs)]
    pub result: super::action::JogH2r_Result,

}



impl Default for JogH2r_GetResult_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::action::rmw::JogH2r_GetResult_Response::default())
  }
}

impl rosidl_runtime_rs::Message for JogH2r_GetResult_Response {
  type RmwMsg = super::action::rmw::JogH2r_GetResult_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        status: msg.status,
        result: super::action::JogH2r_Result::into_rmw_message(std::borrow::Cow::Owned(msg.result)).into_owned(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      status: msg.status,
        result: super::action::JogH2r_Result::into_rmw_message(std::borrow::Cow::Borrowed(&msg.result)).into_owned(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      status: msg.status,
      result: super::action::JogH2r_Result::from_rmw_message(msg.result),
    }
  }
}


// Corresponds to dsr_msgs2__action__MovejH2r_SendGoal_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct MovejH2r_SendGoal_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub goal_id: unique_identifier_msgs::msg::UUID,


    // This member is not documented.
    #[allow(missing_docs)]
    pub goal: super::action::MovejH2r_Goal,

}



impl Default for MovejH2r_SendGoal_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::action::rmw::MovejH2r_SendGoal_Request::default())
  }
}

impl rosidl_runtime_rs::Message for MovejH2r_SendGoal_Request {
  type RmwMsg = super::action::rmw::MovejH2r_SendGoal_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        goal_id: unique_identifier_msgs::msg::UUID::into_rmw_message(std::borrow::Cow::Owned(msg.goal_id)).into_owned(),
        goal: super::action::MovejH2r_Goal::into_rmw_message(std::borrow::Cow::Owned(msg.goal)).into_owned(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        goal_id: unique_identifier_msgs::msg::UUID::into_rmw_message(std::borrow::Cow::Borrowed(&msg.goal_id)).into_owned(),
        goal: super::action::MovejH2r_Goal::into_rmw_message(std::borrow::Cow::Borrowed(&msg.goal)).into_owned(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      goal_id: unique_identifier_msgs::msg::UUID::from_rmw_message(msg.goal_id),
      goal: super::action::MovejH2r_Goal::from_rmw_message(msg.goal),
    }
  }
}


// Corresponds to dsr_msgs2__action__MovejH2r_SendGoal_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct MovejH2r_SendGoal_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub accepted: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub stamp: builtin_interfaces::msg::Time,

}



impl Default for MovejH2r_SendGoal_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::action::rmw::MovejH2r_SendGoal_Response::default())
  }
}

impl rosidl_runtime_rs::Message for MovejH2r_SendGoal_Response {
  type RmwMsg = super::action::rmw::MovejH2r_SendGoal_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        accepted: msg.accepted,
        stamp: builtin_interfaces::msg::Time::into_rmw_message(std::borrow::Cow::Owned(msg.stamp)).into_owned(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      accepted: msg.accepted,
        stamp: builtin_interfaces::msg::Time::into_rmw_message(std::borrow::Cow::Borrowed(&msg.stamp)).into_owned(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      accepted: msg.accepted,
      stamp: builtin_interfaces::msg::Time::from_rmw_message(msg.stamp),
    }
  }
}


// Corresponds to dsr_msgs2__action__MovejH2r_GetResult_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct MovejH2r_GetResult_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub goal_id: unique_identifier_msgs::msg::UUID,

}



impl Default for MovejH2r_GetResult_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::action::rmw::MovejH2r_GetResult_Request::default())
  }
}

impl rosidl_runtime_rs::Message for MovejH2r_GetResult_Request {
  type RmwMsg = super::action::rmw::MovejH2r_GetResult_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        goal_id: unique_identifier_msgs::msg::UUID::into_rmw_message(std::borrow::Cow::Owned(msg.goal_id)).into_owned(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        goal_id: unique_identifier_msgs::msg::UUID::into_rmw_message(std::borrow::Cow::Borrowed(&msg.goal_id)).into_owned(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      goal_id: unique_identifier_msgs::msg::UUID::from_rmw_message(msg.goal_id),
    }
  }
}


// Corresponds to dsr_msgs2__action__MovejH2r_GetResult_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct MovejH2r_GetResult_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub status: i8,


    // This member is not documented.
    #[allow(missing_docs)]
    pub result: super::action::MovejH2r_Result,

}



impl Default for MovejH2r_GetResult_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::action::rmw::MovejH2r_GetResult_Response::default())
  }
}

impl rosidl_runtime_rs::Message for MovejH2r_GetResult_Response {
  type RmwMsg = super::action::rmw::MovejH2r_GetResult_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        status: msg.status,
        result: super::action::MovejH2r_Result::into_rmw_message(std::borrow::Cow::Owned(msg.result)).into_owned(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      status: msg.status,
        result: super::action::MovejH2r_Result::into_rmw_message(std::borrow::Cow::Borrowed(&msg.result)).into_owned(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      status: msg.status,
      result: super::action::MovejH2r_Result::from_rmw_message(msg.result),
    }
  }
}


// Corresponds to dsr_msgs2__action__MovelH2r_SendGoal_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct MovelH2r_SendGoal_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub goal_id: unique_identifier_msgs::msg::UUID,


    // This member is not documented.
    #[allow(missing_docs)]
    pub goal: super::action::MovelH2r_Goal,

}



impl Default for MovelH2r_SendGoal_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::action::rmw::MovelH2r_SendGoal_Request::default())
  }
}

impl rosidl_runtime_rs::Message for MovelH2r_SendGoal_Request {
  type RmwMsg = super::action::rmw::MovelH2r_SendGoal_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        goal_id: unique_identifier_msgs::msg::UUID::into_rmw_message(std::borrow::Cow::Owned(msg.goal_id)).into_owned(),
        goal: super::action::MovelH2r_Goal::into_rmw_message(std::borrow::Cow::Owned(msg.goal)).into_owned(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        goal_id: unique_identifier_msgs::msg::UUID::into_rmw_message(std::borrow::Cow::Borrowed(&msg.goal_id)).into_owned(),
        goal: super::action::MovelH2r_Goal::into_rmw_message(std::borrow::Cow::Borrowed(&msg.goal)).into_owned(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      goal_id: unique_identifier_msgs::msg::UUID::from_rmw_message(msg.goal_id),
      goal: super::action::MovelH2r_Goal::from_rmw_message(msg.goal),
    }
  }
}


// Corresponds to dsr_msgs2__action__MovelH2r_SendGoal_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct MovelH2r_SendGoal_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub accepted: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub stamp: builtin_interfaces::msg::Time,

}



impl Default for MovelH2r_SendGoal_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::action::rmw::MovelH2r_SendGoal_Response::default())
  }
}

impl rosidl_runtime_rs::Message for MovelH2r_SendGoal_Response {
  type RmwMsg = super::action::rmw::MovelH2r_SendGoal_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        accepted: msg.accepted,
        stamp: builtin_interfaces::msg::Time::into_rmw_message(std::borrow::Cow::Owned(msg.stamp)).into_owned(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      accepted: msg.accepted,
        stamp: builtin_interfaces::msg::Time::into_rmw_message(std::borrow::Cow::Borrowed(&msg.stamp)).into_owned(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      accepted: msg.accepted,
      stamp: builtin_interfaces::msg::Time::from_rmw_message(msg.stamp),
    }
  }
}


// Corresponds to dsr_msgs2__action__MovelH2r_GetResult_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct MovelH2r_GetResult_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub goal_id: unique_identifier_msgs::msg::UUID,

}



impl Default for MovelH2r_GetResult_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::action::rmw::MovelH2r_GetResult_Request::default())
  }
}

impl rosidl_runtime_rs::Message for MovelH2r_GetResult_Request {
  type RmwMsg = super::action::rmw::MovelH2r_GetResult_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        goal_id: unique_identifier_msgs::msg::UUID::into_rmw_message(std::borrow::Cow::Owned(msg.goal_id)).into_owned(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        goal_id: unique_identifier_msgs::msg::UUID::into_rmw_message(std::borrow::Cow::Borrowed(&msg.goal_id)).into_owned(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      goal_id: unique_identifier_msgs::msg::UUID::from_rmw_message(msg.goal_id),
    }
  }
}


// Corresponds to dsr_msgs2__action__MovelH2r_GetResult_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct MovelH2r_GetResult_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub status: i8,


    // This member is not documented.
    #[allow(missing_docs)]
    pub result: super::action::MovelH2r_Result,

}



impl Default for MovelH2r_GetResult_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::action::rmw::MovelH2r_GetResult_Response::default())
  }
}

impl rosidl_runtime_rs::Message for MovelH2r_GetResult_Response {
  type RmwMsg = super::action::rmw::MovelH2r_GetResult_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        status: msg.status,
        result: super::action::MovelH2r_Result::into_rmw_message(std::borrow::Cow::Owned(msg.result)).into_owned(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      status: msg.status,
        result: super::action::MovelH2r_Result::into_rmw_message(std::borrow::Cow::Borrowed(&msg.result)).into_owned(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      status: msg.status,
      result: super::action::MovelH2r_Result::from_rmw_message(msg.result),
    }
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






#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_action_type_support_handle__dsr_msgs2__action__JogH2r() -> *const std::ffi::c_void;
}

// Corresponds to dsr_msgs2__action__JogH2r
#[allow(missing_docs, non_camel_case_types)]
pub struct JogH2r;

impl rosidl_runtime_rs::Action for JogH2r {
  // --- Associated types for client library users ---
  /// The goal message defined in the action definition.
  type Goal = JogH2r_Goal;

  /// The result message defined in the action definition.
  type Result = JogH2r_Result;

  /// The feedback message defined in the action definition.
  type Feedback = JogH2r_Feedback;

  // --- Associated types for client library implementation ---
  /// The feedback message with generic fields which wraps the feedback message.
  type FeedbackMessage = super::action::JogH2r_FeedbackMessage;

  /// The send_goal service using a wrapped version of the goal message as a request.
  type SendGoalService = super::action::JogH2r_SendGoal;

  /// The generic service to cancel a goal.
  type CancelGoalService = action_msgs::srv::rmw::CancelGoal;

  /// The get_result service using a wrapped version of the result message as a response.
  type GetResultService = super::action::JogH2r_GetResult;

  // --- Methods for client library implementation ---
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_action_type_support_handle__dsr_msgs2__action__JogH2r() }
  }

  fn create_goal_request(
    goal_id: &[u8; 16],
    goal: super::action::rmw::JogH2r_Goal,
  ) -> super::action::rmw::JogH2r_SendGoal_Request {
   super::action::rmw::JogH2r_SendGoal_Request {
      goal_id: unique_identifier_msgs::msg::rmw::UUID { uuid: *goal_id },
      goal,
    }
  }

  fn split_goal_request(
    request: super::action::rmw::JogH2r_SendGoal_Request,
  ) -> (
    [u8; 16],
   super::action::rmw::JogH2r_Goal,
  ) {
    (request.goal_id.uuid, request.goal)
  }

  fn create_goal_response(
    accepted: bool,
    stamp: (i32, u32),
  ) -> super::action::rmw::JogH2r_SendGoal_Response {
   super::action::rmw::JogH2r_SendGoal_Response {
      accepted,
      stamp: builtin_interfaces::msg::rmw::Time {
        sec: stamp.0,
        nanosec: stamp.1,
      },
    }
  }

  fn get_goal_response_accepted(
    response: &super::action::rmw::JogH2r_SendGoal_Response,
  ) -> bool {
    response.accepted
  }

  fn get_goal_response_stamp(
    response: &super::action::rmw::JogH2r_SendGoal_Response,
  ) -> (i32, u32) {
    (response.stamp.sec, response.stamp.nanosec)
  }

  fn create_feedback_message(
    goal_id: &[u8; 16],
    feedback: super::action::rmw::JogH2r_Feedback,
  ) -> super::action::rmw::JogH2r_FeedbackMessage {
    let mut message = super::action::rmw::JogH2r_FeedbackMessage::default();
    message.goal_id.uuid = *goal_id;
    message.feedback = feedback;
    message
  }

  fn split_feedback_message(
    feedback: super::action::rmw::JogH2r_FeedbackMessage,
  ) -> (
    [u8; 16],
   super::action::rmw::JogH2r_Feedback,
  ) {
    (feedback.goal_id.uuid, feedback.feedback)
  }

  fn create_result_request(
    goal_id: &[u8; 16],
  ) -> super::action::rmw::JogH2r_GetResult_Request {
   super::action::rmw::JogH2r_GetResult_Request {
      goal_id: unique_identifier_msgs::msg::rmw::UUID { uuid: *goal_id },
    }
  }

  fn get_result_request_uuid(
    request: &super::action::rmw::JogH2r_GetResult_Request,
  ) -> &[u8; 16] {
    &request.goal_id.uuid
  }

  fn create_result_response(
    status: i8,
    result: super::action::rmw::JogH2r_Result,
  ) -> super::action::rmw::JogH2r_GetResult_Response {
   super::action::rmw::JogH2r_GetResult_Response {
      status,
      result,
    }
  }

  fn split_result_response(
    response: super::action::rmw::JogH2r_GetResult_Response
  ) -> (
    i8,
   super::action::rmw::JogH2r_Result,
  ) {
    (response.status, response.result)
  }
}




#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_action_type_support_handle__dsr_msgs2__action__MovejH2r() -> *const std::ffi::c_void;
}

// Corresponds to dsr_msgs2__action__MovejH2r
#[allow(missing_docs, non_camel_case_types)]
pub struct MovejH2r;

impl rosidl_runtime_rs::Action for MovejH2r {
  // --- Associated types for client library users ---
  /// The goal message defined in the action definition.
  type Goal = MovejH2r_Goal;

  /// The result message defined in the action definition.
  type Result = MovejH2r_Result;

  /// The feedback message defined in the action definition.
  type Feedback = MovejH2r_Feedback;

  // --- Associated types for client library implementation ---
  /// The feedback message with generic fields which wraps the feedback message.
  type FeedbackMessage = super::action::MovejH2r_FeedbackMessage;

  /// The send_goal service using a wrapped version of the goal message as a request.
  type SendGoalService = super::action::MovejH2r_SendGoal;

  /// The generic service to cancel a goal.
  type CancelGoalService = action_msgs::srv::rmw::CancelGoal;

  /// The get_result service using a wrapped version of the result message as a response.
  type GetResultService = super::action::MovejH2r_GetResult;

  // --- Methods for client library implementation ---
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_action_type_support_handle__dsr_msgs2__action__MovejH2r() }
  }

  fn create_goal_request(
    goal_id: &[u8; 16],
    goal: super::action::rmw::MovejH2r_Goal,
  ) -> super::action::rmw::MovejH2r_SendGoal_Request {
   super::action::rmw::MovejH2r_SendGoal_Request {
      goal_id: unique_identifier_msgs::msg::rmw::UUID { uuid: *goal_id },
      goal,
    }
  }

  fn split_goal_request(
    request: super::action::rmw::MovejH2r_SendGoal_Request,
  ) -> (
    [u8; 16],
   super::action::rmw::MovejH2r_Goal,
  ) {
    (request.goal_id.uuid, request.goal)
  }

  fn create_goal_response(
    accepted: bool,
    stamp: (i32, u32),
  ) -> super::action::rmw::MovejH2r_SendGoal_Response {
   super::action::rmw::MovejH2r_SendGoal_Response {
      accepted,
      stamp: builtin_interfaces::msg::rmw::Time {
        sec: stamp.0,
        nanosec: stamp.1,
      },
    }
  }

  fn get_goal_response_accepted(
    response: &super::action::rmw::MovejH2r_SendGoal_Response,
  ) -> bool {
    response.accepted
  }

  fn get_goal_response_stamp(
    response: &super::action::rmw::MovejH2r_SendGoal_Response,
  ) -> (i32, u32) {
    (response.stamp.sec, response.stamp.nanosec)
  }

  fn create_feedback_message(
    goal_id: &[u8; 16],
    feedback: super::action::rmw::MovejH2r_Feedback,
  ) -> super::action::rmw::MovejH2r_FeedbackMessage {
    let mut message = super::action::rmw::MovejH2r_FeedbackMessage::default();
    message.goal_id.uuid = *goal_id;
    message.feedback = feedback;
    message
  }

  fn split_feedback_message(
    feedback: super::action::rmw::MovejH2r_FeedbackMessage,
  ) -> (
    [u8; 16],
   super::action::rmw::MovejH2r_Feedback,
  ) {
    (feedback.goal_id.uuid, feedback.feedback)
  }

  fn create_result_request(
    goal_id: &[u8; 16],
  ) -> super::action::rmw::MovejH2r_GetResult_Request {
   super::action::rmw::MovejH2r_GetResult_Request {
      goal_id: unique_identifier_msgs::msg::rmw::UUID { uuid: *goal_id },
    }
  }

  fn get_result_request_uuid(
    request: &super::action::rmw::MovejH2r_GetResult_Request,
  ) -> &[u8; 16] {
    &request.goal_id.uuid
  }

  fn create_result_response(
    status: i8,
    result: super::action::rmw::MovejH2r_Result,
  ) -> super::action::rmw::MovejH2r_GetResult_Response {
   super::action::rmw::MovejH2r_GetResult_Response {
      status,
      result,
    }
  }

  fn split_result_response(
    response: super::action::rmw::MovejH2r_GetResult_Response
  ) -> (
    i8,
   super::action::rmw::MovejH2r_Result,
  ) {
    (response.status, response.result)
  }
}




#[link(name = "dsr_msgs2__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_action_type_support_handle__dsr_msgs2__action__MovelH2r() -> *const std::ffi::c_void;
}

// Corresponds to dsr_msgs2__action__MovelH2r
#[allow(missing_docs, non_camel_case_types)]
pub struct MovelH2r;

impl rosidl_runtime_rs::Action for MovelH2r {
  // --- Associated types for client library users ---
  /// The goal message defined in the action definition.
  type Goal = MovelH2r_Goal;

  /// The result message defined in the action definition.
  type Result = MovelH2r_Result;

  /// The feedback message defined in the action definition.
  type Feedback = MovelH2r_Feedback;

  // --- Associated types for client library implementation ---
  /// The feedback message with generic fields which wraps the feedback message.
  type FeedbackMessage = super::action::MovelH2r_FeedbackMessage;

  /// The send_goal service using a wrapped version of the goal message as a request.
  type SendGoalService = super::action::MovelH2r_SendGoal;

  /// The generic service to cancel a goal.
  type CancelGoalService = action_msgs::srv::rmw::CancelGoal;

  /// The get_result service using a wrapped version of the result message as a response.
  type GetResultService = super::action::MovelH2r_GetResult;

  // --- Methods for client library implementation ---
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_action_type_support_handle__dsr_msgs2__action__MovelH2r() }
  }

  fn create_goal_request(
    goal_id: &[u8; 16],
    goal: super::action::rmw::MovelH2r_Goal,
  ) -> super::action::rmw::MovelH2r_SendGoal_Request {
   super::action::rmw::MovelH2r_SendGoal_Request {
      goal_id: unique_identifier_msgs::msg::rmw::UUID { uuid: *goal_id },
      goal,
    }
  }

  fn split_goal_request(
    request: super::action::rmw::MovelH2r_SendGoal_Request,
  ) -> (
    [u8; 16],
   super::action::rmw::MovelH2r_Goal,
  ) {
    (request.goal_id.uuid, request.goal)
  }

  fn create_goal_response(
    accepted: bool,
    stamp: (i32, u32),
  ) -> super::action::rmw::MovelH2r_SendGoal_Response {
   super::action::rmw::MovelH2r_SendGoal_Response {
      accepted,
      stamp: builtin_interfaces::msg::rmw::Time {
        sec: stamp.0,
        nanosec: stamp.1,
      },
    }
  }

  fn get_goal_response_accepted(
    response: &super::action::rmw::MovelH2r_SendGoal_Response,
  ) -> bool {
    response.accepted
  }

  fn get_goal_response_stamp(
    response: &super::action::rmw::MovelH2r_SendGoal_Response,
  ) -> (i32, u32) {
    (response.stamp.sec, response.stamp.nanosec)
  }

  fn create_feedback_message(
    goal_id: &[u8; 16],
    feedback: super::action::rmw::MovelH2r_Feedback,
  ) -> super::action::rmw::MovelH2r_FeedbackMessage {
    let mut message = super::action::rmw::MovelH2r_FeedbackMessage::default();
    message.goal_id.uuid = *goal_id;
    message.feedback = feedback;
    message
  }

  fn split_feedback_message(
    feedback: super::action::rmw::MovelH2r_FeedbackMessage,
  ) -> (
    [u8; 16],
   super::action::rmw::MovelH2r_Feedback,
  ) {
    (feedback.goal_id.uuid, feedback.feedback)
  }

  fn create_result_request(
    goal_id: &[u8; 16],
  ) -> super::action::rmw::MovelH2r_GetResult_Request {
   super::action::rmw::MovelH2r_GetResult_Request {
      goal_id: unique_identifier_msgs::msg::rmw::UUID { uuid: *goal_id },
    }
  }

  fn get_result_request_uuid(
    request: &super::action::rmw::MovelH2r_GetResult_Request,
  ) -> &[u8; 16] {
    &request.goal_id.uuid
  }

  fn create_result_response(
    status: i8,
    result: super::action::rmw::MovelH2r_Result,
  ) -> super::action::rmw::MovelH2r_GetResult_Response {
   super::action::rmw::MovelH2r_GetResult_Response {
      status,
      result,
    }
  }

  fn split_result_response(
    response: super::action::rmw::MovelH2r_GetResult_Response
  ) -> (
    i8,
   super::action::rmw::MovelH2r_Result,
  ) {
    (response.status, response.result)
  }
}


