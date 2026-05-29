# generated from rosidl_generator_py/resource/_idl.py.em
# with input from dsr_msgs2:srv/GetRobotLinkInfo.idl
# generated code does not contain a copyright notice


# Import statements for member types

import rosidl_parser.definition  # noqa: E402, I100


class Metaclass_GetRobotLinkInfo_Request(type):
    """Metaclass of message 'GetRobotLinkInfo_Request'."""

    _CREATE_ROS_MESSAGE = None
    _CONVERT_FROM_PY = None
    _CONVERT_TO_PY = None
    _DESTROY_ROS_MESSAGE = None
    _TYPE_SUPPORT = None

    __constants = {
    }

    @classmethod
    def __import_type_support__(cls):
        try:
            from rosidl_generator_py import import_type_support
            module = import_type_support('dsr_msgs2')
        except ImportError:
            import logging
            import traceback
            logger = logging.getLogger(
                'dsr_msgs2.srv.GetRobotLinkInfo_Request')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__srv__get_robot_link_info__request
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__srv__get_robot_link_info__request
            cls._CONVERT_TO_PY = module.convert_to_py_msg__srv__get_robot_link_info__request
            cls._TYPE_SUPPORT = module.type_support_msg__srv__get_robot_link_info__request
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__srv__get_robot_link_info__request

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class GetRobotLinkInfo_Request(metaclass=Metaclass_GetRobotLinkInfo_Request):
    """Message class 'GetRobotLinkInfo_Request'."""

    __slots__ = [
    ]

    _fields_and_field_types = {
    }

    SLOT_TYPES = (
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))

    def __repr__(self):
        typename = self.__class__.__module__.split('.')
        typename.pop()
        typename.append(self.__class__.__name__)
        args = []
        for s, t in zip(self.__slots__, self.SLOT_TYPES):
            field = getattr(self, s)
            fieldstr = repr(field)
            # We use Python array type for fields that can be directly stored
            # in them, and "normal" sequences for everything else.  If it is
            # a type that we store in an array, strip off the 'array' portion.
            if (
                isinstance(t, rosidl_parser.definition.AbstractSequence) and
                isinstance(t.value_type, rosidl_parser.definition.BasicType) and
                t.value_type.typename in ['float', 'double', 'int8', 'uint8', 'int16', 'uint16', 'int32', 'uint32', 'int64', 'uint64']
            ):
                if len(field) == 0:
                    fieldstr = '[]'
                else:
                    assert fieldstr.startswith('array(')
                    prefix = "array('X', "
                    suffix = ')'
                    fieldstr = fieldstr[len(prefix):-len(suffix)]
            args.append(s[1:] + '=' + fieldstr)
        return '%s(%s)' % ('.'.join(typename), ', '.join(args))

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)


# Import statements for member types

import builtins  # noqa: E402, I100

import math  # noqa: E402, I100

# Member 'd'
# Member 'a'
# Member 'alpha'
# Member 'theta'
# Member 'offset'
import numpy  # noqa: E402, I100

# already imported above
# import rosidl_parser.definition


class Metaclass_GetRobotLinkInfo_Response(type):
    """Metaclass of message 'GetRobotLinkInfo_Response'."""

    _CREATE_ROS_MESSAGE = None
    _CONVERT_FROM_PY = None
    _CONVERT_TO_PY = None
    _DESTROY_ROS_MESSAGE = None
    _TYPE_SUPPORT = None

    __constants = {
    }

    @classmethod
    def __import_type_support__(cls):
        try:
            from rosidl_generator_py import import_type_support
            module = import_type_support('dsr_msgs2')
        except ImportError:
            import logging
            import traceback
            logger = logging.getLogger(
                'dsr_msgs2.srv.GetRobotLinkInfo_Response')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__srv__get_robot_link_info__response
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__srv__get_robot_link_info__response
            cls._CONVERT_TO_PY = module.convert_to_py_msg__srv__get_robot_link_info__response
            cls._TYPE_SUPPORT = module.type_support_msg__srv__get_robot_link_info__response
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__srv__get_robot_link_info__response

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class GetRobotLinkInfo_Response(metaclass=Metaclass_GetRobotLinkInfo_Response):
    """Message class 'GetRobotLinkInfo_Response'."""

    __slots__ = [
        '_d',
        '_a',
        '_alpha',
        '_theta',
        '_offset',
        '_gradient',
        '_rotation',
        '_success',
    ]

    _fields_and_field_types = {
        'd': 'float[6]',
        'a': 'float[6]',
        'alpha': 'float[6]',
        'theta': 'float[6]',
        'offset': 'float[6]',
        'gradient': 'float',
        'rotation': 'float',
        'success': 'boolean',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.Array(rosidl_parser.definition.BasicType('float'), 6),  # noqa: E501
        rosidl_parser.definition.Array(rosidl_parser.definition.BasicType('float'), 6),  # noqa: E501
        rosidl_parser.definition.Array(rosidl_parser.definition.BasicType('float'), 6),  # noqa: E501
        rosidl_parser.definition.Array(rosidl_parser.definition.BasicType('float'), 6),  # noqa: E501
        rosidl_parser.definition.Array(rosidl_parser.definition.BasicType('float'), 6),  # noqa: E501
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
        rosidl_parser.definition.BasicType('boolean'),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        if 'd' not in kwargs:
            self.d = numpy.zeros(6, dtype=numpy.float32)
        else:
            self.d = kwargs.get('d')
        if 'a' not in kwargs:
            self.a = numpy.zeros(6, dtype=numpy.float32)
        else:
            self.a = kwargs.get('a')
        if 'alpha' not in kwargs:
            self.alpha = numpy.zeros(6, dtype=numpy.float32)
        else:
            self.alpha = kwargs.get('alpha')
        if 'theta' not in kwargs:
            self.theta = numpy.zeros(6, dtype=numpy.float32)
        else:
            self.theta = kwargs.get('theta')
        if 'offset' not in kwargs:
            self.offset = numpy.zeros(6, dtype=numpy.float32)
        else:
            self.offset = kwargs.get('offset')
        self.gradient = kwargs.get('gradient', float())
        self.rotation = kwargs.get('rotation', float())
        self.success = kwargs.get('success', bool())

    def __repr__(self):
        typename = self.__class__.__module__.split('.')
        typename.pop()
        typename.append(self.__class__.__name__)
        args = []
        for s, t in zip(self.__slots__, self.SLOT_TYPES):
            field = getattr(self, s)
            fieldstr = repr(field)
            # We use Python array type for fields that can be directly stored
            # in them, and "normal" sequences for everything else.  If it is
            # a type that we store in an array, strip off the 'array' portion.
            if (
                isinstance(t, rosidl_parser.definition.AbstractSequence) and
                isinstance(t.value_type, rosidl_parser.definition.BasicType) and
                t.value_type.typename in ['float', 'double', 'int8', 'uint8', 'int16', 'uint16', 'int32', 'uint32', 'int64', 'uint64']
            ):
                if len(field) == 0:
                    fieldstr = '[]'
                else:
                    assert fieldstr.startswith('array(')
                    prefix = "array('X', "
                    suffix = ')'
                    fieldstr = fieldstr[len(prefix):-len(suffix)]
            args.append(s[1:] + '=' + fieldstr)
        return '%s(%s)' % ('.'.join(typename), ', '.join(args))

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        if any(self.d != other.d):
            return False
        if any(self.a != other.a):
            return False
        if any(self.alpha != other.alpha):
            return False
        if any(self.theta != other.theta):
            return False
        if any(self.offset != other.offset):
            return False
        if self.gradient != other.gradient:
            return False
        if self.rotation != other.rotation:
            return False
        if self.success != other.success:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property
    def d(self):
        """Message field 'd'."""
        return self._d

    @d.setter
    def d(self, value):
        if isinstance(value, numpy.ndarray):
            assert value.dtype == numpy.float32, \
                "The 'd' numpy.ndarray() must have the dtype of 'numpy.float32'"
            assert value.size == 6, \
                "The 'd' numpy.ndarray() must have a size of 6"
            self._d = value
            return
        if __debug__:
            from collections.abc import Sequence
            from collections.abc import Set
            from collections import UserList
            from collections import UserString
            assert \
                ((isinstance(value, Sequence) or
                  isinstance(value, Set) or
                  isinstance(value, UserList)) and
                 not isinstance(value, str) and
                 not isinstance(value, UserString) and
                 len(value) == 6 and
                 all(isinstance(v, float) for v in value) and
                 all(not (val < -3.402823466e+38 or val > 3.402823466e+38) or math.isinf(val) for val in value)), \
                "The 'd' field must be a set or sequence with length 6 and each value of type 'float' and each float in [-340282346600000016151267322115014000640.000000, 340282346600000016151267322115014000640.000000]"
        self._d = numpy.array(value, dtype=numpy.float32)

    @builtins.property
    def a(self):
        """Message field 'a'."""
        return self._a

    @a.setter
    def a(self, value):
        if isinstance(value, numpy.ndarray):
            assert value.dtype == numpy.float32, \
                "The 'a' numpy.ndarray() must have the dtype of 'numpy.float32'"
            assert value.size == 6, \
                "The 'a' numpy.ndarray() must have a size of 6"
            self._a = value
            return
        if __debug__:
            from collections.abc import Sequence
            from collections.abc import Set
            from collections import UserList
            from collections import UserString
            assert \
                ((isinstance(value, Sequence) or
                  isinstance(value, Set) or
                  isinstance(value, UserList)) and
                 not isinstance(value, str) and
                 not isinstance(value, UserString) and
                 len(value) == 6 and
                 all(isinstance(v, float) for v in value) and
                 all(not (val < -3.402823466e+38 or val > 3.402823466e+38) or math.isinf(val) for val in value)), \
                "The 'a' field must be a set or sequence with length 6 and each value of type 'float' and each float in [-340282346600000016151267322115014000640.000000, 340282346600000016151267322115014000640.000000]"
        self._a = numpy.array(value, dtype=numpy.float32)

    @builtins.property
    def alpha(self):
        """Message field 'alpha'."""
        return self._alpha

    @alpha.setter
    def alpha(self, value):
        if isinstance(value, numpy.ndarray):
            assert value.dtype == numpy.float32, \
                "The 'alpha' numpy.ndarray() must have the dtype of 'numpy.float32'"
            assert value.size == 6, \
                "The 'alpha' numpy.ndarray() must have a size of 6"
            self._alpha = value
            return
        if __debug__:
            from collections.abc import Sequence
            from collections.abc import Set
            from collections import UserList
            from collections import UserString
            assert \
                ((isinstance(value, Sequence) or
                  isinstance(value, Set) or
                  isinstance(value, UserList)) and
                 not isinstance(value, str) and
                 not isinstance(value, UserString) and
                 len(value) == 6 and
                 all(isinstance(v, float) for v in value) and
                 all(not (val < -3.402823466e+38 or val > 3.402823466e+38) or math.isinf(val) for val in value)), \
                "The 'alpha' field must be a set or sequence with length 6 and each value of type 'float' and each float in [-340282346600000016151267322115014000640.000000, 340282346600000016151267322115014000640.000000]"
        self._alpha = numpy.array(value, dtype=numpy.float32)

    @builtins.property
    def theta(self):
        """Message field 'theta'."""
        return self._theta

    @theta.setter
    def theta(self, value):
        if isinstance(value, numpy.ndarray):
            assert value.dtype == numpy.float32, \
                "The 'theta' numpy.ndarray() must have the dtype of 'numpy.float32'"
            assert value.size == 6, \
                "The 'theta' numpy.ndarray() must have a size of 6"
            self._theta = value
            return
        if __debug__:
            from collections.abc import Sequence
            from collections.abc import Set
            from collections import UserList
            from collections import UserString
            assert \
                ((isinstance(value, Sequence) or
                  isinstance(value, Set) or
                  isinstance(value, UserList)) and
                 not isinstance(value, str) and
                 not isinstance(value, UserString) and
                 len(value) == 6 and
                 all(isinstance(v, float) for v in value) and
                 all(not (val < -3.402823466e+38 or val > 3.402823466e+38) or math.isinf(val) for val in value)), \
                "The 'theta' field must be a set or sequence with length 6 and each value of type 'float' and each float in [-340282346600000016151267322115014000640.000000, 340282346600000016151267322115014000640.000000]"
        self._theta = numpy.array(value, dtype=numpy.float32)

    @builtins.property
    def offset(self):
        """Message field 'offset'."""
        return self._offset

    @offset.setter
    def offset(self, value):
        if isinstance(value, numpy.ndarray):
            assert value.dtype == numpy.float32, \
                "The 'offset' numpy.ndarray() must have the dtype of 'numpy.float32'"
            assert value.size == 6, \
                "The 'offset' numpy.ndarray() must have a size of 6"
            self._offset = value
            return
        if __debug__:
            from collections.abc import Sequence
            from collections.abc import Set
            from collections import UserList
            from collections import UserString
            assert \
                ((isinstance(value, Sequence) or
                  isinstance(value, Set) or
                  isinstance(value, UserList)) and
                 not isinstance(value, str) and
                 not isinstance(value, UserString) and
                 len(value) == 6 and
                 all(isinstance(v, float) for v in value) and
                 all(not (val < -3.402823466e+38 or val > 3.402823466e+38) or math.isinf(val) for val in value)), \
                "The 'offset' field must be a set or sequence with length 6 and each value of type 'float' and each float in [-340282346600000016151267322115014000640.000000, 340282346600000016151267322115014000640.000000]"
        self._offset = numpy.array(value, dtype=numpy.float32)

    @builtins.property
    def gradient(self):
        """Message field 'gradient'."""
        return self._gradient

    @gradient.setter
    def gradient(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'gradient' field must be of type 'float'"
            assert not (value < -3.402823466e+38 or value > 3.402823466e+38) or math.isinf(value), \
                "The 'gradient' field must be a float in [-3.402823466e+38, 3.402823466e+38]"
        self._gradient = value

    @builtins.property
    def rotation(self):
        """Message field 'rotation'."""
        return self._rotation

    @rotation.setter
    def rotation(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'rotation' field must be of type 'float'"
            assert not (value < -3.402823466e+38 or value > 3.402823466e+38) or math.isinf(value), \
                "The 'rotation' field must be a float in [-3.402823466e+38, 3.402823466e+38]"
        self._rotation = value

    @builtins.property
    def success(self):
        """Message field 'success'."""
        return self._success

    @success.setter
    def success(self, value):
        if __debug__:
            assert \
                isinstance(value, bool), \
                "The 'success' field must be of type 'bool'"
        self._success = value


class Metaclass_GetRobotLinkInfo(type):
    """Metaclass of service 'GetRobotLinkInfo'."""

    _TYPE_SUPPORT = None

    @classmethod
    def __import_type_support__(cls):
        try:
            from rosidl_generator_py import import_type_support
            module = import_type_support('dsr_msgs2')
        except ImportError:
            import logging
            import traceback
            logger = logging.getLogger(
                'dsr_msgs2.srv.GetRobotLinkInfo')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._TYPE_SUPPORT = module.type_support_srv__srv__get_robot_link_info

            from dsr_msgs2.srv import _get_robot_link_info
            if _get_robot_link_info.Metaclass_GetRobotLinkInfo_Request._TYPE_SUPPORT is None:
                _get_robot_link_info.Metaclass_GetRobotLinkInfo_Request.__import_type_support__()
            if _get_robot_link_info.Metaclass_GetRobotLinkInfo_Response._TYPE_SUPPORT is None:
                _get_robot_link_info.Metaclass_GetRobotLinkInfo_Response.__import_type_support__()


class GetRobotLinkInfo(metaclass=Metaclass_GetRobotLinkInfo):
    from dsr_msgs2.srv._get_robot_link_info import GetRobotLinkInfo_Request as Request
    from dsr_msgs2.srv._get_robot_link_info import GetRobotLinkInfo_Response as Response

    def __init__(self):
        raise NotImplementedError('Service classes can not be instantiated')
