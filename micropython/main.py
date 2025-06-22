"""Entry point for the dew point monitor running on a Raspberry Pi Pico."""

import time
from machine import I2C, Pin, WDT
import st7789

from config import (
    I2C_SCL,
    I2C_SDA,
    LED_ROT,
    LED_GELB,
    LED_GRUEN,
    INTERVAL,
    DEWPOINT_DELTA,
    WDT_TIMEOUT,
)
from lib.display_st7789 import Display
from lib.sensor_aht20 import AHT20
from lib.sensor_bmp280 import BMP280
from lib.sensor_sht41 import SHT41
from lib.dewpoint_calc import dewpoint


def setup():
    i2c = I2C(0, scl=Pin(I2C_SCL), sda=Pin(I2C_SDA), freq=100_000)
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
    display = Display()
    return sensors, leds, display


def feed_leds(leds, status):
    for pin in leds.values():
        pin.off()
    leds.get(status, Pin(-1)).on()  # pragma: no cover - hardware only


def blink_error(leds, times=3):
    for _ in range(times):
        leds["rot"].on()
        time.sleep(0.2)
        leds["rot"].off()
        time.sleep(0.2)


def main():
    sensors, leds, display = setup()
    wdt = WDT(timeout=WDT_TIMEOUT)
    last_values = None

    while True:
        wdt.feed()
        try:
            innen_t, innen_rh = sensors["innen"].read()
            aussen_t, aussen_rh = sensors["aussen"].read()
            druck = sensors["druck"].read()

            if None in (innen_t, innen_rh, aussen_t, aussen_rh, druck):
                raise RuntimeError("Sensor read failed")
            last_values = (innen_t, innen_rh, aussen_t, aussen_rh, druck)
        except Exception as exc:
            print("Sensor failure", exc)
            blink_error(leds)
            if last_values is None:
                display.show_error("Sensor")
                time.sleep(5)
                continue
            innen_t, innen_rh, aussen_t, aussen_rh, druck = last_values

        tp_in = dewpoint(innen_t, innen_rh)
        tp_out = dewpoint(aussen_t, aussen_rh)

        try:
            if tp_out < tp_in - DEWPOINT_DELTA:
                feed_leds(leds, "gruen")
            elif tp_out >= tp_in:
                feed_leds(leds, "rot")
            else:
                feed_leds(leds, "gelb")

            display.show_readings(
                (innen_t, innen_rh),
                (aussen_t, aussen_rh),
                druck,
                tp_out,
                time.localtime(),
            )

            print(
                "Innen: %.1fC %.1f%% | Aussen: %.1fC %.1f%% | TP: %.1fC"
                % (innen_t, innen_rh, aussen_t, aussen_rh, tp_out)
            )
        except Exception as exc:
            print("Display failure", exc)
            blink_error(leds, 5)
            display.show_error("Display")
        time.sleep(INTERVAL)


if __name__ == "__main__":
    main()
