// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from dsr_msgs2:srv/FlangeSerialRead.idl
// generated code does not contain a copyright notice

#ifndef DSR_MSGS2__SRV__DETAIL__FLANGE_SERIAL_READ__BUILDER_HPP_
#define DSR_MSGS2__SRV__DETAIL__FLANGE_SERIAL_READ__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "dsr_msgs2/srv/detail/flange_serial_read__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace dsr_msgs2
{

namespace srv
{

namespace builder
{

class Init_FlangeSerialRead_Request_timeout
{
public:
  explicit Init_FlangeSerialRead_Request_timeout(::dsr_msgs2::srv::FlangeSerialRead_Request & msg)
  : msg_(msg)
  {}
  ::dsr_msgs2::srv::FlangeSerialRead_Request timeout(::dsr_msgs2::srv::FlangeSerialRead_Request::_timeout_type arg)
  {
    msg_.timeout = std::move(arg);
    return std::move(msg_);
  }

private:
  ::dsr_msgs2::srv::FlangeSerialRead_Request msg_;
};

class Init_FlangeSerialRead_Request_port
{
public:
  Init_FlangeSerialRead_Request_port()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_FlangeSerialRead_Request_timeout port(::dsr_msgs2::srv::FlangeSerialRead_Request::_port_type arg)
  {
    msg_.port = std::move(arg);
    return Init_FlangeSerialRead_Request_timeout(msg_);
  }

private:
  ::dsr_msgs2::srv::FlangeSerialRead_Request msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::dsr_msgs2::srv::FlangeSerialRead_Request>()
{
  return dsr_msgs2::srv::builder::Init_FlangeSerialRead_Request_port();
}

}  // namespace dsr_msgs2


namespace dsr_msgs2
{

namespace srv
{

namespace builder
{

class Init_FlangeSerialRead_Response_data
{
public:
  explicit Init_FlangeSerialRead_Response_data(::dsr_msgs2::srv::FlangeSerialRead_Response & msg)
  : msg_(msg)
  {}
  ::dsr_msgs2::srv::FlangeSerialRead_Response data(::dsr_msgs2::srv::FlangeSerialRead_Response::_data_type arg)
  {
    msg_.data = std::move(arg);
    return std::move(msg_);
  }

private:
  ::dsr_msgs2::srv::FlangeSerialRead_Response msg_;
};

class Init_FlangeSerialRead_Response_size
{
public:
  explicit Init_FlangeSerialRead_Response_size(::dsr_msgs2::srv::FlangeSerialRead_Response & msg)
  : msg_(msg)
  {}
  Init_FlangeSerialRead_Response_data size(::dsr_msgs2::srv::FlangeSerialRead_Response::_size_type arg)
  {
    msg_.size = std::move(arg);
    return Init_FlangeSerialRead_Response_data(msg_);
  }

private:
  ::dsr_msgs2::srv::FlangeSerialRead_Response msg_;
};

class Init_FlangeSerialRead_Response_success
{
public:
  Init_FlangeSerialRead_Response_success()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_FlangeSerialRead_Response_size success(::dsr_msgs2::srv::FlangeSerialRead_Response::_success_type arg)
  {
    msg_.success = std::move(arg);
    return Init_FlangeSerialRead_Response_size(msg_);
  }

private:
  ::dsr_msgs2::srv::FlangeSerialRead_Response msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::dsr_msgs2::srv::FlangeSerialRead_Response>()
{
  return dsr_msgs2::srv::builder::Init_FlangeSerialRead_Response_success();
}

}  // namespace dsr_msgs2

#endif  // DSR_MSGS2__SRV__DETAIL__FLANGE_SERIAL_READ__BUILDER_HPP_
