# BMP280 Treiber (vollständige Version)
import time
import struct

class BMP280:
    def __init__(self, i2c, addr=0x76):
        self.i2c = i2c
        self.addr = addr
        self.i2c.writeto_mem(self.addr, 0xF4, b'\x27')  # Normal mode, temp and pressure
        self.i2c.writeto_mem(self.addr, 0xF5, b'\xA0')  # Config
        # Kalibrierdaten auslesen
        calib = self.i2c.readfrom_mem(self.addr, 0x88, 24)
        self.dig_T1 = struct.unpack('<H', calib[0:2])[0]
        self.dig_T2 = struct.unpack('<h', calib[2:4])[0]
        self.dig_T3 = struct.unpack('<h', calib[4:6])[0]
        self.dig_P1 = struct.unpack('<H', calib[6:8])[0]
        self.dig_P2 = struct.unpack('<h', calib[8:10])[0]
        self.dig_P3 = struct.unpack('<h', calib[10:12])[0]
        self.dig_P4 = struct.unpack('<h', calib[12:14])[0]
        self.dig_P5 = struct.unpack('<h', calib[14:16])[0]
        self.dig_P6 = struct.unpack('<h', calib[16:18])[0]
        self.dig_P7 = struct.unpack('<h', calib[18:20])[0]
        self.dig_P8 = struct.unpack('<h', calib[20:22])[0]
        self.dig_P9 = struct.unpack('<h', calib[22:24])[0]
        self.t_fine = 0

    def _read_raw_data(self):
        data = self.i2c.readfrom_mem(self.addr, 0xF7, 6)
        adc_p = (data[0] << 12) | (data[1] << 4) | (data[2] >> 4)
        adc_t = (data[3] << 12) | (data[4] << 4) | (data[5] >> 4)
        return adc_t, adc_p

    def _compensate_temperature(self, adc_T):
        var1 = (((adc_T >> 3) - (self.dig_T1 << 1)) * self.dig_T2) >> 11
        var2 = (((((adc_T >> 4) - self.dig_T1) * ((adc_T >> 4) - self.dig_T1)) >> 12) * self.dig_T3) >> 14
        self.t_fine = var1 + var2
        T = (self.t_fine * 5 + 128) >> 8
        return T / 100.0

    def _compensate_pressure(self, adc_P):
        var1 = self.t_fine - 128000
        var2 = var1 * var1 * self.dig_P6
        var2 = var2 + ((var1 * self.dig_P5) << 17)
        var2 = var2 + (self.dig_P4 << 35)
        var1 = ((var1 * var1 * self.dig_P3) >> 8) + ((var1 * self.dig_P2) << 12)
        var1 = (((1 << 47) + var1) * self.dig_P1) >> 33
        if var1 == 0:
            return 0  # Vermeide Division durch 0
        p = 1048576 - adc_P
        p = ((p << 31) - var2) * 3125 // var1
        var1 = (self.dig_P9 * (p >> 13) * (p >> 13)) >> 25
        var2 = (self.dig_P8 * p) >> 19
        p = ((p + var1 + var2) >> 8) + (self.dig_P7 << 4)
        return p / 25600.0  # hPa

    @property
    def temperature(self):
        adc_t, _ = self._read_raw_data()
        return self._compensate_temperature(adc_t)

    @property
    def pressure(self):
        adc_t, adc_p = self._read_raw_data()
        self._compensate_temperature(adc_t)  # t_fine aktualisieren
        return self._compensate_pressure(adc_p)