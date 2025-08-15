import traceback
from types import TracebackType
from typing import Optional, Type

from charmcli.text_styler import TextStyler


def charmcli_excepthook(
    exc_type: Type[BaseException],
    exc_value: BaseException,
    exc_tb: Optional[TracebackType],
) -> None:
    ts = TextStyler()
    tb = traceback.extract_tb(exc_tb)

    for filename, lineno, func, text in tb:
        print("")
        file = filename.split("\\")[-1]
        print(
            f"{ts.style('green')(lineno)} {ts.style('blue')(func)} {ts.style('cyan')(file)}"
        )
        print(f"{ts.style('gray')(f'{filename}, line {lineno}')}")
        if text:
            print(f"   {ts.style('red')('>')} {text.strip()}")

    print("")
    print(f"{ts.style('red')(exc_type.__name__)}: {ts.style('yellow')(exc_value)}\n")
