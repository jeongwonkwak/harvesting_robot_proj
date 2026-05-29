# generated from rosidl_generator_py/resource/_idl.py.em
# with input from dsr_msgs2:srv/FlangeSerialOpen.idl
# generated code does not contain a copyright notice


# Import statements for member types

import builtins  # noqa: E402, I100

import rosidl_parser.definition  # noqa: E402, I100


class Metaclass_FlangeSerialOpen_Request(type):
    """Metaclass of message 'FlangeSerialOpen_Request'."""

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
                'dsr_msgs2.srv.FlangeSerialOpen_Request')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__srv__flange_serial_open__request
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__srv__flange_serial_open__request
            cls._CONVERT_TO_PY = module.convert_to_py_msg__srv__flange_serial_open__request
            cls._TYPE_SUPPORT = module.type_support_msg__srv__flange_serial_open__request
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__srv__flange_serial_open__request

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class FlangeSerialOpen_Request(metaclass=Metaclass_FlangeSerialOpen_Request):
    """Message class 'FlangeSerialOpen_Request'."""

    __slots__ = [
        '_port',
        '_baudrate',
        '_bytesize',
        '_parity',
        '_stopbits',
    ]

    _fields_and_field_types = {
        'port': 'int32',
        'baudrate': 'int32',
        'bytesize': 'int32',
        'parity': 'int32',
        'stopbits': 'int32',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.BasicType('int32'),  # noqa: E501
        rosidl_parser.definition.BasicType('int32'),  # noqa: E501
        rosidl_parser.definition.BasicType('int32'),  # noqa: E501
        rosidl_parser.definition.BasicType('int32'),  # noqa: E501
        rosidl_parser.definition.BasicType('int32'),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        self.port = kwargs.get('port', int())
        self.baudrate = kwargs.get('baudrate', int())
        self.bytesize = kwargs.get('bytesize', int())
        self.parity = kwargs.get('parity', int())
        self.stopbits = kwargs.get('stopbits', int())

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
        if self.baudrate != other.baudrate:
            return False
        if self.bytesize != other.bytesize:
            return False
        if self.parity != other.parity:
            return False
        if self.stopbits != other.stopbits:
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
    def baudrate(self):
        """Message field 'baudrate'."""
        return self._baudrate

    @baudrate.setter
    def baudrate(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'baudrate' field must be of type 'int'"
            assert value >= -2147483648 and value < 2147483648, \
                "The 'baudrate' field must be an integer in [-2147483648, 2147483647]"
        self._baudrate = value

    @builtins.property
    def bytesize(self):
        """Message field 'bytesize'."""
        return self._bytesize

    @bytesize.setter
    def bytesize(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'bytesize' field must be of type 'int'"
            assert value >= -2147483648 and value < 2147483648, \
                "The 'bytesize' field must be an integer in [-2147483648, 2147483647]"
        self._bytesize = value

    @builtins.property
    def parity(self):
        """Message field 'parity'."""
        return self._parity

    @parity.setter
    def parity(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'parity' field must be of type 'int'"
            assert value >= -2147483648 and value < 2147483648, \
                "The 'parity' field must be an integer in [-2147483648, 2147483647]"
        self._parity = value

    @builtins.property
    def stopbits(self):
        """Message field 'stopbits'."""
        return self._stopbits

    @stopbits.setter
    def stopbits(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'stopbits' field must be of type 'int'"
            assert value >= -2147483648 and value < 2147483648, \
                "The 'stopbits' field must be an integer in [-2147483648, 2147483647]"
        self._stopbits = value


# Import statements for member types

# already imported above
# import builtins

# already imported above
# import rosidl_parser.definition


class Metaclass_FlangeSerialOpen_Response(type):
    """Metaclass of message 'FlangeSerialOpen_Response'."""

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
                'dsr_msgs2.srv.FlangeSerialOpen_Response')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__srv__flange_serial_open__response
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__srv__flange_serial_open__response
            cls._CONVERT_TO_PY = module.convert_to_py_msg__srv__flange_serial_open__response
            cls._TYPE_SUPPORT = module.type_support_msg__srv__flange_serial_open__response
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__srv__flange_serial_open__response

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class FlangeSerialOpen_Response(metaclass=Metaclass_FlangeSerialOpen_Response):
    """Message class 'FlangeSerialOpen_Response'."""

    __slots__ = [
        '_success',
    ]

    _fields_and_field_types = {
        'success': 'boolean',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.BasicType('boolean'),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
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
        if self.success != other.success:
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


class Metaclass_FlangeSerialOpen(type):
    """Metaclass of service 'FlangeSerialOpen'."""

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
                'dsr_msgs2.srv.FlangeSerialOpen')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._TYPE_SUPPORT = module.type_support_srv__srv__flange_serial_open

            from dsr_msgs2.srv import _flange_serial_open
            if _flange_serial_open.Metaclass_FlangeSerialOpen_Request._TYPE_SUPPORT is None:
                _flange_serial_open.Metaclass_FlangeSerialOpen_Request.__import_type_support__()
            if _flange_serial_open.Metaclass_FlangeSerialOpen_Response._TYPE_SUPPORT is None:
                _flange_serial_open.Metaclass_FlangeSerialOpen_Response.__import_type_support__()


class FlangeSerialOpen(metaclass=Metaclass_FlangeSerialOpen):
    from dsr_msgs2.srv._flange_serial_open import FlangeSerialOpen_Request as Request
    from dsr_msgs2.srv._flange_serial_open import FlangeSerialOpen_Response as Response

    def __init__(self):
        raise NotImplementedError('Service classes can not be instantiated')
