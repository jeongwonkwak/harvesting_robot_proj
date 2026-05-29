// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from my_robot_interfaces:msg/TurtleStatus.idl
// generated code does not contain a copyright notice

#ifndef MY_ROBOT_INTERFACES__MSG__DETAIL__TURTLE_STATUS__BUILDER_HPP_
#define MY_ROBOT_INTERFACES__MSG__DETAIL__TURTLE_STATUS__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "my_robot_interfaces/msg/detail/turtle_status__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace my_robot_interfaces
{

namespace msg
{

namespace builder
{

class Init_TurtleStatus_is_moving
{
public:
  explicit Init_TurtleStatus_is_moving(::my_robot_interfaces::msg::TurtleStatus & msg)
  : msg_(msg)
  {}
  ::my_robot_interfaces::msg::TurtleStatus is_moving(::my_robot_interfaces::msg::TurtleStatus::_is_moving_type arg)
  {
    msg_.is_moving = std::move(arg);
    return std::move(msg_);
  }

private:
  ::my_robot_interfaces::msg::TurtleStatus msg_;
};

class Init_TurtleStatus_current_state
{
public:
  explicit Init_TurtleStatus_current_state(::my_robot_interfaces::msg::TurtleStatus & msg)
  : msg_(msg)
  {}
  Init_TurtleStatus_is_moving current_state(::my_robot_interfaces::msg::TurtleStatus::_current_state_type arg)
  {
    msg_.current_state = std::move(arg);
    return Init_TurtleStatus_is_moving(msg_);
  }

private:
  ::my_robot_interfaces::msg::TurtleStatus msg_;
};

class Init_TurtleStatus_distance_to_wall
{
public:
  Init_TurtleStatus_distance_to_wall()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_TurtleStatus_current_state distance_to_wall(::my_robot_interfaces::msg::TurtleStatus::_distance_to_wall_type arg)
  {
    msg_.distance_to_wall = std::move(arg);
    return Init_TurtleStatus_current_state(msg_);
  }

private:
  ::my_robot_interfaces::msg::TurtleStatus msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::my_robot_interfaces::msg::TurtleStatus>()
{
  return my_robot_interfaces::msg::builder::Init_TurtleStatus_distance_to_wall();
}

}  // namespace my_robot_interfaces

#endif  // MY_ROBOT_INTERFACES__MSG__DETAIL__TURTLE_STATUS__BUILDER_HPP_
