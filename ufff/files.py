from shutil import move
from pathlib import Path

def move_file(src, dst, stop_dir, overwrite=False):
    src, dst = Path(src), Path(dst)
    if overwrite == False and dst.exists():
        print("SRC: " + src.as_posix())
        print("DST: " + dst.as_posix())
        answer = input(f"Destination file already exists, overwrite? (y/N): ")
        if answer.lower() != "y":
            print("Not Overwriting...")
            return

    # Make the parent directories if needed
    dst.parent.mkdir(parents=True, exist_ok=True)

    # We need to rename the parent folders since they're the wrong case
    src_parent, dst_parent = src.parent, dst.parent
    if str(src_parent).lower() == str(dst_parent).lower() and str(src_parent) != str(dst_parent):
        while dst_parent != Path(stop_dir):
            if str(dst_parent.name) != str(src_parent.name):
                try:
                    move(src_parent, dst_parent)
                except PermissionError as e:
                    print(f"Could not rename folder from {src_parent} to {dst_parent} with error: {e}")
                    return

            src_parent = src_parent.parent
            dst_parent = dst_parent.parent

    move(src, dst)

def delete_empty(dst):
    for item in Path(dst).rglob("*"):
        if item.is_dir() and len(list(item.iterdir())) == 0:
            try:
                item.rmdir()
            except PermissionError as e:
                print(f"Could not delete directory: {e}")
                continue