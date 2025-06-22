"""Simple calibration helper for the sensors."""

from machine import I2C, Pin
import time
from config import I2C_SCL, I2C_SDA, AHT20_ADDR, BMP280_ADDR, SHT41_ADDR
from lib.sensor_aht20 import AHT20
from lib.sensor_bmp280 import BMP280
from lib.sensor_sht41 import SHT41


def main():
    i2c = I2C(0, scl=Pin(I2C_SCL), sda=Pin(I2C_SDA), freq=100000)
    aht = AHT20(i2c, address=AHT20_ADDR)
    bmp = BMP280(i2c, addr=BMP280_ADDR)
    sht = SHT41(i2c, address=SHT41_ADDR)

    while True:
        t_i, rh_i = sht.measurements
        t_o = aht.temperature
        rh_o = aht.relative_humidity
        p = bmp.pressure
        print(f"Innen: {t_i:.1f}C {rh_i:.1f}% | Aussen: {t_o:.1f}C {rh_o:.1f}% | Druck: {p:.0f} hPa")
        time.sleep(1)


if __name__ == "__main__":
    main()
