// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from dsr_msgs2:srv/GetRobotLinkInfo.idl
// generated code does not contain a copyright notice

#ifndef DSR_MSGS2__SRV__DETAIL__GET_ROBOT_LINK_INFO__BUILDER_HPP_
#define DSR_MSGS2__SRV__DETAIL__GET_ROBOT_LINK_INFO__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "dsr_msgs2/srv/detail/get_robot_link_info__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace dsr_msgs2
{

namespace srv
{


}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::dsr_msgs2::srv::GetRobotLinkInfo_Request>()
{
  return ::dsr_msgs2::srv::GetRobotLinkInfo_Request(rosidl_runtime_cpp::MessageInitialization::ZERO);
}

}  // namespace dsr_msgs2


namespace dsr_msgs2
{

namespace srv
{

namespace builder
{

class Init_GetRobotLinkInfo_Response_success
{
public:
  explicit Init_GetRobotLinkInfo_Response_success(::dsr_msgs2::srv::GetRobotLinkInfo_Response & msg)
  : msg_(msg)
  {}
  ::dsr_msgs2::srv::GetRobotLinkInfo_Response success(::dsr_msgs2::srv::GetRobotLinkInfo_Response::_success_type arg)
  {
    msg_.success = std::move(arg);
    return std::move(msg_);
  }

private:
  ::dsr_msgs2::srv::GetRobotLinkInfo_Response msg_;
};

class Init_GetRobotLinkInfo_Response_rotation
{
public:
  explicit Init_GetRobotLinkInfo_Response_rotation(::dsr_msgs2::srv::GetRobotLinkInfo_Response & msg)
  : msg_(msg)
  {}
  Init_GetRobotLinkInfo_Response_success rotation(::dsr_msgs2::srv::GetRobotLinkInfo_Response::_rotation_type arg)
  {
    msg_.rotation = std::move(arg);
    return Init_GetRobotLinkInfo_Response_success(msg_);
  }

private:
  ::dsr_msgs2::srv::GetRobotLinkInfo_Response msg_;
};

class Init_GetRobotLinkInfo_Response_gradient
{
public:
  explicit Init_GetRobotLinkInfo_Response_gradient(::dsr_msgs2::srv::GetRobotLinkInfo_Response & msg)
  : msg_(msg)
  {}
  Init_GetRobotLinkInfo_Response_rotation gradient(::dsr_msgs2::srv::GetRobotLinkInfo_Response::_gradient_type arg)
  {
    msg_.gradient = std::move(arg);
    return Init_GetRobotLinkInfo_Response_rotation(msg_);
  }

private:
  ::dsr_msgs2::srv::GetRobotLinkInfo_Response msg_;
};

class Init_GetRobotLinkInfo_Response_offset
{
public:
  explicit Init_GetRobotLinkInfo_Response_offset(::dsr_msgs2::srv::GetRobotLinkInfo_Response & msg)
  : msg_(msg)
  {}
  Init_GetRobotLinkInfo_Response_gradient offset(::dsr_msgs2::srv::GetRobotLinkInfo_Response::_offset_type arg)
  {
    msg_.offset = std::move(arg);
    return Init_GetRobotLinkInfo_Response_gradient(msg_);
  }

private:
  ::dsr_msgs2::srv::GetRobotLinkInfo_Response msg_;
};

class Init_GetRobotLinkInfo_Response_theta
{
public:
  explicit Init_GetRobotLinkInfo_Response_theta(::dsr_msgs2::srv::GetRobotLinkInfo_Response & msg)
  : msg_(msg)
  {}
  Init_GetRobotLinkInfo_Response_offset theta(::dsr_msgs2::srv::GetRobotLinkInfo_Response::_theta_type arg)
  {
    msg_.theta = std::move(arg);
    return Init_GetRobotLinkInfo_Response_offset(msg_);
  }

private:
  ::dsr_msgs2::srv::GetRobotLinkInfo_Response msg_;
};

class Init_GetRobotLinkInfo_Response_alpha
{
public:
  explicit Init_GetRobotLinkInfo_Response_alpha(::dsr_msgs2::srv::GetRobotLinkInfo_Response & msg)
  : msg_(msg)
  {}
  Init_GetRobotLinkInfo_Response_theta alpha(::dsr_msgs2::srv::GetRobotLinkInfo_Response::_alpha_type arg)
  {
    msg_.alpha = std::move(arg);
    return Init_GetRobotLinkInfo_Response_theta(msg_);
  }

private:
  ::dsr_msgs2::srv::GetRobotLinkInfo_Response msg_;
};

class Init_GetRobotLinkInfo_Response_a
{
public:
  explicit Init_GetRobotLinkInfo_Response_a(::dsr_msgs2::srv::GetRobotLinkInfo_Response & msg)
  : msg_(msg)
  {}
  Init_GetRobotLinkInfo_Response_alpha a(::dsr_msgs2::srv::GetRobotLinkInfo_Response::_a_type arg)
  {
    msg_.a = std::move(arg);
    return Init_GetRobotLinkInfo_Response_alpha(msg_);
  }

private:
  ::dsr_msgs2::srv::GetRobotLinkInfo_Response msg_;
};

class Init_GetRobotLinkInfo_Response_d
{
public:
  Init_GetRobotLinkInfo_Response_d()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_GetRobotLinkInfo_Response_a d(::dsr_msgs2::srv::GetRobotLinkInfo_Response::_d_type arg)
  {
    msg_.d = std::move(arg);
    return Init_GetRobotLinkInfo_Response_a(msg_);
  }

private:
  ::dsr_msgs2::srv::GetRobotLinkInfo_Response msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::dsr_msgs2::srv::GetRobotLinkInfo_Response>()
{
  return dsr_msgs2::srv::builder::Init_GetRobotLinkInfo_Response_d();
}

}  // namespace dsr_msgs2

#endif  // DSR_MSGS2__SRV__DETAIL__GET_ROBOT_LINK_INFO__BUILDER_HPP_
