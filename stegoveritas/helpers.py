
import unicodedata
import re
import hashlib
import random
import logging

# Taken from Django
def slugify(value, allow_unicode=False):
    """
    Convert to ASCII if 'allow_unicode' is False. Convert spaces to hyphens.
    Remove characters that aren't alphanumerics, underscores, or hyphens.
    Convert to lowercase. Also strip leading and trailing whitespace.
    """
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize('NFKC', value)
    else:
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value).strip().lower()
    return re.sub(r'[-\s]+', '-', value)

def generate_nonce():
    """str: Create a nonce."""
    return hashlib.md5(str(random.random()).encode()).hexdigest()

def print_error(error):
    LOGGER.error(error)

    if hasattr(error, "__cause__") and error.__cause__ is not None:
        LOGGER.error(error.__cause__)

LOGGER = logging.getLogger(__name__)
