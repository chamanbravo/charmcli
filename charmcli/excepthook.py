import traceback

from charmcli.text_styler import TextStyler


def charmcli_excepthook(exc_type, exc_value, exc_tb):
    ts = TextStyler()
    tb = traceback.extract_tb(exc_tb)

    for filename, lineno, func, text in tb:
        print("")
        file = filename.split("\\")[-1]
        print(f"{ts.green(lineno)} {ts.blue(func)} {ts.cyan(file)}")
        print(f"{ts.gray(f'{filename}, ' + f'line {lineno}')}")

        if text:
            print(f"   {ts.red('>')} {text.strip()}")

    print("")
    print(f"{ts.red(exc_type.__name__)}: {ts.yellow(exc_value)}\n")
