"""BMP280 sensor helper."""

import bmp280

class BMP280(bmp280.BMP280):
    def __init__(self, i2c, addr=0x76):
        super().__init__(i2c, addr=addr)

