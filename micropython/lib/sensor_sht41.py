"""SHT41 sensor helper."""

import sht4x

class SHT41(sht4x.SHT4x):
    def __init__(self, i2c, address=0x44):
        super().__init__(i2c, address=address)

