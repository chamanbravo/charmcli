from typing import Any, ClassVar, Tuple


class TextStyler:
    styles: ClassVar[dict[str, Tuple[int, int]]] = {
        "bold": (1, 22),
        "dim": (2, 22),
        "italic": (3, 23),
        "underline": (4, 24),
        "overline": (53, 55),
        "inverse": (7, 27),
        "hidden": (8, 28),
        "strikethrough": (9, 29),
        "black": (30, 39),
        "red": (31, 39),
        "green": (32, 39),
        "yellow": (33, 39),
        "blue": (34, 39),
        "magenta": (35, 39),
        "cyan": (36, 39),
        "white": (37, 39),
        "black_bright": (90, 39),
        "gray": (90, 39),
        "grey": (90, 39),
        "red_bright": (91, 39),
        "green_bright": (92, 39),
        "yellow_bright": (93, 39),
        "blue_bright": (94, 39),
        "magenta_bright": (95, 39),
        "cyan_bright": (96, 39),
        "white_bright": (97, 39),
        "bg_black": (40, 49),
        "bg_red": (41, 49),
        "bg_green": (42, 49),
        "bg_yellow": (43, 49),
        "bg_blue": (44, 49),
        "bg_magenta": (45, 49),
        "bg_cyan": (46, 49),
        "bg_white": (47, 49),
        "bg_gray": (100, 49),
        "bg_black_bright": (100, 49),
        "bg_red_bright": (101, 49),
        "bg_green_bright": (102, 49),
        "bg_yellow_bright": (103, 49),
        "bg_blue_bright": (104, 49),
        "bg_magenta_bright": (105, 49),
        "bg_cyan_bright": (106, 49),
        "bg_white_bright": (107, 49),
    }

    def __init__(self, applied_styles: Tuple[str, ...] = ()):
        self._styles = applied_styles

    def style(self, *styles: str) -> "TextStyler":
        for s in styles:
            if s not in self.styles:
                raise ValueError(f"Unknown style: {s}")
        return TextStyler(self._styles + styles)

    def text(self, string: Any) -> str:
        start = "".join(f"\033[{self.styles[s][0]}m" for s in self._styles)
        end = "".join(f"\033[{self.styles[s][1]}m" for s in reversed(self._styles))
        return f"{start}{string}{end}"

    def __call__(self, string: Any) -> str:
        return self.text(string)

    @classmethod
    def reset(cls, string: Any) -> str:
        s, e = (0, 0)
        return f"\033[{s}m{string}\033[{e}m"


if __name__ == "__main__":
    ts = TextStyler()
    print(ts.style("blue")("Blue text"))
    print(ts.style("red", "bold")("Red + bold"))
    print(ts.style("green", "underline")("Green + underline"))
    print(ts.style("yellow", "inverse")("Yellow inverted"))
    print(ts.style("hidden")("Hidden text"))
    print(TextStyler.reset("Back to normal"))
