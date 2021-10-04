#!/usr/bin/env python3
"""Conway's Game of Life --

My initial reaction is this:

Each iteration produces a queue of live cells,
indexed by (x, y) coordinates. We then insert all the live cells
into a queue of live candidates, creating a fresh seen set for each
iteration. We then perform a single-step variant of BFS for each live candidate,
which yields neighbor live candidates while checking if the current cell
is alive in the next iteration. Once we exhaust BFS we return to the
queue to repeat the process until we have no more live candidates.
Then we start the next iteration and repeat.

Some considerations:
- Since the board size is defined in terms of unsigned 64 bit ints -
    we have a boundary, and boundary cases need to be considered.
"""
import os
import sys
from typing import Iterable, List, Set, Tuple

import click
from loguru import logger


class GameOfLife:
    # If CPython is compiled for a 64-bit arch
    # then MAX == sys.maxsize.
    # 1-bit for sign
    MAX_SIZE = 2**63-1
    Cell = Tuple[int, int]

    def __init__(self, input_seq: Iterable[Cell] = None):
        if input_seq is not None:
            self.seed(input_seq)
        else:
            self.initialized = False

    def seed(self, input_seq: Iterable[Cell]):
        self.initialized = True
        self.alive = set(self._boundary_filter(input_seq))

    def step(self):
        if not self.initialized:
            raise RuntimeError("GoL not initialized.")
        # Use self.alive state to determine live candidates.
        self.live_candidates: Set[GameOfLife.Cell] = self._get_candidates()
        logger.debug(f"Processing candidates: {self.live_candidates}")

        alive = []
        while self.live_candidates:
            cell = self.live_candidates.pop()
            if self._is_alive(cell):
                alive.append(cell)

        # In case of a runtime error keep self.alive consistent.
        self.alive = set(alive)
        return self.alive

    def run(self, K: int = 10) -> Set[Cell]:
        if not self.initialized:
            raise RuntimeError("GoL not initialized.")

        for _ in range(K):
            self.step()

        return self.alive

    def _get_candidates(self) -> Set[Cell]:
        candidates = set()
        for cell in self.alive:
            candidates.add(cell)
            candidates |= self._get_neighbors(cell)

        return candidates

    def _is_alive(self, cell: Cell) -> bool:
        alive_neighbors = sum([c in self.alive for c in self._get_neighbors(cell)])
        if cell in self.alive:
            if 2 <= alive_neighbors <= 3:
                return True
            return False
        # Handle dead cell case.
        if alive_neighbors == 3:
            return True
        return False

    def _get_neighbors(self, cell: Cell) -> Set[Cell]:
        return self._boundary_filter([
            (cell[0] - 1, cell[1] - 1),
            (cell[0] - 1, cell[1]),
            (cell[0] - 1, cell[1] + 1),
            (cell[0], cell[1] - 1),
            (cell[0], cell[1] + 1),
            (cell[0] + 1, cell[1] - 1),
            (cell[0] + 1, cell[1]),
            (cell[0] + 1, cell[1] + 1),
        ])

    def _boundary_filter(self, cells: List[Cell]) -> Set[Cell]:
        """This is somewhat inefficient as for every single neighbor we unpack
        the tuple to check if it's outside our boundary and then regenerate
        the neighborhood set. I'll have a thunk on this later.
        """
        return set([(x, y) for x, y in cells if max(abs(x), abs(y)) <= self.MAX_SIZE])


def seed_from_input_file(seed_file: click.File) -> List[GameOfLife.Cell]:
    seed = []
    for line in seed_file.readlines():
        trimmed_line = line.strip()
        if not trimmed_line.startswith("#"):
            seed.append(tuple((int(coord) for coord in trimmed_line.rstrip("\n").split(" "))))

    return seed


def output_from_seed(state: List[GameOfLife.Cell]):
    out_str = "#Life 1.06\n"
    for x, y in state:
        out_str += f"{x} {y}\n"
    sys.stdout.write(out_str)


@click.command()
@click.option("-f", "--seed-file", type=click.File("r"), help='1.06 file seed', required=True)
@click.option("-k", type=int, help="Number of iterations to run", default=10)
def cli(seed_file: click.File, k: int):
    seed = seed_from_input_file(seed_file)
    game = GameOfLife(seed)
    game.run(k)
    output_from_seed(game.alive)


def set_logger_level():
    if "LOGURU_LEVEL" in os.environ:
        level = os.environ["LOGURU_LEVEL"]
    else:
        level = "ERROR"
    
    logger.remove()
    logger.add(sys.stderr, level=level)


if __name__ == "__main__":
    set_logger_level()
    cli()