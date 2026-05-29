// NOLINT: This file starts with a BOM since it contain non-ASCII characters
// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from my_robot_interfaces:msg/TurtleStatus.idl
// generated code does not contain a copyright notice

#ifndef MY_ROBOT_INTERFACES__MSG__DETAIL__TURTLE_STATUS__STRUCT_H_
#define MY_ROBOT_INTERFACES__MSG__DETAIL__TURTLE_STATUS__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'current_state'
#include "rosidl_runtime_c/string.h"

/// Struct defined in msg/TurtleStatus in the package my_robot_interfaces.
typedef struct my_robot_interfaces__msg__TurtleStatus
{
  /// 벽까지의 남은 거리
  double distance_to_wall;
  /// 로봇의 상태 (예: NORMAL, WARN, STOP)
  rosidl_runtime_c__String current_state;
  /// 이동 중 여부
  bool is_moving;
} my_robot_interfaces__msg__TurtleStatus;

// Struct for a sequence of my_robot_interfaces__msg__TurtleStatus.
typedef struct my_robot_interfaces__msg__TurtleStatus__Sequence
{
  my_robot_interfaces__msg__TurtleStatus * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} my_robot_interfaces__msg__TurtleStatus__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // MY_ROBOT_INTERFACES__MSG__DETAIL__TURTLE_STATUS__STRUCT_H_
