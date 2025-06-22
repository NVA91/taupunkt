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

The configuration in `config.py` matches the Waveshare 1.47" display (172x320) and the AHT20/BMP280/SHT41 sensors.
