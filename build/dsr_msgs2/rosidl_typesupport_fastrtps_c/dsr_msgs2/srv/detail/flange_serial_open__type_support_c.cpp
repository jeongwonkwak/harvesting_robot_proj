// generated from rosidl_typesupport_fastrtps_c/resource/idl__type_support_c.cpp.em
// with input from dsr_msgs2:srv/FlangeSerialOpen.idl
// generated code does not contain a copyright notice
#include "dsr_msgs2/srv/detail/flange_serial_open__rosidl_typesupport_fastrtps_c.h"


#include <cassert>
#include <limits>
#include <string>
#include "rosidl_typesupport_fastrtps_c/identifier.h"
#include "rosidl_typesupport_fastrtps_c/wstring_conversion.hpp"
#include "rosidl_typesupport_fastrtps_cpp/message_type_support.h"
#include "dsr_msgs2/msg/rosidl_typesupport_fastrtps_c__visibility_control.h"
#include "dsr_msgs2/srv/detail/flange_serial_open__struct.h"
#include "dsr_msgs2/srv/detail/flange_serial_open__functions.h"
#include "fastcdr/Cdr.h"

#ifndef _WIN32
# pragma GCC diagnostic push
# pragma GCC diagnostic ignored "-Wunused-parameter"
# ifdef __clang__
#  pragma clang diagnostic ignored "-Wdeprecated-register"
#  pragma clang diagnostic ignored "-Wreturn-type-c-linkage"
# endif
#endif
#ifndef _WIN32
# pragma GCC diagnostic pop
#endif

// includes and forward declarations of message dependencies and their conversion functions

#if defined(__cplusplus)
extern "C"
{
#endif


// forward declare type support functions


using _FlangeSerialOpen_Request__ros_msg_type = dsr_msgs2__srv__FlangeSerialOpen_Request;

static bool _FlangeSerialOpen_Request__cdr_serialize(
  const void * untyped_ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  if (!untyped_ros_message) {
    fprintf(stderr, "ros message handle is null\n");
    return false;
  }
  const _FlangeSerialOpen_Request__ros_msg_type * ros_message = static_cast<const _FlangeSerialOpen_Request__ros_msg_type *>(untyped_ros_message);
  // Field name: port
  {
    cdr << ros_message->port;
  }

  // Field name: baudrate
  {
    cdr << ros_message->baudrate;
  }

  // Field name: bytesize
  {
    cdr << ros_message->bytesize;
  }

  // Field name: parity
  {
    cdr << ros_message->parity;
  }

  // Field name: stopbits
  {
    cdr << ros_message->stopbits;
  }

  return true;
}

static bool _FlangeSerialOpen_Request__cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  void * untyped_ros_message)
{
  if (!untyped_ros_message) {
    fprintf(stderr, "ros message handle is null\n");
    return false;
  }
  _FlangeSerialOpen_Request__ros_msg_type * ros_message = static_cast<_FlangeSerialOpen_Request__ros_msg_type *>(untyped_ros_message);
  // Field name: port
  {
    cdr >> ros_message->port;
  }

  // Field name: baudrate
  {
    cdr >> ros_message->baudrate;
  }

  // Field name: bytesize
  {
    cdr >> ros_message->bytesize;
  }

  // Field name: parity
  {
    cdr >> ros_message->parity;
  }

  // Field name: stopbits
  {
    cdr >> ros_message->stopbits;
  }

  return true;
}  // NOLINT(readability/fn_size)

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_dsr_msgs2
size_t get_serialized_size_dsr_msgs2__srv__FlangeSerialOpen_Request(
  const void * untyped_ros_message,
  size_t current_alignment)
{
  const _FlangeSerialOpen_Request__ros_msg_type * ros_message = static_cast<const _FlangeSerialOpen_Request__ros_msg_type *>(untyped_ros_message);
  (void)ros_message;
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  (void)padding;
  (void)wchar_size;

  // field.name port
  {
    size_t item_size = sizeof(ros_message->port);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // field.name baudrate
  {
    size_t item_size = sizeof(ros_message->baudrate);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // field.name bytesize
  {
    size_t item_size = sizeof(ros_message->bytesize);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // field.name parity
  {
    size_t item_size = sizeof(ros_message->parity);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // field.name stopbits
  {
    size_t item_size = sizeof(ros_message->stopbits);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  return current_alignment - initial_alignment;
}

static uint32_t _FlangeSerialOpen_Request__get_serialized_size(const void * untyped_ros_message)
{
  return static_cast<uint32_t>(
    get_serialized_size_dsr_msgs2__srv__FlangeSerialOpen_Request(
      untyped_ros_message, 0));
}

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_dsr_msgs2
size_t max_serialized_size_dsr_msgs2__srv__FlangeSerialOpen_Request(
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

  // member: port
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint32_t);
    current_alignment += array_size * sizeof(uint32_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint32_t));
  }
  // member: baudrate
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint32_t);
    current_alignment += array_size * sizeof(uint32_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint32_t));
  }
  // member: bytesize
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint32_t);
    current_alignment += array_size * sizeof(uint32_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint32_t));
  }
  // member: parity
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint32_t);
    current_alignment += array_size * sizeof(uint32_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint32_t));
  }
  // member: stopbits
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
    using DataType = dsr_msgs2__srv__FlangeSerialOpen_Request;
    is_plain =
      (
      offsetof(DataType, stopbits) +
      last_member_size
      ) == ret_val;
  }

  return ret_val;
}

static size_t _FlangeSerialOpen_Request__max_serialized_size(char & bounds_info)
{
  bool full_bounded;
  bool is_plain;
  size_t ret_val;

  ret_val = max_serialized_size_dsr_msgs2__srv__FlangeSerialOpen_Request(
    full_bounded, is_plain, 0);

  bounds_info =
    is_plain ? ROSIDL_TYPESUPPORT_FASTRTPS_PLAIN_TYPE :
    full_bounded ? ROSIDL_TYPESUPPORT_FASTRTPS_BOUNDED_TYPE : ROSIDL_TYPESUPPORT_FASTRTPS_UNBOUNDED_TYPE;
  return ret_val;
}


static message_type_support_callbacks_t __callbacks_FlangeSerialOpen_Request = {
  "dsr_msgs2::srv",
  "FlangeSerialOpen_Request",
  _FlangeSerialOpen_Request__cdr_serialize,
  _FlangeSerialOpen_Request__cdr_deserialize,
  _FlangeSerialOpen_Request__get_serialized_size,
  _FlangeSerialOpen_Request__max_serialized_size
};

static rosidl_message_type_support_t _FlangeSerialOpen_Request__type_support = {
  rosidl_typesupport_fastrtps_c__identifier,
  &__callbacks_FlangeSerialOpen_Request,
  get_message_typesupport_handle_function,
};

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, dsr_msgs2, srv, FlangeSerialOpen_Request)() {
  return &_FlangeSerialOpen_Request__type_support;
}

#if defined(__cplusplus)
}
#endif

// already included above
// #include <cassert>
// already included above
// #include <limits>
// already included above
// #include <string>
// already included above
// #include "rosidl_typesupport_fastrtps_c/identifier.h"
// already included above
// #include "rosidl_typesupport_fastrtps_c/wstring_conversion.hpp"
// already included above
// #include "rosidl_typesupport_fastrtps_cpp/message_type_support.h"
// already included above
// #include "dsr_msgs2/msg/rosidl_typesupport_fastrtps_c__visibility_control.h"
// already included above
// #include "dsr_msgs2/srv/detail/flange_serial_open__struct.h"
// already included above
// #include "dsr_msgs2/srv/detail/flange_serial_open__functions.h"
// already included above
// #include "fastcdr/Cdr.h"

#ifndef _WIN32
# pragma GCC diagnostic push
# pragma GCC diagnostic ignored "-Wunused-parameter"
# ifdef __clang__
#  pragma clang diagnostic ignored "-Wdeprecated-register"
#  pragma clang diagnostic ignored "-Wreturn-type-c-linkage"
# endif
#endif
#ifndef _WIN32
# pragma GCC diagnostic pop
#endif

// includes and forward declarations of message dependencies and their conversion functions

#if defined(__cplusplus)
extern "C"
{
#endif


// forward declare type support functions


using _FlangeSerialOpen_Response__ros_msg_type = dsr_msgs2__srv__FlangeSerialOpen_Response;

static bool _FlangeSerialOpen_Response__cdr_serialize(
  const void * untyped_ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  if (!untyped_ros_message) {
    fprintf(stderr, "ros message handle is null\n");
    return false;
  }
  const _FlangeSerialOpen_Response__ros_msg_type * ros_message = static_cast<const _FlangeSerialOpen_Response__ros_msg_type *>(untyped_ros_message);
  // Field name: success
  {
    cdr << (ros_message->success ? true : false);
  }

  return true;
}

static bool _FlangeSerialOpen_Response__cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  void * untyped_ros_message)
{
  if (!untyped_ros_message) {
    fprintf(stderr, "ros message handle is null\n");
    return false;
  }
  _FlangeSerialOpen_Response__ros_msg_type * ros_message = static_cast<_FlangeSerialOpen_Response__ros_msg_type *>(untyped_ros_message);
  // Field name: success
  {
    uint8_t tmp;
    cdr >> tmp;
    ros_message->success = tmp ? true : false;
  }

  return true;
}  // NOLINT(readability/fn_size)

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_dsr_msgs2
size_t get_serialized_size_dsr_msgs2__srv__FlangeSerialOpen_Response(
  const void * untyped_ros_message,
  size_t current_alignment)
{
  const _FlangeSerialOpen_Response__ros_msg_type * ros_message = static_cast<const _FlangeSerialOpen_Response__ros_msg_type *>(untyped_ros_message);
  (void)ros_message;
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  (void)padding;
  (void)wchar_size;

  // field.name success
  {
    size_t item_size = sizeof(ros_message->success);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  return current_alignment - initial_alignment;
}

static uint32_t _FlangeSerialOpen_Response__get_serialized_size(const void * untyped_ros_message)
{
  return static_cast<uint32_t>(
    get_serialized_size_dsr_msgs2__srv__FlangeSerialOpen_Response(
      untyped_ros_message, 0));
}

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_dsr_msgs2
size_t max_serialized_size_dsr_msgs2__srv__FlangeSerialOpen_Response(
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

  // member: success
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint8_t);
    current_alignment += array_size * sizeof(uint8_t);
  }

  size_t ret_val = current_alignment - initial_alignment;
  if (is_plain) {
    // All members are plain, and type is not empty.
    // We still need to check that the in-memory alignment
    // is the same as the CDR mandated alignment.
    using DataType = dsr_msgs2__srv__FlangeSerialOpen_Response;
    is_plain =
      (
      offsetof(DataType, success) +
      last_member_size
      ) == ret_val;
  }

  return ret_val;
}

static size_t _FlangeSerialOpen_Response__max_serialized_size(char & bounds_info)
{
  bool full_bounded;
  bool is_plain;
  size_t ret_val;

  ret_val = max_serialized_size_dsr_msgs2__srv__FlangeSerialOpen_Response(
    full_bounded, is_plain, 0);

  bounds_info =
    is_plain ? ROSIDL_TYPESUPPORT_FASTRTPS_PLAIN_TYPE :
    full_bounded ? ROSIDL_TYPESUPPORT_FASTRTPS_BOUNDED_TYPE : ROSIDL_TYPESUPPORT_FASTRTPS_UNBOUNDED_TYPE;
  return ret_val;
}


static message_type_support_callbacks_t __callbacks_FlangeSerialOpen_Response = {
  "dsr_msgs2::srv",
  "FlangeSerialOpen_Response",
  _FlangeSerialOpen_Response__cdr_serialize,
  _FlangeSerialOpen_Response__cdr_deserialize,
  _FlangeSerialOpen_Response__get_serialized_size,
  _FlangeSerialOpen_Response__max_serialized_size
};

static rosidl_message_type_support_t _FlangeSerialOpen_Response__type_support = {
  rosidl_typesupport_fastrtps_c__identifier,
  &__callbacks_FlangeSerialOpen_Response,
  get_message_typesupport_handle_function,
};

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, dsr_msgs2, srv, FlangeSerialOpen_Response)() {
  return &_FlangeSerialOpen_Response__type_support;
}

#if defined(__cplusplus)
}
#endif

#include "rosidl_typesupport_fastrtps_cpp/service_type_support.h"
#include "rosidl_typesupport_cpp/service_type_support.hpp"
// already included above
// #include "rosidl_typesupport_fastrtps_c/identifier.h"
// already included above
// #include "dsr_msgs2/msg/rosidl_typesupport_fastrtps_c__visibility_control.h"
#include "dsr_msgs2/srv/flange_serial_open.h"

#if defined(__cplusplus)
extern "C"
{
#endif

static service_type_support_callbacks_t FlangeSerialOpen__callbacks = {
  "dsr_msgs2::srv",
  "FlangeSerialOpen",
  ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, dsr_msgs2, srv, FlangeSerialOpen_Request)(),
  ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, dsr_msgs2, srv, FlangeSerialOpen_Response)(),
};

static rosidl_service_type_support_t FlangeSerialOpen__handle = {
  rosidl_typesupport_fastrtps_c__identifier,
  &FlangeSerialOpen__callbacks,
  get_service_typesupport_handle_function,
};

const rosidl_service_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, dsr_msgs2, srv, FlangeSerialOpen)() {
  return &FlangeSerialOpen__handle;
}

#if defined(__cplusplus)
}
#endif
