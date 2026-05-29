// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from dsr_msgs2:srv/GetRobotLinkInfo.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "dsr_msgs2/srv/detail/get_robot_link_info__rosidl_typesupport_introspection_c.h"
#include "dsr_msgs2/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "dsr_msgs2/srv/detail/get_robot_link_info__functions.h"
#include "dsr_msgs2/srv/detail/get_robot_link_info__struct.h"


#ifdef __cplusplus
extern "C"
{
#endif

void dsr_msgs2__srv__GetRobotLinkInfo_Request__rosidl_typesupport_introspection_c__GetRobotLinkInfo_Request_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  dsr_msgs2__srv__GetRobotLinkInfo_Request__init(message_memory);
}

void dsr_msgs2__srv__GetRobotLinkInfo_Request__rosidl_typesupport_introspection_c__GetRobotLinkInfo_Request_fini_function(void * message_memory)
{
  dsr_msgs2__srv__GetRobotLinkInfo_Request__fini(message_memory);
}

static rosidl_typesupport_introspection_c__MessageMember dsr_msgs2__srv__GetRobotLinkInfo_Request__rosidl_typesupport_introspection_c__GetRobotLinkInfo_Request_message_member_array[1] = {
  {
    "structure_needs_at_least_one_member",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_UINT8,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(dsr_msgs2__srv__GetRobotLinkInfo_Request, structure_needs_at_least_one_member),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers dsr_msgs2__srv__GetRobotLinkInfo_Request__rosidl_typesupport_introspection_c__GetRobotLinkInfo_Request_message_members = {
  "dsr_msgs2__srv",  // message namespace
  "GetRobotLinkInfo_Request",  // message name
  1,  // number of fields
  sizeof(dsr_msgs2__srv__GetRobotLinkInfo_Request),
  dsr_msgs2__srv__GetRobotLinkInfo_Request__rosidl_typesupport_introspection_c__GetRobotLinkInfo_Request_message_member_array,  // message members
  dsr_msgs2__srv__GetRobotLinkInfo_Request__rosidl_typesupport_introspection_c__GetRobotLinkInfo_Request_init_function,  // function to initialize message memory (memory has to be allocated)
  dsr_msgs2__srv__GetRobotLinkInfo_Request__rosidl_typesupport_introspection_c__GetRobotLinkInfo_Request_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t dsr_msgs2__srv__GetRobotLinkInfo_Request__rosidl_typesupport_introspection_c__GetRobotLinkInfo_Request_message_type_support_handle = {
  0,
  &dsr_msgs2__srv__GetRobotLinkInfo_Request__rosidl_typesupport_introspection_c__GetRobotLinkInfo_Request_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_dsr_msgs2
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, dsr_msgs2, srv, GetRobotLinkInfo_Request)() {
  if (!dsr_msgs2__srv__GetRobotLinkInfo_Request__rosidl_typesupport_introspection_c__GetRobotLinkInfo_Request_message_type_support_handle.typesupport_identifier) {
    dsr_msgs2__srv__GetRobotLinkInfo_Request__rosidl_typesupport_introspection_c__GetRobotLinkInfo_Request_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &dsr_msgs2__srv__GetRobotLinkInfo_Request__rosidl_typesupport_introspection_c__GetRobotLinkInfo_Request_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif

// already included above
// #include <stddef.h>
// already included above
// #include "dsr_msgs2/srv/detail/get_robot_link_info__rosidl_typesupport_introspection_c.h"
// already included above
// #include "dsr_msgs2/msg/rosidl_typesupport_introspection_c__visibility_control.h"
// already included above
// #include "rosidl_typesupport_introspection_c/field_types.h"
// already included above
// #include "rosidl_typesupport_introspection_c/identifier.h"
// already included above
// #include "rosidl_typesupport_introspection_c/message_introspection.h"
// already included above
// #include "dsr_msgs2/srv/detail/get_robot_link_info__functions.h"
// already included above
// #include "dsr_msgs2/srv/detail/get_robot_link_info__struct.h"


#ifdef __cplusplus
extern "C"
{
#endif

void dsr_msgs2__srv__GetRobotLinkInfo_Response__rosidl_typesupport_introspection_c__GetRobotLinkInfo_Response_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  dsr_msgs2__srv__GetRobotLinkInfo_Response__init(message_memory);
}

void dsr_msgs2__srv__GetRobotLinkInfo_Response__rosidl_typesupport_introspection_c__GetRobotLinkInfo_Response_fini_function(void * message_memory)
{
  dsr_msgs2__srv__GetRobotLinkInfo_Response__fini(message_memory);
}

size_t dsr_msgs2__srv__GetRobotLinkInfo_Response__rosidl_typesupport_introspection_c__size_function__GetRobotLinkInfo_Response__d(
  const void * untyped_member)
{
  (void)untyped_member;
  return 6;
}

const void * dsr_msgs2__srv__GetRobotLinkInfo_Response__rosidl_typesupport_introspection_c__get_const_function__GetRobotLinkInfo_Response__d(
  const void * untyped_member, size_t index)
{
  const float * member =
    (const float *)(untyped_member);
  return &member[index];
}

void * dsr_msgs2__srv__GetRobotLinkInfo_Response__rosidl_typesupport_introspection_c__get_function__GetRobotLinkInfo_Response__d(
  void * untyped_member, size_t index)
{
  float * member =
    (float *)(untyped_member);
  return &member[index];
}

void dsr_msgs2__srv__GetRobotLinkInfo_Response__rosidl_typesupport_introspection_c__fetch_function__GetRobotLinkInfo_Response__d(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const float * item =
    ((const float *)
    dsr_msgs2__srv__GetRobotLinkInfo_Response__rosidl_typesupport_introspection_c__get_const_function__GetRobotLinkInfo_Response__d(untyped_member, index));
  float * value =
    (float *)(untyped_value);
  *value = *item;
}

void dsr_msgs2__srv__GetRobotLinkInfo_Response__rosidl_typesupport_introspection_c__assign_function__GetRobotLinkInfo_Response__d(
  void * untyped_member, size_t index, const void * untyped_value)
{
  float * item =
    ((float *)
    dsr_msgs2__srv__GetRobotLinkInfo_Response__rosidl_typesupport_introspection_c__get_function__GetRobotLinkInfo_Response__d(untyped_member, index));
  const float * value =
    (const float *)(untyped_value);
  *item = *value;
}

size_t dsr_msgs2__srv__GetRobotLinkInfo_Response__rosidl_typesupport_introspection_c__size_function__GetRobotLinkInfo_Response__a(
  const void * untyped_member)
{
  (void)untyped_member;
  return 6;
}

const void * dsr_msgs2__srv__GetRobotLinkInfo_Response__rosidl_typesupport_introspection_c__get_const_function__GetRobotLinkInfo_Response__a(
  const void * untyped_member, size_t index)
{
  const float * member =
    (const float *)(untyped_member);
  return &member[index];
}

void * dsr_msgs2__srv__GetRobotLinkInfo_Response__rosidl_typesupport_introspection_c__get_function__GetRobotLinkInfo_Response__a(
  void * untyped_member, size_t index)
{
  float * member =
    (float *)(untyped_member);
  return &member[index];
}

void dsr_msgs2__srv__GetRobotLinkInfo_Response__rosidl_typesupport_introspection_c__fetch_function__GetRobotLinkInfo_Response__a(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const float * item =
    ((const float *)
    dsr_msgs2__srv__GetRobotLinkInfo_Response__rosidl_typesupport_introspection_c__get_const_function__GetRobotLinkInfo_Response__a(untyped_member, index));
  float * value =
    (float *)(untyped_value);
  *value = *item;
}

void dsr_msgs2__srv__GetRobotLinkInfo_Response__rosidl_typesupport_introspection_c__assign_function__GetRobotLinkInfo_Response__a(
  void * untyped_member, size_t index, const void * untyped_value)
{
  float * item =
    ((float *)
    dsr_msgs2__srv__GetRobotLinkInfo_Response__rosidl_typesupport_introspection_c__get_function__GetRobotLinkInfo_Response__a(untyped_member, index));
  const float * value =
    (const float *)(untyped_value);
  *item = *value;
}

size_t dsr_msgs2__srv__GetRobotLinkInfo_Response__rosidl_typesupport_introspection_c__size_function__GetRobotLinkInfo_Response__alpha(
  const void * untyped_member)
{
  (void)untyped_member;
  return 6;
}

const void * dsr_msgs2__srv__GetRobotLinkInfo_Response__rosidl_typesupport_introspection_c__get_const_function__GetRobotLinkInfo_Response__alpha(
  const void * untyped_member, size_t index)
{
  const float * member =
    (const float *)(untyped_member);
  return &member[index];
}

void * dsr_msgs2__srv__GetRobotLinkInfo_Response__rosidl_typesupport_introspection_c__get_function__GetRobotLinkInfo_Response__alpha(
  void * untyped_member, size_t index)
{
  float * member =
    (float *)(untyped_member);
  return &member[index];
}

void dsr_msgs2__srv__GetRobotLinkInfo_Response__rosidl_typesupport_introspection_c__fetch_function__GetRobotLinkInfo_Response__alpha(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const float * item =
    ((const float *)
    dsr_msgs2__srv__GetRobotLinkInfo_Response__rosidl_typesupport_introspection_c__get_const_function__GetRobotLinkInfo_Response__alpha(untyped_member, index));
  float * value =
    (float *)(untyped_value);
  *value = *item;
}

void dsr_msgs2__srv__GetRobotLinkInfo_Response__rosidl_typesupport_introspection_c__assign_function__GetRobotLinkInfo_Response__alpha(
  void * untyped_member, size_t index, const void * untyped_value)
{
  float * item =
    ((float *)
    dsr_msgs2__srv__GetRobotLinkInfo_Response__rosidl_typesupport_introspection_c__get_function__GetRobotLinkInfo_Response__alpha(untyped_member, index));
  const float * value =
    (const float *)(untyped_value);
  *item = *value;
}

size_t dsr_msgs2__srv__GetRobotLinkInfo_Response__rosidl_typesupport_introspection_c__size_function__GetRobotLinkInfo_Response__theta(
  const void * untyped_member)
{
  (void)untyped_member;
  return 6;
}

const void * dsr_msgs2__srv__GetRobotLinkInfo_Response__rosidl_typesupport_introspection_c__get_const_function__GetRobotLinkInfo_Response__theta(
  const void * untyped_member, size_t index)
{
  const float * member =
    (const float *)(untyped_member);
  return &member[index];
}

void * dsr_msgs2__srv__GetRobotLinkInfo_Response__rosidl_typesupport_introspection_c__get_function__GetRobotLinkInfo_Response__theta(
  void * untyped_member, size_t index)
{
  float * member =
    (float *)(untyped_member);
  return &member[index];
}

void dsr_msgs2__srv__GetRobotLinkInfo_Response__rosidl_typesupport_introspection_c__fetch_function__GetRobotLinkInfo_Response__theta(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const float * item =
    ((const float *)
    dsr_msgs2__srv__GetRobotLinkInfo_Response__rosidl_typesupport_introspection_c__get_const_function__GetRobotLinkInfo_Response__theta(untyped_member, index));
  float * value =
    (float *)(untyped_value);
  *value = *item;
}

void dsr_msgs2__srv__GetRobotLinkInfo_Response__rosidl_typesupport_introspection_c__assign_function__GetRobotLinkInfo_Response__theta(
  void * untyped_member, size_t index, const void * untyped_value)
{
  float * item =
    ((float *)
    dsr_msgs2__srv__GetRobotLinkInfo_Response__rosidl_typesupport_introspection_c__get_function__GetRobotLinkInfo_Response__theta(untyped_member, index));
  const float * value =
    (const float *)(untyped_value);
  *item = *value;
}

size_t dsr_msgs2__srv__GetRobotLinkInfo_Response__rosidl_typesupport_introspection_c__size_function__GetRobotLinkInfo_Response__offset(
  const void * untyped_member)
{
  (void)untyped_member;
  return 6;
}

const void * dsr_msgs2__srv__GetRobotLinkInfo_Response__rosidl_typesupport_introspection_c__get_const_function__GetRobotLinkInfo_Response__offset(
  const void * untyped_member, size_t index)
{
  const float * member =
    (const float *)(untyped_member);
  return &member[index];
}

void * dsr_msgs2__srv__GetRobotLinkInfo_Response__rosidl_typesupport_introspection_c__get_function__GetRobotLinkInfo_Response__offset(
  void * untyped_member, size_t index)
{
  float * member =
    (float *)(untyped_member);
  return &member[index];
}

void dsr_msgs2__srv__GetRobotLinkInfo_Response__rosidl_typesupport_introspection_c__fetch_function__GetRobotLinkInfo_Response__offset(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const float * item =
    ((const float *)
    dsr_msgs2__srv__GetRobotLinkInfo_Response__rosidl_typesupport_introspection_c__get_const_function__GetRobotLinkInfo_Response__offset(untyped_member, index));
  float * value =
    (float *)(untyped_value);
  *value = *item;
}

void dsr_msgs2__srv__GetRobotLinkInfo_Response__rosidl_typesupport_introspection_c__assign_function__GetRobotLinkInfo_Response__offset(
  void * untyped_member, size_t index, const void * untyped_value)
{
  float * item =
    ((float *)
    dsr_msgs2__srv__GetRobotLinkInfo_Response__rosidl_typesupport_introspection_c__get_function__GetRobotLinkInfo_Response__offset(untyped_member, index));
  const float * value =
    (const float *)(untyped_value);
  *item = *value;
}

static rosidl_typesupport_introspection_c__MessageMember dsr_msgs2__srv__GetRobotLinkInfo_Response__rosidl_typesupport_introspection_c__GetRobotLinkInfo_Response_message_member_array[8] = {
  {
    "d",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    true,  // is array
    6,  // array size
    false,  // is upper bound
    offsetof(dsr_msgs2__srv__GetRobotLinkInfo_Response, d),  // bytes offset in struct
    NULL,  // default value
    dsr_msgs2__srv__GetRobotLinkInfo_Response__rosidl_typesupport_introspection_c__size_function__GetRobotLinkInfo_Response__d,  // size() function pointer
    dsr_msgs2__srv__GetRobotLinkInfo_Response__rosidl_typesupport_introspection_c__get_const_function__GetRobotLinkInfo_Response__d,  // get_const(index) function pointer
    dsr_msgs2__srv__GetRobotLinkInfo_Response__rosidl_typesupport_introspection_c__get_function__GetRobotLinkInfo_Response__d,  // get(index) function pointer
    dsr_msgs2__srv__GetRobotLinkInfo_Response__rosidl_typesupport_introspection_c__fetch_function__GetRobotLinkInfo_Response__d,  // fetch(index, &value) function pointer
    dsr_msgs2__srv__GetRobotLinkInfo_Response__rosidl_typesupport_introspection_c__assign_function__GetRobotLinkInfo_Response__d,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "a",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    true,  // is array
    6,  // array size
    false,  // is upper bound
    offsetof(dsr_msgs2__srv__GetRobotLinkInfo_Response, a),  // bytes offset in struct
    NULL,  // default value
    dsr_msgs2__srv__GetRobotLinkInfo_Response__rosidl_typesupport_introspection_c__size_function__GetRobotLinkInfo_Response__a,  // size() function pointer
    dsr_msgs2__srv__GetRobotLinkInfo_Response__rosidl_typesupport_introspection_c__get_const_function__GetRobotLinkInfo_Response__a,  // get_const(index) function pointer
    dsr_msgs2__srv__GetRobotLinkInfo_Response__rosidl_typesupport_introspection_c__get_function__GetRobotLinkInfo_Response__a,  // get(index) function pointer
    dsr_msgs2__srv__GetRobotLinkInfo_Response__rosidl_typesupport_introspection_c__fetch_function__GetRobotLinkInfo_Response__a,  // fetch(index, &value) function pointer
    dsr_msgs2__srv__GetRobotLinkInfo_Response__rosidl_typesupport_introspection_c__assign_function__GetRobotLinkInfo_Response__a,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "alpha",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    true,  // is array
    6,  // array size
    false,  // is upper bound
    offsetof(dsr_msgs2__srv__GetRobotLinkInfo_Response, alpha),  // bytes offset in struct
    NULL,  // default value
    dsr_msgs2__srv__GetRobotLinkInfo_Response__rosidl_typesupport_introspection_c__size_function__GetRobotLinkInfo_Response__alpha,  // size() function pointer
    dsr_msgs2__srv__GetRobotLinkInfo_Response__rosidl_typesupport_introspection_c__get_const_function__GetRobotLinkInfo_Response__alpha,  // get_const(index) function pointer
    dsr_msgs2__srv__GetRobotLinkInfo_Response__rosidl_typesupport_introspection_c__get_function__GetRobotLinkInfo_Response__alpha,  // get(index) function pointer
    dsr_msgs2__srv__GetRobotLinkInfo_Response__rosidl_typesupport_introspection_c__fetch_function__GetRobotLinkInfo_Response__alpha,  // fetch(index, &value) function pointer
    dsr_msgs2__srv__GetRobotLinkInfo_Response__rosidl_typesupport_introspection_c__assign_function__GetRobotLinkInfo_Response__alpha,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "theta",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    true,  // is array
    6,  // array size
    false,  // is upper bound
    offsetof(dsr_msgs2__srv__GetRobotLinkInfo_Response, theta),  // bytes offset in struct
    NULL,  // default value
    dsr_msgs2__srv__GetRobotLinkInfo_Response__rosidl_typesupport_introspection_c__size_function__GetRobotLinkInfo_Response__theta,  // size() function pointer
    dsr_msgs2__srv__GetRobotLinkInfo_Response__rosidl_typesupport_introspection_c__get_const_function__GetRobotLinkInfo_Response__theta,  // get_const(index) function pointer
    dsr_msgs2__srv__GetRobotLinkInfo_Response__rosidl_typesupport_introspection_c__get_function__GetRobotLinkInfo_Response__theta,  // get(index) function pointer
    dsr_msgs2__srv__GetRobotLinkInfo_Response__rosidl_typesupport_introspection_c__fetch_function__GetRobotLinkInfo_Response__theta,  // fetch(index, &value) function pointer
    dsr_msgs2__srv__GetRobotLinkInfo_Response__rosidl_typesupport_introspection_c__assign_function__GetRobotLinkInfo_Response__theta,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "offset",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    true,  // is array
    6,  // array size
    false,  // is upper bound
    offsetof(dsr_msgs2__srv__GetRobotLinkInfo_Response, offset),  // bytes offset in struct
    NULL,  // default value
    dsr_msgs2__srv__GetRobotLinkInfo_Response__rosidl_typesupport_introspection_c__size_function__GetRobotLinkInfo_Response__offset,  // size() function pointer
    dsr_msgs2__srv__GetRobotLinkInfo_Response__rosidl_typesupport_introspection_c__get_const_function__GetRobotLinkInfo_Response__offset,  // get_const(index) function pointer
    dsr_msgs2__srv__GetRobotLinkInfo_Response__rosidl_typesupport_introspection_c__get_function__GetRobotLinkInfo_Response__offset,  // get(index) function pointer
    dsr_msgs2__srv__GetRobotLinkInfo_Response__rosidl_typesupport_introspection_c__fetch_function__GetRobotLinkInfo_Response__offset,  // fetch(index, &value) function pointer
    dsr_msgs2__srv__GetRobotLinkInfo_Response__rosidl_typesupport_introspection_c__assign_function__GetRobotLinkInfo_Response__offset,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "gradient",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(dsr_msgs2__srv__GetRobotLinkInfo_Response, gradient),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "rotation",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(dsr_msgs2__srv__GetRobotLinkInfo_Response, rotation),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "success",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_BOOLEAN,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(dsr_msgs2__srv__GetRobotLinkInfo_Response, success),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers dsr_msgs2__srv__GetRobotLinkInfo_Response__rosidl_typesupport_introspection_c__GetRobotLinkInfo_Response_message_members = {
  "dsr_msgs2__srv",  // message namespace
  "GetRobotLinkInfo_Response",  // message name
  8,  // number of fields
  sizeof(dsr_msgs2__srv__GetRobotLinkInfo_Response),
  dsr_msgs2__srv__GetRobotLinkInfo_Response__rosidl_typesupport_introspection_c__GetRobotLinkInfo_Response_message_member_array,  // message members
  dsr_msgs2__srv__GetRobotLinkInfo_Response__rosidl_typesupport_introspection_c__GetRobotLinkInfo_Response_init_function,  // function to initialize message memory (memory has to be allocated)
  dsr_msgs2__srv__GetRobotLinkInfo_Response__rosidl_typesupport_introspection_c__GetRobotLinkInfo_Response_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t dsr_msgs2__srv__GetRobotLinkInfo_Response__rosidl_typesupport_introspection_c__GetRobotLinkInfo_Response_message_type_support_handle = {
  0,
  &dsr_msgs2__srv__GetRobotLinkInfo_Response__rosidl_typesupport_introspection_c__GetRobotLinkInfo_Response_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_dsr_msgs2
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, dsr_msgs2, srv, GetRobotLinkInfo_Response)() {
  if (!dsr_msgs2__srv__GetRobotLinkInfo_Response__rosidl_typesupport_introspection_c__GetRobotLinkInfo_Response_message_type_support_handle.typesupport_identifier) {
    dsr_msgs2__srv__GetRobotLinkInfo_Response__rosidl_typesupport_introspection_c__GetRobotLinkInfo_Response_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &dsr_msgs2__srv__GetRobotLinkInfo_Response__rosidl_typesupport_introspection_c__GetRobotLinkInfo_Response_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif

#include "rosidl_runtime_c/service_type_support_struct.h"
// already included above
// #include "dsr_msgs2/msg/rosidl_typesupport_introspection_c__visibility_control.h"
// already included above
// #include "dsr_msgs2/srv/detail/get_robot_link_info__rosidl_typesupport_introspection_c.h"
// already included above
// #include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/service_introspection.h"

// this is intentionally not const to allow initialization later to prevent an initialization race
static rosidl_typesupport_introspection_c__ServiceMembers dsr_msgs2__srv__detail__get_robot_link_info__rosidl_typesupport_introspection_c__GetRobotLinkInfo_service_members = {
  "dsr_msgs2__srv",  // service namespace
  "GetRobotLinkInfo",  // service name
  // these two fields are initialized below on the first access
  NULL,  // request message
  // dsr_msgs2__srv__detail__get_robot_link_info__rosidl_typesupport_introspection_c__GetRobotLinkInfo_Request_message_type_support_handle,
  NULL  // response message
  // dsr_msgs2__srv__detail__get_robot_link_info__rosidl_typesupport_introspection_c__GetRobotLinkInfo_Response_message_type_support_handle
};

static rosidl_service_type_support_t dsr_msgs2__srv__detail__get_robot_link_info__rosidl_typesupport_introspection_c__GetRobotLinkInfo_service_type_support_handle = {
  0,
  &dsr_msgs2__srv__detail__get_robot_link_info__rosidl_typesupport_introspection_c__GetRobotLinkInfo_service_members,
  get_service_typesupport_handle_function,
};

// Forward declaration of request/response type support functions
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, dsr_msgs2, srv, GetRobotLinkInfo_Request)();

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, dsr_msgs2, srv, GetRobotLinkInfo_Response)();

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_dsr_msgs2
const rosidl_service_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_introspection_c, dsr_msgs2, srv, GetRobotLinkInfo)() {
  if (!dsr_msgs2__srv__detail__get_robot_link_info__rosidl_typesupport_introspection_c__GetRobotLinkInfo_service_type_support_handle.typesupport_identifier) {
    dsr_msgs2__srv__detail__get_robot_link_info__rosidl_typesupport_introspection_c__GetRobotLinkInfo_service_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  rosidl_typesupport_introspection_c__ServiceMembers * service_members =
    (rosidl_typesupport_introspection_c__ServiceMembers *)dsr_msgs2__srv__detail__get_robot_link_info__rosidl_typesupport_introspection_c__GetRobotLinkInfo_service_type_support_handle.data;

  if (!service_members->request_members_) {
    service_members->request_members_ =
      (const rosidl_typesupport_introspection_c__MessageMembers *)
      ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, dsr_msgs2, srv, GetRobotLinkInfo_Request)()->data;
  }
  if (!service_members->response_members_) {
    service_members->response_members_ =
      (const rosidl_typesupport_introspection_c__MessageMembers *)
      ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, dsr_msgs2, srv, GetRobotLinkInfo_Response)()->data;
  }

  return &dsr_msgs2__srv__detail__get_robot_link_info__rosidl_typesupport_introspection_c__GetRobotLinkInfo_service_type_support_handle;
}
