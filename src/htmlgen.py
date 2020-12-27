from typing import List

# TODO: fix class keyword appearing when no classes where provided


class HtmlElementStringFactory:
    @staticmethod
    def image_element(classes: List[str], src: str, alt: str = None) -> str:
        result = f'<img class="{HtmlElementStringFactory.__unpack_classes(classes)}" src="{src}" '
        result += f'alt="{alt}"' if alt is not None else ""
        result += " />"
        return result

    @staticmethod
    def lazy_image_element(classes: List[str], src: str, alt: str = None) -> str:
        result = f'<img class="{HtmlElementStringFactory.__unpack_classes(classes)}" data-src="{src}" '
        result += f'alt="{alt}"' if alt is not None else ""
        result += " />"
        return result

    @staticmethod
    def video_element(classes: List[str], src: str, controls: bool = False) -> str:
        result = f'<video class="{HtmlElementStringFactory.__unpack_classes(classes)}" {"controls" if controls else ""}>'
        result += f'<source src={src} type="video/{src.split(".")[-1]}" /></video>'
        return result

    @staticmethod
    def list_element(classes: List[str], html: str) -> str:
        return f'<li class="{HtmlElementStringFactory.__unpack_classes(classes)}">{html}</li>'

    @staticmethod
    def header(css_path: str, title: str) -> str:
        result = "<head>"
        result += '<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">'
        result += f"<title>{title}</title>"
        result += f'<link rel="stylesheet" href="{css_path}" />'
        result += "</head>"
        return result

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
        classes = (
            HtmlElementStringFactory.__unpack_classes(wrapper_class_names)
            if wrapper_class_names is not None
            else []
        )
        class_strings = f'class="{classes}"' if classes is not [] else ""
        result = f"<{wrapper} {class_strings}>"
        for el in elements:
            result += el
        result += f"</{wrapper}>"
        return result

    @staticmethod
    def link_element(classes: List[str], href: str, children: List[str]) -> str:
        result = f'<a class="{HtmlElementStringFactory.__unpack_classes(classes)}" '
        result += f'href="{href}">'
        result += f"{HtmlElementStringFactory.__unpack_classes(children)}"
        result += "</a>"
        return result

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
    def __unpack_classes(classes: List[str]) -> str:
        class_names = ""
        for class_name in classes:
            class_names += f"{class_name},"
        class_names = class_names[:-1]
        return class_names
