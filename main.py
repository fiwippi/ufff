from pathlib import Path
from files import move_file, delete_empty
from errors import TopLevelItemFoundError
from utils import load_mutagen, is_audio_file, sanitise
from metadata import retrieve_metadata

LIBRARY_DIR = r'D:\Nadav\Music\Collection\Records'

if __name__ == '__main__':
    base = Path(LIBRARY_DIR)
    for folder in base.iterdir():
        # Skip (hidden) files
        if not folder.is_dir() or folder.name.startswith("."):
            continue

        # Ensure only folders exist in the top-level artist directory
        try:
            for item in list(folder.iterdir()):
                if not item.is_dir():
                    raise TopLevelItemFoundError(item.name, folder)
        except TopLevelItemFoundError as e:
            print(e)
            continue

        # Collect all songs an artist has
        file_list = list(folder.rglob("*"))
        if len(file_list) == 0:
            print(f"No songs in : {folder}")

        artist_data = {}
        checked_extra = set() # Remembers if already checked for extra files

        # Go through each song
        for audio_file in file_list:
            if not audio_file.is_dir() and is_audio_file(audio_file):
                # Load the file
                mutagen_file = load_mutagen(audio_file)

                # Retrieve the tags we want
                filename = audio_file.name # Filename
                album, album_artist, date, codec, title, trackn = retrieve_metadata(mutagen_file, filename)

                # Album artist tag is required
                if album_artist == None:
                    print(f"Cannot work on \"{folder}\" due to no \"album artist\" tag in file \"{filename}\"")
                    continue
                # Album tag is required
                if album == None:
                    print(f"Cannot work on \"{folder}\" due to no \"album\" tag in file \"{filename}\"")
                    continue
                # Title tag is required
                if title == None:
                    print(f"Cannot work on \"{folder}\" due to no \"title\" tag in file \"{filename}\"")
                    continue

                audio_filename = ""
                if trackn != None:
                    audio_filename = sanitise(f"{trackn} {title}{audio_file.suffix}")
                else:
                    audio_filename = sanitise(f"{title}{audio_file.suffix}")

                if album not in artist_data:
                    artist_data[album] = {"artist": album_artist,
                                          "date": set(),
                                          "codecs": set(),
                                          "songs": [],
                                          "extras": []}

                artist_data[album]["codecs"].add(codec)
                if date != "":
                    artist_data[album]["date"].add(date)
                artist_data[album]["songs"].append([audio_file.as_posix(), sanitise(audio_filename)])

                # Include additional files, e.g. covers
                if audio_file.parent.as_posix() not in checked_extra:
                    checked_extra.add(audio_file.parent.as_posix())

                    for extra in audio_file.parent.iterdir():
                        if not extra.is_dir() and not is_audio_file(extra):
                            artist_data[album]["extras"].append([extra.parent.as_posix(), sanitise(extra.name)])

        # Done collecting song data
        for album in artist_data:
            codec = "-".join(sorted(artist_data[album]["codecs"]))
            date = "-".join(sorted(artist_data[album]["date"]))
            if date:
                date = " (" + date + ") "
            else:
                date = " "
            artist = sanitise(artist_data[album]["artist"])

            album_dirname = sanitise(f"{artist} – {album}{date}[{codec}]")
            album_path = (f"{folder.parent.as_posix()}/{artist}/{album_dirname}")

            # Copy songs
            for src, filename in artist_data[album]["songs"]:
                dst = f"{album_path}/{filename}"
                if src != dst:
                    input("WAITING TO MOVE")
                    move_file(src, dst, LIBRARY_DIR)

            # Copy extra files
            for oldFolder, filename in artist_data[album]["extras"]:
                src = f"{oldFolder}/{filename}"
                dst = f"{album_path}/{filename}"
                if src != dst:
                    input("WAITING TO MOVE")
                    move_file(src, dst, LIBRARY_DIR)

    delete_empty(LIBRARY_DIR)
