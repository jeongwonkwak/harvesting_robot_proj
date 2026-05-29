// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from dsr_msgs2:srv/GetRobotLinkInfo.idl
// generated code does not contain a copyright notice

#ifndef DSR_MSGS2__SRV__DETAIL__GET_ROBOT_LINK_INFO__TRAITS_HPP_
#define DSR_MSGS2__SRV__DETAIL__GET_ROBOT_LINK_INFO__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "dsr_msgs2/srv/detail/get_robot_link_info__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace dsr_msgs2
{

namespace srv
{

inline void to_flow_style_yaml(
  const GetRobotLinkInfo_Request & msg,
  std::ostream & out)
{
  (void)msg;
  out << "null";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const GetRobotLinkInfo_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  (void)msg;
  (void)indentation;
  out << "null\n";
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const GetRobotLinkInfo_Request & msg, bool use_flow_style = false)
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

}  // namespace dsr_msgs2

namespace rosidl_generator_traits
{

[[deprecated("use dsr_msgs2::srv::to_block_style_yaml() instead")]]
inline void to_yaml(
  const dsr_msgs2::srv::GetRobotLinkInfo_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  dsr_msgs2::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use dsr_msgs2::srv::to_yaml() instead")]]
inline std::string to_yaml(const dsr_msgs2::srv::GetRobotLinkInfo_Request & msg)
{
  return dsr_msgs2::srv::to_yaml(msg);
}

template<>
inline const char * data_type<dsr_msgs2::srv::GetRobotLinkInfo_Request>()
{
  return "dsr_msgs2::srv::GetRobotLinkInfo_Request";
}

template<>
inline const char * name<dsr_msgs2::srv::GetRobotLinkInfo_Request>()
{
  return "dsr_msgs2/srv/GetRobotLinkInfo_Request";
}

template<>
struct has_fixed_size<dsr_msgs2::srv::GetRobotLinkInfo_Request>
  : std::integral_constant<bool, true> {};

template<>
struct has_bounded_size<dsr_msgs2::srv::GetRobotLinkInfo_Request>
  : std::integral_constant<bool, true> {};

template<>
struct is_message<dsr_msgs2::srv::GetRobotLinkInfo_Request>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace dsr_msgs2
{

namespace srv
{

inline void to_flow_style_yaml(
  const GetRobotLinkInfo_Response & msg,
  std::ostream & out)
{
  out << "{";
  // member: d
  {
    if (msg.d.size() == 0) {
      out << "d: []";
    } else {
      out << "d: [";
      size_t pending_items = msg.d.size();
      for (auto item : msg.d) {
        rosidl_generator_traits::value_to_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
    out << ", ";
  }

  // member: a
  {
    if (msg.a.size() == 0) {
      out << "a: []";
    } else {
      out << "a: [";
      size_t pending_items = msg.a.size();
      for (auto item : msg.a) {
        rosidl_generator_traits::value_to_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
    out << ", ";
  }

  // member: alpha
  {
    if (msg.alpha.size() == 0) {
      out << "alpha: []";
    } else {
      out << "alpha: [";
      size_t pending_items = msg.alpha.size();
      for (auto item : msg.alpha) {
        rosidl_generator_traits::value_to_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
    out << ", ";
  }

  // member: theta
  {
    if (msg.theta.size() == 0) {
      out << "theta: []";
    } else {
      out << "theta: [";
      size_t pending_items = msg.theta.size();
      for (auto item : msg.theta) {
        rosidl_generator_traits::value_to_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
    out << ", ";
  }

  // member: offset
  {
    if (msg.offset.size() == 0) {
      out << "offset: []";
    } else {
      out << "offset: [";
      size_t pending_items = msg.offset.size();
      for (auto item : msg.offset) {
        rosidl_generator_traits::value_to_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
    out << ", ";
  }

  // member: gradient
  {
    out << "gradient: ";
    rosidl_generator_traits::value_to_yaml(msg.gradient, out);
    out << ", ";
  }

  // member: rotation
  {
    out << "rotation: ";
    rosidl_generator_traits::value_to_yaml(msg.rotation, out);
    out << ", ";
  }

  // member: success
  {
    out << "success: ";
    rosidl_generator_traits::value_to_yaml(msg.success, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const GetRobotLinkInfo_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: d
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.d.size() == 0) {
      out << "d: []\n";
    } else {
      out << "d:\n";
      for (auto item : msg.d) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "- ";
        rosidl_generator_traits::value_to_yaml(item, out);
        out << "\n";
      }
    }
  }

  // member: a
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.a.size() == 0) {
      out << "a: []\n";
    } else {
      out << "a:\n";
      for (auto item : msg.a) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "- ";
        rosidl_generator_traits::value_to_yaml(item, out);
        out << "\n";
      }
    }
  }

  // member: alpha
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.alpha.size() == 0) {
      out << "alpha: []\n";
    } else {
      out << "alpha:\n";
      for (auto item : msg.alpha) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "- ";
        rosidl_generator_traits::value_to_yaml(item, out);
        out << "\n";
      }
    }
  }

  // member: theta
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.theta.size() == 0) {
      out << "theta: []\n";
    } else {
      out << "theta:\n";
      for (auto item : msg.theta) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "- ";
        rosidl_generator_traits::value_to_yaml(item, out);
        out << "\n";
      }
    }
  }

  // member: offset
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.offset.size() == 0) {
      out << "offset: []\n";
    } else {
      out << "offset:\n";
      for (auto item : msg.offset) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "- ";
        rosidl_generator_traits::value_to_yaml(item, out);
        out << "\n";
      }
    }
  }

  // member: gradient
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "gradient: ";
    rosidl_generator_traits::value_to_yaml(msg.gradient, out);
    out << "\n";
  }

  // member: rotation
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "rotation: ";
    rosidl_generator_traits::value_to_yaml(msg.rotation, out);
    out << "\n";
  }

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

inline std::string to_yaml(const GetRobotLinkInfo_Response & msg, bool use_flow_style = false)
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

}  // namespace dsr_msgs2

namespace rosidl_generator_traits
{

[[deprecated("use dsr_msgs2::srv::to_block_style_yaml() instead")]]
inline void to_yaml(
  const dsr_msgs2::srv::GetRobotLinkInfo_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  dsr_msgs2::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use dsr_msgs2::srv::to_yaml() instead")]]
inline std::string to_yaml(const dsr_msgs2::srv::GetRobotLinkInfo_Response & msg)
{
  return dsr_msgs2::srv::to_yaml(msg);
}

template<>
inline const char * data_type<dsr_msgs2::srv::GetRobotLinkInfo_Response>()
{
  return "dsr_msgs2::srv::GetRobotLinkInfo_Response";
}

template<>
inline const char * name<dsr_msgs2::srv::GetRobotLinkInfo_Response>()
{
  return "dsr_msgs2/srv/GetRobotLinkInfo_Response";
}

template<>
struct has_fixed_size<dsr_msgs2::srv::GetRobotLinkInfo_Response>
  : std::integral_constant<bool, true> {};

template<>
struct has_bounded_size<dsr_msgs2::srv::GetRobotLinkInfo_Response>
  : std::integral_constant<bool, true> {};

template<>
struct is_message<dsr_msgs2::srv::GetRobotLinkInfo_Response>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<dsr_msgs2::srv::GetRobotLinkInfo>()
{
  return "dsr_msgs2::srv::GetRobotLinkInfo";
}

template<>
inline const char * name<dsr_msgs2::srv::GetRobotLinkInfo>()
{
  return "dsr_msgs2/srv/GetRobotLinkInfo";
}

template<>
struct has_fixed_size<dsr_msgs2::srv::GetRobotLinkInfo>
  : std::integral_constant<
    bool,
    has_fixed_size<dsr_msgs2::srv::GetRobotLinkInfo_Request>::value &&
    has_fixed_size<dsr_msgs2::srv::GetRobotLinkInfo_Response>::value
  >
{
};

template<>
struct has_bounded_size<dsr_msgs2::srv::GetRobotLinkInfo>
  : std::integral_constant<
    bool,
    has_bounded_size<dsr_msgs2::srv::GetRobotLinkInfo_Request>::value &&
    has_bounded_size<dsr_msgs2::srv::GetRobotLinkInfo_Response>::value
  >
{
};

template<>
struct is_service<dsr_msgs2::srv::GetRobotLinkInfo>
  : std::true_type
{
};

template<>
struct is_service_request<dsr_msgs2::srv::GetRobotLinkInfo_Request>
  : std::true_type
{
};

template<>
struct is_service_response<dsr_msgs2::srv::GetRobotLinkInfo_Response>
  : std::true_type
{
};

}  // namespace rosidl_generator_traits

#endif  // DSR_MSGS2__SRV__DETAIL__GET_ROBOT_LINK_INFO__TRAITS_HPP_
