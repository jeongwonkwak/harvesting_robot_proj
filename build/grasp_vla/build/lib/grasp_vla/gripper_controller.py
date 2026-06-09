"""
Robotis RH-P12-RN-DF gripper controller via Dynamixel SDK.

Wiring:
  USB2Dynamixel or U2D2 adapter → /dev/ttyUSB0 (default)
  Protocol 2.0 / Baudrate 2 000 000 bps / ID 1

Control-table addresses are for the RH-P12-RN firmware v1.x.
If you use a different firmware or model, adjust the addresses below.
"""

from __future__ import annotations

import time
from typing import Optional

_SDK_AVAILABLE = False
try:
    from dynamixel_sdk import (
        COMM_SUCCESS,
        PacketHandler,
        PortHandler,
    )
    _SDK_AVAILABLE = True
except ImportError:
    pass


# ---------------------------------------------------------------------------
# Control-table addresses (RH-P12-RN, Protocol 2.0)
# ---------------------------------------------------------------------------
_ADDR_OPERATING_MODE    = 11   # 5 = current-based position control
_ADDR_TORQUE_ENABLE     = 512
_ADDR_GOAL_CURRENT      = 604  # 2 bytes, unit = 1 mA
_ADDR_GOAL_POSITION     = 596  # 4 bytes
_ADDR_PRESENT_POSITION  = 611  # 4 bytes (read-only)
_ADDR_PRESENT_CURRENT   = 621  # 2 bytes (read-only)

# Gripper travel: 0 (fully open) → 740 (fully closed, bare contact)
# Adjust CLOSE_POSITION so the fingers just touch the target object.
_POS_OPEN  = 0
_POS_CLOSE = 740

# Default grasp current (mA).  Increase for heavier objects.
_GRASP_CURRENT_MA = 200


class GripperController:
    def __init__(
        self,
        port: str = "/dev/ttyUSB0",
        dxl_id: int = 1,
        baudrate: int = 2_000_000,
        ros_node=None,
        robot_id: str = "dsr01",
    ):
        self._id       = dxl_id
        self._connected = False
        self._ros_node = ros_node
        self._robot_id = robot_id

        # ROS 2 모드 우선
        if self._ros_node is not None:
            from std_srvs.srv import Trigger
            from std_msgs.msg import Int32
            self._open_cli  = self._ros_node.create_client(Trigger, f"/{self._robot_id}/gripper/open")
            self._close_cli = self._ros_node.create_client(Trigger, f"/{self._robot_id}/gripper/close")
            self._pos_cmd_pub = self._ros_node.create_publisher(Int32, f"/{self._robot_id}/gripper/position_cmd", 10)
            self._connected = True
            print(f"[INFO] Gripper connected via ROS2 ({self._robot_id}).")
            return

        if not _SDK_AVAILABLE:
            print("[WARN] dynamixel_sdk not installed – gripper in simulation mode.")
            return

        self._ph = PortHandler(port)
        self._pk = PacketHandler(2.0)

        try:
            opened = self._ph.openPort()
        except Exception as e:
            print(f"[WARN] Cannot open gripper port {port}: {e}. Running without gripper.")
            return
        if not opened:
            print(f"[WARN] Cannot open gripper port {port}. Running without gripper.")
            return
        if not self._ph.setBaudRate(baudrate):
            print("[ERROR] Cannot set gripper baudrate.")
            return

        # Set operating mode: current-based position control (mode 5)
        self._write1(self._id, _ADDR_TORQUE_ENABLE, 0)          # disable torque first
        self._write1(self._id, _ADDR_OPERATING_MODE, 5)
        self._write1(self._id, _ADDR_TORQUE_ENABLE, 1)          # re-enable

        self._connected = True
        print(f"[INFO] Gripper connected on {port} (ID={dxl_id}).")

    # ------------------------------------------------------------------
    # High-level API
    # ------------------------------------------------------------------

    def open(self, wait: float = 1.2) -> None:
        """Fully open the gripper."""
        if self._ros_node is not None:
            from std_srvs.srv import Trigger
            if self._open_cli.service_is_ready():
                req = Trigger.Request()
                self._open_cli.call_async(req)
                self._pos_ratio = 0.0
                time.sleep(wait)
            return

        self._set_current(_GRASP_CURRENT_MA)
        self._set_position(_POS_OPEN)
        time.sleep(wait)

    def close(
        self,
        target_pos: int = _POS_CLOSE,
        current_limit_ma: int = _GRASP_CURRENT_MA,
        wait: float = 1.5,
    ) -> None:
        """
        Close gripper to target_pos with a current limit (compliant grasp).
        The gripper stops when it contacts the object (current saturation).
        """
        if self._ros_node is not None:
            from std_srvs.srv import Trigger
            if self._close_cli.service_is_ready():
                req = Trigger.Request()
                self._close_cli.call_async(req)
                self._pos_ratio = 1.0
                time.sleep(wait)
            return

        self._set_current(current_limit_ma)
        self._set_position(target_pos)
        time.sleep(wait)

    def move_to(self, position: int) -> None:
        """Move gripper to absolute position (0 = open, 740 = closed)."""
        position = max(0, min(_POS_CLOSE, position))
        self._pos_ratio = position / _POS_CLOSE
        if self._ros_node is not None:
            from std_msgs.msg import Int32
            msg = Int32()
            msg.data = position
            self._pos_cmd_pub.publish(msg)
            return
        self._set_current(_GRASP_CURRENT_MA)
        self._set_position(position)

    def set_ratio(self, ratio: float) -> None:
        """Set gripper position by ratio: 0.0 = open, 1.0 = closed."""
        ratio = max(0.0, min(1.0, ratio))
        if self._ros_node is not None:
            self._pos_ratio = ratio
            from std_msgs.msg import Int32
            msg = Int32()
            msg.data = int(ratio * _POS_CLOSE)
            self._pos_cmd_pub.publish(msg)
            return
        self._set_position(int(ratio * _POS_CLOSE))

    def get_position(self) -> float:
        """Return current position as ratio [0.0, 1.0]."""
        if self._ros_node is not None:
            return getattr(self, '_pos_ratio', 0.0)
        if not self._connected:
            return 0.0
        pos, res, _ = self._pk.read4ByteTxRx(self._ph, self._id, _ADDR_PRESENT_POSITION)
        if res == COMM_SUCCESS:
            return pos / _POS_CLOSE
        return 0.0

    def get_current_ma(self) -> Optional[float]:
        """Return present current in mA (for contact detection)."""
        if not self._connected:
            return None
        cur, res, _ = self._pk.read2ByteTxRx(self._ph, self._id, _ADDR_PRESENT_CURRENT)
        if res == COMM_SUCCESS:
            # Value is signed 16-bit in units of ~1 mA
            if cur > 32767:
                cur -= 65536
            return float(cur)
        return None

    # ------------------------------------------------------------------
    # Low-level helpers
    # ------------------------------------------------------------------

    def _set_position(self, position: int) -> None:
        if not self._connected:
            print(f"[SIM] gripper position → {position}")
            return
        self._pk.write4ByteTxRx(self._ph, self._id, _ADDR_GOAL_POSITION, position)

    def _set_current(self, current_ma: int) -> None:
        if not self._connected:
            return
        self._pk.write2ByteTxRx(self._ph, self._id, _ADDR_GOAL_CURRENT, current_ma)

    def _write1(self, dxl_id: int, addr: int, value: int) -> None:
        self._pk.write1ByteTxRx(self._ph, dxl_id, addr, value)

    def __del__(self) -> None:
        if getattr(self, '_ros_node', None) is not None:
            return
        if getattr(self, '_connected', False):
            try:
                self._write1(self._id, _ADDR_TORQUE_ENABLE, 0)
                self._ph.closePort()
            except Exception:
                pass
