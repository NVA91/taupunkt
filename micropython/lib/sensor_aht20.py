"""Wrapper around the AHT20 sensor with basic error handling."""

import time
import machine
import ahtx0
from config import I2C_SCL, I2C_SDA, CACHE_TIMEOUT


class AHT20:
    """Safely read temperature and humidity from an AHT20."""

    def __init__(self, i2c, address=0x38):
        self._i2c = i2c
        self._address = address
        self._sensor = ahtx0.AHT20(i2c, address=address)
        self._last = (None, None)
        self._ts = 0

    def _recover(self):
        try:
            self._i2c.deinit()
        except AttributeError:
            pass
        self._i2c.init(scl=machine.Pin(I2C_SCL), sda=machine.Pin(I2C_SDA), freq=100_000)

    def read(self):
        """Return (temperature, humidity) using cached value when possible."""
        now = time.ticks_ms()
        if time.ticks_diff(now, self._ts) < CACHE_TIMEOUT * 1000 and self._last[0] is not None:
            return self._last
        try:
            data = self._sensor.temperature, self._sensor.relative_humidity
            self._last = data
            self._ts = now
            return data
        except Exception as exc:  # pragma: no cover - hardware only
            print("AHT20 read error", exc)
            self._recover()
            return self._last

    @property
    def temperature(self):  # pragma: no cover - hardware only
        return self.read()[0]

    @property
    def relative_humidity(self):  # pragma: no cover - hardware only
        return self.read()[1]

