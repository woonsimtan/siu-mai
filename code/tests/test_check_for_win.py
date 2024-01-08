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
    tiles = hand.tiles
    for t in tiles:
        encoded[encoding[t.suit_type] + int(t.value) - 1] += 1
    return encoded


def test_check_for_win():
    agari = Agari()
    test_cases = 100  # 0000
    success = 0
    for i in range(test_cases):
        hand = TileList([])
        all_tiles = create_tiles()
        for j in range(14):
            hand.add(all_tiles.remove_random_tile())
        encoded_hand = encode_hand(hand)
        hand.print()
        if hand.check_for_win() == agari.is_agari(encoded_hand):
            success += 1
    assert success == test_cases
