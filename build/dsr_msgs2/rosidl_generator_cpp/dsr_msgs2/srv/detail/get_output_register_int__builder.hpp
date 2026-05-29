// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from dsr_msgs2:srv/GetOutputRegisterInt.idl
// generated code does not contain a copyright notice

#ifndef DSR_MSGS2__SRV__DETAIL__GET_OUTPUT_REGISTER_INT__BUILDER_HPP_
#define DSR_MSGS2__SRV__DETAIL__GET_OUTPUT_REGISTER_INT__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "dsr_msgs2/srv/detail/get_output_register_int__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace dsr_msgs2
{

namespace srv
{

namespace builder
{

class Init_GetOutputRegisterInt_Request_timeout_ms
{
public:
  explicit Init_GetOutputRegisterInt_Request_timeout_ms(::dsr_msgs2::srv::GetOutputRegisterInt_Request & msg)
  : msg_(msg)
  {}
  ::dsr_msgs2::srv::GetOutputRegisterInt_Request timeout_ms(::dsr_msgs2::srv::GetOutputRegisterInt_Request::_timeout_ms_type arg)
  {
    msg_.timeout_ms = std::move(arg);
    return std::move(msg_);
  }

private:
  ::dsr_msgs2::srv::GetOutputRegisterInt_Request msg_;
};

class Init_GetOutputRegisterInt_Request_address
{
public:
  Init_GetOutputRegisterInt_Request_address()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_GetOutputRegisterInt_Request_timeout_ms address(::dsr_msgs2::srv::GetOutputRegisterInt_Request::_address_type arg)
  {
    msg_.address = std::move(arg);
    return Init_GetOutputRegisterInt_Request_timeout_ms(msg_);
  }

private:
  ::dsr_msgs2::srv::GetOutputRegisterInt_Request msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::dsr_msgs2::srv::GetOutputRegisterInt_Request>()
{
  return dsr_msgs2::srv::builder::Init_GetOutputRegisterInt_Request_address();
}

}  // namespace dsr_msgs2


namespace dsr_msgs2
{

namespace srv
{

namespace builder
{

class Init_GetOutputRegisterInt_Response_value
{
public:
  explicit Init_GetOutputRegisterInt_Response_value(::dsr_msgs2::srv::GetOutputRegisterInt_Response & msg)
  : msg_(msg)
  {}
  ::dsr_msgs2::srv::GetOutputRegisterInt_Response value(::dsr_msgs2::srv::GetOutputRegisterInt_Response::_value_type arg)
  {
    msg_.value = std::move(arg);
    return std::move(msg_);
  }

private:
  ::dsr_msgs2::srv::GetOutputRegisterInt_Response msg_;
};

class Init_GetOutputRegisterInt_Response_success
{
public:
  Init_GetOutputRegisterInt_Response_success()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_GetOutputRegisterInt_Response_value success(::dsr_msgs2::srv::GetOutputRegisterInt_Response::_success_type arg)
  {
    msg_.success = std::move(arg);
    return Init_GetOutputRegisterInt_Response_value(msg_);
  }

private:
  ::dsr_msgs2::srv::GetOutputRegisterInt_Response msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::dsr_msgs2::srv::GetOutputRegisterInt_Response>()
{
  return dsr_msgs2::srv::builder::Init_GetOutputRegisterInt_Response_success();
}

}  // namespace dsr_msgs2

#endif  // DSR_MSGS2__SRV__DETAIL__GET_OUTPUT_REGISTER_INT__BUILDER_HPP_
