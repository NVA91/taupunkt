# Configuration for Raspberry Pi Pico 2 dew point monitor
# Pin layout and calibration constants

# I2C pins
from micropython import const

I2C_SDA = const(16)  # GP16
I2C_SCL = const(17)  # GP17

# Sensor addresses
AHT20_ADDR = const(0x38)
BMP280_ADDR = const(0x76)
SHT41_ADDR = const(0x44)

# LED pins
LED_ROT = const(13)
LED_GELB = const(14)
LED_GRUEN = const(15)

# ST7789 display SPI pins
SPI_SCK = const(18)  # GP18
SPI_MOSI = const(19)  # GP19
LCD_DC = const(20)  # GP20
LCD_CS = const(21)  # GP21
LCD_RST = const(22)  # GP22
LCD_BL = const(21)

# Display geometry
TFT_WIDTH = const(172)
TFT_HEIGHT = const(320)
ROTATION = const(3)

# Measurement interval in seconds
INTERVAL = const(30)

# Allowed difference between indoor and outdoor dew point
DEWPOINT_DELTA = const(2)

# Duration for cached sensor values
CACHE_TIMEOUT = const(30)

# Watchdog timeout in milliseconds
WDT_TIMEOUT = const(30_000)
