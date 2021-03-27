import logging
from os import path
from typing import List

from filetypes import FileTypeExtensions
from htmlgen import HtmlElementStringFactory as Hesf
from indexer import FileIndexer


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
        logging.info(dir_path)
        title = get_title(dir_path)
        links: List[str] = []
        make_back_buttons(dir_path, links)
        if dir_path is None:
            dir_path = "."
        if index is None:
            index = self.indexer.index
        level += 1
        self.make_submenus(dir_path, index, level, links)
        files = get_files_from_directory(dir_path, index)
        self.write_to_file(dir_path, files, level, links, title)

    def write_to_file(self, dir_path, files, level, links, title):
        with open(
                path.join(self.root_path, dir_path, "index.html"), "w", encoding="utf-8"
        ) as html_file:
            html_file.write("<html>")
            html_file.write(
                Hesf.header(path.relpath(path.abspath("/" + self.css_file_name)), title)
            )
            writeable_links = Hesf.wrap_with_element("ol", links, ["links"])
            body: List[str] = [writeable_links]
            showable_files = self.get_showable_files(files, level)
            images_with_labels = prepare_images_with_labels_html(showable_files)
            self.add_action_buttons(body, images_with_labels)
            self.append_images_with_labels(body, images_with_labels)
            self.add_js_files(body)
            html_file.writelines(Hesf.wrap_with_element("body", body))
            html_file.write("</html>")

    def append_images_with_labels(self, body, images_with_labels):
        body.append(
            Hesf.wrap_with_element(
                "div",
                images_with_labels,
                ["files", "flex flex-centered flex-wrap"],
            )
        )

    def get_showable_files(self, files, level):
        compiled_files = [image_or_video(file, level) for file in files]
        showable_files = [file for file in compiled_files if file != ""]
        return showable_files

    def add_action_buttons(self, body, images_with_labels):
        if images_with_labels:
            body.append(Hesf.self_closing("hr"))
            self.append_showhide_button(body)
            self.append_changesize_button(body)

    def append_changesize_button(self, body):
        body.append(
            Hesf.button_element(
                classes=["action-button change-size-button"],
                html="CHANGE SIZE",
                id="change-size-button",
            )
        )

    def append_showhide_button(self, body):
        body.append(
            Hesf.button_element(
                classes=["action-button show-button"],
                html="SHOW/HIDE FILES",
                id="show-button",
            )
        )

    def make_submenus(self, dir_path, index, level, links):
        for entry in index:
            if entry == "files":
                continue
            no_of_files_in_dir = len(index[entry].get("files", [])) - 1
            name = (
                f"{entry} [{no_of_files_in_dir}]" if no_of_files_in_dir != 0 else entry
            )
            links.append(
                Hesf.link_element(href=entry, children=[Hesf.list_element(html=name)])
            )
            self.make_menus(path.join(dir_path, entry), index[entry], level)

    def add_js_files(self, element: List[str]) -> None:
        element.append(
            Hesf.script_element(path.relpath(path.abspath("/" + "lazyload.min.js")))
        )
        element.append(
            Hesf.script_element(path.relpath(path.abspath("/" + self.js_file_name)))
        )

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


def image_or_video(file: str, level: int) -> str:
    file_ext = path.splitext(file)[1].lower()
    if file_ext in FileTypeExtensions.IMAGES:
        return Hesf.lazy_image_element(
            ["lazy", "file"], "\\".join(file.split("\\")[level:])
        )
    elif file_ext in FileTypeExtensions.VIDEOS:
        return Hesf.lazy_video_element(
            ["lazy", "file"],
            "\\".join(file.split("\\")[level:]),
            controls=True,
        )
    return ""


def get_files_from_directory(dir_path: str, index: dict) -> List[str]:
    files: List[str] = []
    directory_files = index.get("files", None)
    if directory_files is not None:
        for file in directory_files:
            files.append(path.join(dir_path, file))
    return files


def make_back_buttons(dir_path, links):
    if dir_path is not None:
        links.append(Hesf.root_link(children=[Hesf.list_element(html="HOME")]))
    back_link = Hesf.back_link(
        dir_path=dir_path, children=[Hesf.list_element(html="BACK")]
    )
    if back_link != "":
        links.append(back_link)


def get_title(dir_path: str = None) -> str:
    return dir_path.split("\\")[-1] if dir_path is not None else "Web Gallery"


def prepare_images_with_labels_html(showable_files):
    number_of_files = len(showable_files)

    return [
        Hesf.wrap_with_element(
            wrapper_class_names=["wrapper flex flex-centered flex-wrap"],
            wrapper="div",
            elements=[
                Hesf.wrap_with_element(
                    "p", elements=[f"{iter[0] + 1}/{number_of_files}"]
                ),
                iter[1],
            ],
        )
        for iter in zip(range(number_of_files), showable_files)
    ]
