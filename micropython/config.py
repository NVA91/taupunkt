# Configuration for Raspberry Pi Pico 2 dew point monitor
# Pin layout and calibration constants

# I2C pins
I2C_SDA = 16  # GP16
I2C_SCL = 17  # GP17

# Sensor addresses
AHT20_ADDR = 0x38
BMP280_ADDR = 0x76
SHT41_ADDR = 0x44

# LED pins
LED_ROT = 13
LED_GELB = 14
LED_GRUEN = 15

# ST7789 display SPI pins
SPI_SCK = 18  # GP18
SPI_MOSI = 19  # GP19
LCD_DC = 20  # GP20
LCD_CS = 21  # GP21
LCD_RST = 22  # GP22
LCD_BL = 21

# Display geometry
TFT_WIDTH = 172
TFT_HEIGHT = 320
ROTATION = 3

# Measurement interval in seconds
INTERVAL = 900

# Allowed difference between indoor and outdoor dew point
DEWPOINT_DELTA = 2.0
