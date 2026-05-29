// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from dsr_msgs2:srv/FlangeSerialWrite.idl
// generated code does not contain a copyright notice

#ifndef DSR_MSGS2__SRV__DETAIL__FLANGE_SERIAL_WRITE__BUILDER_HPP_
#define DSR_MSGS2__SRV__DETAIL__FLANGE_SERIAL_WRITE__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "dsr_msgs2/srv/detail/flange_serial_write__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace dsr_msgs2
{

namespace srv
{

namespace builder
{

class Init_FlangeSerialWrite_Request_data
{
public:
  explicit Init_FlangeSerialWrite_Request_data(::dsr_msgs2::srv::FlangeSerialWrite_Request & msg)
  : msg_(msg)
  {}
  ::dsr_msgs2::srv::FlangeSerialWrite_Request data(::dsr_msgs2::srv::FlangeSerialWrite_Request::_data_type arg)
  {
    msg_.data = std::move(arg);
    return std::move(msg_);
  }

private:
  ::dsr_msgs2::srv::FlangeSerialWrite_Request msg_;
};

class Init_FlangeSerialWrite_Request_port
{
public:
  Init_FlangeSerialWrite_Request_port()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_FlangeSerialWrite_Request_data port(::dsr_msgs2::srv::FlangeSerialWrite_Request::_port_type arg)
  {
    msg_.port = std::move(arg);
    return Init_FlangeSerialWrite_Request_data(msg_);
  }

private:
  ::dsr_msgs2::srv::FlangeSerialWrite_Request msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::dsr_msgs2::srv::FlangeSerialWrite_Request>()
{
  return dsr_msgs2::srv::builder::Init_FlangeSerialWrite_Request_port();
}

}  // namespace dsr_msgs2


namespace dsr_msgs2
{

namespace srv
{

namespace builder
{

class Init_FlangeSerialWrite_Response_success
{
public:
  Init_FlangeSerialWrite_Response_success()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::dsr_msgs2::srv::FlangeSerialWrite_Response success(::dsr_msgs2::srv::FlangeSerialWrite_Response::_success_type arg)
  {
    msg_.success = std::move(arg);
    return std::move(msg_);
  }

private:
  ::dsr_msgs2::srv::FlangeSerialWrite_Response msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::dsr_msgs2::srv::FlangeSerialWrite_Response>()
{
  return dsr_msgs2::srv::builder::Init_FlangeSerialWrite_Response_success();
}

}  // namespace dsr_msgs2

#endif  // DSR_MSGS2__SRV__DETAIL__FLANGE_SERIAL_WRITE__BUILDER_HPP_
