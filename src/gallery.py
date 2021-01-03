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
        title = WebGallery.__get_title(dir_path)
        links: List[str] = [hesf.root_link(children=["HOME"]), hesf.back_link(dir_path)]
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

        files = WebGallery.__get_files_from_directory(dir_path, index)

        with open(
            path.join(self.root_path, dir_path, "index.html"), "w", encoding="utf-8"
        ) as html_file:
            html_file.write("<html>")
            html_file.write(
                hesf.header(path.relpath(path.abspath("/" + self.css_file_name)), title)
            )
            writeable_links = hesf.wrap_with_element("ol", links, ["links"])
            body: List[str] = []
            body.append(writeable_links)
            body.append(hesf.self_closing("hr"))
            compiled_files = [self.__image_or_video(file, level) for file in files]
            showable_files = [file for file in compiled_files if file != ""]
            number_of_files = len(showable_files)
            images_with_labels = [
                hesf.wrap_with_element(
                    wrapper_class_names=["wrapper flex flex-centered flex-wrap"],
                    wrapper="div",
                    elements=[
                        hesf.wrap_with_element(
                            "p", elements=[f"{iter[0]+1}/{number_of_files}"]
                        ),
                        iter[1],
                    ],
                )
                for iter in zip(range(number_of_files), showable_files)
            ]
            body.append(
                hesf.wrap_with_element(
                    "div",
                    images_with_labels,
                    ["files", "flex flex-centered flex-wrap"],
                )
            )
            self.add_js_files(body)
            html_file.writelines(hesf.wrap_with_element("body", body))
            html_file.write("</html>")

    def add_js_files(self, element: List[str]) -> None:
        element.append(
            hesf.script_element(path.relpath(path.abspath("/" + "lazyload.min.js")))
        )
        element.append(
            hesf.script_element(path.relpath(path.abspath("/" + self.js_file_name)))
        )

    @staticmethod
    def __get_title(dir_path: str = None) -> str:
        return dir_path.split("\\")[-1] if dir_path is not None else "Web Gallery"

    @staticmethod
    def __get_files_from_directory(dir_path: str, index: dict) -> List[str]:
        files: List[str] = []
        directory_files = index.get("files", None)
        if directory_files is not None:
            for file in directory_files:
                files.append(path.join(dir_path, file))
        return files

    def make_css_file(self) -> None:
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
                ["lazy", "file"], "\\".join(file.split("\\")[level:])
            )
        elif file_ext in FileTypeExtensions.VIDEOS:
            return hesf.video_element(
                ["lazy", "file"],
                "\\".join(file.split("\\")[level:]),
                controls=True,
            )
        return ""
