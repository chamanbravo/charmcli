from charmcli.text_styler import TextStyler


def hyperlink(text: str, url: str) -> str:
    return f"\033]8;;{url}\033\\{text}\033]8;;\033\\"


if __name__ == "__main__":
    author = hyperlink("author (callbackCat)", "https://github.com/chamanbravo")
    repo = hyperlink("repo (Charmcli)", "https://github.com/chamanbravo/")

    print(TextStyler().blue(author))
    print(TextStyler().blue(repo))
