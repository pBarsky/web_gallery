from typing import List
from indexer import FileIndexer
from os import path
from htmlgen import HtmlElementStringFactory as hesf


class WebGallery:
    def __init__(self, root_path: str, css_file_name: str = "style.css") -> None:
        self.indexer = FileIndexer(root_path)
        self.root_path = root_path
        self.css_file_name = css_file_name

    def prepare_file_tree(self):
        self.indexer.traverse()
        self.indexer.dump_to_json(path.join(self.root_path, "tree.json"))

    def make_menus(self, dir_path: str = None, index: dict = None, level: int = 0):
        # separator = "\t"
        # indent = separator * level
        # file_indent = separator * (level + 1)
        links: List[str] = []
        files: List[str] = []
        if dir_path is None:
            dir_path = "."
        if index is None:
            index = self.indexer.index

        # print(f"{indent}{dir_path}")
        for entry in index:
            if entry == "files":
                continue
            links.append(path.join(dir_path, entry))
            self.make_menus(path.join(dir_path, entry), index[entry], level + 1)

        directory_files = index.get("files", None)
        if directory_files is None:
            return
        # print(f"{indent}{dir_path}/[Files]")
        for file in directory_files:
            files.append(path.join(dir_path, file))
            # print(f"{file_indent}{path.join(dir_path,file)}")
        with open(path.join(self.root_path, dir_path, "index.html"), "w") as html_file:
            html_file.write("<html>")
            for link in links:
                html_file.write(hesf.link_element([""], link, [link]))
            for file in files:
                html_file.write(
                    hesf.image_element([""], "\\".join(file.split("\\")[level:]))
                )
            html_file.write("</html>")

    def make_css_file(self):
        with open(path.join(self.root_path, self.css_file_name), "w") as file:
            with open(r"./src/style.css") as copy_css:
                file.write(copy_css.read())


# tester = WebGallery("test")
tester = WebGallery(".sample_data")
tester.prepare_file_tree()
tester.make_menus()
# tester.make_css_file()
