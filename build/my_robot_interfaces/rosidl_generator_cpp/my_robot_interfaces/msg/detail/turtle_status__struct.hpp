// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from my_robot_interfaces:msg/TurtleStatus.idl
// generated code does not contain a copyright notice

#ifndef MY_ROBOT_INTERFACES__MSG__DETAIL__TURTLE_STATUS__STRUCT_HPP_
#define MY_ROBOT_INTERFACES__MSG__DETAIL__TURTLE_STATUS__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <cstdint>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__my_robot_interfaces__msg__TurtleStatus __attribute__((deprecated))
#else
# define DEPRECATED__my_robot_interfaces__msg__TurtleStatus __declspec(deprecated)
#endif

namespace my_robot_interfaces
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct TurtleStatus_
{
  using Type = TurtleStatus_<ContainerAllocator>;

  explicit TurtleStatus_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->distance_to_wall = 0.0;
      this->current_state = "";
      this->is_moving = false;
    }
  }

  explicit TurtleStatus_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : current_state(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->distance_to_wall = 0.0;
      this->current_state = "";
      this->is_moving = false;
    }
  }

  // field types and members
  using _distance_to_wall_type =
    double;
  _distance_to_wall_type distance_to_wall;
  using _current_state_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _current_state_type current_state;
  using _is_moving_type =
    bool;
  _is_moving_type is_moving;

  // setters for named parameter idiom
  Type & set__distance_to_wall(
    const double & _arg)
  {
    this->distance_to_wall = _arg;
    return *this;
  }
  Type & set__current_state(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->current_state = _arg;
    return *this;
  }
  Type & set__is_moving(
    const bool & _arg)
  {
    this->is_moving = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    my_robot_interfaces::msg::TurtleStatus_<ContainerAllocator> *;
  using ConstRawPtr =
    const my_robot_interfaces::msg::TurtleStatus_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<my_robot_interfaces::msg::TurtleStatus_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<my_robot_interfaces::msg::TurtleStatus_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      my_robot_interfaces::msg::TurtleStatus_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<my_robot_interfaces::msg::TurtleStatus_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      my_robot_interfaces::msg::TurtleStatus_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<my_robot_interfaces::msg::TurtleStatus_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<my_robot_interfaces::msg::TurtleStatus_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<my_robot_interfaces::msg::TurtleStatus_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__my_robot_interfaces__msg__TurtleStatus
    std::shared_ptr<my_robot_interfaces::msg::TurtleStatus_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__my_robot_interfaces__msg__TurtleStatus
    std::shared_ptr<my_robot_interfaces::msg::TurtleStatus_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const TurtleStatus_ & other) const
  {
    if (this->distance_to_wall != other.distance_to_wall) {
      return false;
    }
    if (this->current_state != other.current_state) {
      return false;
    }
    if (this->is_moving != other.is_moving) {
      return false;
    }
    return true;
  }
  bool operator!=(const TurtleStatus_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct TurtleStatus_

// alias to use template instance with default allocator
using TurtleStatus =
  my_robot_interfaces::msg::TurtleStatus_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace my_robot_interfaces

#endif  // MY_ROBOT_INTERFACES__MSG__DETAIL__TURTLE_STATUS__STRUCT_HPP_
