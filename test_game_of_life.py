from typing import List, Set
import pytest
from game_of_life import GameOfLife


@pytest.mark.parametrize(
    "seed, out, k",
    [
        ([(0, 1), (1, 2), (2, 1)], {(1, 1), (1, 2)}, 1),
        ([(0, 1), (1, 1), (2, 1)], {(1, 2), (1, 1), (1, 0)}, 1),
        (    # Should not include: (1, GameOfLife.MAX_SIZE + 1).
            [(0, GameOfLife.MAX_SIZE), (1, GameOfLife.MAX_SIZE), (2, GameOfLife.MAX_SIZE)], 
            {(1, GameOfLife.MAX_SIZE), (1, GameOfLife.MAX_SIZE - 1)},
            1
        ),
        (   # Entire input row is below the -MAX_SIZE boundary and thus should return no alive cells.
            [(0, -GameOfLife.MAX_SIZE - 1), (1, -GameOfLife.MAX_SIZE - 1), (2, -GameOfLife.MAX_SIZE - 1)], 
            set(), # 
            1
        ),
        ([], set(), 10),
    ]
)
def test_game_of_life(seed: List[GameOfLife.Cell], out: Set[GameOfLife.Cell], k: int):
    g = GameOfLife(seed)
    g.run(k)
    assert g.alive == out
