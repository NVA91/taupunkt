# Taupunkt Project

Simple dew-point display project for Raspberry Pi Pico 2.

## Hardware

- **Controller**: Raspberry Pi Pico 2
- **Display**: Waveshare 1.47" LCD (ST7789, 172x320)
- **Sensors**:
  - AHT20 humidity/temperature (0x38)
  - BMP280 pressure (0x76)
  - SHT41 indoor humidity/temperature (0x44)

## Usage
To run on the Pico, upload the `micropython` folder to the device and reboot.
The scripts contain all required defaults for the hardware listed above.
