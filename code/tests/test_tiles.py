import pytest
from tiles import *


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
def test_tile_eq(tileA, tileB):
    assert tileA < tileB


@pytest.mark.parametrize(
    "tileA, tileB",
    [(Tile("B", "1"), Tile("A", "1")), (Tile("A", "2"), Tile("A", "1"))],
)
def test_tile_noteq(tileA, tileB):
    assert not tileA < tileB


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


# @pytest.mark.parametrize(
#     "tile_list, tile",
#     [
#         (
#             TileList(
#                 [
#                     Tile("Bamboo", "1"),
#                     Tile("Bamboo", "2"),
#                     Tile("Bamboo", "3"),
#                     Tile("Bamboo", "4"),
#                     Tile("Bamboo", "6"),
#                     Tile("Bamboo", "7"),
#                     Tile("Bamboo", "8"),
#                     Tile("Bamboo", "9"),
#                     Tile("Bamboo", "1"),
#                     Tile("Bamboo", "2"),
#                     Tile("Bamboo", "3"),
#                     Tile("Bamboo", "4"),
#                     Tile("Character", "5"),
#                 ]
#             ),
#             Tile("Bamboo", "5"),
#         ),
#         (
#             TileList(
#                 [
#                     Tile("Character", "1"),
#                     Tile("Character", "1"),
#                     Tile("Character", "1"),
#                     Tile("Character", "5"),
#                     Tile("Character", "5"),
#                     Tile("Character", "5"),
#                     Tile("Character", "9"),
#                     Tile("Character", "9"),
#                     Tile("Character", "9"),
#                     Tile("Character", "3"),
#                     Tile("Character", "3"),
#                     Tile("Character", "3"),
#                     Tile("Character", "7"),
#                 ]
#             ),
#             Tile("Character", "7"),
#         ),
#         (
#             TileList(
#                 [
#                     Tile("Dot", "2"),
#                     Tile("Dot", "2"),
#                     Tile("Dot", "4"),
#                     Tile("Dot", "4"),
#                     Tile("Dot", "6"),
#                     Tile("Dot", "6"),
#                     Tile("Dot", "8"),
#                     Tile("Dot", "8"),
#                     Tile("Dot", "3"),
#                     Tile("Dot", "3"),
#                     Tile("Dot", "7"),
#                     Tile("Dot", "7"),
#                     Tile("Dot", "9"),
#                 ]
#             ),
#             Tile("Dot", "9"),
#         ),
#         (
#             TileList(
#                 [
#                     Tile("Bamboo", "1"),
#                     Tile("Bamboo", "2"),
#                     Tile("Bamboo", "3"),
#                     Tile("Bamboo", "4"),
#                     Tile("Bamboo", "5"),
#                     Tile("Character", "6"),
#                     Tile("Character", "7"),
#                     Tile("Character", "8"),
#                     Tile("Character", "9"),
#                     Tile("Bamboo", "1"),
#                     Tile("Bamboo", "2"),
#                     Tile("Bamboo", "3"),
#                     Tile("Bamboo", "4"),
#                     Tile("Bamboo", "5"),
#                 ]
#             ),
#             Tile("Bamboo", "5"),
#         ),
#         (
#             TileList(
#                 [
#                     Tile("Bamboo", "1"),
#                     Tile("Bamboo", "9"),
#                     Tile("Character", "1"),
#                     Tile("Character", "9"),
#                     Tile("Dot", "1"),
#                     Tile("Dot", "9"),
#                     Tile("Bamboo", "1"),
#                     Tile("Character", "1"),
#                     Tile("Dot", "1"),
#                     Tile("Bamboo", "2"),
#                     Tile("Character", "2"),
#                     Tile("Dot", "2"),
#                     Tile("Bamboo", "1"),
#                 ]
#             ),
#             Tile("Character", "9"),
#         ),
#         (
#             TileList(
#                 [
#                     Tile("Dot", "1"),
#                     Tile("Dot", "2"),
#                     Tile("Dot", "3"),
#                     Tile("Dot", "4"),
#                     Tile("Dot", "5"),
#                     Tile("Dot", "6"),
#                     Tile("Dot", "7"),
#                     Tile("Dot", "8"),
#                     Tile("Dot", "9"),
#                     Tile("Dot", "1"),
#                     Tile("Dot", "2"),
#                     Tile("Dot", "3"),
#                     Tile("Dot", "4"),
#                     Tile("Dot", "5"),
#                 ]
#             ),
#             Tile("Dot", "5"),
#         ),
#         (
#             TileList(
#                 [
#                     Tile("Bamboo", "1"),
#                     Tile("Bamboo", "1"),
#                     Tile("Bamboo", "1"),
#                     Tile("Bamboo", "5"),
#                     Tile("Bamboo", "5"),
#                     Tile("Bamboo", "5"),
#                     Tile("Bamboo", "9"),
#                     Tile("Bamboo", "9"),
#                     Tile("Bamboo", "9"),
#                     Tile("Bamboo", "4"),
#                     Tile("Bamboo", "4"),
#                     Tile("Bamboo", "4"),
#                     Tile("Bamboo", "8"),
#                     Tile("Bamboo", "5"),
#                 ]
#             ),
#             Tile("Bamboo", "8"),
#         ),
#         (
#             TileList(
#                 [
#                     Tile("Character", "2"),
#                     Tile("Character", "2"),
#                     Tile("Character", "4"),
#                     Tile("Character", "4"),
#                     Tile("Character", "6"),
#                     Tile("Character", "6"),
#                     Tile("Character", "8"),
#                     Tile("Character", "8"),
#                     Tile("Character", "3"),
#                     Tile("Character", "3"),
#                     Tile("Character", "7"),
#                     Tile("Character", "7"),
#                     Tile("Character", "9"),
#                 ]
#             ),
#             Tile("Character", "9"),
#         ),
#         (
#             TileList(
#                 [
#                     Tile("Bamboo", "1"),
#                     Tile("Bamboo", "2"),
#                     Tile("Bamboo", "3"),
#                     Tile("Bamboo", "4"),
#                     Tile("Bamboo", "5"),
#                     Tile("Character", "6"),
#                     Tile("Character", "7"),
#                     Tile("Character", "8"),
#                     Tile("Character", "9"),
#                     Tile("Bamboo", "1"),
#                     Tile("Bamboo", "2"),
#                     Tile("Bamboo", "3"),
#                     Tile("Bamboo", "4"),
#                     Tile("Character", "5"),
#                 ]
#             ),
#             Tile("Character", "5"),
#         ),
#         (
#             TileList(
#                 [
#                     Tile("Bamboo", "1"),
#                     Tile("Bamboo", "9"),
#                     Tile("Character", "1"),
#                     Tile("Character", "9"),
#                     Tile("Dot", "1"),
#                     Tile("Dot", "9"),
#                     Tile("Bamboo", "1"),
#                     Tile("Character", "1"),
#                     Tile("Dot", "1"),
#                     Tile("Bamboo", "2"),
#                     Tile("Character", "2"),
#                     Tile("Dot", "2"),
#                     Tile("Bamboo", "1"),
#                 ]
#             ),
#             Tile("Character", "9"),
#         ),
#     ],
# )
# def test_check_win(tile_list, tile):
#     assert tile_list.check_for_win(tile)


# @pytest.mark.parametrize(
#     "tile_list, tile",
#     [
#         (
#             TileList(
#                 [
#                     Tile("A", "1"),
#                     Tile("A", "1"),
#                     Tile("A", "1"),
#                     Tile("A", "2"),
#                     Tile("A", "2"),
#                     Tile("A", "2"),
#                     Tile("A", "3"),
#                     Tile("A", "3"),
#                     Tile("A", "3"),
#                     Tile("A", "4"),
#                     Tile("A", "4"),
#                     Tile("A", "4"),
#                     Tile("A", "5"),
#                 ]
#             ),
#             Tile("B", "5"),
#         ),
#         (
#             TileList(
#                 [
#                     Tile("DUMMY", "TILE"),
#                     Tile("A", "1"),
#                     Tile("A", "1"),
#                     Tile("A", "2"),
#                     Tile("A", "2"),
#                     Tile("A", "2"),
#                     Tile("A", "3"),
#                     Tile("A", "3"),
#                     Tile("A", "3"),
#                     Tile("A", "4"),
#                     Tile("A", "4"),
#                     Tile("A", "4"),
#                     Tile("A", "5"),
#                 ]
#             ),
#             Tile("B", "5"),
#         ),
#         (
#             TileList(
#                 [
#                     Tile("A", "1"),
#                     Tile("A", "1"),
#                     Tile("A", "2"),
#                     Tile("A", "2"),
#                     Tile("A", "3"),
#                     Tile("A", "3"),
#                     Tile("A", "4"),
#                     Tile("A", "4"),
#                     Tile("A", "5"),
#                     Tile("A", "5"),
#                     Tile("A", "6"),
#                     Tile("A", "6"),
#                     Tile("A", "5"),
#                 ]
#             ),
#             Tile("B", "5"),
#         ),
#     ],
# )
# def test_check_not_win(tile_list, tile):
#     assert not tile_list.check_for_win(tile)


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
