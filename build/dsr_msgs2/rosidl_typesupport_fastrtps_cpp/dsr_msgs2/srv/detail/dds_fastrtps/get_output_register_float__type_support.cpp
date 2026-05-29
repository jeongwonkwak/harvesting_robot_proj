// generated from rosidl_typesupport_fastrtps_cpp/resource/idl__type_support.cpp.em
// with input from dsr_msgs2:srv/GetOutputRegisterFloat.idl
// generated code does not contain a copyright notice
#include "dsr_msgs2/srv/detail/get_output_register_float__rosidl_typesupport_fastrtps_cpp.hpp"
#include "dsr_msgs2/srv/detail/get_output_register_float__struct.hpp"

#include <limits>
#include <stdexcept>
#include <string>
#include "rosidl_typesupport_cpp/message_type_support.hpp"
#include "rosidl_typesupport_fastrtps_cpp/identifier.hpp"
#include "rosidl_typesupport_fastrtps_cpp/message_type_support.h"
#include "rosidl_typesupport_fastrtps_cpp/message_type_support_decl.hpp"
#include "rosidl_typesupport_fastrtps_cpp/wstring_conversion.hpp"
#include "fastcdr/Cdr.h"


// forward declaration of message dependencies and their conversion functions

namespace dsr_msgs2
{

namespace srv
{

namespace typesupport_fastrtps_cpp
{

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_dsr_msgs2
cdr_serialize(
  const dsr_msgs2::srv::GetOutputRegisterFloat_Request & ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  // Member: address
  cdr << ros_message.address;
  // Member: timeout_ms
  cdr << ros_message.timeout_ms;
  return true;
}

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_dsr_msgs2
cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  dsr_msgs2::srv::GetOutputRegisterFloat_Request & ros_message)
{
  // Member: address
  cdr >> ros_message.address;

  // Member: timeout_ms
  cdr >> ros_message.timeout_ms;

  return true;
}  // NOLINT(readability/fn_size)

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_dsr_msgs2
get_serialized_size(
  const dsr_msgs2::srv::GetOutputRegisterFloat_Request & ros_message,
  size_t current_alignment)
{
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  (void)padding;
  (void)wchar_size;

  // Member: address
  {
    size_t item_size = sizeof(ros_message.address);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // Member: timeout_ms
  {
    size_t item_size = sizeof(ros_message.timeout_ms);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  return current_alignment - initial_alignment;
}

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_dsr_msgs2
max_serialized_size_GetOutputRegisterFloat_Request(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment)
{
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  size_t last_member_size = 0;
  (void)last_member_size;
  (void)padding;
  (void)wchar_size;

  full_bounded = true;
  is_plain = true;


  // Member: address
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint16_t);
    current_alignment += array_size * sizeof(uint16_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint16_t));
  }

  // Member: timeout_ms
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint32_t);
    current_alignment += array_size * sizeof(uint32_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint32_t));
  }

  size_t ret_val = current_alignment - initial_alignment;
  if (is_plain) {
    // All members are plain, and type is not empty.
    // We still need to check that the in-memory alignment
    // is the same as the CDR mandated alignment.
    using DataType = dsr_msgs2::srv::GetOutputRegisterFloat_Request;
    is_plain =
      (
      offsetof(DataType, timeout_ms) +
      last_member_size
      ) == ret_val;
  }

  return ret_val;
}

static bool _GetOutputRegisterFloat_Request__cdr_serialize(
  const void * untyped_ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  auto typed_message =
    static_cast<const dsr_msgs2::srv::GetOutputRegisterFloat_Request *>(
    untyped_ros_message);
  return cdr_serialize(*typed_message, cdr);
}

static bool _GetOutputRegisterFloat_Request__cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  void * untyped_ros_message)
{
  auto typed_message =
    static_cast<dsr_msgs2::srv::GetOutputRegisterFloat_Request *>(
    untyped_ros_message);
  return cdr_deserialize(cdr, *typed_message);
}

static uint32_t _GetOutputRegisterFloat_Request__get_serialized_size(
  const void * untyped_ros_message)
{
  auto typed_message =
    static_cast<const dsr_msgs2::srv::GetOutputRegisterFloat_Request *>(
    untyped_ros_message);
  return static_cast<uint32_t>(get_serialized_size(*typed_message, 0));
}

static size_t _GetOutputRegisterFloat_Request__max_serialized_size(char & bounds_info)
{
  bool full_bounded;
  bool is_plain;
  size_t ret_val;

  ret_val = max_serialized_size_GetOutputRegisterFloat_Request(full_bounded, is_plain, 0);

  bounds_info =
    is_plain ? ROSIDL_TYPESUPPORT_FASTRTPS_PLAIN_TYPE :
    full_bounded ? ROSIDL_TYPESUPPORT_FASTRTPS_BOUNDED_TYPE : ROSIDL_TYPESUPPORT_FASTRTPS_UNBOUNDED_TYPE;
  return ret_val;
}

static message_type_support_callbacks_t _GetOutputRegisterFloat_Request__callbacks = {
  "dsr_msgs2::srv",
  "GetOutputRegisterFloat_Request",
  _GetOutputRegisterFloat_Request__cdr_serialize,
  _GetOutputRegisterFloat_Request__cdr_deserialize,
  _GetOutputRegisterFloat_Request__get_serialized_size,
  _GetOutputRegisterFloat_Request__max_serialized_size
};

static rosidl_message_type_support_t _GetOutputRegisterFloat_Request__handle = {
  rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
  &_GetOutputRegisterFloat_Request__callbacks,
  get_message_typesupport_handle_function,
};

}  // namespace typesupport_fastrtps_cpp

}  // namespace srv

}  // namespace dsr_msgs2

namespace rosidl_typesupport_fastrtps_cpp
{

template<>
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_EXPORT_dsr_msgs2
const rosidl_message_type_support_t *
get_message_type_support_handle<dsr_msgs2::srv::GetOutputRegisterFloat_Request>()
{
  return &dsr_msgs2::srv::typesupport_fastrtps_cpp::_GetOutputRegisterFloat_Request__handle;
}

}  // namespace rosidl_typesupport_fastrtps_cpp

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, dsr_msgs2, srv, GetOutputRegisterFloat_Request)() {
  return &dsr_msgs2::srv::typesupport_fastrtps_cpp::_GetOutputRegisterFloat_Request__handle;
}

#ifdef __cplusplus
}
#endif

// already included above
// #include <limits>
// already included above
// #include <stdexcept>
// already included above
// #include <string>
// already included above
// #include "rosidl_typesupport_cpp/message_type_support.hpp"
// already included above
// #include "rosidl_typesupport_fastrtps_cpp/identifier.hpp"
// already included above
// #include "rosidl_typesupport_fastrtps_cpp/message_type_support.h"
// already included above
// #include "rosidl_typesupport_fastrtps_cpp/message_type_support_decl.hpp"
// already included above
// #include "rosidl_typesupport_fastrtps_cpp/wstring_conversion.hpp"
// already included above
// #include "fastcdr/Cdr.h"


// forward declaration of message dependencies and their conversion functions

namespace dsr_msgs2
{

namespace srv
{

namespace typesupport_fastrtps_cpp
{

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_dsr_msgs2
cdr_serialize(
  const dsr_msgs2::srv::GetOutputRegisterFloat_Response & ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  // Member: success
  cdr << (ros_message.success ? true : false);
  // Member: value
  cdr << ros_message.value;
  return true;
}

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_dsr_msgs2
cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  dsr_msgs2::srv::GetOutputRegisterFloat_Response & ros_message)
{
  // Member: success
  {
    uint8_t tmp;
    cdr >> tmp;
    ros_message.success = tmp ? true : false;
  }

  // Member: value
  cdr >> ros_message.value;

  return true;
}  // NOLINT(readability/fn_size)

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_dsr_msgs2
get_serialized_size(
  const dsr_msgs2::srv::GetOutputRegisterFloat_Response & ros_message,
  size_t current_alignment)
{
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  (void)padding;
  (void)wchar_size;

  // Member: success
  {
    size_t item_size = sizeof(ros_message.success);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // Member: value
  {
    size_t item_size = sizeof(ros_message.value);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  return current_alignment - initial_alignment;
}

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_dsr_msgs2
max_serialized_size_GetOutputRegisterFloat_Response(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment)
{
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  size_t last_member_size = 0;
  (void)last_member_size;
  (void)padding;
  (void)wchar_size;

  full_bounded = true;
  is_plain = true;


  // Member: success
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint8_t);
    current_alignment += array_size * sizeof(uint8_t);
  }

  // Member: value
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint64_t);
    current_alignment += array_size * sizeof(uint64_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint64_t));
  }

  size_t ret_val = current_alignment - initial_alignment;
  if (is_plain) {
    // All members are plain, and type is not empty.
    // We still need to check that the in-memory alignment
    // is the same as the CDR mandated alignment.
    using DataType = dsr_msgs2::srv::GetOutputRegisterFloat_Response;
    is_plain =
      (
      offsetof(DataType, value) +
      last_member_size
      ) == ret_val;
  }

  return ret_val;
}

static bool _GetOutputRegisterFloat_Response__cdr_serialize(
  const void * untyped_ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  auto typed_message =
    static_cast<const dsr_msgs2::srv::GetOutputRegisterFloat_Response *>(
    untyped_ros_message);
  return cdr_serialize(*typed_message, cdr);
}

static bool _GetOutputRegisterFloat_Response__cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  void * untyped_ros_message)
{
  auto typed_message =
    static_cast<dsr_msgs2::srv::GetOutputRegisterFloat_Response *>(
    untyped_ros_message);
  return cdr_deserialize(cdr, *typed_message);
}

static uint32_t _GetOutputRegisterFloat_Response__get_serialized_size(
  const void * untyped_ros_message)
{
  auto typed_message =
    static_cast<const dsr_msgs2::srv::GetOutputRegisterFloat_Response *>(
    untyped_ros_message);
  return static_cast<uint32_t>(get_serialized_size(*typed_message, 0));
}

static size_t _GetOutputRegisterFloat_Response__max_serialized_size(char & bounds_info)
{
  bool full_bounded;
  bool is_plain;
  size_t ret_val;

  ret_val = max_serialized_size_GetOutputRegisterFloat_Response(full_bounded, is_plain, 0);

  bounds_info =
    is_plain ? ROSIDL_TYPESUPPORT_FASTRTPS_PLAIN_TYPE :
    full_bounded ? ROSIDL_TYPESUPPORT_FASTRTPS_BOUNDED_TYPE : ROSIDL_TYPESUPPORT_FASTRTPS_UNBOUNDED_TYPE;
  return ret_val;
}

static message_type_support_callbacks_t _GetOutputRegisterFloat_Response__callbacks = {
  "dsr_msgs2::srv",
  "GetOutputRegisterFloat_Response",
  _GetOutputRegisterFloat_Response__cdr_serialize,
  _GetOutputRegisterFloat_Response__cdr_deserialize,
  _GetOutputRegisterFloat_Response__get_serialized_size,
  _GetOutputRegisterFloat_Response__max_serialized_size
};

static rosidl_message_type_support_t _GetOutputRegisterFloat_Response__handle = {
  rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
  &_GetOutputRegisterFloat_Response__callbacks,
  get_message_typesupport_handle_function,
};

}  // namespace typesupport_fastrtps_cpp

}  // namespace srv

}  // namespace dsr_msgs2

namespace rosidl_typesupport_fastrtps_cpp
{

template<>
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_EXPORT_dsr_msgs2
const rosidl_message_type_support_t *
get_message_type_support_handle<dsr_msgs2::srv::GetOutputRegisterFloat_Response>()
{
  return &dsr_msgs2::srv::typesupport_fastrtps_cpp::_GetOutputRegisterFloat_Response__handle;
}

}  // namespace rosidl_typesupport_fastrtps_cpp

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, dsr_msgs2, srv, GetOutputRegisterFloat_Response)() {
  return &dsr_msgs2::srv::typesupport_fastrtps_cpp::_GetOutputRegisterFloat_Response__handle;
}

#ifdef __cplusplus
}
#endif

#include "rmw/error_handling.h"
// already included above
// #include "rosidl_typesupport_fastrtps_cpp/identifier.hpp"
#include "rosidl_typesupport_fastrtps_cpp/service_type_support.h"
#include "rosidl_typesupport_fastrtps_cpp/service_type_support_decl.hpp"

namespace dsr_msgs2
{

namespace srv
{

namespace typesupport_fastrtps_cpp
{

static service_type_support_callbacks_t _GetOutputRegisterFloat__callbacks = {
  "dsr_msgs2::srv",
  "GetOutputRegisterFloat",
  ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, dsr_msgs2, srv, GetOutputRegisterFloat_Request)(),
  ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, dsr_msgs2, srv, GetOutputRegisterFloat_Response)(),
};

static rosidl_service_type_support_t _GetOutputRegisterFloat__handle = {
  rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
  &_GetOutputRegisterFloat__callbacks,
  get_service_typesupport_handle_function,
};

}  // namespace typesupport_fastrtps_cpp

}  // namespace srv

}  // namespace dsr_msgs2

namespace rosidl_typesupport_fastrtps_cpp
{

template<>
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_EXPORT_dsr_msgs2
const rosidl_service_type_support_t *
get_service_type_support_handle<dsr_msgs2::srv::GetOutputRegisterFloat>()
{
  return &dsr_msgs2::srv::typesupport_fastrtps_cpp::_GetOutputRegisterFloat__handle;
}

}  // namespace rosidl_typesupport_fastrtps_cpp

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_service_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, dsr_msgs2, srv, GetOutputRegisterFloat)() {
  return &dsr_msgs2::srv::typesupport_fastrtps_cpp::_GetOutputRegisterFloat__handle;
}

#ifdef __cplusplus
}
#endif
