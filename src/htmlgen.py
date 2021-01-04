from os import stat_result
from typing import List

# TODO: fix class keyword appearing when no classes where provided


class HtmlElementStringFactory:
    @staticmethod
    def image_element(
        classes: List[str] = None, src: str = "\\", alt: str = None
    ) -> str:
        class_string = HtmlElementStringFactory.make_class_string(classes)
        result = f'<img {class_string}" src="{src}" '
        result += f'alt="{alt}"' if alt is not None else ""
        result += " />"
        return result

    @staticmethod
    def lazy_image_element(classes: List[str], src: str, alt: str = None) -> str:
        class_string = HtmlElementStringFactory.make_class_string(classes)
        result = f'<img {class_string}" data-src="{src}" '
        result += f'alt="{alt}"' if alt is not None else ""
        result += " />"
        return result

    @staticmethod
    def video_element(
        classes: List[str] = None, src: str = "\\", controls: bool = False
    ) -> str:
        class_string = HtmlElementStringFactory.make_class_string(classes)
        result = f'<video {class_string} {"controls" if controls else ""}>'
        result += f'<source src={src} type="video/{src.split(".")[-1]}" /></video>'
        return result

    @staticmethod
    def make_class_string(classes: List[str] = None) -> str:
        return (
            f'class="{HtmlElementStringFactory.__unpack_classes(classes)}"'
            if classes is not None
            else ""
        )

    @staticmethod
    def list_element(classes: List[str] = None, html: str = "") -> str:
        class_string = class_string = HtmlElementStringFactory.make_class_string(
            classes
        )
        return f'<li {class_string}">{html}</li>'

    @staticmethod
    def header(css_path: str, title: str) -> str:
        result = "<head>"
        result += '<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">'
        result += f"<title>{title}</title>"
        result += f'<link rel="stylesheet" href="{css_path}" />'
        result += "</head>"
        return result

    @staticmethod
    def self_closing(element: str, classes: List[str] = None) -> str:
        class_string = HtmlElementStringFactory.make_class_string(classes)
        return f"<{element} {class_string}/>"

    @staticmethod
    def body(classes: List[str], elements: List[str]) -> str:
        return HtmlElementStringFactory.wrap_with_element("body", elements, classes)

    @staticmethod
    def footer(classes: List[str], elements: List[str]) -> str:
        return HtmlElementStringFactory.wrap_with_element("footer", elements, classes)

    @staticmethod
    def wrap_with_element(
        wrapper: str, elements: List[str], wrapper_class_names: List[str] = None
    ):
        class_string = HtmlElementStringFactory.make_class_string(wrapper_class_names)
        result = f"<{wrapper} {class_string}>"
        for el in elements:
            result += str(el)
        result += f"</{wrapper}>"
        return result

    @staticmethod
    def link_element(
        classes: List[str] = None, href: str = "", children: List[str] = [""]
    ) -> str:
        class_string = HtmlElementStringFactory.make_class_string(classes)
        result = f"<a {class_string}"
        result += f'href="{href}">'
        result += f"{HtmlElementStringFactory.__unpack_classes(children)}"
        result += "</a>"
        return result

    @staticmethod
    def button_element(classes: List[str] = None, html: str = ""):
        class_string = HtmlElementStringFactory.make_class_string(classes)
        return f"<button {class_string}>{html}</button>"

    @staticmethod
    def root_link(children: List[str], classes: List[str] = None) -> str:
        return HtmlElementStringFactory.link_element(classes, "\\", children)

    @staticmethod
    def script_element(src: str, content: List[str] = None) -> str:
        if_src = f'src="{src}"' if src != "" else ""
        stacked_content = ""
        if content is not None:
            for line in content:
                stacked_content += line
        result = f'<script type="text/javascript" {if_src}>{stacked_content}</script>'
        return result

    @staticmethod
    def back_link(children: List[str], dir_path: str = None) -> str:
        if dir_path is None:
            return ""

        test_url = [""]
        test_url.extend([*dir_path.split("\\")[1:-1]])
        url = test_url
        if test_url == [""]:
            url = ["\\"]
        return HtmlElementStringFactory.link_element(
            href="\\".join(url), children=children
        )

    @staticmethod
    def __unpack_classes(classes: List[str]) -> str:
        class_names = ""
        for class_name in classes:
            class_names += f"{class_name} "
        class_names = class_names[:-1]
        return class_names
