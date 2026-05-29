// generated from rosidl_typesupport_cpp/resource/idl__type_support.cpp.em
// with input from dsr_msgs2:srv/FlangeSerialWrite.idl
// generated code does not contain a copyright notice

#include "cstddef"
#include "rosidl_runtime_c/message_type_support_struct.h"
#include "dsr_msgs2/srv/detail/flange_serial_write__struct.hpp"
#include "rosidl_typesupport_cpp/identifier.hpp"
#include "rosidl_typesupport_cpp/message_type_support.hpp"
#include "rosidl_typesupport_c/type_support_map.h"
#include "rosidl_typesupport_cpp/message_type_support_dispatch.hpp"
#include "rosidl_typesupport_cpp/visibility_control.h"
#include "rosidl_typesupport_interface/macros.h"

namespace dsr_msgs2
{

namespace srv
{

namespace rosidl_typesupport_cpp
{

typedef struct _FlangeSerialWrite_Request_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _FlangeSerialWrite_Request_type_support_ids_t;

static const _FlangeSerialWrite_Request_type_support_ids_t _FlangeSerialWrite_Request_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_cpp",  // ::rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
    "rosidl_typesupport_introspection_cpp",  // ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  }
};

typedef struct _FlangeSerialWrite_Request_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _FlangeSerialWrite_Request_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _FlangeSerialWrite_Request_type_support_symbol_names_t _FlangeSerialWrite_Request_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, dsr_msgs2, srv, FlangeSerialWrite_Request)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, dsr_msgs2, srv, FlangeSerialWrite_Request)),
  }
};

typedef struct _FlangeSerialWrite_Request_type_support_data_t
{
  void * data[2];
} _FlangeSerialWrite_Request_type_support_data_t;

static _FlangeSerialWrite_Request_type_support_data_t _FlangeSerialWrite_Request_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _FlangeSerialWrite_Request_message_typesupport_map = {
  2,
  "dsr_msgs2",
  &_FlangeSerialWrite_Request_message_typesupport_ids.typesupport_identifier[0],
  &_FlangeSerialWrite_Request_message_typesupport_symbol_names.symbol_name[0],
  &_FlangeSerialWrite_Request_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t FlangeSerialWrite_Request_message_type_support_handle = {
  ::rosidl_typesupport_cpp::typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_FlangeSerialWrite_Request_message_typesupport_map),
  ::rosidl_typesupport_cpp::get_message_typesupport_handle_function,
};

}  // namespace rosidl_typesupport_cpp

}  // namespace srv

}  // namespace dsr_msgs2

namespace rosidl_typesupport_cpp
{

template<>
ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<dsr_msgs2::srv::FlangeSerialWrite_Request>()
{
  return &::dsr_msgs2::srv::rosidl_typesupport_cpp::FlangeSerialWrite_Request_message_type_support_handle;
}

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_cpp, dsr_msgs2, srv, FlangeSerialWrite_Request)() {
  return get_message_type_support_handle<dsr_msgs2::srv::FlangeSerialWrite_Request>();
}

#ifdef __cplusplus
}
#endif
}  // namespace rosidl_typesupport_cpp

// already included above
// #include "cstddef"
// already included above
// #include "rosidl_runtime_c/message_type_support_struct.h"
// already included above
// #include "dsr_msgs2/srv/detail/flange_serial_write__struct.hpp"
// already included above
// #include "rosidl_typesupport_cpp/identifier.hpp"
// already included above
// #include "rosidl_typesupport_cpp/message_type_support.hpp"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_cpp/message_type_support_dispatch.hpp"
// already included above
// #include "rosidl_typesupport_cpp/visibility_control.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace dsr_msgs2
{

namespace srv
{

namespace rosidl_typesupport_cpp
{

typedef struct _FlangeSerialWrite_Response_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _FlangeSerialWrite_Response_type_support_ids_t;

static const _FlangeSerialWrite_Response_type_support_ids_t _FlangeSerialWrite_Response_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_cpp",  // ::rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
    "rosidl_typesupport_introspection_cpp",  // ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  }
};

typedef struct _FlangeSerialWrite_Response_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _FlangeSerialWrite_Response_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _FlangeSerialWrite_Response_type_support_symbol_names_t _FlangeSerialWrite_Response_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, dsr_msgs2, srv, FlangeSerialWrite_Response)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, dsr_msgs2, srv, FlangeSerialWrite_Response)),
  }
};

typedef struct _FlangeSerialWrite_Response_type_support_data_t
{
  void * data[2];
} _FlangeSerialWrite_Response_type_support_data_t;

static _FlangeSerialWrite_Response_type_support_data_t _FlangeSerialWrite_Response_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _FlangeSerialWrite_Response_message_typesupport_map = {
  2,
  "dsr_msgs2",
  &_FlangeSerialWrite_Response_message_typesupport_ids.typesupport_identifier[0],
  &_FlangeSerialWrite_Response_message_typesupport_symbol_names.symbol_name[0],
  &_FlangeSerialWrite_Response_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t FlangeSerialWrite_Response_message_type_support_handle = {
  ::rosidl_typesupport_cpp::typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_FlangeSerialWrite_Response_message_typesupport_map),
  ::rosidl_typesupport_cpp::get_message_typesupport_handle_function,
};

}  // namespace rosidl_typesupport_cpp

}  // namespace srv

}  // namespace dsr_msgs2

namespace rosidl_typesupport_cpp
{

template<>
ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<dsr_msgs2::srv::FlangeSerialWrite_Response>()
{
  return &::dsr_msgs2::srv::rosidl_typesupport_cpp::FlangeSerialWrite_Response_message_type_support_handle;
}

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_cpp, dsr_msgs2, srv, FlangeSerialWrite_Response)() {
  return get_message_type_support_handle<dsr_msgs2::srv::FlangeSerialWrite_Response>();
}

#ifdef __cplusplus
}
#endif
}  // namespace rosidl_typesupport_cpp

// already included above
// #include "cstddef"
#include "rosidl_runtime_c/service_type_support_struct.h"
// already included above
// #include "dsr_msgs2/srv/detail/flange_serial_write__struct.hpp"
// already included above
// #include "rosidl_typesupport_cpp/identifier.hpp"
#include "rosidl_typesupport_cpp/service_type_support.hpp"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
#include "rosidl_typesupport_cpp/service_type_support_dispatch.hpp"
// already included above
// #include "rosidl_typesupport_cpp/visibility_control.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace dsr_msgs2
{

namespace srv
{

namespace rosidl_typesupport_cpp
{

typedef struct _FlangeSerialWrite_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _FlangeSerialWrite_type_support_ids_t;

static const _FlangeSerialWrite_type_support_ids_t _FlangeSerialWrite_service_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_cpp",  // ::rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
    "rosidl_typesupport_introspection_cpp",  // ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  }
};

typedef struct _FlangeSerialWrite_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _FlangeSerialWrite_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _FlangeSerialWrite_type_support_symbol_names_t _FlangeSerialWrite_service_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, dsr_msgs2, srv, FlangeSerialWrite)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, dsr_msgs2, srv, FlangeSerialWrite)),
  }
};

typedef struct _FlangeSerialWrite_type_support_data_t
{
  void * data[2];
} _FlangeSerialWrite_type_support_data_t;

static _FlangeSerialWrite_type_support_data_t _FlangeSerialWrite_service_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _FlangeSerialWrite_service_typesupport_map = {
  2,
  "dsr_msgs2",
  &_FlangeSerialWrite_service_typesupport_ids.typesupport_identifier[0],
  &_FlangeSerialWrite_service_typesupport_symbol_names.symbol_name[0],
  &_FlangeSerialWrite_service_typesupport_data.data[0],
};

static const rosidl_service_type_support_t FlangeSerialWrite_service_type_support_handle = {
  ::rosidl_typesupport_cpp::typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_FlangeSerialWrite_service_typesupport_map),
  ::rosidl_typesupport_cpp::get_service_typesupport_handle_function,
};

}  // namespace rosidl_typesupport_cpp

}  // namespace srv

}  // namespace dsr_msgs2

namespace rosidl_typesupport_cpp
{

template<>
ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_service_type_support_t *
get_service_type_support_handle<dsr_msgs2::srv::FlangeSerialWrite>()
{
  return &::dsr_msgs2::srv::rosidl_typesupport_cpp::FlangeSerialWrite_service_type_support_handle;
}

}  // namespace rosidl_typesupport_cpp

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_service_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_cpp, dsr_msgs2, srv, FlangeSerialWrite)() {
  return ::rosidl_typesupport_cpp::get_service_type_support_handle<dsr_msgs2::srv::FlangeSerialWrite>();
}

#ifdef __cplusplus
}
#endif
