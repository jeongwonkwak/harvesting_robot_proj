// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from dsr_msgs2:action/JogH2r.idl
// generated code does not contain a copyright notice

#ifndef DSR_MSGS2__ACTION__DETAIL__JOG_H2R__STRUCT_H_
#define DSR_MSGS2__ACTION__DETAIL__JOG_H2R__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

/// Struct defined in action/JogH2r in the package dsr_msgs2.
typedef struct dsr_msgs2__action__JogH2r_Goal
{
  int8_t jog_axis;
  int8_t move_reference;
  double velocity;
} dsr_msgs2__action__JogH2r_Goal;

// Struct for a sequence of dsr_msgs2__action__JogH2r_Goal.
typedef struct dsr_msgs2__action__JogH2r_Goal__Sequence
{
  dsr_msgs2__action__JogH2r_Goal * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} dsr_msgs2__action__JogH2r_Goal__Sequence;


// Constants defined in the message

/// Struct defined in action/JogH2r in the package dsr_msgs2.
typedef struct dsr_msgs2__action__JogH2r_Result
{
  bool success;
} dsr_msgs2__action__JogH2r_Result;

// Struct for a sequence of dsr_msgs2__action__JogH2r_Result.
typedef struct dsr_msgs2__action__JogH2r_Result__Sequence
{
  dsr_msgs2__action__JogH2r_Result * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} dsr_msgs2__action__JogH2r_Result__Sequence;


// Constants defined in the message

/// Struct defined in action/JogH2r in the package dsr_msgs2.
typedef struct dsr_msgs2__action__JogH2r_Feedback
{
  double pos[6];
} dsr_msgs2__action__JogH2r_Feedback;

// Struct for a sequence of dsr_msgs2__action__JogH2r_Feedback.
typedef struct dsr_msgs2__action__JogH2r_Feedback__Sequence
{
  dsr_msgs2__action__JogH2r_Feedback * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} dsr_msgs2__action__JogH2r_Feedback__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'goal_id'
#include "unique_identifier_msgs/msg/detail/uuid__struct.h"
// Member 'goal'
#include "dsr_msgs2/action/detail/jog_h2r__struct.h"

/// Struct defined in action/JogH2r in the package dsr_msgs2.
typedef struct dsr_msgs2__action__JogH2r_SendGoal_Request
{
  unique_identifier_msgs__msg__UUID goal_id;
  dsr_msgs2__action__JogH2r_Goal goal;
} dsr_msgs2__action__JogH2r_SendGoal_Request;

// Struct for a sequence of dsr_msgs2__action__JogH2r_SendGoal_Request.
typedef struct dsr_msgs2__action__JogH2r_SendGoal_Request__Sequence
{
  dsr_msgs2__action__JogH2r_SendGoal_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} dsr_msgs2__action__JogH2r_SendGoal_Request__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'stamp'
#include "builtin_interfaces/msg/detail/time__struct.h"

/// Struct defined in action/JogH2r in the package dsr_msgs2.
typedef struct dsr_msgs2__action__JogH2r_SendGoal_Response
{
  bool accepted;
  builtin_interfaces__msg__Time stamp;
} dsr_msgs2__action__JogH2r_SendGoal_Response;

// Struct for a sequence of dsr_msgs2__action__JogH2r_SendGoal_Response.
typedef struct dsr_msgs2__action__JogH2r_SendGoal_Response__Sequence
{
  dsr_msgs2__action__JogH2r_SendGoal_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} dsr_msgs2__action__JogH2r_SendGoal_Response__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'goal_id'
// already included above
// #include "unique_identifier_msgs/msg/detail/uuid__struct.h"

/// Struct defined in action/JogH2r in the package dsr_msgs2.
typedef struct dsr_msgs2__action__JogH2r_GetResult_Request
{
  unique_identifier_msgs__msg__UUID goal_id;
} dsr_msgs2__action__JogH2r_GetResult_Request;

// Struct for a sequence of dsr_msgs2__action__JogH2r_GetResult_Request.
typedef struct dsr_msgs2__action__JogH2r_GetResult_Request__Sequence
{
  dsr_msgs2__action__JogH2r_GetResult_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} dsr_msgs2__action__JogH2r_GetResult_Request__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'result'
// already included above
// #include "dsr_msgs2/action/detail/jog_h2r__struct.h"

/// Struct defined in action/JogH2r in the package dsr_msgs2.
typedef struct dsr_msgs2__action__JogH2r_GetResult_Response
{
  int8_t status;
  dsr_msgs2__action__JogH2r_Result result;
} dsr_msgs2__action__JogH2r_GetResult_Response;

// Struct for a sequence of dsr_msgs2__action__JogH2r_GetResult_Response.
typedef struct dsr_msgs2__action__JogH2r_GetResult_Response__Sequence
{
  dsr_msgs2__action__JogH2r_GetResult_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} dsr_msgs2__action__JogH2r_GetResult_Response__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'goal_id'
// already included above
// #include "unique_identifier_msgs/msg/detail/uuid__struct.h"
// Member 'feedback'
// already included above
// #include "dsr_msgs2/action/detail/jog_h2r__struct.h"

/// Struct defined in action/JogH2r in the package dsr_msgs2.
typedef struct dsr_msgs2__action__JogH2r_FeedbackMessage
{
  unique_identifier_msgs__msg__UUID goal_id;
  dsr_msgs2__action__JogH2r_Feedback feedback;
} dsr_msgs2__action__JogH2r_FeedbackMessage;

// Struct for a sequence of dsr_msgs2__action__JogH2r_FeedbackMessage.
typedef struct dsr_msgs2__action__JogH2r_FeedbackMessage__Sequence
{
  dsr_msgs2__action__JogH2r_FeedbackMessage * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} dsr_msgs2__action__JogH2r_FeedbackMessage__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // DSR_MSGS2__ACTION__DETAIL__JOG_H2R__STRUCT_H_
