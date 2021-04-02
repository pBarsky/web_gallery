import argparse
import logging
from os import chdir
from pathlib import Path
from time import time

import gallery

def main():
    logging.getLogger().setLevel(logging.INFO)

    args = parse_opts()

    file_path = Path.resolve(Path.absolute(Path(*args.path)))

    source_dir = Path.resolve((Path(__file__).parent.parent))
    if not Path.is_dir(file_path):
        logging.error(f"{file_path} is not a directory")
    logging.info("Changing directory...")
    chdir(source_dir)
    logging.info("Starting indexing...")
    t0 = time()
    gal = gallery.WebGallery(str(file_path), verbose=args.verbose)
    gal.make()
    t1 = time()
    logging.debug(f"Time elapsed: {t1 - t0:.3}s")


def parse_opts():
    parser = argparse.ArgumentParser(description="Make a gallery from supplied folder structure.")
    parser.add_argument('path', metavar='Path', type=str, nargs=1, help='path to the folder structure')
    parser.add_argument("-v", '--verbose', action="store_true",
                        help='print all processed folders')
    return parser.parse_args()


if __name__ == "__main__":
    main()
