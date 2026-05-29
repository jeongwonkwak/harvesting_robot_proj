// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from dsr_msgs2:action/MovelH2r.idl
// generated code does not contain a copyright notice

#ifndef DSR_MSGS2__ACTION__DETAIL__MOVEL_H2R__TRAITS_HPP_
#define DSR_MSGS2__ACTION__DETAIL__MOVEL_H2R__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "dsr_msgs2/action/detail/movel_h2r__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace dsr_msgs2
{

namespace action
{

inline void to_flow_style_yaml(
  const MovelH2r_Goal & msg,
  std::ostream & out)
{
  out << "{";
  // member: target_pos
  {
    if (msg.target_pos.size() == 0) {
      out << "target_pos: []";
    } else {
      out << "target_pos: [";
      size_t pending_items = msg.target_pos.size();
      for (auto item : msg.target_pos) {
        rosidl_generator_traits::value_to_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
    out << ", ";
  }

  // member: target_vel
  {
    if (msg.target_vel.size() == 0) {
      out << "target_vel: []";
    } else {
      out << "target_vel: [";
      size_t pending_items = msg.target_vel.size();
      for (auto item : msg.target_vel) {
        rosidl_generator_traits::value_to_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
    out << ", ";
  }

  // member: target_acc
  {
    if (msg.target_acc.size() == 0) {
      out << "target_acc: []";
    } else {
      out << "target_acc: [";
      size_t pending_items = msg.target_acc.size();
      for (auto item : msg.target_acc) {
        rosidl_generator_traits::value_to_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const MovelH2r_Goal & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: target_pos
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.target_pos.size() == 0) {
      out << "target_pos: []\n";
    } else {
      out << "target_pos:\n";
      for (auto item : msg.target_pos) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "- ";
        rosidl_generator_traits::value_to_yaml(item, out);
        out << "\n";
      }
    }
  }

  // member: target_vel
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.target_vel.size() == 0) {
      out << "target_vel: []\n";
    } else {
      out << "target_vel:\n";
      for (auto item : msg.target_vel) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "- ";
        rosidl_generator_traits::value_to_yaml(item, out);
        out << "\n";
      }
    }
  }

  // member: target_acc
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.target_acc.size() == 0) {
      out << "target_acc: []\n";
    } else {
      out << "target_acc:\n";
      for (auto item : msg.target_acc) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "- ";
        rosidl_generator_traits::value_to_yaml(item, out);
        out << "\n";
      }
    }
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const MovelH2r_Goal & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace action

}  // namespace dsr_msgs2

namespace rosidl_generator_traits
{

[[deprecated("use dsr_msgs2::action::to_block_style_yaml() instead")]]
inline void to_yaml(
  const dsr_msgs2::action::MovelH2r_Goal & msg,
  std::ostream & out, size_t indentation = 0)
{
  dsr_msgs2::action::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use dsr_msgs2::action::to_yaml() instead")]]
inline std::string to_yaml(const dsr_msgs2::action::MovelH2r_Goal & msg)
{
  return dsr_msgs2::action::to_yaml(msg);
}

template<>
inline const char * data_type<dsr_msgs2::action::MovelH2r_Goal>()
{
  return "dsr_msgs2::action::MovelH2r_Goal";
}

template<>
inline const char * name<dsr_msgs2::action::MovelH2r_Goal>()
{
  return "dsr_msgs2/action/MovelH2r_Goal";
}

template<>
struct has_fixed_size<dsr_msgs2::action::MovelH2r_Goal>
  : std::integral_constant<bool, true> {};

template<>
struct has_bounded_size<dsr_msgs2::action::MovelH2r_Goal>
  : std::integral_constant<bool, true> {};

template<>
struct is_message<dsr_msgs2::action::MovelH2r_Goal>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace dsr_msgs2
{

namespace action
{

inline void to_flow_style_yaml(
  const MovelH2r_Result & msg,
  std::ostream & out)
{
  out << "{";
  // member: success
  {
    out << "success: ";
    rosidl_generator_traits::value_to_yaml(msg.success, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const MovelH2r_Result & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: success
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "success: ";
    rosidl_generator_traits::value_to_yaml(msg.success, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const MovelH2r_Result & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace action

}  // namespace dsr_msgs2

namespace rosidl_generator_traits
{

[[deprecated("use dsr_msgs2::action::to_block_style_yaml() instead")]]
inline void to_yaml(
  const dsr_msgs2::action::MovelH2r_Result & msg,
  std::ostream & out, size_t indentation = 0)
{
  dsr_msgs2::action::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use dsr_msgs2::action::to_yaml() instead")]]
inline std::string to_yaml(const dsr_msgs2::action::MovelH2r_Result & msg)
{
  return dsr_msgs2::action::to_yaml(msg);
}

template<>
inline const char * data_type<dsr_msgs2::action::MovelH2r_Result>()
{
  return "dsr_msgs2::action::MovelH2r_Result";
}

template<>
inline const char * name<dsr_msgs2::action::MovelH2r_Result>()
{
  return "dsr_msgs2/action/MovelH2r_Result";
}

template<>
struct has_fixed_size<dsr_msgs2::action::MovelH2r_Result>
  : std::integral_constant<bool, true> {};

template<>
struct has_bounded_size<dsr_msgs2::action::MovelH2r_Result>
  : std::integral_constant<bool, true> {};

template<>
struct is_message<dsr_msgs2::action::MovelH2r_Result>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace dsr_msgs2
{

namespace action
{

inline void to_flow_style_yaml(
  const MovelH2r_Feedback & msg,
  std::ostream & out)
{
  out << "{";
  // member: pos
  {
    if (msg.pos.size() == 0) {
      out << "pos: []";
    } else {
      out << "pos: [";
      size_t pending_items = msg.pos.size();
      for (auto item : msg.pos) {
        rosidl_generator_traits::value_to_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const MovelH2r_Feedback & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: pos
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.pos.size() == 0) {
      out << "pos: []\n";
    } else {
      out << "pos:\n";
      for (auto item : msg.pos) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "- ";
        rosidl_generator_traits::value_to_yaml(item, out);
        out << "\n";
      }
    }
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const MovelH2r_Feedback & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace action

}  // namespace dsr_msgs2

namespace rosidl_generator_traits
{

[[deprecated("use dsr_msgs2::action::to_block_style_yaml() instead")]]
inline void to_yaml(
  const dsr_msgs2::action::MovelH2r_Feedback & msg,
  std::ostream & out, size_t indentation = 0)
{
  dsr_msgs2::action::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use dsr_msgs2::action::to_yaml() instead")]]
inline std::string to_yaml(const dsr_msgs2::action::MovelH2r_Feedback & msg)
{
  return dsr_msgs2::action::to_yaml(msg);
}

template<>
inline const char * data_type<dsr_msgs2::action::MovelH2r_Feedback>()
{
  return "dsr_msgs2::action::MovelH2r_Feedback";
}

template<>
inline const char * name<dsr_msgs2::action::MovelH2r_Feedback>()
{
  return "dsr_msgs2/action/MovelH2r_Feedback";
}

template<>
struct has_fixed_size<dsr_msgs2::action::MovelH2r_Feedback>
  : std::integral_constant<bool, true> {};

template<>
struct has_bounded_size<dsr_msgs2::action::MovelH2r_Feedback>
  : std::integral_constant<bool, true> {};

template<>
struct is_message<dsr_msgs2::action::MovelH2r_Feedback>
  : std::true_type {};

}  // namespace rosidl_generator_traits

// Include directives for member types
// Member 'goal_id'
#include "unique_identifier_msgs/msg/detail/uuid__traits.hpp"
// Member 'goal'
#include "dsr_msgs2/action/detail/movel_h2r__traits.hpp"

namespace dsr_msgs2
{

namespace action
{

inline void to_flow_style_yaml(
  const MovelH2r_SendGoal_Request & msg,
  std::ostream & out)
{
  out << "{";
  // member: goal_id
  {
    out << "goal_id: ";
    to_flow_style_yaml(msg.goal_id, out);
    out << ", ";
  }

  // member: goal
  {
    out << "goal: ";
    to_flow_style_yaml(msg.goal, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const MovelH2r_SendGoal_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: goal_id
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "goal_id:\n";
    to_block_style_yaml(msg.goal_id, out, indentation + 2);
  }

  // member: goal
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "goal:\n";
    to_block_style_yaml(msg.goal, out, indentation + 2);
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const MovelH2r_SendGoal_Request & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace action

}  // namespace dsr_msgs2

namespace rosidl_generator_traits
{

[[deprecated("use dsr_msgs2::action::to_block_style_yaml() instead")]]
inline void to_yaml(
  const dsr_msgs2::action::MovelH2r_SendGoal_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  dsr_msgs2::action::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use dsr_msgs2::action::to_yaml() instead")]]
inline std::string to_yaml(const dsr_msgs2::action::MovelH2r_SendGoal_Request & msg)
{
  return dsr_msgs2::action::to_yaml(msg);
}

template<>
inline const char * data_type<dsr_msgs2::action::MovelH2r_SendGoal_Request>()
{
  return "dsr_msgs2::action::MovelH2r_SendGoal_Request";
}

template<>
inline const char * name<dsr_msgs2::action::MovelH2r_SendGoal_Request>()
{
  return "dsr_msgs2/action/MovelH2r_SendGoal_Request";
}

template<>
struct has_fixed_size<dsr_msgs2::action::MovelH2r_SendGoal_Request>
  : std::integral_constant<bool, has_fixed_size<dsr_msgs2::action::MovelH2r_Goal>::value && has_fixed_size<unique_identifier_msgs::msg::UUID>::value> {};

template<>
struct has_bounded_size<dsr_msgs2::action::MovelH2r_SendGoal_Request>
  : std::integral_constant<bool, has_bounded_size<dsr_msgs2::action::MovelH2r_Goal>::value && has_bounded_size<unique_identifier_msgs::msg::UUID>::value> {};

template<>
struct is_message<dsr_msgs2::action::MovelH2r_SendGoal_Request>
  : std::true_type {};

}  // namespace rosidl_generator_traits

// Include directives for member types
// Member 'stamp'
#include "builtin_interfaces/msg/detail/time__traits.hpp"

namespace dsr_msgs2
{

namespace action
{

inline void to_flow_style_yaml(
  const MovelH2r_SendGoal_Response & msg,
  std::ostream & out)
{
  out << "{";
  // member: accepted
  {
    out << "accepted: ";
    rosidl_generator_traits::value_to_yaml(msg.accepted, out);
    out << ", ";
  }

  // member: stamp
  {
    out << "stamp: ";
    to_flow_style_yaml(msg.stamp, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const MovelH2r_SendGoal_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: accepted
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "accepted: ";
    rosidl_generator_traits::value_to_yaml(msg.accepted, out);
    out << "\n";
  }

  // member: stamp
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "stamp:\n";
    to_block_style_yaml(msg.stamp, out, indentation + 2);
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const MovelH2r_SendGoal_Response & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace action

}  // namespace dsr_msgs2

namespace rosidl_generator_traits
{

[[deprecated("use dsr_msgs2::action::to_block_style_yaml() instead")]]
inline void to_yaml(
  const dsr_msgs2::action::MovelH2r_SendGoal_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  dsr_msgs2::action::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use dsr_msgs2::action::to_yaml() instead")]]
inline std::string to_yaml(const dsr_msgs2::action::MovelH2r_SendGoal_Response & msg)
{
  return dsr_msgs2::action::to_yaml(msg);
}

template<>
inline const char * data_type<dsr_msgs2::action::MovelH2r_SendGoal_Response>()
{
  return "dsr_msgs2::action::MovelH2r_SendGoal_Response";
}

template<>
inline const char * name<dsr_msgs2::action::MovelH2r_SendGoal_Response>()
{
  return "dsr_msgs2/action/MovelH2r_SendGoal_Response";
}

template<>
struct has_fixed_size<dsr_msgs2::action::MovelH2r_SendGoal_Response>
  : std::integral_constant<bool, has_fixed_size<builtin_interfaces::msg::Time>::value> {};

template<>
struct has_bounded_size<dsr_msgs2::action::MovelH2r_SendGoal_Response>
  : std::integral_constant<bool, has_bounded_size<builtin_interfaces::msg::Time>::value> {};

template<>
struct is_message<dsr_msgs2::action::MovelH2r_SendGoal_Response>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<dsr_msgs2::action::MovelH2r_SendGoal>()
{
  return "dsr_msgs2::action::MovelH2r_SendGoal";
}

template<>
inline const char * name<dsr_msgs2::action::MovelH2r_SendGoal>()
{
  return "dsr_msgs2/action/MovelH2r_SendGoal";
}

template<>
struct has_fixed_size<dsr_msgs2::action::MovelH2r_SendGoal>
  : std::integral_constant<
    bool,
    has_fixed_size<dsr_msgs2::action::MovelH2r_SendGoal_Request>::value &&
    has_fixed_size<dsr_msgs2::action::MovelH2r_SendGoal_Response>::value
  >
{
};

template<>
struct has_bounded_size<dsr_msgs2::action::MovelH2r_SendGoal>
  : std::integral_constant<
    bool,
    has_bounded_size<dsr_msgs2::action::MovelH2r_SendGoal_Request>::value &&
    has_bounded_size<dsr_msgs2::action::MovelH2r_SendGoal_Response>::value
  >
{
};

template<>
struct is_service<dsr_msgs2::action::MovelH2r_SendGoal>
  : std::true_type
{
};

template<>
struct is_service_request<dsr_msgs2::action::MovelH2r_SendGoal_Request>
  : std::true_type
{
};

template<>
struct is_service_response<dsr_msgs2::action::MovelH2r_SendGoal_Response>
  : std::true_type
{
};

}  // namespace rosidl_generator_traits

// Include directives for member types
// Member 'goal_id'
// already included above
// #include "unique_identifier_msgs/msg/detail/uuid__traits.hpp"

namespace dsr_msgs2
{

namespace action
{

inline void to_flow_style_yaml(
  const MovelH2r_GetResult_Request & msg,
  std::ostream & out)
{
  out << "{";
  // member: goal_id
  {
    out << "goal_id: ";
    to_flow_style_yaml(msg.goal_id, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const MovelH2r_GetResult_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: goal_id
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "goal_id:\n";
    to_block_style_yaml(msg.goal_id, out, indentation + 2);
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const MovelH2r_GetResult_Request & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace action

}  // namespace dsr_msgs2

namespace rosidl_generator_traits
{

[[deprecated("use dsr_msgs2::action::to_block_style_yaml() instead")]]
inline void to_yaml(
  const dsr_msgs2::action::MovelH2r_GetResult_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  dsr_msgs2::action::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use dsr_msgs2::action::to_yaml() instead")]]
inline std::string to_yaml(const dsr_msgs2::action::MovelH2r_GetResult_Request & msg)
{
  return dsr_msgs2::action::to_yaml(msg);
}

template<>
inline const char * data_type<dsr_msgs2::action::MovelH2r_GetResult_Request>()
{
  return "dsr_msgs2::action::MovelH2r_GetResult_Request";
}

template<>
inline const char * name<dsr_msgs2::action::MovelH2r_GetResult_Request>()
{
  return "dsr_msgs2/action/MovelH2r_GetResult_Request";
}

template<>
struct has_fixed_size<dsr_msgs2::action::MovelH2r_GetResult_Request>
  : std::integral_constant<bool, has_fixed_size<unique_identifier_msgs::msg::UUID>::value> {};

template<>
struct has_bounded_size<dsr_msgs2::action::MovelH2r_GetResult_Request>
  : std::integral_constant<bool, has_bounded_size<unique_identifier_msgs::msg::UUID>::value> {};

template<>
struct is_message<dsr_msgs2::action::MovelH2r_GetResult_Request>
  : std::true_type {};

}  // namespace rosidl_generator_traits

// Include directives for member types
// Member 'result'
// already included above
// #include "dsr_msgs2/action/detail/movel_h2r__traits.hpp"

namespace dsr_msgs2
{

namespace action
{

inline void to_flow_style_yaml(
  const MovelH2r_GetResult_Response & msg,
  std::ostream & out)
{
  out << "{";
  // member: status
  {
    out << "status: ";
    rosidl_generator_traits::value_to_yaml(msg.status, out);
    out << ", ";
  }

  // member: result
  {
    out << "result: ";
    to_flow_style_yaml(msg.result, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const MovelH2r_GetResult_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: status
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "status: ";
    rosidl_generator_traits::value_to_yaml(msg.status, out);
    out << "\n";
  }

  // member: result
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "result:\n";
    to_block_style_yaml(msg.result, out, indentation + 2);
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const MovelH2r_GetResult_Response & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace action

}  // namespace dsr_msgs2

namespace rosidl_generator_traits
{

[[deprecated("use dsr_msgs2::action::to_block_style_yaml() instead")]]
inline void to_yaml(
  const dsr_msgs2::action::MovelH2r_GetResult_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  dsr_msgs2::action::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use dsr_msgs2::action::to_yaml() instead")]]
inline std::string to_yaml(const dsr_msgs2::action::MovelH2r_GetResult_Response & msg)
{
  return dsr_msgs2::action::to_yaml(msg);
}

template<>
inline const char * data_type<dsr_msgs2::action::MovelH2r_GetResult_Response>()
{
  return "dsr_msgs2::action::MovelH2r_GetResult_Response";
}

template<>
inline const char * name<dsr_msgs2::action::MovelH2r_GetResult_Response>()
{
  return "dsr_msgs2/action/MovelH2r_GetResult_Response";
}

template<>
struct has_fixed_size<dsr_msgs2::action::MovelH2r_GetResult_Response>
  : std::integral_constant<bool, has_fixed_size<dsr_msgs2::action::MovelH2r_Result>::value> {};

template<>
struct has_bounded_size<dsr_msgs2::action::MovelH2r_GetResult_Response>
  : std::integral_constant<bool, has_bounded_size<dsr_msgs2::action::MovelH2r_Result>::value> {};

template<>
struct is_message<dsr_msgs2::action::MovelH2r_GetResult_Response>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<dsr_msgs2::action::MovelH2r_GetResult>()
{
  return "dsr_msgs2::action::MovelH2r_GetResult";
}

template<>
inline const char * name<dsr_msgs2::action::MovelH2r_GetResult>()
{
  return "dsr_msgs2/action/MovelH2r_GetResult";
}

template<>
struct has_fixed_size<dsr_msgs2::action::MovelH2r_GetResult>
  : std::integral_constant<
    bool,
    has_fixed_size<dsr_msgs2::action::MovelH2r_GetResult_Request>::value &&
    has_fixed_size<dsr_msgs2::action::MovelH2r_GetResult_Response>::value
  >
{
};

template<>
struct has_bounded_size<dsr_msgs2::action::MovelH2r_GetResult>
  : std::integral_constant<
    bool,
    has_bounded_size<dsr_msgs2::action::MovelH2r_GetResult_Request>::value &&
    has_bounded_size<dsr_msgs2::action::MovelH2r_GetResult_Response>::value
  >
{
};

template<>
struct is_service<dsr_msgs2::action::MovelH2r_GetResult>
  : std::true_type
{
};

template<>
struct is_service_request<dsr_msgs2::action::MovelH2r_GetResult_Request>
  : std::true_type
{
};

template<>
struct is_service_response<dsr_msgs2::action::MovelH2r_GetResult_Response>
  : std::true_type
{
};

}  // namespace rosidl_generator_traits

// Include directives for member types
// Member 'goal_id'
// already included above
// #include "unique_identifier_msgs/msg/detail/uuid__traits.hpp"
// Member 'feedback'
// already included above
// #include "dsr_msgs2/action/detail/movel_h2r__traits.hpp"

namespace dsr_msgs2
{

namespace action
{

inline void to_flow_style_yaml(
  const MovelH2r_FeedbackMessage & msg,
  std::ostream & out)
{
  out << "{";
  // member: goal_id
  {
    out << "goal_id: ";
    to_flow_style_yaml(msg.goal_id, out);
    out << ", ";
  }

  // member: feedback
  {
    out << "feedback: ";
    to_flow_style_yaml(msg.feedback, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const MovelH2r_FeedbackMessage & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: goal_id
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "goal_id:\n";
    to_block_style_yaml(msg.goal_id, out, indentation + 2);
  }

  // member: feedback
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "feedback:\n";
    to_block_style_yaml(msg.feedback, out, indentation + 2);
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const MovelH2r_FeedbackMessage & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace action

}  // namespace dsr_msgs2

namespace rosidl_generator_traits
{

[[deprecated("use dsr_msgs2::action::to_block_style_yaml() instead")]]
inline void to_yaml(
  const dsr_msgs2::action::MovelH2r_FeedbackMessage & msg,
  std::ostream & out, size_t indentation = 0)
{
  dsr_msgs2::action::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use dsr_msgs2::action::to_yaml() instead")]]
inline std::string to_yaml(const dsr_msgs2::action::MovelH2r_FeedbackMessage & msg)
{
  return dsr_msgs2::action::to_yaml(msg);
}

template<>
inline const char * data_type<dsr_msgs2::action::MovelH2r_FeedbackMessage>()
{
  return "dsr_msgs2::action::MovelH2r_FeedbackMessage";
}

template<>
inline const char * name<dsr_msgs2::action::MovelH2r_FeedbackMessage>()
{
  return "dsr_msgs2/action/MovelH2r_FeedbackMessage";
}

template<>
struct has_fixed_size<dsr_msgs2::action::MovelH2r_FeedbackMessage>
  : std::integral_constant<bool, has_fixed_size<dsr_msgs2::action::MovelH2r_Feedback>::value && has_fixed_size<unique_identifier_msgs::msg::UUID>::value> {};

template<>
struct has_bounded_size<dsr_msgs2::action::MovelH2r_FeedbackMessage>
  : std::integral_constant<bool, has_bounded_size<dsr_msgs2::action::MovelH2r_Feedback>::value && has_bounded_size<unique_identifier_msgs::msg::UUID>::value> {};

template<>
struct is_message<dsr_msgs2::action::MovelH2r_FeedbackMessage>
  : std::true_type {};

}  // namespace rosidl_generator_traits


namespace rosidl_generator_traits
{

template<>
struct is_action<dsr_msgs2::action::MovelH2r>
  : std::true_type
{
};

template<>
struct is_action_goal<dsr_msgs2::action::MovelH2r_Goal>
  : std::true_type
{
};

template<>
struct is_action_result<dsr_msgs2::action::MovelH2r_Result>
  : std::true_type
{
};

template<>
struct is_action_feedback<dsr_msgs2::action::MovelH2r_Feedback>
  : std::true_type
{
};

}  // namespace rosidl_generator_traits


#endif  // DSR_MSGS2__ACTION__DETAIL__MOVEL_H2R__TRAITS_HPP_
