import json
from os import scandir, path


class FileIndexer:
    def __init__(self, root_path: str) -> None:
        self.index = {}
        self.root_path = root_path

    def traverse(self, dir_path: str = "", idx: dict = None) -> None:
        if idx is None:
            idx = self.index
        if dir_path == "":
            dir_path = self.root_path
        with scandir(dir_path) as it:
            for entry in it:
                if entry.is_file():
                    if idx.get("files", []) == []:
                        idx["files"] = []
                    idx["files"].append(entry.name)
                elif entry.is_dir():
                    idx[entry.name] = {}
                    self.traverse(path.join(dir_path, entry.name), idx[entry.name])

    def dump_to_json(self, dump_path: str) -> bool:
        try:
            with open(dump_path, "w") as data_file:
                json.dump(self.index, data_file)
        except IOError as error:
            print(f"Could not write to file. {error.strerror}")
            return False
        return True
