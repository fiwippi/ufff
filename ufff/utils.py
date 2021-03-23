import re
import unicodedata
from mutagen import File
from dateutil.parser import parser

def parse_year(date_str):
    return parser().parse(date_str).strftime('%Y')

def is_audio_file(filepath):
    if load_mutagen(filepath) == None:
        return False
    return True

def load_mutagen(filepath):
    with open(filepath, 'rb') as f:
        return File(f)

# Removes dots if file set to true
def sanitise(value):
    value = unicodedata.normalize('NFKC', str(value))
    value = re.sub(r'[\/<>:"\\?*|]', '-', value)
    value = value.rstrip(".").strip(" ").strip("\t").strip("\r").strip("\n").strip("\f").strip("\v").replace("	", "")

    return value