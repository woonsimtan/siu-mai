from tiles import *

tl = TileList(
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
t = Tile("A", "5")

print(tl.check_for_win(t))
