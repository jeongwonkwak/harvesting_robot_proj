// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from dsr_msgs2:srv/SetSingularHandlingForce.idl
// generated code does not contain a copyright notice

#ifndef DSR_MSGS2__SRV__DETAIL__SET_SINGULAR_HANDLING_FORCE__BUILDER_HPP_
#define DSR_MSGS2__SRV__DETAIL__SET_SINGULAR_HANDLING_FORCE__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "dsr_msgs2/srv/detail/set_singular_handling_force__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace dsr_msgs2
{

namespace srv
{

namespace builder
{

class Init_SetSingularHandlingForce_Request_mode
{
public:
  Init_SetSingularHandlingForce_Request_mode()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::dsr_msgs2::srv::SetSingularHandlingForce_Request mode(::dsr_msgs2::srv::SetSingularHandlingForce_Request::_mode_type arg)
  {
    msg_.mode = std::move(arg);
    return std::move(msg_);
  }

private:
  ::dsr_msgs2::srv::SetSingularHandlingForce_Request msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::dsr_msgs2::srv::SetSingularHandlingForce_Request>()
{
  return dsr_msgs2::srv::builder::Init_SetSingularHandlingForce_Request_mode();
}

}  // namespace dsr_msgs2


namespace dsr_msgs2
{

namespace srv
{

namespace builder
{

class Init_SetSingularHandlingForce_Response_success
{
public:
  Init_SetSingularHandlingForce_Response_success()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::dsr_msgs2::srv::SetSingularHandlingForce_Response success(::dsr_msgs2::srv::SetSingularHandlingForce_Response::_success_type arg)
  {
    msg_.success = std::move(arg);
    return std::move(msg_);
  }

private:
  ::dsr_msgs2::srv::SetSingularHandlingForce_Response msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::dsr_msgs2::srv::SetSingularHandlingForce_Response>()
{
  return dsr_msgs2::srv::builder::Init_SetSingularHandlingForce_Response_success();
}

}  // namespace dsr_msgs2

#endif  // DSR_MSGS2__SRV__DETAIL__SET_SINGULAR_HANDLING_FORCE__BUILDER_HPP_
