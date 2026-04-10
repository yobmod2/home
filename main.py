from typing import TYPE_CHECKING, Any, Literal, TypeAlias

import numpy as np

from utils import notate

if TYPE_CHECKING:
    from numpy.typing import NDArray

type IntArray = NDArray[np.int_]
type IntList = list[int]

arr: IntArray = np.asarray([1, 5, 3, 5, 6, 9, 2, 2, 2, 2, 2])


def foo[T: str | bool, S: object](
    data: T,
    alphabettyspaghetti: S,
    somemoredat: str = "",
) -> tuple[T, S]:
    return data, alphabettyspaghetti


def main(a: str) -> None:
    print("Hello from home!")


if __name__ == "__main__":
    a: tuple[Literal[True], IntArray] = foo(True, arr)
    b = foo(True, {"ok": 2})
