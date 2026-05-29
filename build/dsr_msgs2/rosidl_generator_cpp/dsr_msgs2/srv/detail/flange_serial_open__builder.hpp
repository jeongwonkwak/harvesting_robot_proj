// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from dsr_msgs2:srv/FlangeSerialOpen.idl
// generated code does not contain a copyright notice

#ifndef DSR_MSGS2__SRV__DETAIL__FLANGE_SERIAL_OPEN__BUILDER_HPP_
#define DSR_MSGS2__SRV__DETAIL__FLANGE_SERIAL_OPEN__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "dsr_msgs2/srv/detail/flange_serial_open__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace dsr_msgs2
{

namespace srv
{

namespace builder
{

class Init_FlangeSerialOpen_Request_stopbits
{
public:
  explicit Init_FlangeSerialOpen_Request_stopbits(::dsr_msgs2::srv::FlangeSerialOpen_Request & msg)
  : msg_(msg)
  {}
  ::dsr_msgs2::srv::FlangeSerialOpen_Request stopbits(::dsr_msgs2::srv::FlangeSerialOpen_Request::_stopbits_type arg)
  {
    msg_.stopbits = std::move(arg);
    return std::move(msg_);
  }

private:
  ::dsr_msgs2::srv::FlangeSerialOpen_Request msg_;
};

class Init_FlangeSerialOpen_Request_parity
{
public:
  explicit Init_FlangeSerialOpen_Request_parity(::dsr_msgs2::srv::FlangeSerialOpen_Request & msg)
  : msg_(msg)
  {}
  Init_FlangeSerialOpen_Request_stopbits parity(::dsr_msgs2::srv::FlangeSerialOpen_Request::_parity_type arg)
  {
    msg_.parity = std::move(arg);
    return Init_FlangeSerialOpen_Request_stopbits(msg_);
  }

private:
  ::dsr_msgs2::srv::FlangeSerialOpen_Request msg_;
};

class Init_FlangeSerialOpen_Request_bytesize
{
public:
  explicit Init_FlangeSerialOpen_Request_bytesize(::dsr_msgs2::srv::FlangeSerialOpen_Request & msg)
  : msg_(msg)
  {}
  Init_FlangeSerialOpen_Request_parity bytesize(::dsr_msgs2::srv::FlangeSerialOpen_Request::_bytesize_type arg)
  {
    msg_.bytesize = std::move(arg);
    return Init_FlangeSerialOpen_Request_parity(msg_);
  }

private:
  ::dsr_msgs2::srv::FlangeSerialOpen_Request msg_;
};

class Init_FlangeSerialOpen_Request_baudrate
{
public:
  explicit Init_FlangeSerialOpen_Request_baudrate(::dsr_msgs2::srv::FlangeSerialOpen_Request & msg)
  : msg_(msg)
  {}
  Init_FlangeSerialOpen_Request_bytesize baudrate(::dsr_msgs2::srv::FlangeSerialOpen_Request::_baudrate_type arg)
  {
    msg_.baudrate = std::move(arg);
    return Init_FlangeSerialOpen_Request_bytesize(msg_);
  }

private:
  ::dsr_msgs2::srv::FlangeSerialOpen_Request msg_;
};

class Init_FlangeSerialOpen_Request_port
{
public:
  Init_FlangeSerialOpen_Request_port()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_FlangeSerialOpen_Request_baudrate port(::dsr_msgs2::srv::FlangeSerialOpen_Request::_port_type arg)
  {
    msg_.port = std::move(arg);
    return Init_FlangeSerialOpen_Request_baudrate(msg_);
  }

private:
  ::dsr_msgs2::srv::FlangeSerialOpen_Request msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::dsr_msgs2::srv::FlangeSerialOpen_Request>()
{
  return dsr_msgs2::srv::builder::Init_FlangeSerialOpen_Request_port();
}

}  // namespace dsr_msgs2


namespace dsr_msgs2
{

namespace srv
{

namespace builder
{

class Init_FlangeSerialOpen_Response_success
{
public:
  Init_FlangeSerialOpen_Response_success()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::dsr_msgs2::srv::FlangeSerialOpen_Response success(::dsr_msgs2::srv::FlangeSerialOpen_Response::_success_type arg)
  {
    msg_.success = std::move(arg);
    return std::move(msg_);
  }

private:
  ::dsr_msgs2::srv::FlangeSerialOpen_Response msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::dsr_msgs2::srv::FlangeSerialOpen_Response>()
{
  return dsr_msgs2::srv::builder::Init_FlangeSerialOpen_Response_success();
}

}  // namespace dsr_msgs2

#endif  // DSR_MSGS2__SRV__DETAIL__FLANGE_SERIAL_OPEN__BUILDER_HPP_
