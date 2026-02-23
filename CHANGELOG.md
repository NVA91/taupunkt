# Changelog

All notable changes to this project are documented here.

## [Unreleased]

## [0.1.0] – 2025-06-22

### Added
- Initial repository scaffold with `src/`, `tests/`, `micropython/`, `docs/`,
  `csrc/`, and `examples/` directories.
- `micropython/config.py` – centralised pin assignments and runtime constants.
- `micropython/lib/dewpoint_calc.py` – Magnus-formula dew-point calculation.
- `micropython/lib/display_st7789.py` – ST7789 display initialisation helper.
- `micropython/lib/sensor_aht20.py`, `sensor_bmp280.py`, `sensor_sht41.py` –
  thin sensor driver wrappers.
- `micropython/main.py` – application entry point (read sensors, evaluate
  dew-point, control LEDs and display).
- `micropython/boot.py` – disables display backlight during boot to avoid
  flicker.
- `micropython/tools/upload_to_pico.py` – helper to copy firmware to the Pico
  via `mpremote`.
- `micropython/tools/calibrate_sensors.py` – interactive sensor calibration
  utility.
- `docs/index.md` – project documentation.
- CI workflow (`.github/workflows/ci.yml`).
- `pyproject.toml` project metadata.

