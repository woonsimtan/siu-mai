import pytest
from random_agent import RandomAgent
from tiles import Tile, TileList, DUMMY_TILE

# wins on tile A5
random_agent_triple = RandomAgent(
    TileList(
        [
            Tile("A", "1"),
            Tile("A", "1"),
            Tile("A", "1"),
            Tile("A", "2"),
            Tile("A", "2"),
            Tile("A", "2"),
            Tile("A", "3"),
            Tile("A", "3"),
            Tile("A", "3"),
            Tile("A", "4"),
            Tile("A", "4"),
            Tile("A", "4"),
            Tile("A", "5"),
        ]
    )
)
# wins on tile A9
random_agent_consecutive = RandomAgent(
    TileList(
        [
            Tile("A", "1"),
            Tile("A", "2"),
            Tile("A", "3"),
            Tile("B", "2"),
            Tile("B", "3"),
            Tile("B", "4"),
            Tile("A", "5"),
            Tile("A", "6"),
            Tile("A", "7"),
            Tile("B", "6"),
            Tile("B", "7"),
            Tile("B", "8"),
            Tile("A", "9"),
        ]
    )
)


@pytest.mark.parametrize(
    "player, expected",
    [
        (
            random_agent_triple,
            TileList(
                [
                    Tile("A", "1"),
                    Tile("A", "1"),
                    Tile("A", "1"),
                    Tile("A", "2"),
                    Tile("A", "2"),
                    Tile("A", "2"),
                    Tile("A", "3"),
                    Tile("A", "3"),
                    Tile("A", "3"),
                    Tile("A", "4"),
                    Tile("A", "4"),
                    Tile("A", "4"),
                    Tile("A", "5"),
                ]
            ),
        ),
        (
            random_agent_consecutive,
            TileList(
                [
                    Tile("A", "1"),
                    Tile("A", "2"),
                    Tile("A", "3"),
                    Tile("B", "2"),
                    Tile("B", "3"),
                    Tile("B", "4"),
                    Tile("A", "5"),
                    Tile("A", "6"),
                    Tile("A", "7"),
                    Tile("B", "6"),
                    Tile("B", "7"),
                    Tile("B", "8"),
                    Tile("A", "9"),
                ]
            ),
        ),
    ],
)
def test_total_tile_count(player, expected):
    assert player.all_tiles() == expected
    player.lock_three_of_a_kind()
    assert player.all_tiles() == expected
    player.lock_three_consecutive()
    assert player.all_tiles() == expected
    player.lock_pair()
    assert player.all_tiles() == expected


@pytest.mark.parametrize(
    "player, expected",
    [(random_agent_triple, 13), (random_agent_consecutive, 13)],
)
def test_total_tile_count(player, expected):
    assert player.total_tile_count() == expected


@pytest.mark.parametrize(
    "player, tile",
    [
        (random_agent_triple, Tile("A", "5")),
        (random_agent_consecutive, Tile("A", "9")),
    ],
)
def test_play_turn_win(player, tile):
    assert player.play_a_turn(tile) == DUMMY_TILE


# not discarding as expected
@pytest.mark.parametrize(
    "player, tile, expected_discards",
    [
        (random_agent_triple, Tile("B", "5"), [Tile("B", "5"), Tile("A", "5")]),
        # (random_agent_consecutive, Tile("B", "5"), [Tile("B", "5"), Tile("B", "8"), Tile("A", "9")])
    ],
)
def test_play_turn_not_win(player, tile, expected_discards):
    discarded = player.play_a_turn(tile)
    assert discarded in expected_discards


@pytest.mark.parametrize(
    "player, tile",
    [
        (random_agent_triple, Tile("A", "5")),
        (random_agent_consecutive, Tile("A", "9")),
    ],
)
def test_check_for_win(player, tile):
    assert player.check_for_win(tile)


@pytest.mark.parametrize(
    "player, tile",
    [
        (
            RandomAgent(
                TileList(
                    [
                        Tile("A", "1"),
                        Tile("A", "1"),
                    ]
                )
            ),
            Tile("A", "1"),
        ),
    ],
)
def test_check_for_peng(player, tile):
    assert player.check_for_peng(tile)


@pytest.mark.parametrize(
    "player, tile",
    [
        (
            RandomAgent(
                TileList(
                    [
                        Tile("A", "1"),
                        Tile("A", "5"),
                    ]
                )
            ),
            Tile("A", "1"),
        ),
        (
            RandomAgent(
                TileList(
                    [
                        Tile("A", "1"),
                        Tile("A", "1"),
                    ]
                )
            ),
            Tile("A", "5"),
        ),
    ],
)
def test_check_for_peng(player, tile):
    assert not player.check_for_peng(tile)


@pytest.mark.parametrize(
    "player, expected_possible_discard, expected_locked",
    [
        (
            RandomAgent(TileList([Tile("A", "1"), Tile("A", "2"), Tile("A", "3")])),
            TileList([]),
            TileList([Tile("A", "1"), Tile("A", "2"), Tile("A", "3")]),
        ),
        (
            RandomAgent(TileList([Tile("A", "1"), Tile("A", "2"), Tile("A", "4")])),
            TileList([Tile("A", "1"), Tile("A", "2"), Tile("A", "4")]),
            TileList([]),
        ),
    ],
)
def test_lock_three_consecutive(player, expected_possible_discard, expected_locked):
    player.lock_three_consecutive()
    assert player.possible_discards == expected_possible_discard
    assert player.locked_tiles == expected_locked


@pytest.mark.parametrize(
    "player, tile, expected_displayed",
    [
        (
            RandomAgent(TileList([Tile("A", "1"), Tile("A", "1"), Tile("A", "3")])),
            Tile("A", "1"),
            TileList([Tile("A", "1"), Tile("A", "1"), Tile("A", "1")]),
        ),
    ],
)
def test_peng(player, tile, expected_displayed):
    player.peng(tile)
    assert player.displayed_tiles == expected_displayed
