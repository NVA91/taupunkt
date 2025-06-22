"""BMP280 sensor helper with error handling."""

import time
import machine
import bmp280
from config import I2C_SCL, I2C_SDA, CACHE_TIMEOUT


class BMP280:
    """Safely read pressure from a BMP280 sensor."""

    def __init__(self, i2c, addr=0x76):
        self._i2c = i2c
        self._addr = addr
        self._sensor = bmp280.BMP280(i2c, addr=addr)
        self._last = None
        self._ts = 0

    def _recover(self):
        try:
            self._i2c.deinit()
        except AttributeError:
            pass
        self._i2c.init(scl=machine.Pin(I2C_SCL), sda=machine.Pin(I2C_SDA), freq=100_000)

    def read(self):
        now = time.ticks_ms()
        if time.ticks_diff(now, self._ts) < CACHE_TIMEOUT * 1000 and self._last is not None:
            return self._last
        try:
            # library exposes .pressure in hPa
            data = self._sensor.pressure
            self._last = data
            self._ts = now
            return data
        except Exception as exc:  # pragma: no cover - hardware only
            print("BMP280 read error", exc)
            self._recover()
            return self._last

    @property
    def pressure(self):  # pragma: no cover - hardware only
        return self.read()

