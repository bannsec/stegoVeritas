#!/usr/bin/env python3

import logging

# Helper tool to encode something LSB style into an image.

from PIL import Image
import argparse


def parse_args():
    parser = argparse.ArgumentParser(description='Simple tool to add LSB stego into an image.')
    parser.add_argument('-file', type=str, help='If specified, encode this file into the image instead of text.')
    parser.add_argument('-bands', type=str, help='Color order. I.e.: RGB, BGR, GBR, etc', default='RGB')
    parser.add_argument('-output', type=str, default=None, help='Specify the output file name (i.e.: out.png)')
    parser.add_argument('input_file', metavar='file', help='File to add LSB stego into.')
    parser.add_argument('text', nargs='*', help='Text to encode into the file.')
    return parser.parse_args()

def main():
    global img

    args = parse_args()

    # Hide this file inside the input_file
    if args.file:
        with open(args.file, 'rb') as f:
            text = f.read()
    else:
        text = ' '.join(args.text).encode()

    input_file = args.input_file

    img = Image.open(input_file)

    bits = bytes_to_bits(text)

    # TODO: Implement other raster scan orders
    for y in range(img.size[1]):
        for x in range(img.size[0]):
            for band in list(args.bands):
                try:
                    bit_to_encode = next(bits)
                except:
                    break

                encode_pixel(x, y, band, bit_to_encode, bit=0)
        else:
            continue
        break

    # Write it out
    if args.output is not None:
        if args.output.split('.')[-1].lower() not in ['png', 'bmp']:
            logging.warn('Outputting to lossy formats might screw up LSB! Should probably stick to PNG or BMP formats.')

        img.save(args.output)
    else:
        img.save(input_file + '_lsb.png')


def encode_pixel(x, y, band, value, bit=0):
    """Encodes the value (0 or 1) into pixel x,y band on bit 0 (least significant) to 7 (most significant)."""
    assert type(x) is int
    assert type(y) is int
    assert type(band) is str
    assert type(value) is int
    assert value in [0,1]
    assert type(bit) is int
    assert bit in range(8)

    orig_value = get_pixel(x, y, band)
    bitmask = 2**bit

    if value == 0:
        # If the bit is set, unset it
        if orig_value & bitmask != 0:
            new_value = orig_value - bitmask

        # The bit already happened to be correct
        else:
            new_value = orig_value

    else:
        # Or should always bring the value up to 1
        new_value = orig_value | bitmask

    update_pixel(x, y, band, new_value)
    assert get_pixel(x,y,band) == new_value


def get_pixel(x, y, band):
    """Returns the value of band for pixel x,y."""
    assert type(x) is int
    assert type(y) is int
    assert type(band) is str

    band = band.upper()
    band_index = img.getbands().index(band)

    pixels = img.load()
    return pixels[x, y][band_index]


def update_pixel(x, y, band, value):
    """Changes the pixel at x,y band to the given value."""
    assert type(x) is int
    assert type(y) is int
    assert type(band) is str
    assert type(value) is int

    band = band.upper()
    band_index = img.getbands().index(band)

    pixels = img.load()
    pixel = list(pixels[x, y])
    pixel[band_index] = value
    pixels[x, y] = tuple(pixel)

def bytes_to_bits(b, reverse_endian=False):
    if not reverse_endian:
        return map(int, ''.join([bin(i).lstrip('0b').rjust(8,'0') for i in b]))
    else:
        return map(int, ''.join([bin(i).lstrip('0b').rjust(8,'0')[::-1] for i in b]))


if __name__ == '__main__':
    main()
