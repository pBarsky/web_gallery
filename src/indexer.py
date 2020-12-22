import json
from os import scandir, path


class FileIndexer:
    def __init__(self, root_dir: str = ".") -> None:
        self.index = {}
        self.root_dir = root_dir

    def traverse(self, dir_path: str, idx: dict = None) -> None:
        if idx is None:
            idx = self.index
        with scandir(dir_path) as it:
            for entry in it:
                if entry.is_file():
                    if idx.get("files", []) == []:
                        idx["files"] = []
                    idx["files"].append(entry.name)
                elif entry.is_dir():
                    idx[entry.name] = {}
                    self.traverse(path.join(dir_path, entry.name), idx[entry.name])


a = FileIndexer()

a.traverse("..")
with open("data.json", "w") as file:
    json.dump(a.index, file)
