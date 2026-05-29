// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from dsr_msgs2:srv/FlangeSerialRead.idl
// generated code does not contain a copyright notice

#ifndef DSR_MSGS2__SRV__DETAIL__FLANGE_SERIAL_READ__TRAITS_HPP_
#define DSR_MSGS2__SRV__DETAIL__FLANGE_SERIAL_READ__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "dsr_msgs2/srv/detail/flange_serial_read__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace dsr_msgs2
{

namespace srv
{

inline void to_flow_style_yaml(
  const FlangeSerialRead_Request & msg,
  std::ostream & out)
{
  out << "{";
  // member: port
  {
    out << "port: ";
    rosidl_generator_traits::value_to_yaml(msg.port, out);
    out << ", ";
  }

  // member: timeout
  {
    out << "timeout: ";
    rosidl_generator_traits::value_to_yaml(msg.timeout, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const FlangeSerialRead_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: port
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "port: ";
    rosidl_generator_traits::value_to_yaml(msg.port, out);
    out << "\n";
  }

  // member: timeout
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "timeout: ";
    rosidl_generator_traits::value_to_yaml(msg.timeout, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const FlangeSerialRead_Request & msg, bool use_flow_style = false)
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
  const dsr_msgs2::srv::FlangeSerialRead_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  dsr_msgs2::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use dsr_msgs2::srv::to_yaml() instead")]]
inline std::string to_yaml(const dsr_msgs2::srv::FlangeSerialRead_Request & msg)
{
  return dsr_msgs2::srv::to_yaml(msg);
}

template<>
inline const char * data_type<dsr_msgs2::srv::FlangeSerialRead_Request>()
{
  return "dsr_msgs2::srv::FlangeSerialRead_Request";
}

template<>
inline const char * name<dsr_msgs2::srv::FlangeSerialRead_Request>()
{
  return "dsr_msgs2/srv/FlangeSerialRead_Request";
}

template<>
struct has_fixed_size<dsr_msgs2::srv::FlangeSerialRead_Request>
  : std::integral_constant<bool, true> {};

template<>
struct has_bounded_size<dsr_msgs2::srv::FlangeSerialRead_Request>
  : std::integral_constant<bool, true> {};

template<>
struct is_message<dsr_msgs2::srv::FlangeSerialRead_Request>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace dsr_msgs2
{

namespace srv
{

inline void to_flow_style_yaml(
  const FlangeSerialRead_Response & msg,
  std::ostream & out)
{
  out << "{";
  // member: success
  {
    out << "success: ";
    rosidl_generator_traits::value_to_yaml(msg.success, out);
    out << ", ";
  }

  // member: size
  {
    out << "size: ";
    rosidl_generator_traits::value_to_yaml(msg.size, out);
    out << ", ";
  }

  // member: data
  {
    if (msg.data.size() == 0) {
      out << "data: []";
    } else {
      out << "data: [";
      size_t pending_items = msg.data.size();
      for (auto item : msg.data) {
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
  const FlangeSerialRead_Response & msg,
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

  // member: size
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "size: ";
    rosidl_generator_traits::value_to_yaml(msg.size, out);
    out << "\n";
  }

  // member: data
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.data.size() == 0) {
      out << "data: []\n";
    } else {
      out << "data:\n";
      for (auto item : msg.data) {
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

inline std::string to_yaml(const FlangeSerialRead_Response & msg, bool use_flow_style = false)
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
  const dsr_msgs2::srv::FlangeSerialRead_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  dsr_msgs2::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use dsr_msgs2::srv::to_yaml() instead")]]
inline std::string to_yaml(const dsr_msgs2::srv::FlangeSerialRead_Response & msg)
{
  return dsr_msgs2::srv::to_yaml(msg);
}

template<>
inline const char * data_type<dsr_msgs2::srv::FlangeSerialRead_Response>()
{
  return "dsr_msgs2::srv::FlangeSerialRead_Response";
}

template<>
inline const char * name<dsr_msgs2::srv::FlangeSerialRead_Response>()
{
  return "dsr_msgs2/srv/FlangeSerialRead_Response";
}

template<>
struct has_fixed_size<dsr_msgs2::srv::FlangeSerialRead_Response>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<dsr_msgs2::srv::FlangeSerialRead_Response>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<dsr_msgs2::srv::FlangeSerialRead_Response>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<dsr_msgs2::srv::FlangeSerialRead>()
{
  return "dsr_msgs2::srv::FlangeSerialRead";
}

template<>
inline const char * name<dsr_msgs2::srv::FlangeSerialRead>()
{
  return "dsr_msgs2/srv/FlangeSerialRead";
}

template<>
struct has_fixed_size<dsr_msgs2::srv::FlangeSerialRead>
  : std::integral_constant<
    bool,
    has_fixed_size<dsr_msgs2::srv::FlangeSerialRead_Request>::value &&
    has_fixed_size<dsr_msgs2::srv::FlangeSerialRead_Response>::value
  >
{
};

template<>
struct has_bounded_size<dsr_msgs2::srv::FlangeSerialRead>
  : std::integral_constant<
    bool,
    has_bounded_size<dsr_msgs2::srv::FlangeSerialRead_Request>::value &&
    has_bounded_size<dsr_msgs2::srv::FlangeSerialRead_Response>::value
  >
{
};

template<>
struct is_service<dsr_msgs2::srv::FlangeSerialRead>
  : std::true_type
{
};

template<>
struct is_service_request<dsr_msgs2::srv::FlangeSerialRead_Request>
  : std::true_type
{
};

template<>
struct is_service_response<dsr_msgs2::srv::FlangeSerialRead_Response>
  : std::true_type
{
};

}  // namespace rosidl_generator_traits

#endif  // DSR_MSGS2__SRV__DETAIL__FLANGE_SERIAL_READ__TRAITS_HPP_
