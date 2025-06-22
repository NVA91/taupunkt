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
Flash MicroPython 1.20 or newer to the Pico. Upload the `micropython` folder
and reboot. The display will update within a few seconds.

### MicroPython
1. Install `mpremote` via `pip install mpremote`.
2. Connect the Pico via USB.
3. Execute `python micropython/tools/upload_to_pico.py` to copy the files.
4. Reset the board – the `main.py` script starts in under 3 s.

For long‑term deployments you can freeze the modules using
```
mpy-cross lib/*.py
```
and rebuilding MicroPython with the resulting bytecode files.
