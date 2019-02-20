import random
import unittest

from GameLogic.PlayerActions import PlayerActions
from GameLogic.ScoreBoard import ScoreBoard


class TestScoreBoard(unittest.TestCase):

    def setUp(self):
        self.players = [player for player in range(8)]

    def test_add_player_action(self):
        score_board = ScoreBoard(self.players)
        player_actions = {}
        game_round = 1
        for player in self.players:
            action = random.choice(PlayerActions.OPTIONS)
            score_board.add_player_action(player, action, game_round)
            player_actions[player] = action

        round_score = score_board.get_round_score(game_round)
        for player in self.players:
            player_action = round_score.get_player_action(player)
            expected_action = player_actions[player]
            self.assertEqual(expected_action, player_action)
