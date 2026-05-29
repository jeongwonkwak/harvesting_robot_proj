// generated from rosidl_generator_c/resource/idl__functions.h.em
// with input from dsr_msgs2:action/MovelH2r.idl
// generated code does not contain a copyright notice

#ifndef DSR_MSGS2__ACTION__DETAIL__MOVEL_H2R__FUNCTIONS_H_
#define DSR_MSGS2__ACTION__DETAIL__MOVEL_H2R__FUNCTIONS_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stdlib.h>

#include "rosidl_runtime_c/visibility_control.h"
#include "dsr_msgs2/msg/rosidl_generator_c__visibility_control.h"

#include "dsr_msgs2/action/detail/movel_h2r__struct.h"

/// Initialize action/MovelH2r message.
/**
 * If the init function is called twice for the same message without
 * calling fini inbetween previously allocated memory will be leaked.
 * \param[in,out] msg The previously allocated message pointer.
 * Fields without a default value will not be initialized by this function.
 * You might want to call memset(msg, 0, sizeof(
 * dsr_msgs2__action__MovelH2r_Goal
 * )) before or use
 * dsr_msgs2__action__MovelH2r_Goal__create()
 * to allocate and initialize the message.
 * \return true if initialization was successful, otherwise false
 */
ROSIDL_GENERATOR_C_PUBLIC_dsr_msgs2
bool
dsr_msgs2__action__MovelH2r_Goal__init(dsr_msgs2__action__MovelH2r_Goal * msg);

/// Finalize action/MovelH2r message.
/**
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_dsr_msgs2
void
dsr_msgs2__action__MovelH2r_Goal__fini(dsr_msgs2__action__MovelH2r_Goal * msg);

/// Create action/MovelH2r message.
/**
 * It allocates the memory for the message, sets the memory to zero, and
 * calls
 * dsr_msgs2__action__MovelH2r_Goal__init().
 * \return The pointer to the initialized message if successful,
 * otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_dsr_msgs2
dsr_msgs2__action__MovelH2r_Goal *
dsr_msgs2__action__MovelH2r_Goal__create();

/// Destroy action/MovelH2r message.
/**
 * It calls
 * dsr_msgs2__action__MovelH2r_Goal__fini()
 * and frees the memory of the message.
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_dsr_msgs2
void
dsr_msgs2__action__MovelH2r_Goal__destroy(dsr_msgs2__action__MovelH2r_Goal * msg);

/// Check for action/MovelH2r message equality.
/**
 * \param[in] lhs The message on the left hand size of the equality operator.
 * \param[in] rhs The message on the right hand size of the equality operator.
 * \return true if messages are equal, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_dsr_msgs2
bool
dsr_msgs2__action__MovelH2r_Goal__are_equal(const dsr_msgs2__action__MovelH2r_Goal * lhs, const dsr_msgs2__action__MovelH2r_Goal * rhs);

/// Copy a action/MovelH2r message.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source message pointer.
 * \param[out] output The target message pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer is null
 *   or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_dsr_msgs2
bool
dsr_msgs2__action__MovelH2r_Goal__copy(
  const dsr_msgs2__action__MovelH2r_Goal * input,
  dsr_msgs2__action__MovelH2r_Goal * output);

/// Initialize array of action/MovelH2r messages.
/**
 * It allocates the memory for the number of elements and calls
 * dsr_msgs2__action__MovelH2r_Goal__init()
 * for each element of the array.
 * \param[in,out] array The allocated array pointer.
 * \param[in] size The size / capacity of the array.
 * \return true if initialization was successful, otherwise false
 * If the array pointer is valid and the size is zero it is guaranteed
 # to return true.
 */
ROSIDL_GENERATOR_C_PUBLIC_dsr_msgs2
bool
dsr_msgs2__action__MovelH2r_Goal__Sequence__init(dsr_msgs2__action__MovelH2r_Goal__Sequence * array, size_t size);

/// Finalize array of action/MovelH2r messages.
/**
 * It calls
 * dsr_msgs2__action__MovelH2r_Goal__fini()
 * for each element of the array and frees the memory for the number of
 * elements.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_dsr_msgs2
void
dsr_msgs2__action__MovelH2r_Goal__Sequence__fini(dsr_msgs2__action__MovelH2r_Goal__Sequence * array);

/// Create array of action/MovelH2r messages.
/**
 * It allocates the memory for the array and calls
 * dsr_msgs2__action__MovelH2r_Goal__Sequence__init().
 * \param[in] size The size / capacity of the array.
 * \return The pointer to the initialized array if successful, otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_dsr_msgs2
dsr_msgs2__action__MovelH2r_Goal__Sequence *
dsr_msgs2__action__MovelH2r_Goal__Sequence__create(size_t size);

/// Destroy array of action/MovelH2r messages.
/**
 * It calls
 * dsr_msgs2__action__MovelH2r_Goal__Sequence__fini()
 * on the array,
 * and frees the memory of the array.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_dsr_msgs2
void
dsr_msgs2__action__MovelH2r_Goal__Sequence__destroy(dsr_msgs2__action__MovelH2r_Goal__Sequence * array);

/// Check for action/MovelH2r message array equality.
/**
 * \param[in] lhs The message array on the left hand size of the equality operator.
 * \param[in] rhs The message array on the right hand size of the equality operator.
 * \return true if message arrays are equal in size and content, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_dsr_msgs2
bool
dsr_msgs2__action__MovelH2r_Goal__Sequence__are_equal(const dsr_msgs2__action__MovelH2r_Goal__Sequence * lhs, const dsr_msgs2__action__MovelH2r_Goal__Sequence * rhs);

/// Copy an array of action/MovelH2r messages.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source array pointer.
 * \param[out] output The target array pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer
 *   is null or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_dsr_msgs2
bool
dsr_msgs2__action__MovelH2r_Goal__Sequence__copy(
  const dsr_msgs2__action__MovelH2r_Goal__Sequence * input,
  dsr_msgs2__action__MovelH2r_Goal__Sequence * output);

/// Initialize action/MovelH2r message.
/**
 * If the init function is called twice for the same message without
 * calling fini inbetween previously allocated memory will be leaked.
 * \param[in,out] msg The previously allocated message pointer.
 * Fields without a default value will not be initialized by this function.
 * You might want to call memset(msg, 0, sizeof(
 * dsr_msgs2__action__MovelH2r_Result
 * )) before or use
 * dsr_msgs2__action__MovelH2r_Result__create()
 * to allocate and initialize the message.
 * \return true if initialization was successful, otherwise false
 */
ROSIDL_GENERATOR_C_PUBLIC_dsr_msgs2
bool
dsr_msgs2__action__MovelH2r_Result__init(dsr_msgs2__action__MovelH2r_Result * msg);

/// Finalize action/MovelH2r message.
/**
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_dsr_msgs2
void
dsr_msgs2__action__MovelH2r_Result__fini(dsr_msgs2__action__MovelH2r_Result * msg);

/// Create action/MovelH2r message.
/**
 * It allocates the memory for the message, sets the memory to zero, and
 * calls
 * dsr_msgs2__action__MovelH2r_Result__init().
 * \return The pointer to the initialized message if successful,
 * otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_dsr_msgs2
dsr_msgs2__action__MovelH2r_Result *
dsr_msgs2__action__MovelH2r_Result__create();

/// Destroy action/MovelH2r message.
/**
 * It calls
 * dsr_msgs2__action__MovelH2r_Result__fini()
 * and frees the memory of the message.
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_dsr_msgs2
void
dsr_msgs2__action__MovelH2r_Result__destroy(dsr_msgs2__action__MovelH2r_Result * msg);

/// Check for action/MovelH2r message equality.
/**
 * \param[in] lhs The message on the left hand size of the equality operator.
 * \param[in] rhs The message on the right hand size of the equality operator.
 * \return true if messages are equal, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_dsr_msgs2
bool
dsr_msgs2__action__MovelH2r_Result__are_equal(const dsr_msgs2__action__MovelH2r_Result * lhs, const dsr_msgs2__action__MovelH2r_Result * rhs);

/// Copy a action/MovelH2r message.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source message pointer.
 * \param[out] output The target message pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer is null
 *   or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_dsr_msgs2
bool
dsr_msgs2__action__MovelH2r_Result__copy(
  const dsr_msgs2__action__MovelH2r_Result * input,
  dsr_msgs2__action__MovelH2r_Result * output);

/// Initialize array of action/MovelH2r messages.
/**
 * It allocates the memory for the number of elements and calls
 * dsr_msgs2__action__MovelH2r_Result__init()
 * for each element of the array.
 * \param[in,out] array The allocated array pointer.
 * \param[in] size The size / capacity of the array.
 * \return true if initialization was successful, otherwise false
 * If the array pointer is valid and the size is zero it is guaranteed
 # to return true.
 */
ROSIDL_GENERATOR_C_PUBLIC_dsr_msgs2
bool
dsr_msgs2__action__MovelH2r_Result__Sequence__init(dsr_msgs2__action__MovelH2r_Result__Sequence * array, size_t size);

/// Finalize array of action/MovelH2r messages.
/**
 * It calls
 * dsr_msgs2__action__MovelH2r_Result__fini()
 * for each element of the array and frees the memory for the number of
 * elements.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_dsr_msgs2
void
dsr_msgs2__action__MovelH2r_Result__Sequence__fini(dsr_msgs2__action__MovelH2r_Result__Sequence * array);

/// Create array of action/MovelH2r messages.
/**
 * It allocates the memory for the array and calls
 * dsr_msgs2__action__MovelH2r_Result__Sequence__init().
 * \param[in] size The size / capacity of the array.
 * \return The pointer to the initialized array if successful, otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_dsr_msgs2
dsr_msgs2__action__MovelH2r_Result__Sequence *
dsr_msgs2__action__MovelH2r_Result__Sequence__create(size_t size);

/// Destroy array of action/MovelH2r messages.
/**
 * It calls
 * dsr_msgs2__action__MovelH2r_Result__Sequence__fini()
 * on the array,
 * and frees the memory of the array.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_dsr_msgs2
void
dsr_msgs2__action__MovelH2r_Result__Sequence__destroy(dsr_msgs2__action__MovelH2r_Result__Sequence * array);

/// Check for action/MovelH2r message array equality.
/**
 * \param[in] lhs The message array on the left hand size of the equality operator.
 * \param[in] rhs The message array on the right hand size of the equality operator.
 * \return true if message arrays are equal in size and content, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_dsr_msgs2
bool
dsr_msgs2__action__MovelH2r_Result__Sequence__are_equal(const dsr_msgs2__action__MovelH2r_Result__Sequence * lhs, const dsr_msgs2__action__MovelH2r_Result__Sequence * rhs);

/// Copy an array of action/MovelH2r messages.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source array pointer.
 * \param[out] output The target array pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer
 *   is null or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_dsr_msgs2
bool
dsr_msgs2__action__MovelH2r_Result__Sequence__copy(
  const dsr_msgs2__action__MovelH2r_Result__Sequence * input,
  dsr_msgs2__action__MovelH2r_Result__Sequence * output);

/// Initialize action/MovelH2r message.
/**
 * If the init function is called twice for the same message without
 * calling fini inbetween previously allocated memory will be leaked.
 * \param[in,out] msg The previously allocated message pointer.
 * Fields without a default value will not be initialized by this function.
 * You might want to call memset(msg, 0, sizeof(
 * dsr_msgs2__action__MovelH2r_Feedback
 * )) before or use
 * dsr_msgs2__action__MovelH2r_Feedback__create()
 * to allocate and initialize the message.
 * \return true if initialization was successful, otherwise false
 */
ROSIDL_GENERATOR_C_PUBLIC_dsr_msgs2
bool
dsr_msgs2__action__MovelH2r_Feedback__init(dsr_msgs2__action__MovelH2r_Feedback * msg);

/// Finalize action/MovelH2r message.
/**
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_dsr_msgs2
void
dsr_msgs2__action__MovelH2r_Feedback__fini(dsr_msgs2__action__MovelH2r_Feedback * msg);

/// Create action/MovelH2r message.
/**
 * It allocates the memory for the message, sets the memory to zero, and
 * calls
 * dsr_msgs2__action__MovelH2r_Feedback__init().
 * \return The pointer to the initialized message if successful,
 * otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_dsr_msgs2
dsr_msgs2__action__MovelH2r_Feedback *
dsr_msgs2__action__MovelH2r_Feedback__create();

/// Destroy action/MovelH2r message.
/**
 * It calls
 * dsr_msgs2__action__MovelH2r_Feedback__fini()
 * and frees the memory of the message.
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_dsr_msgs2
void
dsr_msgs2__action__MovelH2r_Feedback__destroy(dsr_msgs2__action__MovelH2r_Feedback * msg);

/// Check for action/MovelH2r message equality.
/**
 * \param[in] lhs The message on the left hand size of the equality operator.
 * \param[in] rhs The message on the right hand size of the equality operator.
 * \return true if messages are equal, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_dsr_msgs2
bool
dsr_msgs2__action__MovelH2r_Feedback__are_equal(const dsr_msgs2__action__MovelH2r_Feedback * lhs, const dsr_msgs2__action__MovelH2r_Feedback * rhs);

/// Copy a action/MovelH2r message.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source message pointer.
 * \param[out] output The target message pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer is null
 *   or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_dsr_msgs2
bool
dsr_msgs2__action__MovelH2r_Feedback__copy(
  const dsr_msgs2__action__MovelH2r_Feedback * input,
  dsr_msgs2__action__MovelH2r_Feedback * output);

/// Initialize array of action/MovelH2r messages.
/**
 * It allocates the memory for the number of elements and calls
 * dsr_msgs2__action__MovelH2r_Feedback__init()
 * for each element of the array.
 * \param[in,out] array The allocated array pointer.
 * \param[in] size The size / capacity of the array.
 * \return true if initialization was successful, otherwise false
 * If the array pointer is valid and the size is zero it is guaranteed
 # to return true.
 */
ROSIDL_GENERATOR_C_PUBLIC_dsr_msgs2
bool
dsr_msgs2__action__MovelH2r_Feedback__Sequence__init(dsr_msgs2__action__MovelH2r_Feedback__Sequence * array, size_t size);

/// Finalize array of action/MovelH2r messages.
/**
 * It calls
 * dsr_msgs2__action__MovelH2r_Feedback__fini()
 * for each element of the array and frees the memory for the number of
 * elements.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_dsr_msgs2
void
dsr_msgs2__action__MovelH2r_Feedback__Sequence__fini(dsr_msgs2__action__MovelH2r_Feedback__Sequence * array);

/// Create array of action/MovelH2r messages.
/**
 * It allocates the memory for the array and calls
 * dsr_msgs2__action__MovelH2r_Feedback__Sequence__init().
 * \param[in] size The size / capacity of the array.
 * \return The pointer to the initialized array if successful, otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_dsr_msgs2
dsr_msgs2__action__MovelH2r_Feedback__Sequence *
dsr_msgs2__action__MovelH2r_Feedback__Sequence__create(size_t size);

/// Destroy array of action/MovelH2r messages.
/**
 * It calls
 * dsr_msgs2__action__MovelH2r_Feedback__Sequence__fini()
 * on the array,
 * and frees the memory of the array.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_dsr_msgs2
void
dsr_msgs2__action__MovelH2r_Feedback__Sequence__destroy(dsr_msgs2__action__MovelH2r_Feedback__Sequence * array);

/// Check for action/MovelH2r message array equality.
/**
 * \param[in] lhs The message array on the left hand size of the equality operator.
 * \param[in] rhs The message array on the right hand size of the equality operator.
 * \return true if message arrays are equal in size and content, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_dsr_msgs2
bool
dsr_msgs2__action__MovelH2r_Feedback__Sequence__are_equal(const dsr_msgs2__action__MovelH2r_Feedback__Sequence * lhs, const dsr_msgs2__action__MovelH2r_Feedback__Sequence * rhs);

/// Copy an array of action/MovelH2r messages.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source array pointer.
 * \param[out] output The target array pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer
 *   is null or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_dsr_msgs2
bool
dsr_msgs2__action__MovelH2r_Feedback__Sequence__copy(
  const dsr_msgs2__action__MovelH2r_Feedback__Sequence * input,
  dsr_msgs2__action__MovelH2r_Feedback__Sequence * output);

/// Initialize action/MovelH2r message.
/**
 * If the init function is called twice for the same message without
 * calling fini inbetween previously allocated memory will be leaked.
 * \param[in,out] msg The previously allocated message pointer.
 * Fields without a default value will not be initialized by this function.
 * You might want to call memset(msg, 0, sizeof(
 * dsr_msgs2__action__MovelH2r_SendGoal_Request
 * )) before or use
 * dsr_msgs2__action__MovelH2r_SendGoal_Request__create()
 * to allocate and initialize the message.
 * \return true if initialization was successful, otherwise false
 */
ROSIDL_GENERATOR_C_PUBLIC_dsr_msgs2
bool
dsr_msgs2__action__MovelH2r_SendGoal_Request__init(dsr_msgs2__action__MovelH2r_SendGoal_Request * msg);

/// Finalize action/MovelH2r message.
/**
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_dsr_msgs2
void
dsr_msgs2__action__MovelH2r_SendGoal_Request__fini(dsr_msgs2__action__MovelH2r_SendGoal_Request * msg);

/// Create action/MovelH2r message.
/**
 * It allocates the memory for the message, sets the memory to zero, and
 * calls
 * dsr_msgs2__action__MovelH2r_SendGoal_Request__init().
 * \return The pointer to the initialized message if successful,
 * otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_dsr_msgs2
dsr_msgs2__action__MovelH2r_SendGoal_Request *
dsr_msgs2__action__MovelH2r_SendGoal_Request__create();

/// Destroy action/MovelH2r message.
/**
 * It calls
 * dsr_msgs2__action__MovelH2r_SendGoal_Request__fini()
 * and frees the memory of the message.
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_dsr_msgs2
void
dsr_msgs2__action__MovelH2r_SendGoal_Request__destroy(dsr_msgs2__action__MovelH2r_SendGoal_Request * msg);

/// Check for action/MovelH2r message equality.
/**
 * \param[in] lhs The message on the left hand size of the equality operator.
 * \param[in] rhs The message on the right hand size of the equality operator.
 * \return true if messages are equal, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_dsr_msgs2
bool
dsr_msgs2__action__MovelH2r_SendGoal_Request__are_equal(const dsr_msgs2__action__MovelH2r_SendGoal_Request * lhs, const dsr_msgs2__action__MovelH2r_SendGoal_Request * rhs);

/// Copy a action/MovelH2r message.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source message pointer.
 * \param[out] output The target message pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer is null
 *   or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_dsr_msgs2
bool
dsr_msgs2__action__MovelH2r_SendGoal_Request__copy(
  const dsr_msgs2__action__MovelH2r_SendGoal_Request * input,
  dsr_msgs2__action__MovelH2r_SendGoal_Request * output);

/// Initialize array of action/MovelH2r messages.
/**
 * It allocates the memory for the number of elements and calls
 * dsr_msgs2__action__MovelH2r_SendGoal_Request__init()
 * for each element of the array.
 * \param[in,out] array The allocated array pointer.
 * \param[in] size The size / capacity of the array.
 * \return true if initialization was successful, otherwise false
 * If the array pointer is valid and the size is zero it is guaranteed
 # to return true.
 */
ROSIDL_GENERATOR_C_PUBLIC_dsr_msgs2
bool
dsr_msgs2__action__MovelH2r_SendGoal_Request__Sequence__init(dsr_msgs2__action__MovelH2r_SendGoal_Request__Sequence * array, size_t size);

/// Finalize array of action/MovelH2r messages.
/**
 * It calls
 * dsr_msgs2__action__MovelH2r_SendGoal_Request__fini()
 * for each element of the array and frees the memory for the number of
 * elements.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_dsr_msgs2
void
dsr_msgs2__action__MovelH2r_SendGoal_Request__Sequence__fini(dsr_msgs2__action__MovelH2r_SendGoal_Request__Sequence * array);

/// Create array of action/MovelH2r messages.
/**
 * It allocates the memory for the array and calls
 * dsr_msgs2__action__MovelH2r_SendGoal_Request__Sequence__init().
 * \param[in] size The size / capacity of the array.
 * \return The pointer to the initialized array if successful, otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_dsr_msgs2
dsr_msgs2__action__MovelH2r_SendGoal_Request__Sequence *
dsr_msgs2__action__MovelH2r_SendGoal_Request__Sequence__create(size_t size);

/// Destroy array of action/MovelH2r messages.
/**
 * It calls
 * dsr_msgs2__action__MovelH2r_SendGoal_Request__Sequence__fini()
 * on the array,
 * and frees the memory of the array.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_dsr_msgs2
void
dsr_msgs2__action__MovelH2r_SendGoal_Request__Sequence__destroy(dsr_msgs2__action__MovelH2r_SendGoal_Request__Sequence * array);

/// Check for action/MovelH2r message array equality.
/**
 * \param[in] lhs The message array on the left hand size of the equality operator.
 * \param[in] rhs The message array on the right hand size of the equality operator.
 * \return true if message arrays are equal in size and content, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_dsr_msgs2
bool
dsr_msgs2__action__MovelH2r_SendGoal_Request__Sequence__are_equal(const dsr_msgs2__action__MovelH2r_SendGoal_Request__Sequence * lhs, const dsr_msgs2__action__MovelH2r_SendGoal_Request__Sequence * rhs);

/// Copy an array of action/MovelH2r messages.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source array pointer.
 * \param[out] output The target array pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer
 *   is null or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_dsr_msgs2
bool
dsr_msgs2__action__MovelH2r_SendGoal_Request__Sequence__copy(
  const dsr_msgs2__action__MovelH2r_SendGoal_Request__Sequence * input,
  dsr_msgs2__action__MovelH2r_SendGoal_Request__Sequence * output);

/// Initialize action/MovelH2r message.
/**
 * If the init function is called twice for the same message without
 * calling fini inbetween previously allocated memory will be leaked.
 * \param[in,out] msg The previously allocated message pointer.
 * Fields without a default value will not be initialized by this function.
 * You might want to call memset(msg, 0, sizeof(
 * dsr_msgs2__action__MovelH2r_SendGoal_Response
 * )) before or use
 * dsr_msgs2__action__MovelH2r_SendGoal_Response__create()
 * to allocate and initialize the message.
 * \return true if initialization was successful, otherwise false
 */
ROSIDL_GENERATOR_C_PUBLIC_dsr_msgs2
bool
dsr_msgs2__action__MovelH2r_SendGoal_Response__init(dsr_msgs2__action__MovelH2r_SendGoal_Response * msg);

/// Finalize action/MovelH2r message.
/**
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_dsr_msgs2
void
dsr_msgs2__action__MovelH2r_SendGoal_Response__fini(dsr_msgs2__action__MovelH2r_SendGoal_Response * msg);

/// Create action/MovelH2r message.
/**
 * It allocates the memory for the message, sets the memory to zero, and
 * calls
 * dsr_msgs2__action__MovelH2r_SendGoal_Response__init().
 * \return The pointer to the initialized message if successful,
 * otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_dsr_msgs2
dsr_msgs2__action__MovelH2r_SendGoal_Response *
dsr_msgs2__action__MovelH2r_SendGoal_Response__create();

/// Destroy action/MovelH2r message.
/**
 * It calls
 * dsr_msgs2__action__MovelH2r_SendGoal_Response__fini()
 * and frees the memory of the message.
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_dsr_msgs2
void
dsr_msgs2__action__MovelH2r_SendGoal_Response__destroy(dsr_msgs2__action__MovelH2r_SendGoal_Response * msg);

/// Check for action/MovelH2r message equality.
/**
 * \param[in] lhs The message on the left hand size of the equality operator.
 * \param[in] rhs The message on the right hand size of the equality operator.
 * \return true if messages are equal, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_dsr_msgs2
bool
dsr_msgs2__action__MovelH2r_SendGoal_Response__are_equal(const dsr_msgs2__action__MovelH2r_SendGoal_Response * lhs, const dsr_msgs2__action__MovelH2r_SendGoal_Response * rhs);

/// Copy a action/MovelH2r message.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source message pointer.
 * \param[out] output The target message pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer is null
 *   or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_dsr_msgs2
bool
dsr_msgs2__action__MovelH2r_SendGoal_Response__copy(
  const dsr_msgs2__action__MovelH2r_SendGoal_Response * input,
  dsr_msgs2__action__MovelH2r_SendGoal_Response * output);

/// Initialize array of action/MovelH2r messages.
/**
 * It allocates the memory for the number of elements and calls
 * dsr_msgs2__action__MovelH2r_SendGoal_Response__init()
 * for each element of the array.
 * \param[in,out] array The allocated array pointer.
 * \param[in] size The size / capacity of the array.
 * \return true if initialization was successful, otherwise false
 * If the array pointer is valid and the size is zero it is guaranteed
 # to return true.
 */
ROSIDL_GENERATOR_C_PUBLIC_dsr_msgs2
bool
dsr_msgs2__action__MovelH2r_SendGoal_Response__Sequence__init(dsr_msgs2__action__MovelH2r_SendGoal_Response__Sequence * array, size_t size);

/// Finalize array of action/MovelH2r messages.
/**
 * It calls
 * dsr_msgs2__action__MovelH2r_SendGoal_Response__fini()
 * for each element of the array and frees the memory for the number of
 * elements.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_dsr_msgs2
void
dsr_msgs2__action__MovelH2r_SendGoal_Response__Sequence__fini(dsr_msgs2__action__MovelH2r_SendGoal_Response__Sequence * array);

/// Create array of action/MovelH2r messages.
/**
 * It allocates the memory for the array and calls
 * dsr_msgs2__action__MovelH2r_SendGoal_Response__Sequence__init().
 * \param[in] size The size / capacity of the array.
 * \return The pointer to the initialized array if successful, otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_dsr_msgs2
dsr_msgs2__action__MovelH2r_SendGoal_Response__Sequence *
dsr_msgs2__action__MovelH2r_SendGoal_Response__Sequence__create(size_t size);

/// Destroy array of action/MovelH2r messages.
/**
 * It calls
 * dsr_msgs2__action__MovelH2r_SendGoal_Response__Sequence__fini()
 * on the array,
 * and frees the memory of the array.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_dsr_msgs2
void
dsr_msgs2__action__MovelH2r_SendGoal_Response__Sequence__destroy(dsr_msgs2__action__MovelH2r_SendGoal_Response__Sequence * array);

/// Check for action/MovelH2r message array equality.
/**
 * \param[in] lhs The message array on the left hand size of the equality operator.
 * \param[in] rhs The message array on the right hand size of the equality operator.
 * \return true if message arrays are equal in size and content, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_dsr_msgs2
bool
dsr_msgs2__action__MovelH2r_SendGoal_Response__Sequence__are_equal(const dsr_msgs2__action__MovelH2r_SendGoal_Response__Sequence * lhs, const dsr_msgs2__action__MovelH2r_SendGoal_Response__Sequence * rhs);

/// Copy an array of action/MovelH2r messages.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source array pointer.
 * \param[out] output The target array pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer
 *   is null or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_dsr_msgs2
bool
dsr_msgs2__action__MovelH2r_SendGoal_Response__Sequence__copy(
  const dsr_msgs2__action__MovelH2r_SendGoal_Response__Sequence * input,
  dsr_msgs2__action__MovelH2r_SendGoal_Response__Sequence * output);

/// Initialize action/MovelH2r message.
/**
 * If the init function is called twice for the same message without
 * calling fini inbetween previously allocated memory will be leaked.
 * \param[in,out] msg The previously allocated message pointer.
 * Fields without a default value will not be initialized by this function.
 * You might want to call memset(msg, 0, sizeof(
 * dsr_msgs2__action__MovelH2r_GetResult_Request
 * )) before or use
 * dsr_msgs2__action__MovelH2r_GetResult_Request__create()
 * to allocate and initialize the message.
 * \return true if initialization was successful, otherwise false
 */
ROSIDL_GENERATOR_C_PUBLIC_dsr_msgs2
bool
dsr_msgs2__action__MovelH2r_GetResult_Request__init(dsr_msgs2__action__MovelH2r_GetResult_Request * msg);

/// Finalize action/MovelH2r message.
/**
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_dsr_msgs2
void
dsr_msgs2__action__MovelH2r_GetResult_Request__fini(dsr_msgs2__action__MovelH2r_GetResult_Request * msg);

/// Create action/MovelH2r message.
/**
 * It allocates the memory for the message, sets the memory to zero, and
 * calls
 * dsr_msgs2__action__MovelH2r_GetResult_Request__init().
 * \return The pointer to the initialized message if successful,
 * otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_dsr_msgs2
dsr_msgs2__action__MovelH2r_GetResult_Request *
dsr_msgs2__action__MovelH2r_GetResult_Request__create();

/// Destroy action/MovelH2r message.
/**
 * It calls
 * dsr_msgs2__action__MovelH2r_GetResult_Request__fini()
 * and frees the memory of the message.
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_dsr_msgs2
void
dsr_msgs2__action__MovelH2r_GetResult_Request__destroy(dsr_msgs2__action__MovelH2r_GetResult_Request * msg);

/// Check for action/MovelH2r message equality.
/**
 * \param[in] lhs The message on the left hand size of the equality operator.
 * \param[in] rhs The message on the right hand size of the equality operator.
 * \return true if messages are equal, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_dsr_msgs2
bool
dsr_msgs2__action__MovelH2r_GetResult_Request__are_equal(const dsr_msgs2__action__MovelH2r_GetResult_Request * lhs, const dsr_msgs2__action__MovelH2r_GetResult_Request * rhs);

/// Copy a action/MovelH2r message.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source message pointer.
 * \param[out] output The target message pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer is null
 *   or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_dsr_msgs2
bool
dsr_msgs2__action__MovelH2r_GetResult_Request__copy(
  const dsr_msgs2__action__MovelH2r_GetResult_Request * input,
  dsr_msgs2__action__MovelH2r_GetResult_Request * output);

/// Initialize array of action/MovelH2r messages.
/**
 * It allocates the memory for the number of elements and calls
 * dsr_msgs2__action__MovelH2r_GetResult_Request__init()
 * for each element of the array.
 * \param[in,out] array The allocated array pointer.
 * \param[in] size The size / capacity of the array.
 * \return true if initialization was successful, otherwise false
 * If the array pointer is valid and the size is zero it is guaranteed
 # to return true.
 */
ROSIDL_GENERATOR_C_PUBLIC_dsr_msgs2
bool
dsr_msgs2__action__MovelH2r_GetResult_Request__Sequence__init(dsr_msgs2__action__MovelH2r_GetResult_Request__Sequence * array, size_t size);

/// Finalize array of action/MovelH2r messages.
/**
 * It calls
 * dsr_msgs2__action__MovelH2r_GetResult_Request__fini()
 * for each element of the array and frees the memory for the number of
 * elements.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_dsr_msgs2
void
dsr_msgs2__action__MovelH2r_GetResult_Request__Sequence__fini(dsr_msgs2__action__MovelH2r_GetResult_Request__Sequence * array);

/// Create array of action/MovelH2r messages.
/**
 * It allocates the memory for the array and calls
 * dsr_msgs2__action__MovelH2r_GetResult_Request__Sequence__init().
 * \param[in] size The size / capacity of the array.
 * \return The pointer to the initialized array if successful, otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_dsr_msgs2
dsr_msgs2__action__MovelH2r_GetResult_Request__Sequence *
dsr_msgs2__action__MovelH2r_GetResult_Request__Sequence__create(size_t size);

/// Destroy array of action/MovelH2r messages.
/**
 * It calls
 * dsr_msgs2__action__MovelH2r_GetResult_Request__Sequence__fini()
 * on the array,
 * and frees the memory of the array.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_dsr_msgs2
void
dsr_msgs2__action__MovelH2r_GetResult_Request__Sequence__destroy(dsr_msgs2__action__MovelH2r_GetResult_Request__Sequence * array);

/// Check for action/MovelH2r message array equality.
/**
 * \param[in] lhs The message array on the left hand size of the equality operator.
 * \param[in] rhs The message array on the right hand size of the equality operator.
 * \return true if message arrays are equal in size and content, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_dsr_msgs2
bool
dsr_msgs2__action__MovelH2r_GetResult_Request__Sequence__are_equal(const dsr_msgs2__action__MovelH2r_GetResult_Request__Sequence * lhs, const dsr_msgs2__action__MovelH2r_GetResult_Request__Sequence * rhs);

/// Copy an array of action/MovelH2r messages.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source array pointer.
 * \param[out] output The target array pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer
 *   is null or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_dsr_msgs2
bool
dsr_msgs2__action__MovelH2r_GetResult_Request__Sequence__copy(
  const dsr_msgs2__action__MovelH2r_GetResult_Request__Sequence * input,
  dsr_msgs2__action__MovelH2r_GetResult_Request__Sequence * output);

/// Initialize action/MovelH2r message.
/**
 * If the init function is called twice for the same message without
 * calling fini inbetween previously allocated memory will be leaked.
 * \param[in,out] msg The previously allocated message pointer.
 * Fields without a default value will not be initialized by this function.
 * You might want to call memset(msg, 0, sizeof(
 * dsr_msgs2__action__MovelH2r_GetResult_Response
 * )) before or use
 * dsr_msgs2__action__MovelH2r_GetResult_Response__create()
 * to allocate and initialize the message.
 * \return true if initialization was successful, otherwise false
 */
ROSIDL_GENERATOR_C_PUBLIC_dsr_msgs2
bool
dsr_msgs2__action__MovelH2r_GetResult_Response__init(dsr_msgs2__action__MovelH2r_GetResult_Response * msg);

/// Finalize action/MovelH2r message.
/**
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_dsr_msgs2
void
dsr_msgs2__action__MovelH2r_GetResult_Response__fini(dsr_msgs2__action__MovelH2r_GetResult_Response * msg);

/// Create action/MovelH2r message.
/**
 * It allocates the memory for the message, sets the memory to zero, and
 * calls
 * dsr_msgs2__action__MovelH2r_GetResult_Response__init().
 * \return The pointer to the initialized message if successful,
 * otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_dsr_msgs2
dsr_msgs2__action__MovelH2r_GetResult_Response *
dsr_msgs2__action__MovelH2r_GetResult_Response__create();

/// Destroy action/MovelH2r message.
/**
 * It calls
 * dsr_msgs2__action__MovelH2r_GetResult_Response__fini()
 * and frees the memory of the message.
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_dsr_msgs2
void
dsr_msgs2__action__MovelH2r_GetResult_Response__destroy(dsr_msgs2__action__MovelH2r_GetResult_Response * msg);

/// Check for action/MovelH2r message equality.
/**
 * \param[in] lhs The message on the left hand size of the equality operator.
 * \param[in] rhs The message on the right hand size of the equality operator.
 * \return true if messages are equal, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_dsr_msgs2
bool
dsr_msgs2__action__MovelH2r_GetResult_Response__are_equal(const dsr_msgs2__action__MovelH2r_GetResult_Response * lhs, const dsr_msgs2__action__MovelH2r_GetResult_Response * rhs);

/// Copy a action/MovelH2r message.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source message pointer.
 * \param[out] output The target message pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer is null
 *   or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_dsr_msgs2
bool
dsr_msgs2__action__MovelH2r_GetResult_Response__copy(
  const dsr_msgs2__action__MovelH2r_GetResult_Response * input,
  dsr_msgs2__action__MovelH2r_GetResult_Response * output);

/// Initialize array of action/MovelH2r messages.
/**
 * It allocates the memory for the number of elements and calls
 * dsr_msgs2__action__MovelH2r_GetResult_Response__init()
 * for each element of the array.
 * \param[in,out] array The allocated array pointer.
 * \param[in] size The size / capacity of the array.
 * \return true if initialization was successful, otherwise false
 * If the array pointer is valid and the size is zero it is guaranteed
 # to return true.
 */
ROSIDL_GENERATOR_C_PUBLIC_dsr_msgs2
bool
dsr_msgs2__action__MovelH2r_GetResult_Response__Sequence__init(dsr_msgs2__action__MovelH2r_GetResult_Response__Sequence * array, size_t size);

/// Finalize array of action/MovelH2r messages.
/**
 * It calls
 * dsr_msgs2__action__MovelH2r_GetResult_Response__fini()
 * for each element of the array and frees the memory for the number of
 * elements.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_dsr_msgs2
void
dsr_msgs2__action__MovelH2r_GetResult_Response__Sequence__fini(dsr_msgs2__action__MovelH2r_GetResult_Response__Sequence * array);

/// Create array of action/MovelH2r messages.
/**
 * It allocates the memory for the array and calls
 * dsr_msgs2__action__MovelH2r_GetResult_Response__Sequence__init().
 * \param[in] size The size / capacity of the array.
 * \return The pointer to the initialized array if successful, otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_dsr_msgs2
dsr_msgs2__action__MovelH2r_GetResult_Response__Sequence *
dsr_msgs2__action__MovelH2r_GetResult_Response__Sequence__create(size_t size);

/// Destroy array of action/MovelH2r messages.
/**
 * It calls
 * dsr_msgs2__action__MovelH2r_GetResult_Response__Sequence__fini()
 * on the array,
 * and frees the memory of the array.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_dsr_msgs2
void
dsr_msgs2__action__MovelH2r_GetResult_Response__Sequence__destroy(dsr_msgs2__action__MovelH2r_GetResult_Response__Sequence * array);

/// Check for action/MovelH2r message array equality.
/**
 * \param[in] lhs The message array on the left hand size of the equality operator.
 * \param[in] rhs The message array on the right hand size of the equality operator.
 * \return true if message arrays are equal in size and content, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_dsr_msgs2
bool
dsr_msgs2__action__MovelH2r_GetResult_Response__Sequence__are_equal(const dsr_msgs2__action__MovelH2r_GetResult_Response__Sequence * lhs, const dsr_msgs2__action__MovelH2r_GetResult_Response__Sequence * rhs);

/// Copy an array of action/MovelH2r messages.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source array pointer.
 * \param[out] output The target array pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer
 *   is null or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_dsr_msgs2
bool
dsr_msgs2__action__MovelH2r_GetResult_Response__Sequence__copy(
  const dsr_msgs2__action__MovelH2r_GetResult_Response__Sequence * input,
  dsr_msgs2__action__MovelH2r_GetResult_Response__Sequence * output);

/// Initialize action/MovelH2r message.
/**
 * If the init function is called twice for the same message without
 * calling fini inbetween previously allocated memory will be leaked.
 * \param[in,out] msg The previously allocated message pointer.
 * Fields without a default value will not be initialized by this function.
 * You might want to call memset(msg, 0, sizeof(
 * dsr_msgs2__action__MovelH2r_FeedbackMessage
 * )) before or use
 * dsr_msgs2__action__MovelH2r_FeedbackMessage__create()
 * to allocate and initialize the message.
 * \return true if initialization was successful, otherwise false
 */
ROSIDL_GENERATOR_C_PUBLIC_dsr_msgs2
bool
dsr_msgs2__action__MovelH2r_FeedbackMessage__init(dsr_msgs2__action__MovelH2r_FeedbackMessage * msg);

/// Finalize action/MovelH2r message.
/**
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_dsr_msgs2
void
dsr_msgs2__action__MovelH2r_FeedbackMessage__fini(dsr_msgs2__action__MovelH2r_FeedbackMessage * msg);

/// Create action/MovelH2r message.
/**
 * It allocates the memory for the message, sets the memory to zero, and
 * calls
 * dsr_msgs2__action__MovelH2r_FeedbackMessage__init().
 * \return The pointer to the initialized message if successful,
 * otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_dsr_msgs2
dsr_msgs2__action__MovelH2r_FeedbackMessage *
dsr_msgs2__action__MovelH2r_FeedbackMessage__create();

/// Destroy action/MovelH2r message.
/**
 * It calls
 * dsr_msgs2__action__MovelH2r_FeedbackMessage__fini()
 * and frees the memory of the message.
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_dsr_msgs2
void
dsr_msgs2__action__MovelH2r_FeedbackMessage__destroy(dsr_msgs2__action__MovelH2r_FeedbackMessage * msg);

/// Check for action/MovelH2r message equality.
/**
 * \param[in] lhs The message on the left hand size of the equality operator.
 * \param[in] rhs The message on the right hand size of the equality operator.
 * \return true if messages are equal, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_dsr_msgs2
bool
dsr_msgs2__action__MovelH2r_FeedbackMessage__are_equal(const dsr_msgs2__action__MovelH2r_FeedbackMessage * lhs, const dsr_msgs2__action__MovelH2r_FeedbackMessage * rhs);

/// Copy a action/MovelH2r message.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source message pointer.
 * \param[out] output The target message pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer is null
 *   or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_dsr_msgs2
bool
dsr_msgs2__action__MovelH2r_FeedbackMessage__copy(
  const dsr_msgs2__action__MovelH2r_FeedbackMessage * input,
  dsr_msgs2__action__MovelH2r_FeedbackMessage * output);

/// Initialize array of action/MovelH2r messages.
/**
 * It allocates the memory for the number of elements and calls
 * dsr_msgs2__action__MovelH2r_FeedbackMessage__init()
 * for each element of the array.
 * \param[in,out] array The allocated array pointer.
 * \param[in] size The size / capacity of the array.
 * \return true if initialization was successful, otherwise false
 * If the array pointer is valid and the size is zero it is guaranteed
 # to return true.
 */
ROSIDL_GENERATOR_C_PUBLIC_dsr_msgs2
bool
dsr_msgs2__action__MovelH2r_FeedbackMessage__Sequence__init(dsr_msgs2__action__MovelH2r_FeedbackMessage__Sequence * array, size_t size);

/// Finalize array of action/MovelH2r messages.
/**
 * It calls
 * dsr_msgs2__action__MovelH2r_FeedbackMessage__fini()
 * for each element of the array and frees the memory for the number of
 * elements.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_dsr_msgs2
void
dsr_msgs2__action__MovelH2r_FeedbackMessage__Sequence__fini(dsr_msgs2__action__MovelH2r_FeedbackMessage__Sequence * array);

/// Create array of action/MovelH2r messages.
/**
 * It allocates the memory for the array and calls
 * dsr_msgs2__action__MovelH2r_FeedbackMessage__Sequence__init().
 * \param[in] size The size / capacity of the array.
 * \return The pointer to the initialized array if successful, otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_dsr_msgs2
dsr_msgs2__action__MovelH2r_FeedbackMessage__Sequence *
dsr_msgs2__action__MovelH2r_FeedbackMessage__Sequence__create(size_t size);

/// Destroy array of action/MovelH2r messages.
/**
 * It calls
 * dsr_msgs2__action__MovelH2r_FeedbackMessage__Sequence__fini()
 * on the array,
 * and frees the memory of the array.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_dsr_msgs2
void
dsr_msgs2__action__MovelH2r_FeedbackMessage__Sequence__destroy(dsr_msgs2__action__MovelH2r_FeedbackMessage__Sequence * array);

/// Check for action/MovelH2r message array equality.
/**
 * \param[in] lhs The message array on the left hand size of the equality operator.
 * \param[in] rhs The message array on the right hand size of the equality operator.
 * \return true if message arrays are equal in size and content, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_dsr_msgs2
bool
dsr_msgs2__action__MovelH2r_FeedbackMessage__Sequence__are_equal(const dsr_msgs2__action__MovelH2r_FeedbackMessage__Sequence * lhs, const dsr_msgs2__action__MovelH2r_FeedbackMessage__Sequence * rhs);

/// Copy an array of action/MovelH2r messages.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source array pointer.
 * \param[out] output The target array pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer
 *   is null or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_dsr_msgs2
bool
dsr_msgs2__action__MovelH2r_FeedbackMessage__Sequence__copy(
  const dsr_msgs2__action__MovelH2r_FeedbackMessage__Sequence * input,
  dsr_msgs2__action__MovelH2r_FeedbackMessage__Sequence * output);

#ifdef __cplusplus
}
#endif

#endif  // DSR_MSGS2__ACTION__DETAIL__MOVEL_H2R__FUNCTIONS_H_
