// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from dsr_msgs2:srv/GetOutputRegisterInt.idl
// generated code does not contain a copyright notice

#ifndef DSR_MSGS2__SRV__DETAIL__GET_OUTPUT_REGISTER_INT__STRUCT_H_
#define DSR_MSGS2__SRV__DETAIL__GET_OUTPUT_REGISTER_INT__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

/// Struct defined in srv/GetOutputRegisterInt in the package dsr_msgs2.
typedef struct dsr_msgs2__srv__GetOutputRegisterInt_Request
{
  uint16_t address;
  uint32_t timeout_ms;
} dsr_msgs2__srv__GetOutputRegisterInt_Request;

// Struct for a sequence of dsr_msgs2__srv__GetOutputRegisterInt_Request.
typedef struct dsr_msgs2__srv__GetOutputRegisterInt_Request__Sequence
{
  dsr_msgs2__srv__GetOutputRegisterInt_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} dsr_msgs2__srv__GetOutputRegisterInt_Request__Sequence;


// Constants defined in the message

/// Struct defined in srv/GetOutputRegisterInt in the package dsr_msgs2.
typedef struct dsr_msgs2__srv__GetOutputRegisterInt_Response
{
  bool success;
  int32_t value;
} dsr_msgs2__srv__GetOutputRegisterInt_Response;

// Struct for a sequence of dsr_msgs2__srv__GetOutputRegisterInt_Response.
typedef struct dsr_msgs2__srv__GetOutputRegisterInt_Response__Sequence
{
  dsr_msgs2__srv__GetOutputRegisterInt_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} dsr_msgs2__srv__GetOutputRegisterInt_Response__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // DSR_MSGS2__SRV__DETAIL__GET_OUTPUT_REGISTER_INT__STRUCT_H_
