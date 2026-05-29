// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from my_robot_interfaces:srv/SetTurtleMode.idl
// generated code does not contain a copyright notice

#ifndef MY_ROBOT_INTERFACES__SRV__DETAIL__SET_TURTLE_MODE__BUILDER_HPP_
#define MY_ROBOT_INTERFACES__SRV__DETAIL__SET_TURTLE_MODE__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "my_robot_interfaces/srv/detail/set_turtle_mode__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace my_robot_interfaces
{

namespace srv
{

namespace builder
{

class Init_SetTurtleMode_Request_target_speed
{
public:
  explicit Init_SetTurtleMode_Request_target_speed(::my_robot_interfaces::srv::SetTurtleMode_Request & msg)
  : msg_(msg)
  {}
  ::my_robot_interfaces::srv::SetTurtleMode_Request target_speed(::my_robot_interfaces::srv::SetTurtleMode_Request::_target_speed_type arg)
  {
    msg_.target_speed = std::move(arg);
    return std::move(msg_);
  }

private:
  ::my_robot_interfaces::srv::SetTurtleMode_Request msg_;
};

class Init_SetTurtleMode_Request_mode_name
{
public:
  Init_SetTurtleMode_Request_mode_name()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_SetTurtleMode_Request_target_speed mode_name(::my_robot_interfaces::srv::SetTurtleMode_Request::_mode_name_type arg)
  {
    msg_.mode_name = std::move(arg);
    return Init_SetTurtleMode_Request_target_speed(msg_);
  }

private:
  ::my_robot_interfaces::srv::SetTurtleMode_Request msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::my_robot_interfaces::srv::SetTurtleMode_Request>()
{
  return my_robot_interfaces::srv::builder::Init_SetTurtleMode_Request_mode_name();
}

}  // namespace my_robot_interfaces


namespace my_robot_interfaces
{

namespace srv
{

namespace builder
{

class Init_SetTurtleMode_Response_message
{
public:
  explicit Init_SetTurtleMode_Response_message(::my_robot_interfaces::srv::SetTurtleMode_Response & msg)
  : msg_(msg)
  {}
  ::my_robot_interfaces::srv::SetTurtleMode_Response message(::my_robot_interfaces::srv::SetTurtleMode_Response::_message_type arg)
  {
    msg_.message = std::move(arg);
    return std::move(msg_);
  }

private:
  ::my_robot_interfaces::srv::SetTurtleMode_Response msg_;
};

class Init_SetTurtleMode_Response_success
{
public:
  Init_SetTurtleMode_Response_success()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_SetTurtleMode_Response_message success(::my_robot_interfaces::srv::SetTurtleMode_Response::_success_type arg)
  {
    msg_.success = std::move(arg);
    return Init_SetTurtleMode_Response_message(msg_);
  }

private:
  ::my_robot_interfaces::srv::SetTurtleMode_Response msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::my_robot_interfaces::srv::SetTurtleMode_Response>()
{
  return my_robot_interfaces::srv::builder::Init_SetTurtleMode_Response_success();
}

}  // namespace my_robot_interfaces

#endif  // MY_ROBOT_INTERFACES__SRV__DETAIL__SET_TURTLE_MODE__BUILDER_HPP_
