import logging
import gallery
import sys
from pathlib import Path
from os import chdir
from time import time


def main():
    logging.getLogger().setLevel(logging.INFO)

    if len(sys.argv) != 2:
        logging.info(f"Usage: python {sys.argv[0]} <path_to_directory>")
        return
    file_path = Path.resolve(Path.absolute(Path(sys.argv[1])))

    source_dir = Path.resolve((Path(__file__).parent.parent))
    if not Path.is_dir(file_path):
        logging.error(f"{file_path} is not a directory")

    chdir(source_dir)
    t0 = time()
    gal = gallery.WebGallery(str(file_path))
    gal.make()
    t1 = time()
    logging.debug(f"Time elapsed: {t1 - t0:.3}s")


if __name__ == "__main__":
    main()
