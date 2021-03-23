from shutil import move
from pathlib import Path

def move_file(src, dst, stop_dir, overwrite=False):
    if src == dst:
        return

    src = Path(src)
    dst = Path(dst)

    if dst.exists() and str(src) == str(dst) and not overwrite:
        # print(str(src), str(dst), str(src) == str(dst))
        print("SRC: " + src.as_posix())
        print("DST: " + dst.as_posix())
        answer = input(f"Destination file already exists, overwrite? (Y/n): ")
        if answer.lower() == "n":
            return

    # Make the parent directories if needed
    dst.parent.mkdir(parents=True, exist_ok=True)

    # TODO Fix case insensitivity so a new directory is created instead of renaming the old one
    # Ensure the capitalisation of the directories is correct
    dstTree = dst.parent
    srcTree = src.parent
    while dstTree != Path(stop_dir):
        if str(dstTree.name) != str(srcTree.name):
            move(srcTree, dstTree)

        srcTree = srcTree.parent
        dstTree = dstTree.parent


    move(src, dst)

def delete_empty(dst):
    for item in Path(dst).rglob("*"):
        if item.is_dir() and len(list(item.iterdir())) == 0:
            try:
                item.rmdir()
            except PermissionError as e:
                print(f"Could not delete directory: {e}")
                continue