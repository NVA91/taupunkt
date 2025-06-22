# MicroPython Deployment

This folder contains all files required to run the dew-point monitor on a Raspberry Pi Pico 2.

```
micropython/
├── boot.py           # Backlight off during boot
├── config.py         # Pin assignments and thresholds
├── lib/              # Helper modules for display and sensors
├── main.py           # Example application
└── tools/            # Utility scripts (upload, calibration)
```

## Usage
1. Connect the Pico via USB.
2. Upload the entire directory with:
   ```bash
   python tools/upload_to_pico.py
   ```
3. Reboot the Pico. The `main.py` script will start automatically and display the sensor data.

The `config.py` file contains the exact pin mapping:

```
I2C  SDA GP16  SCL GP17
SPI  SCK GP18  MOSI GP19  DC GP20  CS GP21  RST GP22
LEDs GP13/14/15
```

Sensors are addressed at 0x38 (AHT20), 0x76 (BMP280) and 0x44 (SHT41).
