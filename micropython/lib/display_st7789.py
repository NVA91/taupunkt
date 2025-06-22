"""Driver helpers for the Waveshare 1.47 inch ST7789 display."""

from machine import Pin, SPI
import gc
import st7789
import vga1_8x8 as font
from config import (
    SPI_SCK,
    SPI_MOSI,
    LCD_DC,
    LCD_CS,
    LCD_RST,
    LCD_BL,
    TFT_WIDTH,
    TFT_HEIGHT,
    ROTATION,
)


class Display:
    """Simple wrapper around the ST7789 driver with drawing helpers."""

    def __init__(self):
        self._init_display()

    def _init_display(self):
        spi = SPI(0, baudrate=30_000_000, sck=Pin(SPI_SCK), mosi=Pin(SPI_MOSI))
        self.tft = st7789.ST7789(
            spi,
            TFT_WIDTH,
            TFT_HEIGHT,
            reset=Pin(LCD_RST, Pin.OUT),
            dc=Pin(LCD_DC, Pin.OUT),
            cs=Pin(LCD_CS, Pin.OUT),
            rotation=ROTATION,
        )
        self.tft.init()
        Pin(LCD_BL, Pin.OUT).on()

    def clear(self, color=st7789.BLACK):  # pragma: no cover - hardware only
        self.tft.fill(color)

    def _center(self, text, y, color=st7789.WHITE):  # pragma: no cover - hardware only
        x = (TFT_WIDTH - len(text) * 8) // 2
        self.tft.text(font, text, x, y, color)

    def show_error(self, msg):  # pragma: no cover - hardware only
        self.clear(st7789.RED)
        self._center("ERROR", 80, st7789.WHITE)
        self._center(msg, 100, st7789.WHITE)
        gc.collect()

    def show_readings(self, innen, aussen, pressure, dewpoint, timestamp):
        """Display sensor data and time."""  # pragma: no cover - hardware only

        try:
            self.clear()
            self._center("TAUPUNKT", 0, st7789.CYAN)

            y = 20
            self.tft.text(font, "AUSSEN:", 0, y, st7789.WHITE)
            y += 12
            self.tft.text(font, f"T {aussen[0]:5.1f}C", 10, y, st7789.WHITE)
            y += 12
            self.tft.text(font, f"RH {aussen[1]:3.0f}%", 10, y, st7789.WHITE)
            y += 12
            self.tft.text(font, f"P {pressure:4.0f} hPa", 10, y, st7789.WHITE)

            y += 18
            self.tft.text(font, "INNEN:", 0, y, st7789.WHITE)
            y += 12
            self.tft.text(font, f"T {innen[0]:5.1f}C", 10, y, st7789.WHITE)
            y += 12
            self.tft.text(font, f"RH {innen[1]:3.0f}%", 10, y, st7789.WHITE)

            y += 18
            self.tft.text(font, "TAUPUNKT:", 0, y, st7789.WHITE)
            y += 12
            self.tft.text(font, f"{dewpoint:5.1f}C", 10, y, st7789.WHITE)

            dt = "{:02d}:{:02d} {:02d}.{:02d}.{:02d}".format(
                timestamp[3], timestamp[4], timestamp[2], timestamp[1], timestamp[0] % 100
            )
            self._center(dt, TFT_HEIGHT - 16, st7789.CYAN)
        except Exception as exc:
            print("Display update error", exc)
            self._init_display()
            self.show_error("Display")
        finally:
            gc.collect()


def init_display():  # pragma: no cover - legacy API
    """Return a :class:`Display` instance for backward compatibility."""
    return Display().tft
