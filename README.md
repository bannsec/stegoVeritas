# StegoDone
Yet another Stego Tool

# Quick Start
StegoDone has default actions for most image types (gif,jpeg,png,tiff,bmp)

`stegodone.py <file>`

If you want to do something specific, you can check out the help:

```
stegodone.py -h
usage: stegodone.py [-h] [-outDir dir] [-meta] [-imageTransform] [-bruteLSB]
                    [-colorMap [N [N ...]]] [-colorMapRange Start End]
                    [-extractLSB] [-red index [index ...]]
                    [-green index [index ...]] [-blue index [index ...]]
                    [-alpha index [index ...]] [-trailing]
                    file

Yet another Stego tool

positional arguments:
  file                  The file to analyze

optional arguments:
  -h, --help            show this help message and exit
  -outDir dir           Directory to place output in. Defaults to ./results
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
  -trailing             Check for trailing data on the given file
```
