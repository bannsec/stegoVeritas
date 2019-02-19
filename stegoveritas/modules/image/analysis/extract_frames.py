
import logging
logger = logging.getLogger('StegoVeritas:Modules:Image:Analysis:ExtractFrames')

import os
from PIL import Image

import png
from copy import copy
from struct import pack, unpack

from apng import APNG

def run(image):
    """Extracts individual frames from an animated gif.

    Args:
        image: SVImage class instance

    Returns:
        None

    Saves the result to RESULTSDIR
    """

    args = image.veritas.args

    # Nothing to do
    if not args.auto and not args.extract_frames:
        logger.debug('Nothing to do.')
        return

    if image.file.format == 'PNG':
        extract_png(image)

    elif image.file.format == 'GIF':
        extract_gif(image)


def extract_png(image):

    # TODO: Maybe just use APNG: https://pypi.org/project/apng/

    img = APNG.open(image.veritas.file_name)

    if len(img.frames) == 1:
        logger.debug('Only one frame detected.')
        return

    print("Extracting {} PNG frames.".format(len(img.frames)))
    for i, (png, control) in enumerate(img.frames):
        outfile = os.path.join(image.veritas.results_directory, '{}_frame_{}.png'.format(os.path.basename(image.veritas.file_name), i))
        png.save(outfile)

    return

    ### Below is some original work before finding that library
    
    # PIL apparently can't handle this. Neither can ffmpeg. ImageMagick can be fooled.
    # Time to write my own animated png extractor

    img = png.Reader(image.veritas.file_name)
    chunks = list(img.chunks())

    num_frames = len(list(x for x in chunks if x[0] in [b'fcTL']))
    
    """
    actl = next(x for x in chunks if x[0] == b'acTL')

    # How many frames does the image claim to have
    given_num_frames, _ = unpack('>II', actl[1])

    if given_num_frames != num_frames:
        print('Image only claims {} frames, but I discovered {}'.format(given_num_frames, num_frames))
        print('Patching and attempting to extract the frames')

        new_actl = (b'acTL', pack('>II',num_frames,0))

        new_chunks = []
        frame_number = 0
        for t,v in chunks:
            if t == b'acTL':
                new_chunks.append(new_actl)

            elif t == b'fcTL':
                new_chunks.append((t, pack('>I', frame_number) + v[4:]))
                frame_number += 1

            else:
                new_chunks.append((t,v))

        with open('blerg.png','wb') as f:
            png.write_chunks(f, new_chunks)

    return
    """

    #######

    if num_frames == 1:
        logger.debug('Only one frame discovered.')
        return

    print('Discovered multuple PNG frames. Attempting to extract them...')

    header_chunk = next(x for x in chunks if x[0] in [b'IHDR'])
    end_chunk = (b'IEND', b'')
    actl_chunk = (b'acTL', b'\x00\x00\x00\x01\x00\x00\x00\x00') # looping, 1 frame

    new_image = []
    num_frames = 0

    # Type and value for the chunks
    for t, val in chunks:
        print(t)
        
        # We're done with this image
        if t in [b'fcTL', b'IEND']:

            # We have something to save
            if new_image != []:

                # Put propper chunks in place
                new_image.insert(0, copy(actl_chunk))
                new_header_chunk = list(copy(header_chunk))
                #new_header_chunk[1] = pack('>II', width, height) + new_header_chunk[1][8:]
                #new_header_chunk[1] = width_height + new_header_chunk[1][8:]
                new_header_chunk = tuple(new_header_chunk)
                new_image.insert(0, new_header_chunk)
                #new_image.insert(0, copy(header_chunk))
                new_image.append(copy(end_chunk))
                print(new_image)

                outfile = os.path.join(image.veritas.results_directory, '{}_frame_{}.png'.format(os.path.basename(image.veritas.file_name), num_frames))
                print(outfile)

                with open(outfile, 'wb') as f:
                    png.write_chunks(f, new_image)

                #new_image = [(t, val)]
                new_image = []
                num_frames += 1

            if t == b'fcTL':
                # Update our frame size
                #width, height = unpack('>II', val[4:12])
                #print('width and height: ' + str(width) + ' ' + str(height))
                #width_height = val[4:12]
                #new_image.append((t, b'\x00\x00\x00\x00' + val[4:]))
                new_image.append((t, val))

            # Nothing to save, just add our header in
            #else:
            #    new_image.append((t, val))

        elif t == b'IDAT':
            new_image.append((t, val))

        elif t == b'fdAT':
            # fdAT is simply IDAT with 4 bytes at the beginning
            new_image.append((b'IDAT', val[4:]))


        """
        # Chunk data between image designators
        elif t in [b'IDAT', b'fdAT']:
            new_image.append((t, val))
        """



    

def extract_gif(image):

    if not hasattr(image.file, 'is_animated') or image.file.is_animated is False:
        logger.debug('This file is not an animated image.')
        return

    frame_number = 0

    while True:
        outfile = os.path.join(image.veritas.results_directory, '{}_frame_{}.gif'.format(os.path.basename(image.veritas.file_name), frame_number))
        image.file.save(outfile)
        
        frame_number += 1

        try:
            image.file.seek(frame_number)
        except EOFError:
            break

    # Be kind, please rewind.
    image.file.seek(0)
