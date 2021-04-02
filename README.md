# web_gallery

A script to generate html pages for provided folder structure.

## Features

By default, only generates the files needed to use the gallery. User has to run his own server in the root directory of
the provided folder structure. Script traverses every directory in the tree and creates index.html files for every
directory.

## Todo

- [x] show number of subdirectories next to a link name
- [ ] let user provide path to css/js/template files from commandline
- [ ] host web server on its own rather than require user to do it
- [ ] slideshow mode
- [ ] installer

## Usage
Run python on `src/main.py` with *path to directory* as an argument.
You can also run `src/main.py` with *-h* option to show help.

```text
usage: main.py [-h] [-v] Path

Make a gallery from supplied folder structure.

positional arguments:
  Path           path to the folder structure

optional arguments:
  -h, --help     show this help message and exit
  -v, --verbose  print all processed folders
```