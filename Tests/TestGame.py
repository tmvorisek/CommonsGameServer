import unittest
from unittest.mock import MagicMock

from GameLogic.Game import Game


class TestGame(unittest.TestCase):

    def setUp(self):
        self.num_players = 4
        pass

    def test_init(self):
        game = Game(self.num_players)
        self.assertEqual(0, game.current_round)
        self.assertEqual(self.num_players, len(game.players))

    def test_end_summit(self):
        game = Game(self.num_players)
        game.update_score_board = MagicMock()
        game.update_commons_index = MagicMock
        summit_length = 4
        game.end_summit(summit_length)
        game_round_0 = game.current_round
        game.end_summit(summit_length)
        game_round_1 = game.current_round
        self.assertEqual(game_round_0, 4)
        self.assertEqual(game_round_1, 8)

