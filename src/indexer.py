import json
from os import listdir, path


class FileIndexer:
    def __init__(self, root_dir: str = "."):
        self.index = {}
        self.root_dir = root_dir

    def traverse(self, dir_path: str, idx: dict = None):
        if idx is None:
            idx = self.index
        for dir in listdir(dir_path):
            if path.isdir(path.join(dir_path, dir)):
                idx[dir] = {}
                self.traverse(path.join(dir_path, dir), idx[dir])
            else:
                if idx.get("files", []) == []:
                    idx["files"] = []
                idx["files"].append(dir)


a = FileIndexer()

a.traverse("..")
with open("data.json", "w") as file:
    json.dump(a.index, file)
