// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from dsr_msgs2:srv/FlangeSerialOpen.idl
// generated code does not contain a copyright notice

#ifndef DSR_MSGS2__SRV__DETAIL__FLANGE_SERIAL_OPEN__STRUCT_HPP_
#define DSR_MSGS2__SRV__DETAIL__FLANGE_SERIAL_OPEN__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <cstdint>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__dsr_msgs2__srv__FlangeSerialOpen_Request __attribute__((deprecated))
#else
# define DEPRECATED__dsr_msgs2__srv__FlangeSerialOpen_Request __declspec(deprecated)
#endif

namespace dsr_msgs2
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct FlangeSerialOpen_Request_
{
  using Type = FlangeSerialOpen_Request_<ContainerAllocator>;

  explicit FlangeSerialOpen_Request_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->port = 0l;
      this->baudrate = 0l;
      this->bytesize = 0l;
      this->parity = 0l;
      this->stopbits = 0l;
    }
  }

  explicit FlangeSerialOpen_Request_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_alloc;
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->port = 0l;
      this->baudrate = 0l;
      this->bytesize = 0l;
      this->parity = 0l;
      this->stopbits = 0l;
    }
  }

  // field types and members
  using _port_type =
    int32_t;
  _port_type port;
  using _baudrate_type =
    int32_t;
  _baudrate_type baudrate;
  using _bytesize_type =
    int32_t;
  _bytesize_type bytesize;
  using _parity_type =
    int32_t;
  _parity_type parity;
  using _stopbits_type =
    int32_t;
  _stopbits_type stopbits;

  // setters for named parameter idiom
  Type & set__port(
    const int32_t & _arg)
  {
    this->port = _arg;
    return *this;
  }
  Type & set__baudrate(
    const int32_t & _arg)
  {
    this->baudrate = _arg;
    return *this;
  }
  Type & set__bytesize(
    const int32_t & _arg)
  {
    this->bytesize = _arg;
    return *this;
  }
  Type & set__parity(
    const int32_t & _arg)
  {
    this->parity = _arg;
    return *this;
  }
  Type & set__stopbits(
    const int32_t & _arg)
  {
    this->stopbits = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    dsr_msgs2::srv::FlangeSerialOpen_Request_<ContainerAllocator> *;
  using ConstRawPtr =
    const dsr_msgs2::srv::FlangeSerialOpen_Request_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<dsr_msgs2::srv::FlangeSerialOpen_Request_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<dsr_msgs2::srv::FlangeSerialOpen_Request_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      dsr_msgs2::srv::FlangeSerialOpen_Request_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<dsr_msgs2::srv::FlangeSerialOpen_Request_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      dsr_msgs2::srv::FlangeSerialOpen_Request_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<dsr_msgs2::srv::FlangeSerialOpen_Request_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<dsr_msgs2::srv::FlangeSerialOpen_Request_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<dsr_msgs2::srv::FlangeSerialOpen_Request_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__dsr_msgs2__srv__FlangeSerialOpen_Request
    std::shared_ptr<dsr_msgs2::srv::FlangeSerialOpen_Request_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__dsr_msgs2__srv__FlangeSerialOpen_Request
    std::shared_ptr<dsr_msgs2::srv::FlangeSerialOpen_Request_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const FlangeSerialOpen_Request_ & other) const
  {
    if (this->port != other.port) {
      return false;
    }
    if (this->baudrate != other.baudrate) {
      return false;
    }
    if (this->bytesize != other.bytesize) {
      return false;
    }
    if (this->parity != other.parity) {
      return false;
    }
    if (this->stopbits != other.stopbits) {
      return false;
    }
    return true;
  }
  bool operator!=(const FlangeSerialOpen_Request_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct FlangeSerialOpen_Request_

// alias to use template instance with default allocator
using FlangeSerialOpen_Request =
  dsr_msgs2::srv::FlangeSerialOpen_Request_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace dsr_msgs2


#ifndef _WIN32
# define DEPRECATED__dsr_msgs2__srv__FlangeSerialOpen_Response __attribute__((deprecated))
#else
# define DEPRECATED__dsr_msgs2__srv__FlangeSerialOpen_Response __declspec(deprecated)
#endif

namespace dsr_msgs2
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct FlangeSerialOpen_Response_
{
  using Type = FlangeSerialOpen_Response_<ContainerAllocator>;

  explicit FlangeSerialOpen_Response_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->success = false;
    }
  }

  explicit FlangeSerialOpen_Response_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_alloc;
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->success = false;
    }
  }

  // field types and members
  using _success_type =
    bool;
  _success_type success;

  // setters for named parameter idiom
  Type & set__success(
    const bool & _arg)
  {
    this->success = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    dsr_msgs2::srv::FlangeSerialOpen_Response_<ContainerAllocator> *;
  using ConstRawPtr =
    const dsr_msgs2::srv::FlangeSerialOpen_Response_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<dsr_msgs2::srv::FlangeSerialOpen_Response_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<dsr_msgs2::srv::FlangeSerialOpen_Response_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      dsr_msgs2::srv::FlangeSerialOpen_Response_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<dsr_msgs2::srv::FlangeSerialOpen_Response_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      dsr_msgs2::srv::FlangeSerialOpen_Response_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<dsr_msgs2::srv::FlangeSerialOpen_Response_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<dsr_msgs2::srv::FlangeSerialOpen_Response_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<dsr_msgs2::srv::FlangeSerialOpen_Response_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__dsr_msgs2__srv__FlangeSerialOpen_Response
    std::shared_ptr<dsr_msgs2::srv::FlangeSerialOpen_Response_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__dsr_msgs2__srv__FlangeSerialOpen_Response
    std::shared_ptr<dsr_msgs2::srv::FlangeSerialOpen_Response_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const FlangeSerialOpen_Response_ & other) const
  {
    if (this->success != other.success) {
      return false;
    }
    return true;
  }
  bool operator!=(const FlangeSerialOpen_Response_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct FlangeSerialOpen_Response_

// alias to use template instance with default allocator
using FlangeSerialOpen_Response =
  dsr_msgs2::srv::FlangeSerialOpen_Response_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace dsr_msgs2

namespace dsr_msgs2
{

namespace srv
{

struct FlangeSerialOpen
{
  using Request = dsr_msgs2::srv::FlangeSerialOpen_Request;
  using Response = dsr_msgs2::srv::FlangeSerialOpen_Response;
};

}  // namespace srv

}  // namespace dsr_msgs2

#endif  // DSR_MSGS2__SRV__DETAIL__FLANGE_SERIAL_OPEN__STRUCT_HPP_
