// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from dsr_msgs2:action/MovejH2r.idl
// generated code does not contain a copyright notice

#ifndef DSR_MSGS2__ACTION__DETAIL__MOVEJ_H2R__BUILDER_HPP_
#define DSR_MSGS2__ACTION__DETAIL__MOVEJ_H2R__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "dsr_msgs2/action/detail/movej_h2r__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace dsr_msgs2
{

namespace action
{

namespace builder
{

class Init_MovejH2r_Goal_target_acc
{
public:
  explicit Init_MovejH2r_Goal_target_acc(::dsr_msgs2::action::MovejH2r_Goal & msg)
  : msg_(msg)
  {}
  ::dsr_msgs2::action::MovejH2r_Goal target_acc(::dsr_msgs2::action::MovejH2r_Goal::_target_acc_type arg)
  {
    msg_.target_acc = std::move(arg);
    return std::move(msg_);
  }

private:
  ::dsr_msgs2::action::MovejH2r_Goal msg_;
};

class Init_MovejH2r_Goal_target_vel
{
public:
  explicit Init_MovejH2r_Goal_target_vel(::dsr_msgs2::action::MovejH2r_Goal & msg)
  : msg_(msg)
  {}
  Init_MovejH2r_Goal_target_acc target_vel(::dsr_msgs2::action::MovejH2r_Goal::_target_vel_type arg)
  {
    msg_.target_vel = std::move(arg);
    return Init_MovejH2r_Goal_target_acc(msg_);
  }

private:
  ::dsr_msgs2::action::MovejH2r_Goal msg_;
};

class Init_MovejH2r_Goal_target_pos
{
public:
  Init_MovejH2r_Goal_target_pos()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_MovejH2r_Goal_target_vel target_pos(::dsr_msgs2::action::MovejH2r_Goal::_target_pos_type arg)
  {
    msg_.target_pos = std::move(arg);
    return Init_MovejH2r_Goal_target_vel(msg_);
  }

private:
  ::dsr_msgs2::action::MovejH2r_Goal msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::dsr_msgs2::action::MovejH2r_Goal>()
{
  return dsr_msgs2::action::builder::Init_MovejH2r_Goal_target_pos();
}

}  // namespace dsr_msgs2


namespace dsr_msgs2
{

namespace action
{

namespace builder
{

class Init_MovejH2r_Result_success
{
public:
  Init_MovejH2r_Result_success()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::dsr_msgs2::action::MovejH2r_Result success(::dsr_msgs2::action::MovejH2r_Result::_success_type arg)
  {
    msg_.success = std::move(arg);
    return std::move(msg_);
  }

private:
  ::dsr_msgs2::action::MovejH2r_Result msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::dsr_msgs2::action::MovejH2r_Result>()
{
  return dsr_msgs2::action::builder::Init_MovejH2r_Result_success();
}

}  // namespace dsr_msgs2


namespace dsr_msgs2
{

namespace action
{

namespace builder
{

class Init_MovejH2r_Feedback_pos
{
public:
  Init_MovejH2r_Feedback_pos()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::dsr_msgs2::action::MovejH2r_Feedback pos(::dsr_msgs2::action::MovejH2r_Feedback::_pos_type arg)
  {
    msg_.pos = std::move(arg);
    return std::move(msg_);
  }

private:
  ::dsr_msgs2::action::MovejH2r_Feedback msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::dsr_msgs2::action::MovejH2r_Feedback>()
{
  return dsr_msgs2::action::builder::Init_MovejH2r_Feedback_pos();
}

}  // namespace dsr_msgs2


namespace dsr_msgs2
{

namespace action
{

namespace builder
{

class Init_MovejH2r_SendGoal_Request_goal
{
public:
  explicit Init_MovejH2r_SendGoal_Request_goal(::dsr_msgs2::action::MovejH2r_SendGoal_Request & msg)
  : msg_(msg)
  {}
  ::dsr_msgs2::action::MovejH2r_SendGoal_Request goal(::dsr_msgs2::action::MovejH2r_SendGoal_Request::_goal_type arg)
  {
    msg_.goal = std::move(arg);
    return std::move(msg_);
  }

private:
  ::dsr_msgs2::action::MovejH2r_SendGoal_Request msg_;
};

class Init_MovejH2r_SendGoal_Request_goal_id
{
public:
  Init_MovejH2r_SendGoal_Request_goal_id()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_MovejH2r_SendGoal_Request_goal goal_id(::dsr_msgs2::action::MovejH2r_SendGoal_Request::_goal_id_type arg)
  {
    msg_.goal_id = std::move(arg);
    return Init_MovejH2r_SendGoal_Request_goal(msg_);
  }

private:
  ::dsr_msgs2::action::MovejH2r_SendGoal_Request msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::dsr_msgs2::action::MovejH2r_SendGoal_Request>()
{
  return dsr_msgs2::action::builder::Init_MovejH2r_SendGoal_Request_goal_id();
}

}  // namespace dsr_msgs2


namespace dsr_msgs2
{

namespace action
{

namespace builder
{

class Init_MovejH2r_SendGoal_Response_stamp
{
public:
  explicit Init_MovejH2r_SendGoal_Response_stamp(::dsr_msgs2::action::MovejH2r_SendGoal_Response & msg)
  : msg_(msg)
  {}
  ::dsr_msgs2::action::MovejH2r_SendGoal_Response stamp(::dsr_msgs2::action::MovejH2r_SendGoal_Response::_stamp_type arg)
  {
    msg_.stamp = std::move(arg);
    return std::move(msg_);
  }

private:
  ::dsr_msgs2::action::MovejH2r_SendGoal_Response msg_;
};

class Init_MovejH2r_SendGoal_Response_accepted
{
public:
  Init_MovejH2r_SendGoal_Response_accepted()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_MovejH2r_SendGoal_Response_stamp accepted(::dsr_msgs2::action::MovejH2r_SendGoal_Response::_accepted_type arg)
  {
    msg_.accepted = std::move(arg);
    return Init_MovejH2r_SendGoal_Response_stamp(msg_);
  }

private:
  ::dsr_msgs2::action::MovejH2r_SendGoal_Response msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::dsr_msgs2::action::MovejH2r_SendGoal_Response>()
{
  return dsr_msgs2::action::builder::Init_MovejH2r_SendGoal_Response_accepted();
}

}  // namespace dsr_msgs2


namespace dsr_msgs2
{

namespace action
{

namespace builder
{

class Init_MovejH2r_GetResult_Request_goal_id
{
public:
  Init_MovejH2r_GetResult_Request_goal_id()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::dsr_msgs2::action::MovejH2r_GetResult_Request goal_id(::dsr_msgs2::action::MovejH2r_GetResult_Request::_goal_id_type arg)
  {
    msg_.goal_id = std::move(arg);
    return std::move(msg_);
  }

private:
  ::dsr_msgs2::action::MovejH2r_GetResult_Request msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::dsr_msgs2::action::MovejH2r_GetResult_Request>()
{
  return dsr_msgs2::action::builder::Init_MovejH2r_GetResult_Request_goal_id();
}

}  // namespace dsr_msgs2


namespace dsr_msgs2
{

namespace action
{

namespace builder
{

class Init_MovejH2r_GetResult_Response_result
{
public:
  explicit Init_MovejH2r_GetResult_Response_result(::dsr_msgs2::action::MovejH2r_GetResult_Response & msg)
  : msg_(msg)
  {}
  ::dsr_msgs2::action::MovejH2r_GetResult_Response result(::dsr_msgs2::action::MovejH2r_GetResult_Response::_result_type arg)
  {
    msg_.result = std::move(arg);
    return std::move(msg_);
  }

private:
  ::dsr_msgs2::action::MovejH2r_GetResult_Response msg_;
};

class Init_MovejH2r_GetResult_Response_status
{
public:
  Init_MovejH2r_GetResult_Response_status()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_MovejH2r_GetResult_Response_result status(::dsr_msgs2::action::MovejH2r_GetResult_Response::_status_type arg)
  {
    msg_.status = std::move(arg);
    return Init_MovejH2r_GetResult_Response_result(msg_);
  }

private:
  ::dsr_msgs2::action::MovejH2r_GetResult_Response msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::dsr_msgs2::action::MovejH2r_GetResult_Response>()
{
  return dsr_msgs2::action::builder::Init_MovejH2r_GetResult_Response_status();
}

}  // namespace dsr_msgs2


namespace dsr_msgs2
{

namespace action
{

namespace builder
{

class Init_MovejH2r_FeedbackMessage_feedback
{
public:
  explicit Init_MovejH2r_FeedbackMessage_feedback(::dsr_msgs2::action::MovejH2r_FeedbackMessage & msg)
  : msg_(msg)
  {}
  ::dsr_msgs2::action::MovejH2r_FeedbackMessage feedback(::dsr_msgs2::action::MovejH2r_FeedbackMessage::_feedback_type arg)
  {
    msg_.feedback = std::move(arg);
    return std::move(msg_);
  }

private:
  ::dsr_msgs2::action::MovejH2r_FeedbackMessage msg_;
};

class Init_MovejH2r_FeedbackMessage_goal_id
{
public:
  Init_MovejH2r_FeedbackMessage_goal_id()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_MovejH2r_FeedbackMessage_feedback goal_id(::dsr_msgs2::action::MovejH2r_FeedbackMessage::_goal_id_type arg)
  {
    msg_.goal_id = std::move(arg);
    return Init_MovejH2r_FeedbackMessage_feedback(msg_);
  }

private:
  ::dsr_msgs2::action::MovejH2r_FeedbackMessage msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::dsr_msgs2::action::MovejH2r_FeedbackMessage>()
{
  return dsr_msgs2::action::builder::Init_MovejH2r_FeedbackMessage_goal_id();
}

}  // namespace dsr_msgs2

#endif  // DSR_MSGS2__ACTION__DETAIL__MOVEJ_H2R__BUILDER_HPP_
