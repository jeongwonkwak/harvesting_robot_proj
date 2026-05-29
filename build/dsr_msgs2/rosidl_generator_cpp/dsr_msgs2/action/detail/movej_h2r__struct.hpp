// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from dsr_msgs2:action/MovejH2r.idl
// generated code does not contain a copyright notice

#ifndef DSR_MSGS2__ACTION__DETAIL__MOVEJ_H2R__STRUCT_HPP_
#define DSR_MSGS2__ACTION__DETAIL__MOVEJ_H2R__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <cstdint>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__dsr_msgs2__action__MovejH2r_Goal __attribute__((deprecated))
#else
# define DEPRECATED__dsr_msgs2__action__MovejH2r_Goal __declspec(deprecated)
#endif

namespace dsr_msgs2
{

namespace action
{

// message struct
template<class ContainerAllocator>
struct MovejH2r_Goal_
{
  using Type = MovejH2r_Goal_<ContainerAllocator>;

  explicit MovejH2r_Goal_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      std::fill<typename std::array<double, 6>::iterator, double>(this->target_pos.begin(), this->target_pos.end(), 0.0);
      std::fill<typename std::array<double, 6>::iterator, double>(this->target_vel.begin(), this->target_vel.end(), 0.0);
      std::fill<typename std::array<double, 6>::iterator, double>(this->target_acc.begin(), this->target_acc.end(), 0.0);
    }
  }

  explicit MovejH2r_Goal_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : target_pos(_alloc),
    target_vel(_alloc),
    target_acc(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      std::fill<typename std::array<double, 6>::iterator, double>(this->target_pos.begin(), this->target_pos.end(), 0.0);
      std::fill<typename std::array<double, 6>::iterator, double>(this->target_vel.begin(), this->target_vel.end(), 0.0);
      std::fill<typename std::array<double, 6>::iterator, double>(this->target_acc.begin(), this->target_acc.end(), 0.0);
    }
  }

  // field types and members
  using _target_pos_type =
    std::array<double, 6>;
  _target_pos_type target_pos;
  using _target_vel_type =
    std::array<double, 6>;
  _target_vel_type target_vel;
  using _target_acc_type =
    std::array<double, 6>;
  _target_acc_type target_acc;

  // setters for named parameter idiom
  Type & set__target_pos(
    const std::array<double, 6> & _arg)
  {
    this->target_pos = _arg;
    return *this;
  }
  Type & set__target_vel(
    const std::array<double, 6> & _arg)
  {
    this->target_vel = _arg;
    return *this;
  }
  Type & set__target_acc(
    const std::array<double, 6> & _arg)
  {
    this->target_acc = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    dsr_msgs2::action::MovejH2r_Goal_<ContainerAllocator> *;
  using ConstRawPtr =
    const dsr_msgs2::action::MovejH2r_Goal_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<dsr_msgs2::action::MovejH2r_Goal_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<dsr_msgs2::action::MovejH2r_Goal_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      dsr_msgs2::action::MovejH2r_Goal_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<dsr_msgs2::action::MovejH2r_Goal_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      dsr_msgs2::action::MovejH2r_Goal_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<dsr_msgs2::action::MovejH2r_Goal_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<dsr_msgs2::action::MovejH2r_Goal_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<dsr_msgs2::action::MovejH2r_Goal_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__dsr_msgs2__action__MovejH2r_Goal
    std::shared_ptr<dsr_msgs2::action::MovejH2r_Goal_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__dsr_msgs2__action__MovejH2r_Goal
    std::shared_ptr<dsr_msgs2::action::MovejH2r_Goal_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const MovejH2r_Goal_ & other) const
  {
    if (this->target_pos != other.target_pos) {
      return false;
    }
    if (this->target_vel != other.target_vel) {
      return false;
    }
    if (this->target_acc != other.target_acc) {
      return false;
    }
    return true;
  }
  bool operator!=(const MovejH2r_Goal_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct MovejH2r_Goal_

// alias to use template instance with default allocator
using MovejH2r_Goal =
  dsr_msgs2::action::MovejH2r_Goal_<std::allocator<void>>;

// constant definitions

}  // namespace action

}  // namespace dsr_msgs2


#ifndef _WIN32
# define DEPRECATED__dsr_msgs2__action__MovejH2r_Result __attribute__((deprecated))
#else
# define DEPRECATED__dsr_msgs2__action__MovejH2r_Result __declspec(deprecated)
#endif

namespace dsr_msgs2
{

namespace action
{

// message struct
template<class ContainerAllocator>
struct MovejH2r_Result_
{
  using Type = MovejH2r_Result_<ContainerAllocator>;

  explicit MovejH2r_Result_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->success = false;
    }
  }

  explicit MovejH2r_Result_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
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
    dsr_msgs2::action::MovejH2r_Result_<ContainerAllocator> *;
  using ConstRawPtr =
    const dsr_msgs2::action::MovejH2r_Result_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<dsr_msgs2::action::MovejH2r_Result_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<dsr_msgs2::action::MovejH2r_Result_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      dsr_msgs2::action::MovejH2r_Result_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<dsr_msgs2::action::MovejH2r_Result_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      dsr_msgs2::action::MovejH2r_Result_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<dsr_msgs2::action::MovejH2r_Result_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<dsr_msgs2::action::MovejH2r_Result_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<dsr_msgs2::action::MovejH2r_Result_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__dsr_msgs2__action__MovejH2r_Result
    std::shared_ptr<dsr_msgs2::action::MovejH2r_Result_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__dsr_msgs2__action__MovejH2r_Result
    std::shared_ptr<dsr_msgs2::action::MovejH2r_Result_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const MovejH2r_Result_ & other) const
  {
    if (this->success != other.success) {
      return false;
    }
    return true;
  }
  bool operator!=(const MovejH2r_Result_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct MovejH2r_Result_

// alias to use template instance with default allocator
using MovejH2r_Result =
  dsr_msgs2::action::MovejH2r_Result_<std::allocator<void>>;

// constant definitions

}  // namespace action

}  // namespace dsr_msgs2


#ifndef _WIN32
# define DEPRECATED__dsr_msgs2__action__MovejH2r_Feedback __attribute__((deprecated))
#else
# define DEPRECATED__dsr_msgs2__action__MovejH2r_Feedback __declspec(deprecated)
#endif

namespace dsr_msgs2
{

namespace action
{

// message struct
template<class ContainerAllocator>
struct MovejH2r_Feedback_
{
  using Type = MovejH2r_Feedback_<ContainerAllocator>;

  explicit MovejH2r_Feedback_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      std::fill<typename std::array<double, 6>::iterator, double>(this->pos.begin(), this->pos.end(), 0.0);
    }
  }

  explicit MovejH2r_Feedback_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : pos(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      std::fill<typename std::array<double, 6>::iterator, double>(this->pos.begin(), this->pos.end(), 0.0);
    }
  }

  // field types and members
  using _pos_type =
    std::array<double, 6>;
  _pos_type pos;

  // setters for named parameter idiom
  Type & set__pos(
    const std::array<double, 6> & _arg)
  {
    this->pos = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    dsr_msgs2::action::MovejH2r_Feedback_<ContainerAllocator> *;
  using ConstRawPtr =
    const dsr_msgs2::action::MovejH2r_Feedback_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<dsr_msgs2::action::MovejH2r_Feedback_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<dsr_msgs2::action::MovejH2r_Feedback_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      dsr_msgs2::action::MovejH2r_Feedback_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<dsr_msgs2::action::MovejH2r_Feedback_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      dsr_msgs2::action::MovejH2r_Feedback_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<dsr_msgs2::action::MovejH2r_Feedback_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<dsr_msgs2::action::MovejH2r_Feedback_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<dsr_msgs2::action::MovejH2r_Feedback_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__dsr_msgs2__action__MovejH2r_Feedback
    std::shared_ptr<dsr_msgs2::action::MovejH2r_Feedback_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__dsr_msgs2__action__MovejH2r_Feedback
    std::shared_ptr<dsr_msgs2::action::MovejH2r_Feedback_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const MovejH2r_Feedback_ & other) const
  {
    if (this->pos != other.pos) {
      return false;
    }
    return true;
  }
  bool operator!=(const MovejH2r_Feedback_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct MovejH2r_Feedback_

// alias to use template instance with default allocator
using MovejH2r_Feedback =
  dsr_msgs2::action::MovejH2r_Feedback_<std::allocator<void>>;

// constant definitions

}  // namespace action

}  // namespace dsr_msgs2


// Include directives for member types
// Member 'goal_id'
#include "unique_identifier_msgs/msg/detail/uuid__struct.hpp"
// Member 'goal'
#include "dsr_msgs2/action/detail/movej_h2r__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__dsr_msgs2__action__MovejH2r_SendGoal_Request __attribute__((deprecated))
#else
# define DEPRECATED__dsr_msgs2__action__MovejH2r_SendGoal_Request __declspec(deprecated)
#endif

namespace dsr_msgs2
{

namespace action
{

// message struct
template<class ContainerAllocator>
struct MovejH2r_SendGoal_Request_
{
  using Type = MovejH2r_SendGoal_Request_<ContainerAllocator>;

  explicit MovejH2r_SendGoal_Request_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : goal_id(_init),
    goal(_init)
  {
    (void)_init;
  }

  explicit MovejH2r_SendGoal_Request_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : goal_id(_alloc, _init),
    goal(_alloc, _init)
  {
    (void)_init;
  }

  // field types and members
  using _goal_id_type =
    unique_identifier_msgs::msg::UUID_<ContainerAllocator>;
  _goal_id_type goal_id;
  using _goal_type =
    dsr_msgs2::action::MovejH2r_Goal_<ContainerAllocator>;
  _goal_type goal;

  // setters for named parameter idiom
  Type & set__goal_id(
    const unique_identifier_msgs::msg::UUID_<ContainerAllocator> & _arg)
  {
    this->goal_id = _arg;
    return *this;
  }
  Type & set__goal(
    const dsr_msgs2::action::MovejH2r_Goal_<ContainerAllocator> & _arg)
  {
    this->goal = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    dsr_msgs2::action::MovejH2r_SendGoal_Request_<ContainerAllocator> *;
  using ConstRawPtr =
    const dsr_msgs2::action::MovejH2r_SendGoal_Request_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<dsr_msgs2::action::MovejH2r_SendGoal_Request_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<dsr_msgs2::action::MovejH2r_SendGoal_Request_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      dsr_msgs2::action::MovejH2r_SendGoal_Request_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<dsr_msgs2::action::MovejH2r_SendGoal_Request_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      dsr_msgs2::action::MovejH2r_SendGoal_Request_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<dsr_msgs2::action::MovejH2r_SendGoal_Request_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<dsr_msgs2::action::MovejH2r_SendGoal_Request_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<dsr_msgs2::action::MovejH2r_SendGoal_Request_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__dsr_msgs2__action__MovejH2r_SendGoal_Request
    std::shared_ptr<dsr_msgs2::action::MovejH2r_SendGoal_Request_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__dsr_msgs2__action__MovejH2r_SendGoal_Request
    std::shared_ptr<dsr_msgs2::action::MovejH2r_SendGoal_Request_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const MovejH2r_SendGoal_Request_ & other) const
  {
    if (this->goal_id != other.goal_id) {
      return false;
    }
    if (this->goal != other.goal) {
      return false;
    }
    return true;
  }
  bool operator!=(const MovejH2r_SendGoal_Request_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct MovejH2r_SendGoal_Request_

// alias to use template instance with default allocator
using MovejH2r_SendGoal_Request =
  dsr_msgs2::action::MovejH2r_SendGoal_Request_<std::allocator<void>>;

// constant definitions

}  // namespace action

}  // namespace dsr_msgs2


// Include directives for member types
// Member 'stamp'
#include "builtin_interfaces/msg/detail/time__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__dsr_msgs2__action__MovejH2r_SendGoal_Response __attribute__((deprecated))
#else
# define DEPRECATED__dsr_msgs2__action__MovejH2r_SendGoal_Response __declspec(deprecated)
#endif

namespace dsr_msgs2
{

namespace action
{

// message struct
template<class ContainerAllocator>
struct MovejH2r_SendGoal_Response_
{
  using Type = MovejH2r_SendGoal_Response_<ContainerAllocator>;

  explicit MovejH2r_SendGoal_Response_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : stamp(_init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->accepted = false;
    }
  }

  explicit MovejH2r_SendGoal_Response_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : stamp(_alloc, _init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->accepted = false;
    }
  }

  // field types and members
  using _accepted_type =
    bool;
  _accepted_type accepted;
  using _stamp_type =
    builtin_interfaces::msg::Time_<ContainerAllocator>;
  _stamp_type stamp;

  // setters for named parameter idiom
  Type & set__accepted(
    const bool & _arg)
  {
    this->accepted = _arg;
    return *this;
  }
  Type & set__stamp(
    const builtin_interfaces::msg::Time_<ContainerAllocator> & _arg)
  {
    this->stamp = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    dsr_msgs2::action::MovejH2r_SendGoal_Response_<ContainerAllocator> *;
  using ConstRawPtr =
    const dsr_msgs2::action::MovejH2r_SendGoal_Response_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<dsr_msgs2::action::MovejH2r_SendGoal_Response_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<dsr_msgs2::action::MovejH2r_SendGoal_Response_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      dsr_msgs2::action::MovejH2r_SendGoal_Response_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<dsr_msgs2::action::MovejH2r_SendGoal_Response_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      dsr_msgs2::action::MovejH2r_SendGoal_Response_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<dsr_msgs2::action::MovejH2r_SendGoal_Response_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<dsr_msgs2::action::MovejH2r_SendGoal_Response_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<dsr_msgs2::action::MovejH2r_SendGoal_Response_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__dsr_msgs2__action__MovejH2r_SendGoal_Response
    std::shared_ptr<dsr_msgs2::action::MovejH2r_SendGoal_Response_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__dsr_msgs2__action__MovejH2r_SendGoal_Response
    std::shared_ptr<dsr_msgs2::action::MovejH2r_SendGoal_Response_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const MovejH2r_SendGoal_Response_ & other) const
  {
    if (this->accepted != other.accepted) {
      return false;
    }
    if (this->stamp != other.stamp) {
      return false;
    }
    return true;
  }
  bool operator!=(const MovejH2r_SendGoal_Response_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct MovejH2r_SendGoal_Response_

// alias to use template instance with default allocator
using MovejH2r_SendGoal_Response =
  dsr_msgs2::action::MovejH2r_SendGoal_Response_<std::allocator<void>>;

// constant definitions

}  // namespace action

}  // namespace dsr_msgs2

namespace dsr_msgs2
{

namespace action
{

struct MovejH2r_SendGoal
{
  using Request = dsr_msgs2::action::MovejH2r_SendGoal_Request;
  using Response = dsr_msgs2::action::MovejH2r_SendGoal_Response;
};

}  // namespace action

}  // namespace dsr_msgs2


// Include directives for member types
// Member 'goal_id'
// already included above
// #include "unique_identifier_msgs/msg/detail/uuid__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__dsr_msgs2__action__MovejH2r_GetResult_Request __attribute__((deprecated))
#else
# define DEPRECATED__dsr_msgs2__action__MovejH2r_GetResult_Request __declspec(deprecated)
#endif

namespace dsr_msgs2
{

namespace action
{

// message struct
template<class ContainerAllocator>
struct MovejH2r_GetResult_Request_
{
  using Type = MovejH2r_GetResult_Request_<ContainerAllocator>;

  explicit MovejH2r_GetResult_Request_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : goal_id(_init)
  {
    (void)_init;
  }

  explicit MovejH2r_GetResult_Request_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : goal_id(_alloc, _init)
  {
    (void)_init;
  }

  // field types and members
  using _goal_id_type =
    unique_identifier_msgs::msg::UUID_<ContainerAllocator>;
  _goal_id_type goal_id;

  // setters for named parameter idiom
  Type & set__goal_id(
    const unique_identifier_msgs::msg::UUID_<ContainerAllocator> & _arg)
  {
    this->goal_id = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    dsr_msgs2::action::MovejH2r_GetResult_Request_<ContainerAllocator> *;
  using ConstRawPtr =
    const dsr_msgs2::action::MovejH2r_GetResult_Request_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<dsr_msgs2::action::MovejH2r_GetResult_Request_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<dsr_msgs2::action::MovejH2r_GetResult_Request_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      dsr_msgs2::action::MovejH2r_GetResult_Request_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<dsr_msgs2::action::MovejH2r_GetResult_Request_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      dsr_msgs2::action::MovejH2r_GetResult_Request_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<dsr_msgs2::action::MovejH2r_GetResult_Request_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<dsr_msgs2::action::MovejH2r_GetResult_Request_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<dsr_msgs2::action::MovejH2r_GetResult_Request_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__dsr_msgs2__action__MovejH2r_GetResult_Request
    std::shared_ptr<dsr_msgs2::action::MovejH2r_GetResult_Request_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__dsr_msgs2__action__MovejH2r_GetResult_Request
    std::shared_ptr<dsr_msgs2::action::MovejH2r_GetResult_Request_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const MovejH2r_GetResult_Request_ & other) const
  {
    if (this->goal_id != other.goal_id) {
      return false;
    }
    return true;
  }
  bool operator!=(const MovejH2r_GetResult_Request_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct MovejH2r_GetResult_Request_

// alias to use template instance with default allocator
using MovejH2r_GetResult_Request =
  dsr_msgs2::action::MovejH2r_GetResult_Request_<std::allocator<void>>;

// constant definitions

}  // namespace action

}  // namespace dsr_msgs2


// Include directives for member types
// Member 'result'
// already included above
// #include "dsr_msgs2/action/detail/movej_h2r__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__dsr_msgs2__action__MovejH2r_GetResult_Response __attribute__((deprecated))
#else
# define DEPRECATED__dsr_msgs2__action__MovejH2r_GetResult_Response __declspec(deprecated)
#endif

namespace dsr_msgs2
{

namespace action
{

// message struct
template<class ContainerAllocator>
struct MovejH2r_GetResult_Response_
{
  using Type = MovejH2r_GetResult_Response_<ContainerAllocator>;

  explicit MovejH2r_GetResult_Response_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : result(_init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->status = 0;
    }
  }

  explicit MovejH2r_GetResult_Response_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : result(_alloc, _init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->status = 0;
    }
  }

  // field types and members
  using _status_type =
    int8_t;
  _status_type status;
  using _result_type =
    dsr_msgs2::action::MovejH2r_Result_<ContainerAllocator>;
  _result_type result;

  // setters for named parameter idiom
  Type & set__status(
    const int8_t & _arg)
  {
    this->status = _arg;
    return *this;
  }
  Type & set__result(
    const dsr_msgs2::action::MovejH2r_Result_<ContainerAllocator> & _arg)
  {
    this->result = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    dsr_msgs2::action::MovejH2r_GetResult_Response_<ContainerAllocator> *;
  using ConstRawPtr =
    const dsr_msgs2::action::MovejH2r_GetResult_Response_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<dsr_msgs2::action::MovejH2r_GetResult_Response_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<dsr_msgs2::action::MovejH2r_GetResult_Response_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      dsr_msgs2::action::MovejH2r_GetResult_Response_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<dsr_msgs2::action::MovejH2r_GetResult_Response_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      dsr_msgs2::action::MovejH2r_GetResult_Response_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<dsr_msgs2::action::MovejH2r_GetResult_Response_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<dsr_msgs2::action::MovejH2r_GetResult_Response_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<dsr_msgs2::action::MovejH2r_GetResult_Response_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__dsr_msgs2__action__MovejH2r_GetResult_Response
    std::shared_ptr<dsr_msgs2::action::MovejH2r_GetResult_Response_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__dsr_msgs2__action__MovejH2r_GetResult_Response
    std::shared_ptr<dsr_msgs2::action::MovejH2r_GetResult_Response_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const MovejH2r_GetResult_Response_ & other) const
  {
    if (this->status != other.status) {
      return false;
    }
    if (this->result != other.result) {
      return false;
    }
    return true;
  }
  bool operator!=(const MovejH2r_GetResult_Response_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct MovejH2r_GetResult_Response_

// alias to use template instance with default allocator
using MovejH2r_GetResult_Response =
  dsr_msgs2::action::MovejH2r_GetResult_Response_<std::allocator<void>>;

// constant definitions

}  // namespace action

}  // namespace dsr_msgs2

namespace dsr_msgs2
{

namespace action
{

struct MovejH2r_GetResult
{
  using Request = dsr_msgs2::action::MovejH2r_GetResult_Request;
  using Response = dsr_msgs2::action::MovejH2r_GetResult_Response;
};

}  // namespace action

}  // namespace dsr_msgs2


// Include directives for member types
// Member 'goal_id'
// already included above
// #include "unique_identifier_msgs/msg/detail/uuid__struct.hpp"
// Member 'feedback'
// already included above
// #include "dsr_msgs2/action/detail/movej_h2r__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__dsr_msgs2__action__MovejH2r_FeedbackMessage __attribute__((deprecated))
#else
# define DEPRECATED__dsr_msgs2__action__MovejH2r_FeedbackMessage __declspec(deprecated)
#endif

namespace dsr_msgs2
{

namespace action
{

// message struct
template<class ContainerAllocator>
struct MovejH2r_FeedbackMessage_
{
  using Type = MovejH2r_FeedbackMessage_<ContainerAllocator>;

  explicit MovejH2r_FeedbackMessage_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : goal_id(_init),
    feedback(_init)
  {
    (void)_init;
  }

  explicit MovejH2r_FeedbackMessage_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : goal_id(_alloc, _init),
    feedback(_alloc, _init)
  {
    (void)_init;
  }

  // field types and members
  using _goal_id_type =
    unique_identifier_msgs::msg::UUID_<ContainerAllocator>;
  _goal_id_type goal_id;
  using _feedback_type =
    dsr_msgs2::action::MovejH2r_Feedback_<ContainerAllocator>;
  _feedback_type feedback;

  // setters for named parameter idiom
  Type & set__goal_id(
    const unique_identifier_msgs::msg::UUID_<ContainerAllocator> & _arg)
  {
    this->goal_id = _arg;
    return *this;
  }
  Type & set__feedback(
    const dsr_msgs2::action::MovejH2r_Feedback_<ContainerAllocator> & _arg)
  {
    this->feedback = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    dsr_msgs2::action::MovejH2r_FeedbackMessage_<ContainerAllocator> *;
  using ConstRawPtr =
    const dsr_msgs2::action::MovejH2r_FeedbackMessage_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<dsr_msgs2::action::MovejH2r_FeedbackMessage_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<dsr_msgs2::action::MovejH2r_FeedbackMessage_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      dsr_msgs2::action::MovejH2r_FeedbackMessage_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<dsr_msgs2::action::MovejH2r_FeedbackMessage_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      dsr_msgs2::action::MovejH2r_FeedbackMessage_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<dsr_msgs2::action::MovejH2r_FeedbackMessage_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<dsr_msgs2::action::MovejH2r_FeedbackMessage_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<dsr_msgs2::action::MovejH2r_FeedbackMessage_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__dsr_msgs2__action__MovejH2r_FeedbackMessage
    std::shared_ptr<dsr_msgs2::action::MovejH2r_FeedbackMessage_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__dsr_msgs2__action__MovejH2r_FeedbackMessage
    std::shared_ptr<dsr_msgs2::action::MovejH2r_FeedbackMessage_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const MovejH2r_FeedbackMessage_ & other) const
  {
    if (this->goal_id != other.goal_id) {
      return false;
    }
    if (this->feedback != other.feedback) {
      return false;
    }
    return true;
  }
  bool operator!=(const MovejH2r_FeedbackMessage_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct MovejH2r_FeedbackMessage_

// alias to use template instance with default allocator
using MovejH2r_FeedbackMessage =
  dsr_msgs2::action::MovejH2r_FeedbackMessage_<std::allocator<void>>;

// constant definitions

}  // namespace action

}  // namespace dsr_msgs2

#include "action_msgs/srv/cancel_goal.hpp"
#include "action_msgs/msg/goal_info.hpp"
#include "action_msgs/msg/goal_status_array.hpp"

namespace dsr_msgs2
{

namespace action
{

struct MovejH2r
{
  /// The goal message defined in the action definition.
  using Goal = dsr_msgs2::action::MovejH2r_Goal;
  /// The result message defined in the action definition.
  using Result = dsr_msgs2::action::MovejH2r_Result;
  /// The feedback message defined in the action definition.
  using Feedback = dsr_msgs2::action::MovejH2r_Feedback;

  struct Impl
  {
    /// The send_goal service using a wrapped version of the goal message as a request.
    using SendGoalService = dsr_msgs2::action::MovejH2r_SendGoal;
    /// The get_result service using a wrapped version of the result message as a response.
    using GetResultService = dsr_msgs2::action::MovejH2r_GetResult;
    /// The feedback message with generic fields which wraps the feedback message.
    using FeedbackMessage = dsr_msgs2::action::MovejH2r_FeedbackMessage;

    /// The generic service to cancel a goal.
    using CancelGoalService = action_msgs::srv::CancelGoal;
    /// The generic message for the status of a goal.
    using GoalStatusMessage = action_msgs::msg::GoalStatusArray;
  };
};

typedef struct MovejH2r MovejH2r;

}  // namespace action

}  // namespace dsr_msgs2

#endif  // DSR_MSGS2__ACTION__DETAIL__MOVEJ_H2R__STRUCT_HPP_
