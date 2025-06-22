"""Main entry point for the Pico.
Initialises sensors and display and shows dew point information.
"""

import st7789
from machine import I2C, Pin
import time

from config import (
    I2C_SCL,
    I2C_SDA,
    LED_ROT,
    LED_GELB,
    LED_GRUEN,
    INTERVAL,
    DEWPOINT_DELTA,
)
from lib.display_st7789 import init_display
from lib.sensor_aht20 import AHT20
from lib.sensor_bmp280 import BMP280
from lib.sensor_sht41 import SHT41
from lib.dewpoint_calc import dewpoint


def setup():
    i2c = I2C(0, scl=Pin(I2C_SCL), sda=Pin(I2C_SDA), freq=100000)
    sensors = {
        "innen": SHT41(i2c),
        "aussen": AHT20(i2c),
        "druck": BMP280(i2c),
    }
    leds = {
        "rot": Pin(LED_ROT, Pin.OUT),
        "gelb": Pin(LED_GELB, Pin.OUT),
        "gruen": Pin(LED_GRUEN, Pin.OUT),
    }
    display = init_display()
    return sensors, leds, display


def show_status(tft, text, color):
    import vga1_8x8 as font
    tft.fill(color)
    tft.text(font, text, 10, 10, st7789.WHITE)


def main():
    sensors, leds, tft = setup()
    while True:
        innen_t, innen_rh = sensors["innen"].measurements
        aussen_t = sensors["aussen"].temperature
        aussen_rh = sensors["aussen"].relative_humidity
        tp_in = dewpoint(innen_t, innen_rh)
        tp_out = dewpoint(aussen_t, aussen_rh)

        for pin in leds.values():
            pin.off()

        if tp_out < tp_in - DEWPOINT_DELTA:
            leds["gruen"].on()
        elif tp_out >= tp_in:
            leds["rot"].on()
        else:
            leds["gelb"].on()

        print(
            f"Innen: {innen_t:.1f}C/{innen_rh:.1f}% -> {tp_in:.1f}C | "
            f"Aussen: {aussen_t:.1f}C/{aussen_rh:.1f}% -> {tp_out:.1f}C"
        )
        time.sleep(INTERVAL)


if __name__ == "__main__":
    main()
