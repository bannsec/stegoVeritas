
import logging
logger = logging.getLogger('StegoVeritas:Modules:Image:Analysis:ExtractFrames')

import os
from PIL import Image

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
