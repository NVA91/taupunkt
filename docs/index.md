# Taupunkt – Project Documentation

## Overview

Taupunkt is a dew-point monitor for the Raspberry Pi Pico 2.  It reads
temperature and humidity from two sensor positions (indoor / outdoor) and
recommends whether ventilating the room would reduce moisture condensation risk.
The result is shown on a small ST7789 LCD and signalled through a traffic-light
LED strip.

## Hardware

| Component | Description |
|-----------|-------------|
| Controller | Raspberry Pi Pico 2 |
| Display | Waveshare 1.47″ LCD (ST7789, 172 × 320) |
| Indoor sensor | SHT41 – I²C address 0x44 |
| Outdoor sensor | AHT20 – I²C address 0x38 |
| Pressure sensor | BMP280 – I²C address 0x76 |
| LEDs | Red / Yellow / Green traffic-light |

Default pin assignments are defined in `micropython/config.py`.

## Repository Layout

```
taupunkt/
├── csrc/               # Optional C driver sources (ST7789)
├── docs/               # This documentation
├── examples/           # Pre-built firmware binaries
├── micropython/        # MicroPython firmware for the Pico
│   ├── boot.py         # Disables backlight during boot
│   ├── config.py       # Pin assignments and thresholds
│   ├── lib/            # Reusable modules
│   │   ├── dewpoint_calc.py    # Magnus-formula dew-point calculation
│   │   ├── display_st7789.py   # Display initialisation helper
│   │   ├── sensor_aht20.py     # AHT20 driver wrapper
│   │   ├── sensor_bmp280.py    # BMP280 driver wrapper
│   │   └── sensor_sht41.py     # SHT41 driver wrapper
│   ├── main.py         # Application entry point
│   └── tools/          # Developer utilities
│       ├── calibrate_sensors.py
│       └── upload_to_pico.py
├── src/taupunkt/       # Python package stub (host-side use)
└── tests/              # Unit tests
```

## Dew-Point Logic

The Magnus formula is used to convert temperature *T* (°C) and relative
humidity *RH* (%) into a dew-point temperature:

```
α = (a·T / (b + T)) + ln(RH / 100)
Td = b·α / (a − α)     with a = 17.27, b = 237.7
```

| Condition | LED | Meaning |
|-----------|-----|---------|
| `Td_out < Td_in − DEWPOINT_DELTA` | 🟢 Green | Ventilating is recommended |
| `Td_out >= Td_in` | 🔴 Red | Do not ventilate |
| otherwise | 🟡 Yellow | Ventilate with caution |

`DEWPOINT_DELTA` defaults to `2.0 °C` and can be changed in `config.py`.

## Getting Started

### Flash MicroPython

Download the latest MicroPython UF2 for RP2350 from
<https://micropython.org/download/RPI_PICO2/> and flash it onto the Pico.

### Upload the Firmware

```bash
pip install mpremote
python micropython/tools/upload_to_pico.py
```

The script copies the entire `micropython/` folder to the device root.  Reboot
the Pico to start the application.

### Configuration

Edit `micropython/config.py` before uploading to adjust pin numbers,
the measurement interval (`INTERVAL`, in seconds), or the dew-point threshold
(`DEWPOINT_DELTA`).

## Running the Tests

```bash
pip install pytest
pytest tests/
```
