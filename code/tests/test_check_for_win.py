import pytest
from tiles import *
from mahjong.agari import Agari
from base_game import create_tiles


def encode_hand(hand):
    # Bamboo Suit: 0-8
    # Character Suit: 9-17
    # Dot Suit: 18-26
    encoded = [0] * 34
    encoding = {"Bamboo": 0, "Numbers": 9, "Circles": 18}
    # encoded = []
    tiles = hand.tiles
    for t in tiles:
        encoded[encoding[t.suit_type] + int(t.value) - 1] += 1
    return encoded


def test_check_for_win():
    agari = Agari()

    for i in range(10000):
        hand = TileList([])
        all_tiles = create_tiles()
        for j in range(14):
            hand.add(all_tiles.remove_random_tile())
        encoded_hand = encode_hand(hand)
        hand.print()

        assert hand.check_for_win() == agari.is_agari(encoded_hand)


# def test_matches(tileA, tileB):
#     assert hand.check_for_win(tile) == agari.is_agari(encoded_hand)
