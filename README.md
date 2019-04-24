[![Build Status](https://travis-ci.org/bannsec/stegoVeritas.svg?branch=master)](https://travis-ci.org/bannsec/stegoVeritas)
[![PyPI Statistics](https://img.shields.io/pypi/dm/stegoveritas.svg)](https://pypistats.org/packages/stegoveritas)
[![Latest Release](https://img.shields.io/pypi/v/stegoveritas.svg)](https://pypi.python.org/pypi/stegoveritas/)

# StegoVeritas
Yet another Stego Tool

# Quick Start

## Install

### Option 1 -- pip

```bash
$ pip3 install stegoveritas
$ stegoveritas_install_deps
```

`stegoveritas_install_deps` currently supports: ubuntu, debian, kali, fedora, archlinux.

### Option 2 -- docker

```bash
$ sudo docker run -it --rm bannsec/stegoveritas
```

### Option 3 -- [BlackArch](https://blackarch.org/)

```bash
$ sudo pacman -S stegoveritas
```

[PKGBUILD](https://github.com/BlackArch/blackarch/blob/master/packages/stegoveritas/PKGBUILD)

## Running
StegoVeritas has default actions for most image types (gif,jpeg,png,tiff,bmp)
and will attempt to run on __any__ file.

`stegoveritas <file>`

If you want to do something specific, you can check out the help:

```
stegoveritas -h
usage: stegoveritas [-h] [-out dir] [-debug] [-meta] [-imageTransform]
                    [-bruteLSB] [-colorMap [N [N ...]]]
                    [-colorMapRange Start End] [-extractLSB]
                    [-red index [index ...]] [-green index [index ...]]
                    [-blue index [index ...]] [-alpha index [index ...]]
                    [-extract_frames] [-trailing] [-exif] [-xmp] [-carve]
                    file

Yet another Stego tool

positional arguments:
  file                  The file to analyze

optional arguments:
  -h, --help            show this help message and exit
  -out dir              Directory to place output in. Defaults to ./results
  -debug                Enable debugging logging.

image options:
  -meta                 Check file for metadata information
  -imageTransform       Perform various image transformations on the input
                        image and save them to the output directory
  -bruteLSB             Attempt to brute force any LSB related stegonography.
  -colorMap [N [N ...]]
                        Analyze a color map. Optional arguments are colormap
                        indexes to save while searching
  -colorMapRange Start End
                        Analyze a color map. Same as colorMap but implies a
                        range of colorMap values to keep
  -extractLSB           Extract a specific LSB RGB from the image. Use with
                        -red, -green, -blue, and -alpha
  -red index [index ...]
  -green index [index ...]
  -blue index [index ...]
  -alpha index [index ...]
  -extract_frames       Split up an animated gif into individual frames.
  -trailing             Check for trailing data on the given file

multi options:
  -exif                 Check this file for exif information.
  -xmp                  Check this file for XMP information.
  -carve                Attempt to carve/extract things from this file.

Have a good example? Wish it did something more? Submit a ticket:
https://github.com/bannsec/stegoVeritas
```
