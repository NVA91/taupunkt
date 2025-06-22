"""Boot-time hardware initialisation."""

from machine import Pin
from config import LCD_BL

# Disable backlight during boot to avoid flicker
Pin(LCD_BL, Pin.OUT).off()
