import random
import unittest

from GameLogic.CommonsIndex import CommonsIndex
from GameLogic.PlayerActions import PlayerActions
from GameLogic.ScoreBoard import ScoreBoard


class TestScoreBoard(unittest.TestCase):

    def setUp(self):
        self.players = [player for player in range(8)]
        self.game_round = 1

    def test_add_player_action(self):
        score_board = ScoreBoard(self.players)
        player_actions = self.add_player_actions(score_board)
        round_score = score_board.get_round_score(self.game_round)
        for player in self.players:
            player_action = round_score.get_player_action(player)
            expected_action = player_actions[player]
            self.assertEqual(expected_action, player_action)

    def add_player_actions(self, score_board):
        player_actions = {}
        for player in self.players:
            action = random.choice(PlayerActions.OPTIONS)
            score_board.add_player_action(player, action, self.game_round)
            player_actions[player] = action
        return player_actions

    def test_set_end_of_round_scores(self):
        commons_index = CommonsIndex(7.0)
        score_board = ScoreBoard(self.players)
        player_actions = self.add_player_actions(score_board)
        score_board.set_end_of_round_scores(self.game_round, commons_index)
        round_score = score_board.get_round_score(self.game_round)
        self.assertEqual(self.game_round, round_score.game_round)
        for player, action in player_actions.items():
            score = round_score.get_player_score(player)
            expected = commons_index.get_yield(round_score, action)
            self.assertEqual(expected, score)

    def test_get_round_score(self):
        score_board = ScoreBoard(self.players)
        round_score = score_board.get_round_score(self.game_round)
        self.assertEqual(self.game_round, round_score.game_round)
