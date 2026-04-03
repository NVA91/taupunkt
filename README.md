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

Install [mpremote](https://pypi.org/project/mpremote/) and run:

```bash
python micropython/tools/upload_to_pico.py
```

This copies all firmware files to the Pico.  Reboot the device to start the
application.  All pin assignments and thresholds can be adjusted in
`micropython/config.py`.

## Documentation

Full documentation is available in [`docs/index.md`](docs/index.md).

## Changelog

See [`CHANGELOG.md`](CHANGELOG.md) for a history of notable changes.
