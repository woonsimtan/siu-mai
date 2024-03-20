import pytest
from mahjong.agari import Agari

from tiles import *
from base_game import create_tiles


@pytest.mark.parametrize(
    "tileA, tileB",
    [
        (Tile("A", "1"), Tile("A", "1")),
    ],
)
def test_tile_eq(tileA, tileB):
    assert tileA == tileB


@pytest.mark.parametrize(
    "tileA, tileB",
    [
        (Tile("B", "1"), Tile("A", "1")),
        (Tile("A", "2"), Tile("A", "1")),
        (Tile("B", "2"), Tile("A", "1")),
    ],
)
def test_tile_noteq(tileA, tileB):
    assert tileA != tileB


@pytest.mark.parametrize(
    "tile, expected",
    [
        (Tile("A", "1"), "A1"),
    ],
)
def test_tile_to_str(tile, expected):
    assert tile.to_string() == expected


@pytest.mark.parametrize(
    "tileA, tileB",
    [
        (Tile("A", "1"), Tile("A", "2")),
        (Tile("A", "1"), Tile("B", "2")),
        (Tile("A", "1"), Tile("B", "1")),
    ],
)
def test_tile_lt(tileA, tileB):
    assert tileA < tileB


@pytest.mark.parametrize(
    "tileA, tileB",
    [(Tile("B", "1"), Tile("A", "1")), (Tile("A", "2"), Tile("A", "1"))],
)
def test_tile_notlt(tileA, tileB):
    assert not tileA < tileB


@pytest.mark.parametrize("tile, expected", [(Tile("A", "1"), "A1\n")])
def test_tile_print(tile, expected, capsys):
    tile.print()
    captured = capsys.readouterr()
    assert captured.out == expected


@pytest.mark.parametrize("tile", [(Tile("A", "1")), (DUMMY_TILE)])
def test_tile_copy(tile):
    assert tile.copy() == tile


@pytest.mark.parametrize(
    "tile_list, expected",
    [
        (
            TileList([Tile("A", "1"), Tile("A", "1")]),
            TileList([Tile("A", "1"), Tile("A", "1")]),
        ),
        (
            TileList([Tile("A", "2"), Tile("A", "1")]),
            TileList([Tile("A", "1"), Tile("A", "2")]),
        ),
        (
            TileList([Tile("B", "1"), Tile("A", "1")]),
            TileList([Tile("A", "1"), Tile("B", "1")]),
        ),
        (
            TileList([Tile("B", "2"), Tile("A", "1")]),
            TileList([Tile("A", "1"), Tile("B", "2")]),
        ),
    ],
)
def test_tile_list_sort(tile_list, expected):
    tile_list.sort()
    assert tile_list == expected


@pytest.mark.parametrize(
    "tiles, expected",
    [
        (
            TileList([Tile("Bamboo", "1"), Tile("Numbers", "2"), Tile("Circles", "3")]),
            {
                "Bamboo": TileList([Tile("Bamboo", "1")]),
                "Numbers": TileList([Tile("Numbers", "2")]),
                "Circles": TileList([Tile("Circles", "3")]),
            },
        ),
        (
            TileList([]),
            {
                "Bamboo": TileList([]),
                "Numbers": TileList([]),
                "Circles": TileList([]),
            },
        ),
    ],
)
def test_get_tiles_by_suit(tiles, expected):
    assert tiles.get_tiles_by_suit() == expected


@pytest.mark.parametrize(
    "tile_list, expected",
    [
        (TileList([Tile("B", "2"), Tile("A", "1")]), ["A1", "B2"]),
    ],
)
def test_tile_list_print_form(tile_list, expected):
    assert tile_list.print_form() == expected


@pytest.mark.parametrize(
    "tile_list, new_tile, expected",
    [
        (
            TileList([Tile("B", "2"), Tile("A", "1")]),
            Tile("B", "1"),
            TileList([Tile("B", "2"), Tile("A", "1"), Tile("B", "1")]),
        ),
    ],
)
def test_tile_list_add(tile_list, new_tile, expected):
    tile_list.add(new_tile)
    assert tile_list == expected


@pytest.mark.parametrize(
    "tile_list, new_tiles, expected",
    [
        (
            TileList([Tile("B", "2"), Tile("A", "1")]),
            TileList([Tile("B", "2"), Tile("A", "1")]),
            TileList([Tile("B", "2"), Tile("A", "1"), Tile("B", "2"), Tile("A", "1")]),
        ),
        (
            TileList([Tile("B", "2"), Tile("A", "1")]),
            TileList(),
            TileList([Tile("B", "2"), Tile("A", "1")]),
        ),
    ],
)
def test_tile_list_add_tiles(tile_list, new_tiles, expected):
    tile_list.add_tiles(new_tiles)
    assert tile_list == expected


def test_tile_list_remove_fails():
    with pytest.raises(ValueError, match="Tile to be removed is not in list."):
        TileList([Tile("B", "2"), Tile("A", "1")]).remove(Tile("B", "1"))


@pytest.mark.parametrize(
    "tile_list, tile, expected",
    [
        (
            TileList([Tile("B", "2"), Tile("A", "1")]),
            Tile("B", "2"),
            TileList([Tile("A", "1")]),
        ),
    ],
)
def test_tile_list_remove(tile_list, tile, expected):
    tile_list.remove(tile)
    assert tile_list == expected


@pytest.mark.parametrize(
    "tile_list, to_remove, expected",
    [
        (
            TileList([Tile("B", "2"), Tile("A", "1")]),
            TileList([Tile("B", "2"), Tile("A", "1")]),
            TileList([]),
        ),
    ],
)
def test_tile_list_add_tiles(tile_list, to_remove, expected):
    tile_list.remove_tiles(to_remove)
    assert tile_list == expected


@pytest.mark.parametrize(
    "tile_list, expected",
    [
        (TileList([Tile("A", "1"), Tile("A", "1")]), TileList([Tile("A", "1")])),
        (
            TileList([Tile("B", "2"), Tile("A", "1")]),
            TileList([Tile("B", "2"), Tile("A", "1")]),
        ),
    ],
)
def test_unique_tiles(tile_list, expected):
    tile_set = tile_list.unique_tiles()
    assert tile_set == expected


@pytest.mark.parametrize(
    "tile_list, expected",
    [
        (TileList([Tile("A", "1"), Tile("A", "1")]), {"A1": 2}),
        (TileList([Tile("B", "2"), Tile("A", "1")]), {"A1": 1, "B2": 1}),
    ],
)
def test_tile_counts(tile_list, expected):
    assert tile_list.tile_counts() == expected


@pytest.mark.parametrize("tile_list", [(TileList([Tile("B", "2"), Tile("A", "1")]))])
def test_remove_random(tile_list):
    original_count = tile_list.size()
    tile_list.remove_random_tile()
    assert tile_list.size() == original_count - 1


@pytest.mark.parametrize(
    "tile_list, tile, expected",
    [
        (TileList([Tile("B", "2"), Tile("A", "1")]), Tile("B", "2"), True),
        (TileList([Tile("B", "2"), Tile("A", "1")]), Tile("B", "1"), False),
    ],
)
def test_tile_list_contains(tile_list, tile, expected):
    assert tile_list.contains(tile) == expected


@pytest.mark.parametrize(
    "tile_list, tile, expected",
    [
        (
            TileList([Tile("A", "1"), Tile("A", "1"), Tile("B", "2")]),
            Tile("A", "1"),
            True,
        ),
        (
            TileList([Tile("B", "2"), Tile("A", "1"), Tile("B", "2")]),
            Tile("B", "1"),
            False,
        ),
        (
            TileList([Tile("A", "1"), Tile("A", "1"), Tile("B", "2")]),
            Tile("B", "1"),
            False,
        ),
    ],
)
def test_tile_list_check_peng(tile_list, tile, expected):
    assert tile_list.check_for_peng(tile) == expected


@pytest.mark.parametrize(
    "tile_list, tile, expected",
    [
        (TileList([Tile("A", "1"), Tile("A", "1"), Tile("B", "2")]), Tile("A", "1"), 2),
        (TileList([Tile("B", "2"), Tile("A", "1"), Tile("B", "2")]), Tile("B", "1"), 0),
        (TileList([Tile("A", "1"), Tile("A", "1"), Tile("B", "1")]), Tile("B", "1"), 1),
    ],
)
def test_tile_list_check_count(tile_list, tile, expected):
    assert tile_list.count(tile) == expected


@pytest.mark.parametrize(
    "tile_list, expected",
    [
        (
            TileList([Tile("A", "1"), Tile("A", "1"), Tile("B", "2")]),
            (TileList([Tile("A", "1"), Tile("A", "1"), Tile("B", "2")])),
        ),
        (TileList(), TileList()),
    ],
)
def test_copy_tile_list(tile_list, expected):
    assert tile_list.copy() == tile_list


@pytest.mark.parametrize(
    "tile_list, new_tiles, expected_tile_list, expected_copy",
    [
        (
            TileList(),
            TileList([Tile("A", "1")]),
            TileList(),
            TileList([Tile("A", "1")]),
        ),
        (
            TileList([Tile("B", "2"), Tile("A", "1")]),
            TileList([Tile("B", "2"), Tile("A", "1")]),
            TileList([Tile("B", "2"), Tile("A", "1")]),
            TileList([Tile("B", "2"), Tile("A", "1"), Tile("B", "2"), Tile("A", "1")]),
        ),
    ],
)
def test_copy_tile_list(tile_list, new_tiles, expected_tile_list, expected_copy):
    copy = tile_list.copy()
    assert tile_list == copy
    copy.add_tiles(new_tiles)
    assert tile_list == expected_tile_list
    assert copy == expected_copy


def test_check_win_too_many_tiles():
    tile_list = TileList(
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
            Tile("A", "5"),
            Tile("A", "5"),
        ]
    )
    tile = Tile("DUMMY", "TILE")
    with pytest.raises(ValueError, match="Invalid number of tiles."):
        tile_list.check_for_win(tile)


def encode_hand(hand):
    # Bamboo Suit: 0-8
    # Character Suit: 9-17
    # Dot Suit: 18-26
    encoded = [0] * 34
    encoding = {"Bamboo": 0, "Numbers": 9, "Circles": 18}
    tiles = hand.tiles
    for t in tiles:
        encoded[encoding[t.suit_type] + int(t.value) - 1] += 1
    return encoded


# random test cases
def test_check_for_win():
    agari = Agari()
    test_cases = 100
    success = 0
    for i in range(test_cases):
        hand = TileList([])
        all_tiles = create_tiles()
        for j in range(14):
            hand.add(all_tiles.remove_random_tile())
        encoded_hand = encode_hand(hand)
        if hand.check_for_win() == agari.is_agari(encoded_hand):
            success += 1
    assert success == test_cases


@pytest.mark.parametrize(
    "hand, new_tile",
    [
        (
            TileList(
                [
                    Tile("Circles", "1"),
                    Tile("Circles", "2"),
                    Tile("Circles", "3"),
                    Tile("Circles", "3"),
                    Tile("Circles", "3"),
                    Tile("Circles", "4"),
                    Tile("Circles", "4"),
                    Tile("Circles", "4"),
                    Tile("Circles", "5"),
                    Tile("Circles", "5"),
                    Tile("Circles", "5"),
                    Tile("Circles", "6"),
                    Tile("Circles", "6"),
                ]
            ),
            Tile("Circles", "7"),
        ),
        (
            TileList(
                [
                    Tile("Circles", "1"),
                    Tile("Circles", "2"),
                    Tile("Circles", "3"),
                    Tile("Circles", "3"),
                    Tile("Circles", "3"),
                    Tile("Circles", "4"),
                    Tile("Circles", "4"),
                    Tile("Circles", "4"),
                    Tile("Circles", "5"),
                    Tile("Circles", "5"),
                    Tile("Circles", "5"),
                    Tile("Circles", "6"),
                    Tile("Circles", "6"),
                ]
            ),
            DUMMY_TILE,
        ),
        (TileList([Tile("Circles", str(i)) for i in range(1, 8)] * 2), DUMMY_TILE),
    ],
)
def test_check_for_win_specific_cases(hand, new_tile):
    agari = Agari()
    hand_copy = hand.copy()
    if new_tile != DUMMY_TILE:
        hand_copy.add(new_tile)
    encoded_hand = encode_hand(hand_copy)
    assert hand.check_for_win(new_tile) == agari.is_agari(encoded_hand)


def test_hand_score_bounded():
    exp = 0
    success = 0
    for i in range(1000):
        hand = TileList([])
        all_tiles = TileList(
            [Tile("Circles", str(i)) for i in range(1, 10)] * 4
            + [Tile("Numbers", str(i)) for i in range(1, 10)] * 4
        )
        for j in range(14):
            hand.add(all_tiles.remove_random_tile())
        if not hand.check_for_win():
            exp += 1
            if hand.hand_score("Bamboo") < 1:
                success += 1
    assert success == exp


@pytest.mark.parametrize(
    "hand, unwanted_suit",
    [
        (TileList([Tile("Circles", "1")] * 13), "Circles"),
    ],
)
def test_hand_score_unwanted(hand, unwanted_suit):
    assert hand.hand_score(unwanted_suit) == -1
