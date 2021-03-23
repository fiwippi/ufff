import re
import unicodedata
from mutagen import File
from dateutil.parser import parser

def parse_date(date_str):
    return parser().parse(date_str).strftime('%Y')

def is_audio_file(filepath):
    if load_mutagen(filepath) == None:
        return False
    return True

def load_mutagen(filepath):
    with open(filepath, 'rb') as f:
        return File(f)

def sanitise(value):
    value = unicodedata.normalize('NFKC', str(value))
    value = re.sub(r'[\/<>:"\\?*|]', '-', value)
    return value.rstrip(".").strip(" ").strip("\t").strip("\r").strip("\n").strip("\f").strip("\v").replace("	", "")