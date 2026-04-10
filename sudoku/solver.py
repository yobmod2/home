import csv
import json
import logging
import time
import unittest
from copy import deepcopy
from pathlib import Path

from input_grids import PUZZLES

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s: %(message)s",
)

# create logger named "solver"
logger = logging.getLogger(__name__)

OUTPUT_DIR = Path(__file__).parent / "output"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


class SudokuSolver:
    """Backtracking Sudoku solver using the Python standard library."""

    def __init__(
        self,
        grid: list[list[int]],
        save_as_json: bool = False,
        save_as_csv: bool = False,
        save_logs_to_file: bool = False,
        name: str = "",
    ) -> None:
        self.input_grid = grid
        self.grid = deepcopy(grid)

        self.solved_grid = list[list[int]] | None  # set to ._is_solved() when call .solve()
        self.duration: float = 0.0  # set in .solve() if ._is_solved()

        self.name = name
        self.save_as_json = save_as_json
        self.save_as_csv = save_as_csv
        self.save_logs_to_file = save_logs_to_file

        self.config_logger()  # Call before any validation if want error logging
        self._is_valid_input()

        if self.save_as_csv and not self.name:
            raise ValueError("Require 'name' arg to use as csv filename")

    def config_logger(self, filename: str = "solver_logs.txt") -> None:
        if self.save_logs_to_file:
            handler = logging.FileHandler(str(OUTPUT_DIR / filename), mode="a")
            handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s: %(message)s"))
            logging.getLogger(__name__).addHandler(handler)

    @staticmethod
    def validate_input_grid(grid: list[list[int]]) -> bool:
        """Static method to validate input grids"""
        return (
            isinstance(grid, list)
            and all(isinstance(row, list) for row in grid)
            and len(grid) == 9
            and all(len(row) == 9 for row in grid)
            and all(isinstance(value, int) for row in grid for value in row)
            and all(0 <= value <= 9 for row in grid for value in row)
        )

    def _is_valid_input(self) -> bool:
        """Instance method for validating input grid"""
        if not self.validate_input_grid(self.input_grid):
            msg = f"InputError: Sudoku grid should be a list of 9 lists of 9 ints. \nReceived {self.input_grid}"
            logger.error(msg)
            raise TypeError(msg)
        else:
            return True

    def solve(self) -> list[list[int]]:
        start_time = time.perf_counter()
        if not self._search():
            raise ValueError("Sudoku puzzle is unsolvable")
        self.duration = time.perf_counter() - start_time
        logger.info(f"{self.name} solved in {self.duration:.6f} seconds")
        if self._is_solved():
            self.solved_grid = self.grid
            suffix = "solved"
        else:
            suffix = "failed"
        if self.save_as_csv and self.name:
            self.save_csv(f"{self.name}_{suffix}.csv")

        return self.grid

    def _find_empty(self) -> tuple[int, int] | None:
        """Get position of empty values"""
        for row in range(9):
            for col in range(9):
                if self.grid[row][col] == 0:
                    return row, col
        return None

    def _search(self) -> bool:
        """Insert values into an empty position until valid found"""
        empty = self._find_empty()
        if empty is None:
            return True
        row, col = empty
        for value in range(1, 10):
            if self._is_valid_value(value, row, col):
                self.grid[row][col] = value
                if self._search():
                    return True
                self.grid[row][col] = 0
        return False

    def _is_valid_value(self, value: int, row: int, col: int) -> bool:
        """check if value is valid for a given position"""
        if any(self.grid[row][c] == value for c in range(9)):
            return False
        if any(self.grid[r][col] == value for r in range(9)):
            return False
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for r in range(start_row, start_row + 3):
            for c in range(start_col, start_col + 3):
                if self.grid[r][c] == value:
                    return False
        return True

    def _check_rows(self) -> bool:
        for row in range(9):
            seen = set()
            for value in self.grid[row]:
                if value == 0:
                    continue
                if value in seen:
                    return False
                seen.add(value)
        return True

    def _check_cols(self) -> bool:
        for col in range(9):
            seen = set()
            for row in range(9):
                value = self.grid[row][col]
                if value == 0:
                    continue
                if value in seen:
                    return False
                seen.add(value)
        return True

    def _check_boxes(self) -> bool:
        for block_row in range(0, 9, 3):
            for block_col in range(0, 9, 3):
                seen = set()
                for row in range(block_row, block_row + 3):
                    for col in range(block_col, block_col + 3):
                        value = self.grid[row][col]
                        if value == 0:
                            continue
                        if value in seen:
                            return False
                        seen.add(value)
        return True

    def _is_filled(self) -> bool:
        return all(1 <= value <= 9 for row in self.grid for value in row)

    def _is_solved(self) -> bool:
        return self._check_rows() and self._check_cols() and self._check_boxes() and self._is_filled()

    def save_json(self, filename: str, grid: list[list[int]] | None = None) -> str:
        path = OUTPUT_DIR / filename
        data = grid if grid is not None else self.grid
        with path.open("w", encoding="utf-8") as json_file:
            json.dump(data, json_file, indent=2)
        logger.info(f"Saved JSON to {path}")
        return str(path)

    def save_csv(self, filename: str, grid: list[list[int]] | None = None) -> str:
        path = OUTPUT_DIR / filename
        data = grid if grid is not None else self.grid
        with path.open("w", encoding="utf-8", newline="") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerows(self.input_grid)
            writer.writerows(["", "", ""])
            writer.writerows(data)
        logger.info(f"Saved CSV to {path}")
        return str(path)


TEST_PUZZLES = {
    "test": [  # 0.000 sec
        [9, 8, 0, 0, 0, 0, 0, 0, 0],
        [7, 0, 0, 0, 0, 6, 5, 0, 0],
        [0, 5, 0, 0, 0, 0, 9, 6, 0],
        [0, 0, 4, 0, 8, 0, 0, 3, 0],
        [0, 0, 0, 0, 6, 7, 8, 0, 0],
        [0, 7, 0, 3, 0, 0, 0, 0, 9],
        [0, 0, 0, 0, 5, 0, 0, 0, 6],
        [0, 0, 0, 6, 0, 9, 3, 8, 0],
        [0, 0, 2, 0, 0, 3, 0, 7, 0],
    ],
}

TEST_PUZZLES = PUZZLES


class TestSudokuSolver(unittest.TestCase):
    def test_puzzles_validate_input(self) -> None:
        for name, puzzle in TEST_PUZZLES.items():
            solver = SudokuSolver(puzzle, save_as_csv=True, save_logs_to_file=True, name=name)
            self.assertTrue(SudokuSolver.validate_input_grid(puzzle), f"{name} Sudoku shape or values not valid")
            self.assertTrue(solver._is_valid_input(), f"{name} Instantiated without valid input")

    def test_puzzles_solve(self) -> None:
        for name, puzzle in TEST_PUZZLES.items():
            solver = SudokuSolver(puzzle, save_as_csv=True, save_logs_to_file=True, name=name)
            solver.solve()
            # solver.save_json(f"{name}_solved.json", solved)
            self.assertTrue(solver._is_solved(), f"{name} puzzle did not solve correctly")


if __name__ == "__main__":
    # unittest.main()
    name = "easy"  # key name of a grid in puzzles dict
    solver = SudokuSolver(
        TEST_PUZZLES[name],
        save_as_csv=True,
        save_logs_to_file=True,
        name=name,
    ).solve()
