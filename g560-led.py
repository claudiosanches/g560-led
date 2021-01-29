#!env/bin/python

#
# Logitech G560 Gaming Speakers LED control
#

import sys
import usb.core
import usb.util
import re
import binascii

vendor_id = 0x046d # Logitech
product_id = 0x0a78 # G560 Gaming Speaker
default_rate = 10000
default_brightness = 100
dev = None
wIndex = None


def help():
    print("""Logitech G560 Gaming Speaker LED control

Usage:
\tg560-led [help|--help|-h] - This help
\tg560-led solid {color} - Solid color mode
\tg560-led cycle [{rate} [{brightness}]] - Cycle through all colors
\tg560-led breathe {color} [{rate} [{brightness}]] - Single color breathing
\tg560-led off - Turn lights off

Arguments:
\tcolor: RRGGBB (RGB hex value)
\trate: 100-60000 (Value in milliseconds. Default: 10000ms)
\tbrightness: 0-100 (Percentage. Default: 100%)""")


def main():
    if (len(sys.argv) < 2):
        help()
        sys.exit()

    args = sys.argv + [None] * (5 - len(sys.argv))

    if (args[1] in ['--help', '-h', 'help']):
        help()
        sys.exit()

    mode = args[1]
    if mode == 'solid':
        set_led_solid(process_color(args[2]))
    elif mode == 'cycle':
        set_led_cycle(process_rate(args[2]), process_brightness(args[3]))
    elif mode == 'breathe':
        set_led_breathe(
            process_color(args[2]),
            process_rate(args[3]),
            process_brightness(args[4])
        )
    if mode == 'off':
        set_led_solid(process_color('000000'))
    else:
        print_error('Unknown mode.')


def print_error(msg):
    print('Error: ' + msg)
    sys.exit(1)


def process_color(color):
    if not color:
        print_error('No color specifed.')
    if color[0] == '#':
        color = color[1:]
    if not re.match('^[0-9a-fA-F]{6}$', color):
        print_error('Invalid color specified.')
    return color.lower()


def process_rate(rate):
    if not rate:
        rate = default_rate
    try:
        return '{:04x}'.format(max(100, min(65535, int(rate))))
    except ValueError:
        print_error('Invalid rate specified.')


def process_brightness(brightness):
    if not brightness:
        brightness = default_brightness
    try:
        return '{:02x}'.format(max(1, min(100, int(brightness))))
    except ValueError:
        print_error('Invalid brightness specified.')


def set_led_solid(color):
    return set_led('01', color + '0000000000')


def set_led_breathe(color, rate, brightness):
    return set_led('04', color + rate + '00' + brightness + '00')


def set_led_cycle(rate, brightness):
    return set_led('02', '0000000000' + rate + brightness)


def set_led(mode, data):
    global device
    global wIndex

    prefix = '11ff043a'
    left_secondary = '00'
    right_secondary = '01'
    left_primary = '02'
    right_primary = '03'

    suffix = '000000000000'
    send_command(prefix + left_secondary + mode + data + suffix)
    send_command(prefix + right_secondary + mode + data + suffix)
    send_command(prefix + left_primary + mode + data + suffix)
    send_command(prefix + right_primary + mode + data + suffix)


def send_command(data):
    attach_device()
    device.ctrl_transfer(0x21, 0x09, 0x0211, wIndex, binascii.unhexlify(data))
    detach_device()


def attach_device():
    global device
    global wIndex

    device = usb.core.find(idVendor=vendor_id, idProduct=product_id)
    if device is None:
        print_error('No compatible devices found.')

    wIndex = 0x02
    if device.is_kernel_driver_active(wIndex) is True:
        device.detach_kernel_driver(wIndex)
        usb.util.claim_interface(device, wIndex)


def detach_device():
    global device
    global wIndex
    if wIndex is not None:
        usb.util.release_interface(device, wIndex)
        device.attach_kernel_driver(wIndex)
        device = None
        wIndex = None


if __name__ == '__main__':
    main()
