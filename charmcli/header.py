import shutil
from typing import Literal

from charmcli.text_styler import TextStyler

AlignMethod = Literal["left", "center", "right"]


class Header:
    def __init__(
        self,
        title="",
        characters: str = "─",
        align: AlignMethod = "center",
        style: str = "green",
    ):
        self.title = title
        self.characters = characters
        self.align = align
        self.style = style

        if not self.supports_char(self.characters):
            self.characters = "-"

        if len(characters) < 1:
            raise ValueError(
                "'characters' argument must have a cell width of at least 1"
            )

        if align not in ("left", "center", "right"):
            raise ValueError(
                f'invalid value for align, expected "left", "center", "right" (not {align!r})'
            )

    def supports_char(self, char: str) -> bool:
        try:
            print(char, end="\r")
            return True
        except UnicodeEncodeError:
            return False

    def __call__(self, *args, **kwds):
        term_width = shutil.get_terminal_size().columns
        required_space = 2 if self.align == "center" else 1
        text_width = len(self.title) + required_space
        dash_total = max(term_width - text_width, 0)
        line = TextStyler().green(self.characters)

        if self.align == "center":
            left_line = dash_total // 2
            right_line = dash_total - left_line
            print(line * left_line + " " + self.title + " " + line * right_line)
        if self.align == "right":
            print(line * (dash_total) + " " + self.title)
        if self.align == "left":
            print(self.title + " " + line * dash_total)


if __name__ == "__main__":
    Header("chaddiman")()
