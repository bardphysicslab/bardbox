"""
gt521s_driver.py
Bard Box driver for the GT-521S optical particle counter.

Channels : c03 (≥ 0.3 µm), c05 (≥ 0.5 µm)
Interface: USB serial via CP2102 (Silicon Labs)
Baud rate: 9600
Count units: count/ft³  (CU 0)

Conforms to the Bard Box driver interface defined in
docs/pi-driver-instructions.md.
"""

import re
import threading
import time
from typing import Any, Dict, List, Optional

import serial


DEFAULT_PORT = (
    "/dev/serial/by-id/"
    "usb-Silicon_Labs_CP2102_USB_to_UART_Bridge_Controller_Y10162-if00-port0"
)
DEFAULT_BAUD = 9600

_CHANNELS: List[Dict[str, str]] = [
    {"channel": "c03", "description": "Particle count ≥ 0.3 µm", "unit": "count/ft³"},
    {"channel": "c05", "description": "Particle count ≥ 0.5 µm", "unit": "count/ft³"},
]


class GT521SDriver:
    """
    Bard Box driver for the GT-521S optical particle counter.

    Usage
    -----
    driver = GT521SDriver()
    driver.start()
    reading = driver.get_reading()   # {"ts": "...", "c03": 1452, "c05": 87}
    driver.stop()
    """

    def __init__(self, port: str = DEFAULT_PORT, baud: int = DEFAULT_BAUD):
        self._port = port
        self._baud = baud
        self._ser: Optional[serial.Serial] = None
        self._lock = threading.Lock()
        self._latest: Optional[Dict[str, Any]] = None
        self._stop_event = threading.Event()
        self._thread: Optional[threading.Thread] = None

    # ------------------------------------------------------------------
    # Bard Box driver interface
    # ------------------------------------------------------------------

    def get_info(self) -> Dict[str, Any]:
        """Return static sensor and serial configuration."""
        return {
            "driver": "gt521s_driver",
            "sensor": "GT-521S",
            "interface": "USB serial (CP2102)",
            "port": self._port,
            "baud": self._baud,
            "count_units": "count/ft³ (CU 0)",
        }

    def get_capabilities(self) -> List[Dict[str, str]]:
        """Return list of channels this driver produces."""
        return list(_CHANNELS)

    def get_reading(self) -> Optional[Dict[str, Any]]:
        """Return the most recent parsed reading, or None if none yet received."""
        with self._lock:
            return dict(self._latest) if self._latest else None

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    def start(self):
        """Open serial port, configure device, and start the reader thread."""
        self._open()
        self._send(b"CU 0")   # count/ft³  — Bard Box standard
        self._send(b"SR 1")   # CSV output
        self._send(b"S")      # start sampling
        self._stop_event.clear()
        self._thread = threading.Thread(target=self._reader_loop, daemon=True)
        self._thread.start()

    def stop(self):
        """Stop sampling and shut down the reader thread."""
        self._stop_event.set()
        self._send(b"E")
        if self._thread:
            self._thread.join(timeout=2.0)

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    def _open(self):
        if self._ser and self._ser.is_open:
            return
        self._ser = serial.Serial(self._port, self._baud, timeout=0)
        try:
            self._ser.dtr = True
            self._ser.rts = True
        except Exception:
            pass
        time.sleep(1.0)
        try:
            self._ser.reset_input_buffer()
        except Exception:
            pass

    def _send(self, cmd: bytes):
        if self._ser and self._ser.is_open:
            self._ser.write(cmd + b"\r")
            self._ser.flush()
            time.sleep(0.1)

    def _reader_loop(self):
        buf = b""
        while not self._stop_event.is_set():
            if not self._ser:
                time.sleep(0.1)
                continue
            n = self._ser.in_waiting
            if n:
                buf += self._ser.read(n)
                buf = buf.replace(b"\r", b"\n")
                while b"\n" in buf:
                    line, buf = buf.split(b"\n", 1)
                    parsed = self._parse(line.decode(errors="replace"))
                    if parsed:
                        with self._lock:
                            self._latest = parsed
            else:
                time.sleep(0.05)

    @staticmethod
    def _parse(line: str) -> Optional[Dict[str, Any]]:
        """Parse one CSV line from the GT-521S into a channel dict."""
        line = line.strip().lstrip("*")
        if not re.match(r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},", line):
            return None
        if "*" in line:
            line = line.split("*", 1)[0].strip().rstrip(",")
        parts = [p.strip() for p in line.split(",")]
        if len(parts) < 5:
            return None
        ts = parts[0]
        try:
            size1, cnt1 = float(parts[1]), int(parts[2])
            size2, cnt2 = float(parts[3]), int(parts[4])
        except (ValueError, IndexError):
            return None
        result: Dict[str, Any] = {"ts": ts}
        for size, cnt in [(size1, cnt1), (size2, cnt2)]:
            if abs(size - 0.3) < 0.05:
                result["c03"] = cnt
            elif abs(size - 0.5) < 0.05:
                result["c05"] = cnt
        return result if len(result) > 1 else None
