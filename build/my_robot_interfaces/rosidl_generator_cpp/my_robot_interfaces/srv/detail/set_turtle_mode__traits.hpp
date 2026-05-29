// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from my_robot_interfaces:srv/SetTurtleMode.idl
// generated code does not contain a copyright notice

#ifndef MY_ROBOT_INTERFACES__SRV__DETAIL__SET_TURTLE_MODE__TRAITS_HPP_
#define MY_ROBOT_INTERFACES__SRV__DETAIL__SET_TURTLE_MODE__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "my_robot_interfaces/srv/detail/set_turtle_mode__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace my_robot_interfaces
{

namespace srv
{

inline void to_flow_style_yaml(
  const SetTurtleMode_Request & msg,
  std::ostream & out)
{
  out << "{";
  // member: mode_name
  {
    out << "mode_name: ";
    rosidl_generator_traits::value_to_yaml(msg.mode_name, out);
    out << ", ";
  }

  // member: target_speed
  {
    out << "target_speed: ";
    rosidl_generator_traits::value_to_yaml(msg.target_speed, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const SetTurtleMode_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: mode_name
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "mode_name: ";
    rosidl_generator_traits::value_to_yaml(msg.mode_name, out);
    out << "\n";
  }

  // member: target_speed
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "target_speed: ";
    rosidl_generator_traits::value_to_yaml(msg.target_speed, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const SetTurtleMode_Request & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace srv

}  // namespace my_robot_interfaces

namespace rosidl_generator_traits
{

[[deprecated("use my_robot_interfaces::srv::to_block_style_yaml() instead")]]
inline void to_yaml(
  const my_robot_interfaces::srv::SetTurtleMode_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  my_robot_interfaces::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use my_robot_interfaces::srv::to_yaml() instead")]]
inline std::string to_yaml(const my_robot_interfaces::srv::SetTurtleMode_Request & msg)
{
  return my_robot_interfaces::srv::to_yaml(msg);
}

template<>
inline const char * data_type<my_robot_interfaces::srv::SetTurtleMode_Request>()
{
  return "my_robot_interfaces::srv::SetTurtleMode_Request";
}

template<>
inline const char * name<my_robot_interfaces::srv::SetTurtleMode_Request>()
{
  return "my_robot_interfaces/srv/SetTurtleMode_Request";
}

template<>
struct has_fixed_size<my_robot_interfaces::srv::SetTurtleMode_Request>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<my_robot_interfaces::srv::SetTurtleMode_Request>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<my_robot_interfaces::srv::SetTurtleMode_Request>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace my_robot_interfaces
{

namespace srv
{

inline void to_flow_style_yaml(
  const SetTurtleMode_Response & msg,
  std::ostream & out)
{
  out << "{";
  // member: success
  {
    out << "success: ";
    rosidl_generator_traits::value_to_yaml(msg.success, out);
    out << ", ";
  }

  // member: message
  {
    out << "message: ";
    rosidl_generator_traits::value_to_yaml(msg.message, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const SetTurtleMode_Response & msg,
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

  // member: message
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "message: ";
    rosidl_generator_traits::value_to_yaml(msg.message, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const SetTurtleMode_Response & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace srv

}  // namespace my_robot_interfaces

namespace rosidl_generator_traits
{

[[deprecated("use my_robot_interfaces::srv::to_block_style_yaml() instead")]]
inline void to_yaml(
  const my_robot_interfaces::srv::SetTurtleMode_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  my_robot_interfaces::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use my_robot_interfaces::srv::to_yaml() instead")]]
inline std::string to_yaml(const my_robot_interfaces::srv::SetTurtleMode_Response & msg)
{
  return my_robot_interfaces::srv::to_yaml(msg);
}

template<>
inline const char * data_type<my_robot_interfaces::srv::SetTurtleMode_Response>()
{
  return "my_robot_interfaces::srv::SetTurtleMode_Response";
}

template<>
inline const char * name<my_robot_interfaces::srv::SetTurtleMode_Response>()
{
  return "my_robot_interfaces/srv/SetTurtleMode_Response";
}

template<>
struct has_fixed_size<my_robot_interfaces::srv::SetTurtleMode_Response>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<my_robot_interfaces::srv::SetTurtleMode_Response>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<my_robot_interfaces::srv::SetTurtleMode_Response>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<my_robot_interfaces::srv::SetTurtleMode>()
{
  return "my_robot_interfaces::srv::SetTurtleMode";
}

template<>
inline const char * name<my_robot_interfaces::srv::SetTurtleMode>()
{
  return "my_robot_interfaces/srv/SetTurtleMode";
}

template<>
struct has_fixed_size<my_robot_interfaces::srv::SetTurtleMode>
  : std::integral_constant<
    bool,
    has_fixed_size<my_robot_interfaces::srv::SetTurtleMode_Request>::value &&
    has_fixed_size<my_robot_interfaces::srv::SetTurtleMode_Response>::value
  >
{
};

template<>
struct has_bounded_size<my_robot_interfaces::srv::SetTurtleMode>
  : std::integral_constant<
    bool,
    has_bounded_size<my_robot_interfaces::srv::SetTurtleMode_Request>::value &&
    has_bounded_size<my_robot_interfaces::srv::SetTurtleMode_Response>::value
  >
{
};

template<>
struct is_service<my_robot_interfaces::srv::SetTurtleMode>
  : std::true_type
{
};

template<>
struct is_service_request<my_robot_interfaces::srv::SetTurtleMode_Request>
  : std::true_type
{
};

template<>
struct is_service_response<my_robot_interfaces::srv::SetTurtleMode_Response>
  : std::true_type
{
};

}  // namespace rosidl_generator_traits

#endif  // MY_ROBOT_INTERFACES__SRV__DETAIL__SET_TURTLE_MODE__TRAITS_HPP_
