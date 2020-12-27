from typing import List
from indexer import FileIndexer
from os import path
from htmlgen import HtmlElementStringFactory as hesf


class WebGallery:
    def __init__(
        self,
        root_path: str,
        css_file_name: str = "style.css",
        js_file_name: str = "index.js",
    ) -> None:
        self.indexer = FileIndexer(root_path)
        self.root_path = root_path
        self.css_file_name = css_file_name
        self.js_file_name = js_file_name

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
            html_file.write(
                hesf.header(path.relpath(path.abspath("/" + self.css_file_name)), "aaa")
            )
            writeable_links = hesf.wrap_with_element("ol", links, ["links"])
            body: List[str] = []
            body.append(writeable_links)
            for file in files:
                body.append(self.__image_or_video(file, level))
            body.append(
                hesf.script_element(path.relpath(path.abspath("/" + "lazyload.min.js")))
            )
            body.append(
                hesf.script_element(path.relpath(path.abspath("/" + self.js_file_name)))
            )
            html_file.writelines(body)
            html_file.write("</html>")

    def make_css_file(self):
        with open(path.join(self.root_path, self.css_file_name), "w") as file:
            with open(r"./src/style.css") as copy_css:
                file.write(copy_css.read())

    def make_js_files(self) -> None:
        with open(path.join(self.root_path, self.js_file_name), "w") as file:
            with open(r"./src/index.js") as copy_js:
                file.write(copy_js.read())
        with open(path.join(self.root_path, "lazyload.min.js"), "w") as file:
            with open(r"./src/lazyload.min.js") as copy_js:
                file.write(copy_js.read())

    def make(self):
        self.prepare_file_tree()
        self.make_css_file()
        self.make_js_files()
        self.make_menus()

    @staticmethod
    def __image_or_video(file: str, level: int) -> str:
        file_ext = path.splitext(file)[1].lower()
        if file_ext in FileTypeExtensions.IMAGES:
            return hesf.lazy_image_element(
                ["lazy"], "\\".join(file.split("\\")[level:])
            )
        elif file_ext in FileTypeExtensions.VIDEOS:
            return hesf.video_element(
                ["lazy"], "\\".join(file.split("\\")[level:]), controls=True
            )
        return ""
