"""SHT41 sensor helper with robust reads."""

import time
import machine
import sht4x
from config import I2C_SCL, I2C_SDA, CACHE_TIMEOUT


class SHT41:
    """Read temperature and humidity from the SHT41 sensor."""

    def __init__(self, i2c, address=0x44):
        self._i2c = i2c
        self._address = address
        self._sensor = sht4x.SHT4x(i2c, address=address)
        self._last = (None, None)
        self._ts = 0

    def _recover(self):
        try:
            self._i2c.deinit()
        except AttributeError:
            pass
        self._i2c.init(scl=machine.Pin(I2C_SCL), sda=machine.Pin(I2C_SDA), freq=100_000)

    def read(self):
        now = time.ticks_ms()
        if time.ticks_diff(now, self._ts) < CACHE_TIMEOUT * 1000 and self._last[0] is not None:
            return self._last
        try:
            data = self._sensor.measurements
            self._last = data
            self._ts = now
            return data
        except Exception as exc:  # pragma: no cover - hardware only
            print("SHT41 read error", exc)
            self._recover()
            return self._last

    @property
    def measurements(self):  # pragma: no cover - hardware only
        return self.read()

