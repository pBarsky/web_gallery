import json
import logging
from os import path, scandir


class FileIndexer:
    def __init__(self, root_path: str) -> None:
        self.index = {}
        self.root_path = root_path

    def dump_to_json(self, dump_path: str) -> bool:
        logging.debug(f'{dump_path=}')
        try:
            with open(dump_path, "w") as data_file:
                json.dump(self.index, data_file)
        except IOError as error:
            print(f"Could not write to file. {error.strerror}")
            return False
        return True

    def traverse(self, dir_path: str = "", idx: dict = None, level: int = 0) -> None:
        tabs = '  ' * level
        logging.debug(f'{tabs}{dir_path=}')
        if idx is None:
            idx = self.index
        if dir_path == "":
            dir_path = self.root_path
        self.__scan_directory(dir_path, idx, level=level + 1)

    def __scan_directory(self, dir_path, idx, level: int = 0):
        tabs = '  ' * level
        logging.debug(f'{tabs}{dir_path=}')
        with scandir(dir_path) as it:
            for entry in it:
                self.__handle_file(entry, idx)
                self.__handle_subdir(dir_path, entry, idx, level=level + 1)

    def __handle_subdir(self, dir_path, entry, idx, level: int = 0):
        if entry.is_dir():
            idx[entry.name] = {}
            self.traverse(path.join(dir_path, entry.name), idx[entry.name], level=level + 1)

    @staticmethod
    def __handle_file(entry, idx):
        if not entry.is_file():
            return
        if not idx.get("files", []):
            idx["files"] = []
        idx["files"].append(entry.name)
