import pytest
from unittest import mock

from random_agent import RandomAgent
from tiles import Tile, TileList, DUMMY_TILE
from base_game import *


@pytest.mark.parametrize(
    "tiles, expected",
    [
        (
            {"A": ["1"]},
            TileList([Tile("A", "1"), Tile("A", "1"), Tile("A", "1"), Tile("A", "1")]),
        ),
    ],
)
def test_create_tiles(tiles, expected):
    assert create_tiles(tiles) == expected


@pytest.mark.parametrize(
    "n",
    [(52), (108)],
)
def test_distribute_tiles(n):
    tiles = TileList([DUMMY_TILE for i in range(n)])
    assert distribute_tiles(tiles) == [
        TileList([DUMMY_TILE for i in range(13)]) for j in range(4)
    ]
    assert tiles.size() == n - 52


@pytest.mark.parametrize(
    "players, tile, expected",
    [
        (
            [
                RandomAgent(TileList([])),
                RandomAgent(TileList([])),
                RandomAgent(TileList([])),
                RandomAgent(TileList([])),
            ],
            DUMMY_TILE,
            -1,
        ),
        (
            [
                RandomAgent(TileList([])),
                RandomAgent(TileList([DUMMY_TILE for i in range(2)])),
                RandomAgent(TileList([])),
                RandomAgent(TileList([])),
            ],
            DUMMY_TILE,
            1,
        ),
    ],
)
def test_any_peng(players, tile, expected):
    assert any_peng(players, tile) == expected


DUMMY_AGENT = RandomAgent(
    TileList(
        [
            Tile("A", "1"),
            Tile("A", "1"),
            Tile("A", "2"),
            Tile("A", "2"),
            Tile("A", "3"),
            Tile("A", "3"),
            Tile("A", "4"),
            Tile("A", "4"),
            Tile("A", "5"),
            Tile("A", "5"),
            Tile("A", "6"),
            Tile("A", "6"),
            Tile("A", "7"),
        ]
    )
)
DUMMY_AGENT_WINNING_HAND = RandomAgent(TileList([Tile("B", "1") for i in range(13)]))


@pytest.mark.parametrize(
    "players, tile, expected",
    [
        ([DUMMY_AGENT, DUMMY_AGENT, DUMMY_AGENT, DUMMY_AGENT], DUMMY_TILE, -1),
        (
            [DUMMY_AGENT, DUMMY_AGENT_WINNING_HAND, DUMMY_AGENT, DUMMY_AGENT],
            Tile("B", "1"),
            1,
        ),
    ],
)
def test_any_wins(players, tile, expected):
    assert any_wins(players, tile) == expected


@pytest.mark.parametrize(
    "players, tile, expected",
    [
        # ([DUMMY_AGENT, RandomAgent(TileList([DUMMY_TILE for i in range(13)])), DUMMY_AGENT, DUMMY_AGENT], DUMMY_TILE, "Player 1 has invalid number of tiles: 0"),
        (
            [
                DUMMY_AGENT,
                RandomAgent(TileList([Tile("A", "1") for i in range(15)])),
                DUMMY_AGENT,
                DUMMY_AGENT,
            ],
            DUMMY_TILE,
            "Player 1 has invalid number of tiles: 15",
        ),
    ],
)
def test_any_wins_error(players, tile, expected):
    with pytest.raises(ValueError, match=expected):
        any_wins(players, tile)
