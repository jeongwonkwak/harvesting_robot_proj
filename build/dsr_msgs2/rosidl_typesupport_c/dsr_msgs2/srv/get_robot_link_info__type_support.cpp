// generated from rosidl_typesupport_c/resource/idl__type_support.cpp.em
// with input from dsr_msgs2:srv/GetRobotLinkInfo.idl
// generated code does not contain a copyright notice

#include "cstddef"
#include "rosidl_runtime_c/message_type_support_struct.h"
#include "dsr_msgs2/srv/detail/get_robot_link_info__struct.h"
#include "dsr_msgs2/srv/detail/get_robot_link_info__type_support.h"
#include "rosidl_typesupport_c/identifier.h"
#include "rosidl_typesupport_c/message_type_support_dispatch.h"
#include "rosidl_typesupport_c/type_support_map.h"
#include "rosidl_typesupport_c/visibility_control.h"
#include "rosidl_typesupport_interface/macros.h"

namespace dsr_msgs2
{

namespace srv
{

namespace rosidl_typesupport_c
{

typedef struct _GetRobotLinkInfo_Request_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _GetRobotLinkInfo_Request_type_support_ids_t;

static const _GetRobotLinkInfo_Request_type_support_ids_t _GetRobotLinkInfo_Request_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_c",  // ::rosidl_typesupport_fastrtps_c::typesupport_identifier,
    "rosidl_typesupport_introspection_c",  // ::rosidl_typesupport_introspection_c::typesupport_identifier,
  }
};

typedef struct _GetRobotLinkInfo_Request_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _GetRobotLinkInfo_Request_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _GetRobotLinkInfo_Request_type_support_symbol_names_t _GetRobotLinkInfo_Request_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, dsr_msgs2, srv, GetRobotLinkInfo_Request)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, dsr_msgs2, srv, GetRobotLinkInfo_Request)),
  }
};

typedef struct _GetRobotLinkInfo_Request_type_support_data_t
{
  void * data[2];
} _GetRobotLinkInfo_Request_type_support_data_t;

static _GetRobotLinkInfo_Request_type_support_data_t _GetRobotLinkInfo_Request_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _GetRobotLinkInfo_Request_message_typesupport_map = {
  2,
  "dsr_msgs2",
  &_GetRobotLinkInfo_Request_message_typesupport_ids.typesupport_identifier[0],
  &_GetRobotLinkInfo_Request_message_typesupport_symbol_names.symbol_name[0],
  &_GetRobotLinkInfo_Request_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t GetRobotLinkInfo_Request_message_type_support_handle = {
  rosidl_typesupport_c__typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_GetRobotLinkInfo_Request_message_typesupport_map),
  rosidl_typesupport_c__get_message_typesupport_handle_function,
};

}  // namespace rosidl_typesupport_c

}  // namespace srv

}  // namespace dsr_msgs2

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_c, dsr_msgs2, srv, GetRobotLinkInfo_Request)() {
  return &::dsr_msgs2::srv::rosidl_typesupport_c::GetRobotLinkInfo_Request_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif

// already included above
// #include "cstddef"
// already included above
// #include "rosidl_runtime_c/message_type_support_struct.h"
// already included above
// #include "dsr_msgs2/srv/detail/get_robot_link_info__struct.h"
// already included above
// #include "dsr_msgs2/srv/detail/get_robot_link_info__type_support.h"
// already included above
// #include "rosidl_typesupport_c/identifier.h"
// already included above
// #include "rosidl_typesupport_c/message_type_support_dispatch.h"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_c/visibility_control.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace dsr_msgs2
{

namespace srv
{

namespace rosidl_typesupport_c
{

typedef struct _GetRobotLinkInfo_Response_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _GetRobotLinkInfo_Response_type_support_ids_t;

static const _GetRobotLinkInfo_Response_type_support_ids_t _GetRobotLinkInfo_Response_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_c",  // ::rosidl_typesupport_fastrtps_c::typesupport_identifier,
    "rosidl_typesupport_introspection_c",  // ::rosidl_typesupport_introspection_c::typesupport_identifier,
  }
};

typedef struct _GetRobotLinkInfo_Response_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _GetRobotLinkInfo_Response_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _GetRobotLinkInfo_Response_type_support_symbol_names_t _GetRobotLinkInfo_Response_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, dsr_msgs2, srv, GetRobotLinkInfo_Response)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, dsr_msgs2, srv, GetRobotLinkInfo_Response)),
  }
};

typedef struct _GetRobotLinkInfo_Response_type_support_data_t
{
  void * data[2];
} _GetRobotLinkInfo_Response_type_support_data_t;

static _GetRobotLinkInfo_Response_type_support_data_t _GetRobotLinkInfo_Response_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _GetRobotLinkInfo_Response_message_typesupport_map = {
  2,
  "dsr_msgs2",
  &_GetRobotLinkInfo_Response_message_typesupport_ids.typesupport_identifier[0],
  &_GetRobotLinkInfo_Response_message_typesupport_symbol_names.symbol_name[0],
  &_GetRobotLinkInfo_Response_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t GetRobotLinkInfo_Response_message_type_support_handle = {
  rosidl_typesupport_c__typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_GetRobotLinkInfo_Response_message_typesupport_map),
  rosidl_typesupport_c__get_message_typesupport_handle_function,
};

}  // namespace rosidl_typesupport_c

}  // namespace srv

}  // namespace dsr_msgs2

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_c, dsr_msgs2, srv, GetRobotLinkInfo_Response)() {
  return &::dsr_msgs2::srv::rosidl_typesupport_c::GetRobotLinkInfo_Response_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif

// already included above
// #include "cstddef"
#include "rosidl_runtime_c/service_type_support_struct.h"
// already included above
// #include "dsr_msgs2/srv/detail/get_robot_link_info__type_support.h"
// already included above
// #include "rosidl_typesupport_c/identifier.h"
#include "rosidl_typesupport_c/service_type_support_dispatch.h"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace dsr_msgs2
{

namespace srv
{

namespace rosidl_typesupport_c
{

typedef struct _GetRobotLinkInfo_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _GetRobotLinkInfo_type_support_ids_t;

static const _GetRobotLinkInfo_type_support_ids_t _GetRobotLinkInfo_service_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_c",  // ::rosidl_typesupport_fastrtps_c::typesupport_identifier,
    "rosidl_typesupport_introspection_c",  // ::rosidl_typesupport_introspection_c::typesupport_identifier,
  }
};

typedef struct _GetRobotLinkInfo_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _GetRobotLinkInfo_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _GetRobotLinkInfo_type_support_symbol_names_t _GetRobotLinkInfo_service_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, dsr_msgs2, srv, GetRobotLinkInfo)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_introspection_c, dsr_msgs2, srv, GetRobotLinkInfo)),
  }
};

typedef struct _GetRobotLinkInfo_type_support_data_t
{
  void * data[2];
} _GetRobotLinkInfo_type_support_data_t;

static _GetRobotLinkInfo_type_support_data_t _GetRobotLinkInfo_service_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _GetRobotLinkInfo_service_typesupport_map = {
  2,
  "dsr_msgs2",
  &_GetRobotLinkInfo_service_typesupport_ids.typesupport_identifier[0],
  &_GetRobotLinkInfo_service_typesupport_symbol_names.symbol_name[0],
  &_GetRobotLinkInfo_service_typesupport_data.data[0],
};

static const rosidl_service_type_support_t GetRobotLinkInfo_service_type_support_handle = {
  rosidl_typesupport_c__typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_GetRobotLinkInfo_service_typesupport_map),
  rosidl_typesupport_c__get_service_typesupport_handle_function,
};

}  // namespace rosidl_typesupport_c

}  // namespace srv

}  // namespace dsr_msgs2

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_service_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_c, dsr_msgs2, srv, GetRobotLinkInfo)() {
  return &::dsr_msgs2::srv::rosidl_typesupport_c::GetRobotLinkInfo_service_type_support_handle;
}

#ifdef __cplusplus
}
#endif
