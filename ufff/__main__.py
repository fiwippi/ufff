if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-src", "--source-dir", type=str, help="Directory to scan files from", required=True)
    parser.add_argument("-dst", "--destination-dir", type=str, help="Where to copy the files with corrected folder structure to", required=True)
    args = vars(parser.parse_args())

    scan_dir = args["source_dir"]
    output_dir = args["destination_dir"]

    from pathlib import Path
    if not Path(scan_dir).exists():
        print(f"Error: Directory does not exist: '{scan_dir}'")
        exit(1)
    if not Path(output_dir).exists():
        print(f"Error: Directory does not exist: '{output_dir}'")
        exit(1)

    import ufff
    ufff.main(scan_dir, output_dir)