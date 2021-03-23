from .utils import parse_year

def fix_index(item):
    try:
        if len(item) > 0:
            return item[0]
    except TypeError: # raised by TDRC
        return item

def retrieve_metadata(mutagen_file, filename):
    # Album artist
    album_artist = mutagen_file.get("albumartist")
    if album_artist == None:
        album_artist = mutagen_file.get("TPE2")
        if album_artist == None:
            album_artist = mutagen_file.get('aART')
            if album_artist == None:
                album_artist = mutagen_file.get('ALBUM ARTIST')
    album_artist = fix_index(album_artist)

    # Year
    date = mutagen_file.get("date", None)
    if date == None:
        date = mutagen_file.get("TDRC", None)
        if date == None:
            try:
                date = mutagen_file.get("\xa9day", None)
            except ValueError: # For Ogg Opus files
                pass
            if date == None:
                date = mutagen_file.get('DATE') # TODO ensure discovery date exists
    if date != None:
        date = parse_year(str(fix_index(date)))
    else:
        print(f"No date loaded for: {filename}")
        date = ""

    # Codec
    codec = type(mutagen_file).__name__
    if codec == "MP4":
        codec = "M4A"
    if codec == "WAVE":
        codec = "WAV"
    if codec == "OggOpus":
        codec = "OPUS"

    # Album
    album = mutagen_file.get("album")
    if album == None:
        album = mutagen_file.get("TALB")
        if album == None:
            album = mutagen_file.get("\xa9alb") # ©alb
            if album == None:
                album = mutagen_file.get("ALBUM") # ©alb
    album = fix_index(album)

    # Title
    title = mutagen_file.get("title")
    if title == None:
        title = mutagen_file.get("TIT2")
        if title == None:
            title = mutagen_file.get("\xa9nam") # ©nam
            if title == None:
                title = mutagen_file.get("TITLE")
    title = fix_index(title)

    # Track Number
    tracknum = mutagen_file.get("tracknumber")
    if tracknum == None:
        tracknum = mutagen_file.get("TRCK")
        if tracknum == None:
            tracknum = mutagen_file.get("trkn")
    tracknum = fix_index(tracknum)
    if tracknum != None:
        if codec == "M4A":
            tracknum = tracknum[0]
        tracknum = str(tracknum).zfill(2)
    else:
        print(f"No track number loaded for: {filename}")

    return album, album_artist, str(date), codec, title, tracknum