# Logitech G560 Gaming Speakers LED control

Allows you to control the LED lighting of your G560 Gaming Speakers programmatically.

## Requirements

- Python 3.5+
- PyUSB 1.1.1+
- **Root privileges**

## Installation

```bash
git clone https://github.com/claudiosanches/g560-led.git
cd g560-led
virtualenv ./env
env/bin/pip install -r requirements.txt
```

## Usage

```text
Usage:
    g560-led solid {color} - Solid color mode
    g560-led cycle [{rate} [{brightness}]] - Cycle through all colors
    g560-led breathe {color} [{rate} [{brightness}]] - Single color breathing

Arguments:
    Color: RRGGBB (RGB hex value)
    Rate: 100-60000 (Number of milliseconds. Default: 10000ms)
    Brightness: 0-100 (Percentage. Default: 100%)
```

Note that the g560 has four independent lights: currently this script will set all to the same color.

Inspired by and based on [g810-led](https://github.com/MatMoul/g810-led),
[g203-led](https://github.com/smasty/g203-led), [g403-led](https://github.com/stelcheck/g403-led), and [g560-led](https://github.com/mijoe/g560-led).
