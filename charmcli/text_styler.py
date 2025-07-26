from typing import Any, ClassVar, Literal

StyleName = Literal[
    "bold",
    "dim",
    "italic",
    "underline",
    "overline",
    "inverse",
    "hidden",
    "strikethrough",
    # colors
    "black",
    "red",
    "green",
    "yellow",
    "blue",
    "magenta",
    "cyan",
    "white",
    "black_bright",
    "gray",
    "grey",
    "red_bright",
    "green_bright",
    "yellow_bright",
    "blue_bright",
    "magenta_bright",
    "cyan_bright",
    "white_bright",
    # bg_colors
    "bg_black",
    "bg_red",
    "bg_green",
    "bg_yellow",
    "bg_blue",
    "bg_magenta",
    "bg_cyan",
    "bg_white",
    "bg_gray",
    "bg_black_bright",
    "bg_red_bright",
    "bg_green_bright",
    "bg_yellow_bright",
    "bg_blue_bright",
    "bg_magenta_bright",
    "bg_cyan_bright",
    "bg_white_bright",
]


class TextStyler:
    styles: ClassVar[dict[str, list[int]]] = {
        "_reset": [0, 0],
        "bold": [1, 22],
        "dim": [2, 22],
        "italic": [3, 23],
        "underline": [4, 24],
        "overline": [53, 55],
        "inverse": [7, 27],
        "hidden": [8, 28],
        "strikethrough": [9, 29],
        # colors
        "black": [30, 39],
        "red": [31, 39],
        "green": [32, 39],
        "yellow": [33, 39],
        "blue": [34, 39],
        "magenta": [35, 39],
        "cyan": [36, 39],
        "white": [37, 39],
        "black_bright": [90, 39],
        "gray": [90, 39],
        "grey": [90, 39],
        "red_bright": [91, 39],
        "green_bright": [92, 39],
        "yellow_bright": [93, 39],
        "blue_bright": [94, 39],
        "magenta_bright": [95, 39],
        "cyan_bright": [96, 39],
        "white_bright": [97, 39],
        # bg_colors
        "bg_black": [40, 49],
        "bg_red": [41, 49],
        "bg_green": [42, 49],
        "bg_yellow": [43, 49],
        "bg_blue": [44, 49],
        "bg_magenta": [45, 49],
        "bg_cyan": [46, 49],
        "bg_white": [47, 49],
        "bg_gray": [100, 49],
        "bg_black_bright": [100, 49],
        "bg_red_bright": [101, 49],
        "bg_green_bright": [102, 49],
        "bg_yellow_bright": [103, 49],
        "bg_blue_bright": [104, 49],
        "bg_magenta_bright": [105, 49],
        "bg_cyan_bright": [106, 49],
        "bg_white_bright": [107, 49],
    }

    def __init__(self, styles: list[str] = []):
        self._styles = styles or []

    def text(self, string: str):
        text_styles = [self.styles.get(style, "") for style in self._styles]
        starting, ending = "", ""
        for s, e in text_styles:
            starting += f"\033[{s}m"
            ending += f"\033[{e}m"
        return starting + str(string) + ending

    def __getattr__(self, name: StyleName):
        return self.__class__(self._styles + [name])

    def __call__(self, *args: Any, **kwds: Any):
        return self.text(*args, **kwds)


if __name__ == "__main__":
    ts = TextStyler()
    print(ts.blue("Normal colored text"))
    print(ts.red("Normal colored text"))
    print(ts.green("Normal colored text"))
    print(ts.yellow("Normal colored text"))
    print(ts.hidden("Hidden text"))
    print(ts.blue.inverse("Normal colored text"))
    print(ts.red.inverse("Normal colored text"))
    print(ts.green.inverse("Normal colored text"))
    print(ts.yellow.inverse("Normal colored text"))
