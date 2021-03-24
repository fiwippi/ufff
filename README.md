# ufff
## Overview
**ufff** will structure songs into folders based on song metadata

## Install
```console
# Clone the repo
$ git clone https://github.com/fiwippi/ufff.git

# Change the working directory to ufff
$ cd ufff

# Install the requirements
$ python3 -m pip install -r requirements.txt
```

## Usage
```console
$ python3 ufff --help
usage: python ufff [-h] -src SOURCE_DIR -dst DESTINATION_DIR

arguments:
  -h, --help            show this help message and exit
  -src SOURCE_DIR, --source-dir SOURCE_DIR
                        Directory to scan files from
  -dst DESTINATION_DIR, --destination-dir DESTINATION_DIR
                        Where to copy the files with corrected folder structure to
```

## Folder Structure
### Naming
The folder naming follow: `/Artist/Artist – Album Title (Year) [Encoding]/Track No. Song Title`

### Example Tree
```
├── iri
│   ├── iri – Life EP (2017) [FLAC]
│   │   └── 05 会いたいわ.flac
│   └── iri – Shade (2019) [FLAC]
│       └── 03 Wonderland.flac
├── isagen
│   └── isagen – c.b.a.g. EP (2018) [FLAC]
│       └── 03 Child.flac
├── momü
│   └── momü – at arm's length... (2018) [FLAC]
│       ├── 01 at arm's length....flac
│       └── cover.jpg
```

## Notes
- The program requires 3 tags to be present for each song:
    - `Album`
    - `Album Artist`
    - `Title`
- Behaviour with hidden files is undefined
- The program also copied additional files, e.g. cover.jpg into the created album folder. 
If multiple songs from different albums are in the src folder, and are not separated by
folders, then all additional files will be associated with the first song processed
  
## License
`MIT`