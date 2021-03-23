import argparse
from pathlib import Path
from ufff.metadata import retrieve_metadata
from ufff.files import move_file, delete_empty
from ufff.utils import load_mutagen, is_audio_file, sanitise

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-src", "--source-dir", type=str, help="Directory to scan files from", required=True)
    parser.add_argument("-dst", "--destination-dir", type=str, help="Where to copy the files with corrected folder structure to", required=True)
    args = vars(parser.parse_args())

    scan_dir = args["source_dir"]
    output_dir = args["destination_dir"]

    data = {}
    visited_folders = set() # Keeps track of which folders have been checked for additional files

    items =  list(Path(scan_dir).rglob("*"))
    if len(items) == 0:
        print(f"No files/folders in: {scan_dir}")
        exit(0)

    for item in items:
        if item.is_dir():
            continue

        if is_audio_file(item):
            # Load the file
            mutagen_file = load_mutagen(item)

            # Retrieve the tags we want
            filename = item.name # Filename
            album, album_artist, date, codec, title, tracknum = retrieve_metadata(mutagen_file, filename)

            # Album artist tag is required
            if album_artist == None:
                print(f"No \"album artist\" tag in file \"{item}\"")
                continue
            # Album tag is required
            if album == None:
                print(f"No \"album\" tag in file \"{item}\"")
                continue
            # Title tag is required
            if title == None:
                print(f"No \"title\" tag in file \"{item}\"")
                continue

            # Enables these keys to be hashable by ensuring they're strings
            # This check should only happen after they're confirmed to exist
            # Also cleans up album/artist/title names by removing whitespaces
            album_artist, album, title = str(album_artist), str(album), str(title)
            # Notifies user if extra whitespace is found in the core tags
            if album_artist != album_artist.strip():
                album_artist = album_artist.strip()
                print(f"Album artist tag for {item} has whitespace")
            if album != album.strip():
                album = album.strip()
                print(f"Album tag for {item} has whitespace")
            if title != title.strip():
                title = title.strip()
                print(f"Title tag for {item} has whitespace")

            # Ensure the Album and Album Artist keys exist in the data dictionary
            if album_artist not in data:
                data[album_artist] = {}
            if album not in data[album_artist]:
                data[album_artist][album] = {"date": set(), "codecs": set(), "songs": [], "extras": []}

            # Create a sanitised audio filename
            audio_filename = ""
            if tracknum != None:
                audio_filename = sanitise(f"{tracknum} {title}{item.suffix}")
            else:
                audio_filename = sanitise(f"{title}{item.suffix}")

            # Add the metadata to the data struct
            data[album_artist][album]["codecs"].add(codec)
            if date != "":
                data[album_artist][album]["date"].add(date)
            data[album_artist][album]["songs"].append([item.as_posix(), audio_filename])

            # Include additional files, e.g. covers. Anything in the same
            # directory as the audio file counts as an additional file
            if item.parent.as_posix() not in visited_folders:
                visited_folders.add(item.parent.as_posix())

                for extra in item.parent.iterdir():
                    if not extra.is_dir() and not is_audio_file(extra):
                        data[album_artist][album]["extras"].append([extra.parent.as_posix(), sanitise(extra.name)])

    # Once metadata is collected about each file they're processed and moved to a correctly named folder
    for artist in data:
        for album in data[artist]:
            codec = "-".join(sorted(data[artist][album]["codecs"]))
            date = "-".join(sorted(data[artist][album]["date"]))

            album_dirname = sanitise(f"{artist} – {album}{' (' + date + ') ' if date else ' '}[{codec}]")
            folder_path = (f"{Path(output_dir).as_posix()}/{sanitise(artist)}/{album_dirname}")

            # Copy songs
            for src, filename in data[artist][album]["songs"]:
                dst = f"{folder_path}/{filename}"
                if src != dst:
                    move_file(src, dst, output_dir)

            # Copy additional files
            for folder, filename in data[artist][album]["extras"]:
                src = f"{folder}/{filename}"
                dst = f"{folder_path}/{filename}"
                if src != dst:
                    move_file(src, dst, output_dir)

    # Removes all empty directories
    delete_empty(scan_dir)
