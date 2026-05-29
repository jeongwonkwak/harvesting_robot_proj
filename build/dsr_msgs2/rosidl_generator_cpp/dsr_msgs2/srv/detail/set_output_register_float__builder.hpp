// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from dsr_msgs2:srv/SetOutputRegisterFloat.idl
// generated code does not contain a copyright notice

#ifndef DSR_MSGS2__SRV__DETAIL__SET_OUTPUT_REGISTER_FLOAT__BUILDER_HPP_
#define DSR_MSGS2__SRV__DETAIL__SET_OUTPUT_REGISTER_FLOAT__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "dsr_msgs2/srv/detail/set_output_register_float__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace dsr_msgs2
{

namespace srv
{

namespace builder
{

class Init_SetOutputRegisterFloat_Request_value
{
public:
  explicit Init_SetOutputRegisterFloat_Request_value(::dsr_msgs2::srv::SetOutputRegisterFloat_Request & msg)
  : msg_(msg)
  {}
  ::dsr_msgs2::srv::SetOutputRegisterFloat_Request value(::dsr_msgs2::srv::SetOutputRegisterFloat_Request::_value_type arg)
  {
    msg_.value = std::move(arg);
    return std::move(msg_);
  }

private:
  ::dsr_msgs2::srv::SetOutputRegisterFloat_Request msg_;
};

class Init_SetOutputRegisterFloat_Request_address
{
public:
  Init_SetOutputRegisterFloat_Request_address()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_SetOutputRegisterFloat_Request_value address(::dsr_msgs2::srv::SetOutputRegisterFloat_Request::_address_type arg)
  {
    msg_.address = std::move(arg);
    return Init_SetOutputRegisterFloat_Request_value(msg_);
  }

private:
  ::dsr_msgs2::srv::SetOutputRegisterFloat_Request msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::dsr_msgs2::srv::SetOutputRegisterFloat_Request>()
{
  return dsr_msgs2::srv::builder::Init_SetOutputRegisterFloat_Request_address();
}

}  // namespace dsr_msgs2


namespace dsr_msgs2
{

namespace srv
{

namespace builder
{

class Init_SetOutputRegisterFloat_Response_success
{
public:
  Init_SetOutputRegisterFloat_Response_success()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::dsr_msgs2::srv::SetOutputRegisterFloat_Response success(::dsr_msgs2::srv::SetOutputRegisterFloat_Response::_success_type arg)
  {
    msg_.success = std::move(arg);
    return std::move(msg_);
  }

private:
  ::dsr_msgs2::srv::SetOutputRegisterFloat_Response msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::dsr_msgs2::srv::SetOutputRegisterFloat_Response>()
{
  return dsr_msgs2::srv::builder::Init_SetOutputRegisterFloat_Response_success();
}

}  // namespace dsr_msgs2

#endif  // DSR_MSGS2__SRV__DETAIL__SET_OUTPUT_REGISTER_FLOAT__BUILDER_HPP_
