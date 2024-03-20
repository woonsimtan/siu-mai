import pytest
from v1.tiles import TileList, Tile
from v1.players import Player

default_tiles = TileList(
    [Tile("Bamboo", "1"), Tile("Bamboo", "2"), Tile("Circles", "3")]
)


def test_player_unwanted_suit():
    # Create a TileList with tiles of different suits
    unwanted_bamboo_player = Player(default_tiles.copy(), TileList([]))

    # Check that the unwanted_suit attribute is set correctly
    assert unwanted_bamboo_player.unwanted_suit == "Numbers"

    # Create a Player with a specified unwanted suit
    specified_unwanted_player = Player(
        TileList([Tile("Bamboo", "1")]), unwanted_suit="Bamboo"
    )

    # Check that the unwanted_suit attribute is set to the specified suit
    assert specified_unwanted_player.unwanted_suit == "Bamboo"


def test_displayed_tiles():
    display_tiles = TileList([Tile("Bamboo", "1")] * 3)
    player = Player(default_tiles.copy(), display_tiles)
    assert player.displayed_tiles == display_tiles


def test_pickup():
    player = Player(default_tiles.copy(), TileList([]))
    player.pickup(Tile("Bamboo", "1"))
    assert player.possible_discards == TileList(
        [
            Tile("Bamboo", "1"),
            Tile("Bamboo", "2"),
            Tile("Circles", "3"),
            Tile("Bamboo", "1"),
        ]
    )


@pytest.mark.parametrize(
    "displayed_tiles, expected",
    [
        (
            TileList([Tile("Numbers", "1")] * 3),
            TileList([Tile("Numbers", "1")] * 3 + default_tiles.tiles),
        ),
        (TileList([]), default_tiles.copy()),
    ],
)
def test_all_tiles(displayed_tiles, expected):
    player = Player(default_tiles.copy(), displayed_tiles)
    assert player.all_tiles() == expected


@pytest.mark.parametrize(
    "player, expected",
    [
        (
            Player(
                TileList(
                    [
                        Tile("Bamboo", "1"),
                        Tile("Bamboo", "2"),
                        Tile("Bamboo", "3"),
                        Tile("Bamboo", "1"),
                        Tile("Numbers", "1"),
                        Tile("Numbers", "2"),
                        Tile("Numbers", "3"),
                        Tile("Numbers", "1"),
                        Tile("Numbers", "2"),
                        Tile("Numbers", "3"),
                        Tile("Numbers", "1"),
                        Tile("Numbers", "2"),
                        Tile("Numbers", "3"),
                        Tile("Bamboo", "1"),
                    ]
                ),
            ),
            True,
        ),
        (
            Player(
                TileList(
                    [
                        Tile("Bamboo", "1"),
                        Tile("Bamboo", "2"),
                        Tile("Bamboo", "3"),
                        Tile("Bamboo", "1"),
                        Tile("Numbers", "1"),
                        Tile("Numbers", "2"),
                        Tile("Numbers", "3"),
                        Tile("Numbers", "1"),
                        Tile("Numbers", "2"),
                        Tile("Numbers", "3"),
                        Tile("Numbers", "1"),
                        Tile("Numbers", "2"),
                        Tile("Numbers", "3"),
                        Tile("Bamboo", "7"),
                    ]
                ),
            ),
            False,
        ),
        (
            Player(
                TileList(
                    [
                        Tile("Bamboo", "1"),
                        Tile("Bamboo", "2"),
                        Tile("Bamboo", "3"),
                        Tile("Bamboo", "1"),
                        Tile("Numbers", "1"),
                        Tile("Numbers", "2"),
                        Tile("Numbers", "3"),
                        Tile("Numbers", "1"),
                        Tile("Numbers", "2"),
                        Tile("Numbers", "3"),
                        Tile("Numbers", "1"),
                        Tile("Numbers", "2"),
                        Tile("Numbers", "3"),
                        Tile("Bamboo", "1"),
                    ]
                ),
                unwanted_suit="Numbers",
            ),
            False,
        ),
    ],
)
def test_check_for_win(player, expected):
    assert player.check_for_win() == expected


@pytest.mark.parametrize(
    "player, tile, expected",
    [
        (
            Player(TileList([Tile("Bamboo", "1"), Tile("Bamboo", "1")])),
            Tile("Bamboo", "1"),
            True,
        ),
        (
            Player(
                TileList([Tile("Bamboo", "1"), Tile("Bamboo", "1")]),
                unwanted_suit="Bamboo",
            ),
            Tile("Bamboo", "1"),
            False,
        ),
        (
            Player(TileList([Tile("Bamboo", "1"), Tile("Bamboo", "1")])),
            Tile("Bamboo", "2"),
            False,
        ),
        (
            Player(TileList([Tile("Bamboo", "1"), Tile("Bamboo", "2")])),
            Tile("Bamboo", "1"),
            False,
        ),
    ],
)
def test_check_for_peng(player, tile, expected):
    assert player.check_for_peng(tile) == expected
