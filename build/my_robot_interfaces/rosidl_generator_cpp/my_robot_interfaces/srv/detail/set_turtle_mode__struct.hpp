// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from my_robot_interfaces:srv/SetTurtleMode.idl
// generated code does not contain a copyright notice

#ifndef MY_ROBOT_INTERFACES__SRV__DETAIL__SET_TURTLE_MODE__STRUCT_HPP_
#define MY_ROBOT_INTERFACES__SRV__DETAIL__SET_TURTLE_MODE__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <cstdint>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__my_robot_interfaces__srv__SetTurtleMode_Request __attribute__((deprecated))
#else
# define DEPRECATED__my_robot_interfaces__srv__SetTurtleMode_Request __declspec(deprecated)
#endif

namespace my_robot_interfaces
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct SetTurtleMode_Request_
{
  using Type = SetTurtleMode_Request_<ContainerAllocator>;

  explicit SetTurtleMode_Request_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->mode_name = "";
      this->target_speed = 0.0;
    }
  }

  explicit SetTurtleMode_Request_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : mode_name(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->mode_name = "";
      this->target_speed = 0.0;
    }
  }

  // field types and members
  using _mode_name_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _mode_name_type mode_name;
  using _target_speed_type =
    double;
  _target_speed_type target_speed;

  // setters for named parameter idiom
  Type & set__mode_name(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->mode_name = _arg;
    return *this;
  }
  Type & set__target_speed(
    const double & _arg)
  {
    this->target_speed = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    my_robot_interfaces::srv::SetTurtleMode_Request_<ContainerAllocator> *;
  using ConstRawPtr =
    const my_robot_interfaces::srv::SetTurtleMode_Request_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<my_robot_interfaces::srv::SetTurtleMode_Request_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<my_robot_interfaces::srv::SetTurtleMode_Request_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      my_robot_interfaces::srv::SetTurtleMode_Request_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<my_robot_interfaces::srv::SetTurtleMode_Request_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      my_robot_interfaces::srv::SetTurtleMode_Request_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<my_robot_interfaces::srv::SetTurtleMode_Request_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<my_robot_interfaces::srv::SetTurtleMode_Request_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<my_robot_interfaces::srv::SetTurtleMode_Request_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__my_robot_interfaces__srv__SetTurtleMode_Request
    std::shared_ptr<my_robot_interfaces::srv::SetTurtleMode_Request_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__my_robot_interfaces__srv__SetTurtleMode_Request
    std::shared_ptr<my_robot_interfaces::srv::SetTurtleMode_Request_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const SetTurtleMode_Request_ & other) const
  {
    if (this->mode_name != other.mode_name) {
      return false;
    }
    if (this->target_speed != other.target_speed) {
      return false;
    }
    return true;
  }
  bool operator!=(const SetTurtleMode_Request_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct SetTurtleMode_Request_

// alias to use template instance with default allocator
using SetTurtleMode_Request =
  my_robot_interfaces::srv::SetTurtleMode_Request_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace my_robot_interfaces


#ifndef _WIN32
# define DEPRECATED__my_robot_interfaces__srv__SetTurtleMode_Response __attribute__((deprecated))
#else
# define DEPRECATED__my_robot_interfaces__srv__SetTurtleMode_Response __declspec(deprecated)
#endif

namespace my_robot_interfaces
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct SetTurtleMode_Response_
{
  using Type = SetTurtleMode_Response_<ContainerAllocator>;

  explicit SetTurtleMode_Response_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->success = false;
      this->message = "";
    }
  }

  explicit SetTurtleMode_Response_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : message(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->success = false;
      this->message = "";
    }
  }

  // field types and members
  using _success_type =
    bool;
  _success_type success;
  using _message_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _message_type message;

  // setters for named parameter idiom
  Type & set__success(
    const bool & _arg)
  {
    this->success = _arg;
    return *this;
  }
  Type & set__message(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->message = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    my_robot_interfaces::srv::SetTurtleMode_Response_<ContainerAllocator> *;
  using ConstRawPtr =
    const my_robot_interfaces::srv::SetTurtleMode_Response_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<my_robot_interfaces::srv::SetTurtleMode_Response_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<my_robot_interfaces::srv::SetTurtleMode_Response_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      my_robot_interfaces::srv::SetTurtleMode_Response_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<my_robot_interfaces::srv::SetTurtleMode_Response_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      my_robot_interfaces::srv::SetTurtleMode_Response_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<my_robot_interfaces::srv::SetTurtleMode_Response_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<my_robot_interfaces::srv::SetTurtleMode_Response_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<my_robot_interfaces::srv::SetTurtleMode_Response_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__my_robot_interfaces__srv__SetTurtleMode_Response
    std::shared_ptr<my_robot_interfaces::srv::SetTurtleMode_Response_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__my_robot_interfaces__srv__SetTurtleMode_Response
    std::shared_ptr<my_robot_interfaces::srv::SetTurtleMode_Response_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const SetTurtleMode_Response_ & other) const
  {
    if (this->success != other.success) {
      return false;
    }
    if (this->message != other.message) {
      return false;
    }
    return true;
  }
  bool operator!=(const SetTurtleMode_Response_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct SetTurtleMode_Response_

// alias to use template instance with default allocator
using SetTurtleMode_Response =
  my_robot_interfaces::srv::SetTurtleMode_Response_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace my_robot_interfaces

namespace my_robot_interfaces
{

namespace srv
{

struct SetTurtleMode
{
  using Request = my_robot_interfaces::srv::SetTurtleMode_Request;
  using Response = my_robot_interfaces::srv::SetTurtleMode_Response;
};

}  // namespace srv

}  // namespace my_robot_interfaces

#endif  // MY_ROBOT_INTERFACES__SRV__DETAIL__SET_TURTLE_MODE__STRUCT_HPP_
