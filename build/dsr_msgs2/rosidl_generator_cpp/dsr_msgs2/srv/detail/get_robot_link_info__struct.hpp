// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from dsr_msgs2:srv/GetRobotLinkInfo.idl
// generated code does not contain a copyright notice

#ifndef DSR_MSGS2__SRV__DETAIL__GET_ROBOT_LINK_INFO__STRUCT_HPP_
#define DSR_MSGS2__SRV__DETAIL__GET_ROBOT_LINK_INFO__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <cstdint>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__dsr_msgs2__srv__GetRobotLinkInfo_Request __attribute__((deprecated))
#else
# define DEPRECATED__dsr_msgs2__srv__GetRobotLinkInfo_Request __declspec(deprecated)
#endif

namespace dsr_msgs2
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct GetRobotLinkInfo_Request_
{
  using Type = GetRobotLinkInfo_Request_<ContainerAllocator>;

  explicit GetRobotLinkInfo_Request_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->structure_needs_at_least_one_member = 0;
    }
  }

  explicit GetRobotLinkInfo_Request_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_alloc;
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->structure_needs_at_least_one_member = 0;
    }
  }

  // field types and members
  using _structure_needs_at_least_one_member_type =
    uint8_t;
  _structure_needs_at_least_one_member_type structure_needs_at_least_one_member;


  // constant declarations

  // pointer types
  using RawPtr =
    dsr_msgs2::srv::GetRobotLinkInfo_Request_<ContainerAllocator> *;
  using ConstRawPtr =
    const dsr_msgs2::srv::GetRobotLinkInfo_Request_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<dsr_msgs2::srv::GetRobotLinkInfo_Request_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<dsr_msgs2::srv::GetRobotLinkInfo_Request_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      dsr_msgs2::srv::GetRobotLinkInfo_Request_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<dsr_msgs2::srv::GetRobotLinkInfo_Request_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      dsr_msgs2::srv::GetRobotLinkInfo_Request_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<dsr_msgs2::srv::GetRobotLinkInfo_Request_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<dsr_msgs2::srv::GetRobotLinkInfo_Request_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<dsr_msgs2::srv::GetRobotLinkInfo_Request_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__dsr_msgs2__srv__GetRobotLinkInfo_Request
    std::shared_ptr<dsr_msgs2::srv::GetRobotLinkInfo_Request_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__dsr_msgs2__srv__GetRobotLinkInfo_Request
    std::shared_ptr<dsr_msgs2::srv::GetRobotLinkInfo_Request_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const GetRobotLinkInfo_Request_ & other) const
  {
    if (this->structure_needs_at_least_one_member != other.structure_needs_at_least_one_member) {
      return false;
    }
    return true;
  }
  bool operator!=(const GetRobotLinkInfo_Request_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct GetRobotLinkInfo_Request_

// alias to use template instance with default allocator
using GetRobotLinkInfo_Request =
  dsr_msgs2::srv::GetRobotLinkInfo_Request_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace dsr_msgs2


#ifndef _WIN32
# define DEPRECATED__dsr_msgs2__srv__GetRobotLinkInfo_Response __attribute__((deprecated))
#else
# define DEPRECATED__dsr_msgs2__srv__GetRobotLinkInfo_Response __declspec(deprecated)
#endif

namespace dsr_msgs2
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct GetRobotLinkInfo_Response_
{
  using Type = GetRobotLinkInfo_Response_<ContainerAllocator>;

  explicit GetRobotLinkInfo_Response_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      std::fill<typename std::array<float, 6>::iterator, float>(this->d.begin(), this->d.end(), 0.0f);
      std::fill<typename std::array<float, 6>::iterator, float>(this->a.begin(), this->a.end(), 0.0f);
      std::fill<typename std::array<float, 6>::iterator, float>(this->alpha.begin(), this->alpha.end(), 0.0f);
      std::fill<typename std::array<float, 6>::iterator, float>(this->theta.begin(), this->theta.end(), 0.0f);
      std::fill<typename std::array<float, 6>::iterator, float>(this->offset.begin(), this->offset.end(), 0.0f);
      this->gradient = 0.0f;
      this->rotation = 0.0f;
      this->success = false;
    }
  }

  explicit GetRobotLinkInfo_Response_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : d(_alloc),
    a(_alloc),
    alpha(_alloc),
    theta(_alloc),
    offset(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      std::fill<typename std::array<float, 6>::iterator, float>(this->d.begin(), this->d.end(), 0.0f);
      std::fill<typename std::array<float, 6>::iterator, float>(this->a.begin(), this->a.end(), 0.0f);
      std::fill<typename std::array<float, 6>::iterator, float>(this->alpha.begin(), this->alpha.end(), 0.0f);
      std::fill<typename std::array<float, 6>::iterator, float>(this->theta.begin(), this->theta.end(), 0.0f);
      std::fill<typename std::array<float, 6>::iterator, float>(this->offset.begin(), this->offset.end(), 0.0f);
      this->gradient = 0.0f;
      this->rotation = 0.0f;
      this->success = false;
    }
  }

  // field types and members
  using _d_type =
    std::array<float, 6>;
  _d_type d;
  using _a_type =
    std::array<float, 6>;
  _a_type a;
  using _alpha_type =
    std::array<float, 6>;
  _alpha_type alpha;
  using _theta_type =
    std::array<float, 6>;
  _theta_type theta;
  using _offset_type =
    std::array<float, 6>;
  _offset_type offset;
  using _gradient_type =
    float;
  _gradient_type gradient;
  using _rotation_type =
    float;
  _rotation_type rotation;
  using _success_type =
    bool;
  _success_type success;

  // setters for named parameter idiom
  Type & set__d(
    const std::array<float, 6> & _arg)
  {
    this->d = _arg;
    return *this;
  }
  Type & set__a(
    const std::array<float, 6> & _arg)
  {
    this->a = _arg;
    return *this;
  }
  Type & set__alpha(
    const std::array<float, 6> & _arg)
  {
    this->alpha = _arg;
    return *this;
  }
  Type & set__theta(
    const std::array<float, 6> & _arg)
  {
    this->theta = _arg;
    return *this;
  }
  Type & set__offset(
    const std::array<float, 6> & _arg)
  {
    this->offset = _arg;
    return *this;
  }
  Type & set__gradient(
    const float & _arg)
  {
    this->gradient = _arg;
    return *this;
  }
  Type & set__rotation(
    const float & _arg)
  {
    this->rotation = _arg;
    return *this;
  }
  Type & set__success(
    const bool & _arg)
  {
    this->success = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    dsr_msgs2::srv::GetRobotLinkInfo_Response_<ContainerAllocator> *;
  using ConstRawPtr =
    const dsr_msgs2::srv::GetRobotLinkInfo_Response_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<dsr_msgs2::srv::GetRobotLinkInfo_Response_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<dsr_msgs2::srv::GetRobotLinkInfo_Response_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      dsr_msgs2::srv::GetRobotLinkInfo_Response_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<dsr_msgs2::srv::GetRobotLinkInfo_Response_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      dsr_msgs2::srv::GetRobotLinkInfo_Response_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<dsr_msgs2::srv::GetRobotLinkInfo_Response_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<dsr_msgs2::srv::GetRobotLinkInfo_Response_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<dsr_msgs2::srv::GetRobotLinkInfo_Response_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__dsr_msgs2__srv__GetRobotLinkInfo_Response
    std::shared_ptr<dsr_msgs2::srv::GetRobotLinkInfo_Response_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__dsr_msgs2__srv__GetRobotLinkInfo_Response
    std::shared_ptr<dsr_msgs2::srv::GetRobotLinkInfo_Response_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const GetRobotLinkInfo_Response_ & other) const
  {
    if (this->d != other.d) {
      return false;
    }
    if (this->a != other.a) {
      return false;
    }
    if (this->alpha != other.alpha) {
      return false;
    }
    if (this->theta != other.theta) {
      return false;
    }
    if (this->offset != other.offset) {
      return false;
    }
    if (this->gradient != other.gradient) {
      return false;
    }
    if (this->rotation != other.rotation) {
      return false;
    }
    if (this->success != other.success) {
      return false;
    }
    return true;
  }
  bool operator!=(const GetRobotLinkInfo_Response_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct GetRobotLinkInfo_Response_

// alias to use template instance with default allocator
using GetRobotLinkInfo_Response =
  dsr_msgs2::srv::GetRobotLinkInfo_Response_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace dsr_msgs2

namespace dsr_msgs2
{

namespace srv
{

struct GetRobotLinkInfo
{
  using Request = dsr_msgs2::srv::GetRobotLinkInfo_Request;
  using Response = dsr_msgs2::srv::GetRobotLinkInfo_Response;
};

}  // namespace srv

}  // namespace dsr_msgs2

#endif  // DSR_MSGS2__SRV__DETAIL__GET_ROBOT_LINK_INFO__STRUCT_HPP_
