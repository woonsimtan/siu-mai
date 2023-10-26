import pytest
# from base_game import *
from tiles import *

@pytest.mark.parametrize("tileA, tileB", [
    (Tile("A", "1"), Tile("A", "1")),
    ])
def test_tile_eq(tileA, tileB):
    assert tileA == tileB

@pytest.mark.parametrize("tileA, tileB", [
    (Tile("B", "1"), Tile("A", "1")),
    (Tile("A", "2"), Tile("A", "1")),
    (Tile("B", "2"), Tile("A", "1")),
    ])
def test_tile_noteq(tileA, tileB):
    assert tileA != tileB

@pytest.mark.parametrize("tile, expected", [
    (Tile("A", "1"), "A1"),
    ])
def test_tile_to_str(tile, expected):
    assert tile.to_string() == expected

@pytest.mark.parametrize("tile_list, expected", [
    (TileList([Tile("A", "1"), Tile("A", "1")]), TileList([Tile("A", "1"), Tile("A", "1")])),
    (TileList([Tile("A", "2"), Tile("A", "1")]), TileList([Tile("A", "1"), Tile("A", "2")])),
    (TileList([Tile("B", "1"), Tile("A", "1")]), TileList([Tile("A", "1"), Tile("B", "1")])),
    (TileList([Tile("B", "2"), Tile("A", "1")]), TileList([Tile("A", "1"), Tile("B", "2")])),
    ])
def test_tile_list_sort(tile_list, expected):
    tile_list.sort()
    assert tile_list == expected

@pytest.mark.parametrize("tile_list, expected", [
    (TileList([Tile("B", "2"), Tile("A", "1")]), ["A1", "B2"]),
    ])
def test_tile_list_print_form(tile_list, expected):
    assert tile_list.print_form() == expected

@pytest.mark.parametrize("tile_list, new_tile, expected", [
    (TileList([Tile("B", "2"), Tile("A", "1")]), Tile("B", "1"),  TileList([Tile("B", "2"), Tile("A", "1"), Tile("B", "1")])),
    ])
def test_tile_list_add(tile_list, new_tile, expected):
    tile_list.add(new_tile)
    assert tile_list == expected

@pytest.mark.parametrize("tile_list, new_tiles, expected", [
    (TileList([Tile("B", "2"), Tile("A", "1")]), TileList([Tile("B", "2"), Tile("A", "1")]),  TileList([Tile("B", "2"), Tile("A", "1"), Tile("B", "2"), Tile("A", "1")])),
    ])
def test_tile_list_add_tiles(tile_list, new_tiles, expected):
    tile_list.add_tiles(new_tiles)
    assert tile_list == expected

def test_tile_list_remove_fails():
    with pytest.raises(ValueError, match = "Tile to be removed is not in list."):
        TileList([Tile("B", "2"), Tile("A", "1")]).remove(Tile("B", "1"))

@pytest.mark.parametrize("tile_list, tile, expected", [
    (TileList([Tile("B", "2"), Tile("A", "1")]), Tile("B", "2"),  TileList([Tile("A", "1")])),
    ])
def test_tile_list_remove(tile_list, tile, expected):
    tile_list.remove(tile)
    assert tile_list == expected

@pytest.mark.parametrize("tile_list, to_remove, expected", [
    (TileList([Tile("B", "2"), Tile("A", "1")]), TileList([Tile("B", "2"), Tile("A", "1")]),  TileList([])),
    ])
def test_tile_list_add_tiles(tile_list, to_remove, expected):
    tile_list.remove_tiles(to_remove)
    assert tile_list == expected

# TypeError: TileList.unique_tiles() takes 0 positional arguments but 1 was given
@pytest.mark.parametrize("tile_list, expected", [
    (TileList([Tile("A", "1"), Tile("A", "1")]), TileList([Tile("A", "1")])),
    (TileList([Tile("B", "2"), Tile("A", "1")]), TileList([Tile("B", "2"), Tile("A", "1")]))
    ])
def test_unique_tiles(tile_list, expected):
    tile_set = tile_list.unique_tiles()
    assert tile_set == expected

@pytest.mark.parametrize("tile_list, expected", [
    (TileList([Tile("A", "1"), Tile("A", "1")]), {"A1": 2}),
    (TileList([Tile("B", "2"), Tile("A", "1")]), {"A1": 1, "B2": 1})
    ])
def test_tile_counts(tile_list, expected):
    assert tile_list.tile_counts() == expected

@pytest.mark.parametrize("tile_list", [
    (TileList([Tile("B", "2"), Tile("A", "1")]))
    ])
def test_remove_random(tile_list):
    original_count = tile_list.size()
    tile_list.remove_random_tile()
    assert tile_list.size() == original_count - 1

@pytest.mark.parametrize("tile_list, tile, expected", [
    (TileList([Tile("B", "2"), Tile("A", "1")]), Tile("B", "2"), True),
    (TileList([Tile("B", "2"), Tile("A", "1")]), Tile("B", "1"), False)
    ])
def test_tile_list_contains(tile_list, tile, expected):
    assert tile_list.contains(tile) == expected

@pytest.mark.parametrize("tile_list, tile, expected", [
    (TileList([Tile("A", "1"), Tile("A", "1"), Tile("B", "2")]), Tile("A", "1"), True),
    (TileList([Tile("B", "2"), Tile("A", "1"), Tile("B", "2")]), Tile("B", "1"), False),
    (TileList([Tile("A", "1"), Tile("A", "1"), Tile("B", "2")]), Tile("B", "1"), False),
    ])
def test_tile_list_check_peng(tile_list, tile, expected):
    assert tile_list.check_for_peng(tile) == expected

@pytest.mark.parametrize("tile_list, tile, expected", [
    (TileList([Tile("A", "1"), Tile("A", "1"), Tile("B", "2")]), Tile("A", "1"), 2),
    (TileList([Tile("B", "2"), Tile("A", "1"), Tile("B", "2")]), Tile("B", "1"), 0),
    (TileList([Tile("A", "1"), Tile("A", "1"), Tile("B", "1")]), Tile("B", "1"), 1),
    ])
def test_tile_list_check_count(tile_list, tile, expected):
    assert tile_list.count(tile) == expected

# def test_check_win(tile_list, expected):
#     pass

