// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from dsr_msgs2:srv/FlangeSerialRead.idl
// generated code does not contain a copyright notice

#ifndef DSR_MSGS2__SRV__DETAIL__FLANGE_SERIAL_READ__STRUCT_HPP_
#define DSR_MSGS2__SRV__DETAIL__FLANGE_SERIAL_READ__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <cstdint>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__dsr_msgs2__srv__FlangeSerialRead_Request __attribute__((deprecated))
#else
# define DEPRECATED__dsr_msgs2__srv__FlangeSerialRead_Request __declspec(deprecated)
#endif

namespace dsr_msgs2
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct FlangeSerialRead_Request_
{
  using Type = FlangeSerialRead_Request_<ContainerAllocator>;

  explicit FlangeSerialRead_Request_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->port = 0l;
      this->timeout = 0.0f;
    }
  }

  explicit FlangeSerialRead_Request_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_alloc;
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->port = 0l;
      this->timeout = 0.0f;
    }
  }

  // field types and members
  using _port_type =
    int32_t;
  _port_type port;
  using _timeout_type =
    float;
  _timeout_type timeout;

  // setters for named parameter idiom
  Type & set__port(
    const int32_t & _arg)
  {
    this->port = _arg;
    return *this;
  }
  Type & set__timeout(
    const float & _arg)
  {
    this->timeout = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    dsr_msgs2::srv::FlangeSerialRead_Request_<ContainerAllocator> *;
  using ConstRawPtr =
    const dsr_msgs2::srv::FlangeSerialRead_Request_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<dsr_msgs2::srv::FlangeSerialRead_Request_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<dsr_msgs2::srv::FlangeSerialRead_Request_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      dsr_msgs2::srv::FlangeSerialRead_Request_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<dsr_msgs2::srv::FlangeSerialRead_Request_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      dsr_msgs2::srv::FlangeSerialRead_Request_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<dsr_msgs2::srv::FlangeSerialRead_Request_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<dsr_msgs2::srv::FlangeSerialRead_Request_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<dsr_msgs2::srv::FlangeSerialRead_Request_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__dsr_msgs2__srv__FlangeSerialRead_Request
    std::shared_ptr<dsr_msgs2::srv::FlangeSerialRead_Request_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__dsr_msgs2__srv__FlangeSerialRead_Request
    std::shared_ptr<dsr_msgs2::srv::FlangeSerialRead_Request_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const FlangeSerialRead_Request_ & other) const
  {
    if (this->port != other.port) {
      return false;
    }
    if (this->timeout != other.timeout) {
      return false;
    }
    return true;
  }
  bool operator!=(const FlangeSerialRead_Request_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct FlangeSerialRead_Request_

// alias to use template instance with default allocator
using FlangeSerialRead_Request =
  dsr_msgs2::srv::FlangeSerialRead_Request_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace dsr_msgs2


#ifndef _WIN32
# define DEPRECATED__dsr_msgs2__srv__FlangeSerialRead_Response __attribute__((deprecated))
#else
# define DEPRECATED__dsr_msgs2__srv__FlangeSerialRead_Response __declspec(deprecated)
#endif

namespace dsr_msgs2
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct FlangeSerialRead_Response_
{
  using Type = FlangeSerialRead_Response_<ContainerAllocator>;

  explicit FlangeSerialRead_Response_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->success = false;
      this->size = 0l;
    }
  }

  explicit FlangeSerialRead_Response_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_alloc;
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->success = false;
      this->size = 0l;
    }
  }

  // field types and members
  using _success_type =
    bool;
  _success_type success;
  using _size_type =
    int32_t;
  _size_type size;
  using _data_type =
    std::vector<uint8_t, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<uint8_t>>;
  _data_type data;

  // setters for named parameter idiom
  Type & set__success(
    const bool & _arg)
  {
    this->success = _arg;
    return *this;
  }
  Type & set__size(
    const int32_t & _arg)
  {
    this->size = _arg;
    return *this;
  }
  Type & set__data(
    const std::vector<uint8_t, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<uint8_t>> & _arg)
  {
    this->data = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    dsr_msgs2::srv::FlangeSerialRead_Response_<ContainerAllocator> *;
  using ConstRawPtr =
    const dsr_msgs2::srv::FlangeSerialRead_Response_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<dsr_msgs2::srv::FlangeSerialRead_Response_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<dsr_msgs2::srv::FlangeSerialRead_Response_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      dsr_msgs2::srv::FlangeSerialRead_Response_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<dsr_msgs2::srv::FlangeSerialRead_Response_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      dsr_msgs2::srv::FlangeSerialRead_Response_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<dsr_msgs2::srv::FlangeSerialRead_Response_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<dsr_msgs2::srv::FlangeSerialRead_Response_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<dsr_msgs2::srv::FlangeSerialRead_Response_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__dsr_msgs2__srv__FlangeSerialRead_Response
    std::shared_ptr<dsr_msgs2::srv::FlangeSerialRead_Response_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__dsr_msgs2__srv__FlangeSerialRead_Response
    std::shared_ptr<dsr_msgs2::srv::FlangeSerialRead_Response_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const FlangeSerialRead_Response_ & other) const
  {
    if (this->success != other.success) {
      return false;
    }
    if (this->size != other.size) {
      return false;
    }
    if (this->data != other.data) {
      return false;
    }
    return true;
  }
  bool operator!=(const FlangeSerialRead_Response_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct FlangeSerialRead_Response_

// alias to use template instance with default allocator
using FlangeSerialRead_Response =
  dsr_msgs2::srv::FlangeSerialRead_Response_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace dsr_msgs2

namespace dsr_msgs2
{

namespace srv
{

struct FlangeSerialRead
{
  using Request = dsr_msgs2::srv::FlangeSerialRead_Request;
  using Response = dsr_msgs2::srv::FlangeSerialRead_Response;
};

}  // namespace srv

}  // namespace dsr_msgs2

#endif  // DSR_MSGS2__SRV__DETAIL__FLANGE_SERIAL_READ__STRUCT_HPP_
