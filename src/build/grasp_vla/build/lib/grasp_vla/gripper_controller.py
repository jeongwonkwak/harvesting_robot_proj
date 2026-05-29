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
    ):
        self._id       = dxl_id
        self._connected = False

        if not _SDK_AVAILABLE:
            print("[WARN] dynamixel_sdk not installed – gripper in simulation mode.")
            return

        self._ph = PortHandler(port)
        self._pk = PacketHandler(2.0)

        if not self._ph.openPort():
            print(f"[ERROR] Cannot open gripper port {port}.")
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
        self._set_current(current_limit_ma)
        self._set_position(target_pos)
        time.sleep(wait)

    def set_ratio(self, ratio: float) -> None:
        """Set gripper position by ratio: 0.0 = open, 1.0 = closed."""
        ratio = max(0.0, min(1.0, ratio))
        self._set_position(int(ratio * _POS_CLOSE))

    def get_position(self) -> float:
        """Return current position as ratio [0.0, 1.0]."""
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
        if self._connected:
            self._write1(self._id, _ADDR_TORQUE_ENABLE, 0)
            self._ph.closePort()
