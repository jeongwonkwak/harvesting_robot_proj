// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from dsr_msgs2:srv/GetRobotLinkInfo.idl
// generated code does not contain a copyright notice

#ifndef DSR_MSGS2__SRV__DETAIL__GET_ROBOT_LINK_INFO__STRUCT_H_
#define DSR_MSGS2__SRV__DETAIL__GET_ROBOT_LINK_INFO__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

/// Struct defined in srv/GetRobotLinkInfo in the package dsr_msgs2.
typedef struct dsr_msgs2__srv__GetRobotLinkInfo_Request
{
  uint8_t structure_needs_at_least_one_member;
} dsr_msgs2__srv__GetRobotLinkInfo_Request;

// Struct for a sequence of dsr_msgs2__srv__GetRobotLinkInfo_Request.
typedef struct dsr_msgs2__srv__GetRobotLinkInfo_Request__Sequence
{
  dsr_msgs2__srv__GetRobotLinkInfo_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} dsr_msgs2__srv__GetRobotLinkInfo_Request__Sequence;


// Constants defined in the message

/// Struct defined in srv/GetRobotLinkInfo in the package dsr_msgs2.
typedef struct dsr_msgs2__srv__GetRobotLinkInfo_Response
{
  float d[6];
  float a[6];
  float alpha[6];
  float theta[6];
  float offset[6];
  float gradient;
  float rotation;
  bool success;
} dsr_msgs2__srv__GetRobotLinkInfo_Response;

// Struct for a sequence of dsr_msgs2__srv__GetRobotLinkInfo_Response.
typedef struct dsr_msgs2__srv__GetRobotLinkInfo_Response__Sequence
{
  dsr_msgs2__srv__GetRobotLinkInfo_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} dsr_msgs2__srv__GetRobotLinkInfo_Response__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // DSR_MSGS2__SRV__DETAIL__GET_ROBOT_LINK_INFO__STRUCT_H_
