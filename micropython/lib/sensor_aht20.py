"""Thin wrapper around the AHT20 sensor driver."""

import ahtx0

class AHT20(ahtx0.AHT20):
    def __init__(self, i2c, address=0x38):
        super().__init__(i2c, address=address)

