"""Functions to print function name and docstring and add additional notes.
Contains:\n

\t FORMAT - dataclass of string formatting codes
\t notate() - decorator function
\t test() - example function to show output
\t TODO: notate partial function
"""

import functools
from dataclasses import dataclass
from typing import TYPE_CHECKING, ParamSpec, TypeVar

if TYPE_CHECKING:
    from collections.abc import Callable


@dataclass
class FORMAT:
    VIOLET = "\033[95m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    WHITE = "\033[97m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    ENDFMT = "\033[0m"
    NONE: str = ""


def notate[**P, R](  # P = ParamSpec("P"); R = TypeVar("R")
    notate: bool,
    *,
    docs: bool = True,
    note: str = "",
    warn: str = "",
    name_fmt: str = FORMAT.BOLD,
    docs_fmt: str = FORMAT.NONE,
    note_fmt: str = FORMAT.YELLOW,
    warn_fmt: str = FORMAT.RED + FORMAT.BOLD,
) -> Callable[[Callable[P, R]], Callable[P, R]]:
    # wrapper for functions to print their docstring if docs is True
    def outer_wrapper(func: Callable[P, R]) -> Callable[P, R]:
        # wraps to preserve the original function's metadata (like __name__ and __doc__)
        @functools.wraps(func)
        def inner_wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            if notate:
                print(f"{name_fmt}{func.__name__}{args} kwargs: {kwargs}{FORMAT.ENDFMT}")
                if docs:
                    print(f"\t{docs_fmt} Doc:  {func.__doc__}{FORMAT.ENDFMT}")
                if note:
                    print(f"\t{note_fmt} Note: {note}{FORMAT.ENDFMT}")
                if warn:
                    print(f"\t{warn_fmt} Warning: {warn}{FORMAT.ENDFMT}")
            return func(*args, **kwargs)

        return inner_wrapper

    return outer_wrapper


# class Notator():
#     def __init__(self):
#         self.notate = notate()
#         self.FORMAT = FORMAT


@notate(True, note="test notation", warn="test WARNING!")
def test(test_kw: str = "kw_str") -> int:
    """test docstring"""
    return 1


if __name__ == "__main__":
    test(test_kw="arg")
