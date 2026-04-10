from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import TypedDict, cast

import tomlkit

from utils.notate import notate

sys.path.append("./")


class ColorVals(TypedDict):
    rgb: tuple[int, int, int]
    hex: str


ColorDict = dict[str, ColorVals]


class ColorSchema(TypedDict):
    name: str
    rgbValues: list[int]
    hexValue: str


@notate(True, note="output schema: {color_name: {rgb: tuple, hex: str}}")
def load_colors(input_dir: Path | None = None, filename: str = "colors_input.json") -> ColorDict:
    """Load colors from input_dir/filename json file into a dict[str, ColorVals].
    Default filepath = ./colors_input.json"""

    json_dir = input_dir if input_dir is not None else Path(__file__).resolve().parent
    json_path = json_dir / filename

    if not json_path.exists():
        raise ImportError(f"{json_path=}")

    with json_path.open("r", encoding="utf-8") as f:
        col_dict: ColorDict = {}
        data: list[ColorSchema] = json.load(f)
        for entry in data:
            name_ = entry["name"]
            rgb_ = cast(tuple[int, int, int], tuple(entry["rgbValues"]))
            hex_ = entry["hexValue"]
            new_entry: dict[str, ColorVals] = {name_: {"rgb": rgb_, "hex": hex_}}
            col_dict.update(new_entry)

    assert col_dict["red"] == {"rgb": (255, 0, 0), "hex": "#ff0000"}
    return col_dict


if __name__ == "__main__":
    colors = load_colors()
    # print(colors.keys())

    col_json = json.dumps(colors)
    # print(col_json)

    col_toml = tomlkit.dumps(colors)
    print(col_toml)
