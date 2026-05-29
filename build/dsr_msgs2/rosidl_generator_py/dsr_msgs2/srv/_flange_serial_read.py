# generated from rosidl_generator_py/resource/_idl.py.em
# with input from dsr_msgs2:srv/FlangeSerialRead.idl
# generated code does not contain a copyright notice


# Import statements for member types

import builtins  # noqa: E402, I100

import math  # noqa: E402, I100

import rosidl_parser.definition  # noqa: E402, I100


class Metaclass_FlangeSerialRead_Request(type):
    """Metaclass of message 'FlangeSerialRead_Request'."""

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
                'dsr_msgs2.srv.FlangeSerialRead_Request')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__srv__flange_serial_read__request
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__srv__flange_serial_read__request
            cls._CONVERT_TO_PY = module.convert_to_py_msg__srv__flange_serial_read__request
            cls._TYPE_SUPPORT = module.type_support_msg__srv__flange_serial_read__request
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__srv__flange_serial_read__request

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class FlangeSerialRead_Request(metaclass=Metaclass_FlangeSerialRead_Request):
    """Message class 'FlangeSerialRead_Request'."""

    __slots__ = [
        '_port',
        '_timeout',
    ]

    _fields_and_field_types = {
        'port': 'int32',
        'timeout': 'float',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.BasicType('int32'),  # noqa: E501
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        self.port = kwargs.get('port', int())
        self.timeout = kwargs.get('timeout', float())

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
        if self.port != other.port:
            return False
        if self.timeout != other.timeout:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property
    def port(self):
        """Message field 'port'."""
        return self._port

    @port.setter
    def port(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'port' field must be of type 'int'"
            assert value >= -2147483648 and value < 2147483648, \
                "The 'port' field must be an integer in [-2147483648, 2147483647]"
        self._port = value

    @builtins.property
    def timeout(self):
        """Message field 'timeout'."""
        return self._timeout

    @timeout.setter
    def timeout(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'timeout' field must be of type 'float'"
            assert not (value < -3.402823466e+38 or value > 3.402823466e+38) or math.isinf(value), \
                "The 'timeout' field must be a float in [-3.402823466e+38, 3.402823466e+38]"
        self._timeout = value


# Import statements for member types

# Member 'data'
import array  # noqa: E402, I100

# already imported above
# import builtins

# already imported above
# import rosidl_parser.definition


class Metaclass_FlangeSerialRead_Response(type):
    """Metaclass of message 'FlangeSerialRead_Response'."""

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
                'dsr_msgs2.srv.FlangeSerialRead_Response')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__srv__flange_serial_read__response
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__srv__flange_serial_read__response
            cls._CONVERT_TO_PY = module.convert_to_py_msg__srv__flange_serial_read__response
            cls._TYPE_SUPPORT = module.type_support_msg__srv__flange_serial_read__response
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__srv__flange_serial_read__response

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class FlangeSerialRead_Response(metaclass=Metaclass_FlangeSerialRead_Response):
    """Message class 'FlangeSerialRead_Response'."""

    __slots__ = [
        '_success',
        '_size',
        '_data',
    ]

    _fields_and_field_types = {
        'success': 'boolean',
        'size': 'int32',
        'data': 'sequence<uint8>',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.BasicType('boolean'),  # noqa: E501
        rosidl_parser.definition.BasicType('int32'),  # noqa: E501
        rosidl_parser.definition.UnboundedSequence(rosidl_parser.definition.BasicType('uint8')),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        self.success = kwargs.get('success', bool())
        self.size = kwargs.get('size', int())
        self.data = array.array('B', kwargs.get('data', []))

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
        if self.success != other.success:
            return False
        if self.size != other.size:
            return False
        if self.data != other.data:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

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

    @builtins.property
    def size(self):
        """Message field 'size'."""
        return self._size

    @size.setter
    def size(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'size' field must be of type 'int'"
            assert value >= -2147483648 and value < 2147483648, \
                "The 'size' field must be an integer in [-2147483648, 2147483647]"
        self._size = value

    @builtins.property
    def data(self):
        """Message field 'data'."""
        return self._data

    @data.setter
    def data(self, value):
        if isinstance(value, array.array):
            assert value.typecode == 'B', \
                "The 'data' array.array() must have the type code of 'B'"
            self._data = value
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
                 all(isinstance(v, int) for v in value) and
                 all(val >= 0 and val < 256 for val in value)), \
                "The 'data' field must be a set or sequence and each value of type 'int' and each unsigned integer in [0, 255]"
        self._data = array.array('B', value)


class Metaclass_FlangeSerialRead(type):
    """Metaclass of service 'FlangeSerialRead'."""

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
                'dsr_msgs2.srv.FlangeSerialRead')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._TYPE_SUPPORT = module.type_support_srv__srv__flange_serial_read

            from dsr_msgs2.srv import _flange_serial_read
            if _flange_serial_read.Metaclass_FlangeSerialRead_Request._TYPE_SUPPORT is None:
                _flange_serial_read.Metaclass_FlangeSerialRead_Request.__import_type_support__()
            if _flange_serial_read.Metaclass_FlangeSerialRead_Response._TYPE_SUPPORT is None:
                _flange_serial_read.Metaclass_FlangeSerialRead_Response.__import_type_support__()


class FlangeSerialRead(metaclass=Metaclass_FlangeSerialRead):
    from dsr_msgs2.srv._flange_serial_read import FlangeSerialRead_Request as Request
    from dsr_msgs2.srv._flange_serial_read import FlangeSerialRead_Response as Response

    def __init__(self):
        raise NotImplementedError('Service classes can not be instantiated')
