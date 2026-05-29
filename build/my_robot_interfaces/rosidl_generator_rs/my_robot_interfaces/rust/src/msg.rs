#[cfg(feature = "serde")]
use serde::{Deserialize, Serialize};



// Corresponds to my_robot_interfaces__msg__TurtleStatus

// This struct is not documented.
#[allow(missing_docs)]

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct TurtleStatus {
    /// 벽까지의 남은 거리
    pub distance_to_wall: f64,

    /// 로봇의 상태 (예: NORMAL, WARN, STOP)
    pub current_state: std::string::String,

    /// 이동 중 여부
    pub is_moving: bool,

}



impl Default for TurtleStatus {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::TurtleStatus::default())
  }
}

impl rosidl_runtime_rs::Message for TurtleStatus {
  type RmwMsg = super::msg::rmw::TurtleStatus;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        distance_to_wall: msg.distance_to_wall,
        current_state: msg.current_state.as_str().into(),
        is_moving: msg.is_moving,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      distance_to_wall: msg.distance_to_wall,
        current_state: msg.current_state.as_str().into(),
      is_moving: msg.is_moving,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      distance_to_wall: msg.distance_to_wall,
      current_state: msg.current_state.to_string(),
      is_moving: msg.is_moving,
    }
  }
}


