from charmcli.header import Header
from charmcli.hyperlink import hyperlink
from charmcli.text_styler import TextStyler

if __name__ == "__main__":
    ts = TextStyler()
    print()

    Header(title="CharmCli Features")()
    Header(
        title="Charmcli, build great CLIs. Easy to code. Based on Python type hints.",
        characters=" ",
    )()
    print()

    fg_colors = [
        "black",
        "red",
        "green",
        "yellow",
        "blue",
        "magenta",
        "cyan",
        "white",
        "black_bright",
        "red_bright",
        "green_bright",
        "yellow_bright",
        "blue_bright",
        "magenta_bright",
        "cyan_bright",
        "white_bright",
    ]

    color_title = ts.magenta(f"{'Colors':<15}")
    color_line = color_title + "".join(getattr(ts, color)("███") for color in fg_colors)
    print(color_line)
    print()

    styles_title = ts.magenta(f"{'Styles':<15}") + "All ansi styles: "
    styled_text = ", ".join(
        getattr(ts, style)(style.capitalize())
        for style in [
            "bold",
            "dim",
            "italic",
            "underline",
            "overline",
            "inverse",
            "strikethrough",
        ]
    )
    print(styles_title + styled_text + " etc")
    print()

    hyperlink_title = ts.magenta(f"{'Hyperlinks':<15}")
    author_link = hyperlink("author (callbackCat)", "https://github.com/chamanbravo")
    repo_link = hyperlink("repo (Charmcli)", "https://github.com/chamanbravo/")
    print(hyperlink_title + ts.blue(author_link) + " " + ts.blue(repo_link))
    print()

    more_title = ts.magenta(f"{'+more!':<15}")
    print(more_title + "Progress bars, tracebacks, etc and more features to be added.")
    print()
