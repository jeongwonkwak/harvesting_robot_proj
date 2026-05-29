// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from dsr_msgs2:srv/FlangeSerialWrite.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "dsr_msgs2/srv/detail/flange_serial_write__rosidl_typesupport_introspection_c.h"
#include "dsr_msgs2/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "dsr_msgs2/srv/detail/flange_serial_write__functions.h"
#include "dsr_msgs2/srv/detail/flange_serial_write__struct.h"


// Include directives for member types
// Member `data`
#include "rosidl_runtime_c/primitives_sequence_functions.h"

#ifdef __cplusplus
extern "C"
{
#endif

void dsr_msgs2__srv__FlangeSerialWrite_Request__rosidl_typesupport_introspection_c__FlangeSerialWrite_Request_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  dsr_msgs2__srv__FlangeSerialWrite_Request__init(message_memory);
}

void dsr_msgs2__srv__FlangeSerialWrite_Request__rosidl_typesupport_introspection_c__FlangeSerialWrite_Request_fini_function(void * message_memory)
{
  dsr_msgs2__srv__FlangeSerialWrite_Request__fini(message_memory);
}

size_t dsr_msgs2__srv__FlangeSerialWrite_Request__rosidl_typesupport_introspection_c__size_function__FlangeSerialWrite_Request__data(
  const void * untyped_member)
{
  const rosidl_runtime_c__uint8__Sequence * member =
    (const rosidl_runtime_c__uint8__Sequence *)(untyped_member);
  return member->size;
}

const void * dsr_msgs2__srv__FlangeSerialWrite_Request__rosidl_typesupport_introspection_c__get_const_function__FlangeSerialWrite_Request__data(
  const void * untyped_member, size_t index)
{
  const rosidl_runtime_c__uint8__Sequence * member =
    (const rosidl_runtime_c__uint8__Sequence *)(untyped_member);
  return &member->data[index];
}

void * dsr_msgs2__srv__FlangeSerialWrite_Request__rosidl_typesupport_introspection_c__get_function__FlangeSerialWrite_Request__data(
  void * untyped_member, size_t index)
{
  rosidl_runtime_c__uint8__Sequence * member =
    (rosidl_runtime_c__uint8__Sequence *)(untyped_member);
  return &member->data[index];
}

void dsr_msgs2__srv__FlangeSerialWrite_Request__rosidl_typesupport_introspection_c__fetch_function__FlangeSerialWrite_Request__data(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const uint8_t * item =
    ((const uint8_t *)
    dsr_msgs2__srv__FlangeSerialWrite_Request__rosidl_typesupport_introspection_c__get_const_function__FlangeSerialWrite_Request__data(untyped_member, index));
  uint8_t * value =
    (uint8_t *)(untyped_value);
  *value = *item;
}

void dsr_msgs2__srv__FlangeSerialWrite_Request__rosidl_typesupport_introspection_c__assign_function__FlangeSerialWrite_Request__data(
  void * untyped_member, size_t index, const void * untyped_value)
{
  uint8_t * item =
    ((uint8_t *)
    dsr_msgs2__srv__FlangeSerialWrite_Request__rosidl_typesupport_introspection_c__get_function__FlangeSerialWrite_Request__data(untyped_member, index));
  const uint8_t * value =
    (const uint8_t *)(untyped_value);
  *item = *value;
}

bool dsr_msgs2__srv__FlangeSerialWrite_Request__rosidl_typesupport_introspection_c__resize_function__FlangeSerialWrite_Request__data(
  void * untyped_member, size_t size)
{
  rosidl_runtime_c__uint8__Sequence * member =
    (rosidl_runtime_c__uint8__Sequence *)(untyped_member);
  rosidl_runtime_c__uint8__Sequence__fini(member);
  return rosidl_runtime_c__uint8__Sequence__init(member, size);
}

static rosidl_typesupport_introspection_c__MessageMember dsr_msgs2__srv__FlangeSerialWrite_Request__rosidl_typesupport_introspection_c__FlangeSerialWrite_Request_message_member_array[2] = {
  {
    "port",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_INT32,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(dsr_msgs2__srv__FlangeSerialWrite_Request, port),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "data",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_UINT8,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(dsr_msgs2__srv__FlangeSerialWrite_Request, data),  // bytes offset in struct
    NULL,  // default value
    dsr_msgs2__srv__FlangeSerialWrite_Request__rosidl_typesupport_introspection_c__size_function__FlangeSerialWrite_Request__data,  // size() function pointer
    dsr_msgs2__srv__FlangeSerialWrite_Request__rosidl_typesupport_introspection_c__get_const_function__FlangeSerialWrite_Request__data,  // get_const(index) function pointer
    dsr_msgs2__srv__FlangeSerialWrite_Request__rosidl_typesupport_introspection_c__get_function__FlangeSerialWrite_Request__data,  // get(index) function pointer
    dsr_msgs2__srv__FlangeSerialWrite_Request__rosidl_typesupport_introspection_c__fetch_function__FlangeSerialWrite_Request__data,  // fetch(index, &value) function pointer
    dsr_msgs2__srv__FlangeSerialWrite_Request__rosidl_typesupport_introspection_c__assign_function__FlangeSerialWrite_Request__data,  // assign(index, value) function pointer
    dsr_msgs2__srv__FlangeSerialWrite_Request__rosidl_typesupport_introspection_c__resize_function__FlangeSerialWrite_Request__data  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers dsr_msgs2__srv__FlangeSerialWrite_Request__rosidl_typesupport_introspection_c__FlangeSerialWrite_Request_message_members = {
  "dsr_msgs2__srv",  // message namespace
  "FlangeSerialWrite_Request",  // message name
  2,  // number of fields
  sizeof(dsr_msgs2__srv__FlangeSerialWrite_Request),
  dsr_msgs2__srv__FlangeSerialWrite_Request__rosidl_typesupport_introspection_c__FlangeSerialWrite_Request_message_member_array,  // message members
  dsr_msgs2__srv__FlangeSerialWrite_Request__rosidl_typesupport_introspection_c__FlangeSerialWrite_Request_init_function,  // function to initialize message memory (memory has to be allocated)
  dsr_msgs2__srv__FlangeSerialWrite_Request__rosidl_typesupport_introspection_c__FlangeSerialWrite_Request_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t dsr_msgs2__srv__FlangeSerialWrite_Request__rosidl_typesupport_introspection_c__FlangeSerialWrite_Request_message_type_support_handle = {
  0,
  &dsr_msgs2__srv__FlangeSerialWrite_Request__rosidl_typesupport_introspection_c__FlangeSerialWrite_Request_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_dsr_msgs2
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, dsr_msgs2, srv, FlangeSerialWrite_Request)() {
  if (!dsr_msgs2__srv__FlangeSerialWrite_Request__rosidl_typesupport_introspection_c__FlangeSerialWrite_Request_message_type_support_handle.typesupport_identifier) {
    dsr_msgs2__srv__FlangeSerialWrite_Request__rosidl_typesupport_introspection_c__FlangeSerialWrite_Request_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &dsr_msgs2__srv__FlangeSerialWrite_Request__rosidl_typesupport_introspection_c__FlangeSerialWrite_Request_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif

// already included above
// #include <stddef.h>
// already included above
// #include "dsr_msgs2/srv/detail/flange_serial_write__rosidl_typesupport_introspection_c.h"
// already included above
// #include "dsr_msgs2/msg/rosidl_typesupport_introspection_c__visibility_control.h"
// already included above
// #include "rosidl_typesupport_introspection_c/field_types.h"
// already included above
// #include "rosidl_typesupport_introspection_c/identifier.h"
// already included above
// #include "rosidl_typesupport_introspection_c/message_introspection.h"
// already included above
// #include "dsr_msgs2/srv/detail/flange_serial_write__functions.h"
// already included above
// #include "dsr_msgs2/srv/detail/flange_serial_write__struct.h"


#ifdef __cplusplus
extern "C"
{
#endif

void dsr_msgs2__srv__FlangeSerialWrite_Response__rosidl_typesupport_introspection_c__FlangeSerialWrite_Response_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  dsr_msgs2__srv__FlangeSerialWrite_Response__init(message_memory);
}

void dsr_msgs2__srv__FlangeSerialWrite_Response__rosidl_typesupport_introspection_c__FlangeSerialWrite_Response_fini_function(void * message_memory)
{
  dsr_msgs2__srv__FlangeSerialWrite_Response__fini(message_memory);
}

static rosidl_typesupport_introspection_c__MessageMember dsr_msgs2__srv__FlangeSerialWrite_Response__rosidl_typesupport_introspection_c__FlangeSerialWrite_Response_message_member_array[1] = {
  {
    "success",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_BOOLEAN,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(dsr_msgs2__srv__FlangeSerialWrite_Response, success),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers dsr_msgs2__srv__FlangeSerialWrite_Response__rosidl_typesupport_introspection_c__FlangeSerialWrite_Response_message_members = {
  "dsr_msgs2__srv",  // message namespace
  "FlangeSerialWrite_Response",  // message name
  1,  // number of fields
  sizeof(dsr_msgs2__srv__FlangeSerialWrite_Response),
  dsr_msgs2__srv__FlangeSerialWrite_Response__rosidl_typesupport_introspection_c__FlangeSerialWrite_Response_message_member_array,  // message members
  dsr_msgs2__srv__FlangeSerialWrite_Response__rosidl_typesupport_introspection_c__FlangeSerialWrite_Response_init_function,  // function to initialize message memory (memory has to be allocated)
  dsr_msgs2__srv__FlangeSerialWrite_Response__rosidl_typesupport_introspection_c__FlangeSerialWrite_Response_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t dsr_msgs2__srv__FlangeSerialWrite_Response__rosidl_typesupport_introspection_c__FlangeSerialWrite_Response_message_type_support_handle = {
  0,
  &dsr_msgs2__srv__FlangeSerialWrite_Response__rosidl_typesupport_introspection_c__FlangeSerialWrite_Response_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_dsr_msgs2
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, dsr_msgs2, srv, FlangeSerialWrite_Response)() {
  if (!dsr_msgs2__srv__FlangeSerialWrite_Response__rosidl_typesupport_introspection_c__FlangeSerialWrite_Response_message_type_support_handle.typesupport_identifier) {
    dsr_msgs2__srv__FlangeSerialWrite_Response__rosidl_typesupport_introspection_c__FlangeSerialWrite_Response_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &dsr_msgs2__srv__FlangeSerialWrite_Response__rosidl_typesupport_introspection_c__FlangeSerialWrite_Response_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif

#include "rosidl_runtime_c/service_type_support_struct.h"
// already included above
// #include "dsr_msgs2/msg/rosidl_typesupport_introspection_c__visibility_control.h"
// already included above
// #include "dsr_msgs2/srv/detail/flange_serial_write__rosidl_typesupport_introspection_c.h"
// already included above
// #include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/service_introspection.h"

// this is intentionally not const to allow initialization later to prevent an initialization race
static rosidl_typesupport_introspection_c__ServiceMembers dsr_msgs2__srv__detail__flange_serial_write__rosidl_typesupport_introspection_c__FlangeSerialWrite_service_members = {
  "dsr_msgs2__srv",  // service namespace
  "FlangeSerialWrite",  // service name
  // these two fields are initialized below on the first access
  NULL,  // request message
  // dsr_msgs2__srv__detail__flange_serial_write__rosidl_typesupport_introspection_c__FlangeSerialWrite_Request_message_type_support_handle,
  NULL  // response message
  // dsr_msgs2__srv__detail__flange_serial_write__rosidl_typesupport_introspection_c__FlangeSerialWrite_Response_message_type_support_handle
};

static rosidl_service_type_support_t dsr_msgs2__srv__detail__flange_serial_write__rosidl_typesupport_introspection_c__FlangeSerialWrite_service_type_support_handle = {
  0,
  &dsr_msgs2__srv__detail__flange_serial_write__rosidl_typesupport_introspection_c__FlangeSerialWrite_service_members,
  get_service_typesupport_handle_function,
};

// Forward declaration of request/response type support functions
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, dsr_msgs2, srv, FlangeSerialWrite_Request)();

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, dsr_msgs2, srv, FlangeSerialWrite_Response)();

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_dsr_msgs2
const rosidl_service_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_introspection_c, dsr_msgs2, srv, FlangeSerialWrite)() {
  if (!dsr_msgs2__srv__detail__flange_serial_write__rosidl_typesupport_introspection_c__FlangeSerialWrite_service_type_support_handle.typesupport_identifier) {
    dsr_msgs2__srv__detail__flange_serial_write__rosidl_typesupport_introspection_c__FlangeSerialWrite_service_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  rosidl_typesupport_introspection_c__ServiceMembers * service_members =
    (rosidl_typesupport_introspection_c__ServiceMembers *)dsr_msgs2__srv__detail__flange_serial_write__rosidl_typesupport_introspection_c__FlangeSerialWrite_service_type_support_handle.data;

  if (!service_members->request_members_) {
    service_members->request_members_ =
      (const rosidl_typesupport_introspection_c__MessageMembers *)
      ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, dsr_msgs2, srv, FlangeSerialWrite_Request)()->data;
  }
  if (!service_members->response_members_) {
    service_members->response_members_ =
      (const rosidl_typesupport_introspection_c__MessageMembers *)
      ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, dsr_msgs2, srv, FlangeSerialWrite_Response)()->data;
  }

  return &dsr_msgs2__srv__detail__flange_serial_write__rosidl_typesupport_introspection_c__FlangeSerialWrite_service_type_support_handle;
}
