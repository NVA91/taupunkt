"""Helper for initializing the Waveshare 1.47 inch ST7789 display."""

from machine import Pin, SPI
import st7789
from config import SPI_SCK, SPI_MOSI, LCD_DC, LCD_CS, LCD_RST, LCD_BL, TFT_WIDTH, TFT_HEIGHT, ROTATION


def init_display():
    spi = SPI(0, baudrate=30_000_000, sck=Pin(SPI_SCK), mosi=Pin(SPI_MOSI))
    tft = st7789.ST7789(
        spi, TFT_WIDTH, TFT_HEIGHT,
        reset=Pin(LCD_RST, Pin.OUT),
        dc=Pin(LCD_DC, Pin.OUT),
        cs=Pin(LCD_CS, Pin.OUT),
        rotation=ROTATION,
    )
    tft.init()
    Pin(LCD_BL, Pin.OUT).on()
    return tft
