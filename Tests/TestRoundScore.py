import unittest

from GameLogic.CommonsIndex import CommonsIndex
from GameLogic.RoundScore import RoundScore
from GameLogic.PlayerActions import PlayerActions


class TestRoundScore(unittest.TestCase):

    def setUp(self):
        self.players = {i: i for i in range(4)}
        s = PlayerActions.SUSTAIN
        o = PlayerActions.OVERHARVEST
        r = PlayerActions.RESTORE
        p = PlayerActions.POLICE
        self.one_each_actions = [s, o, r, p]
        self.multi_actions = [o, o, o, o, r, r, r, r, r, s, s, p, p, p]
        self.game_round = 1

    def make_round_score(self, actions):
        round_score = RoundScore(self.game_round)
        for player_num in range(len(actions)):
            action = actions[player_num]
            round_score.set_player_action(player_num, action)
        return round_score

    def test_game_round(self):
        round_score = RoundScore(self.game_round)
        expected = self.game_round
        actual = round_score.game_round
        self.assertEqual(expected, actual)

    def test_player_action(self):
        round_score = RoundScore(self.game_round)
        p1 = self.players[0]
        p2 = self.players[1]
        p1_action = PlayerActions.POLICE
        p2_action = PlayerActions.SUSTAIN
        round_score.set_player_action(p1, p1_action)
        round_score.set_player_action(p2, p2_action)
        p1_actual_action = round_score.get_player_action(p1)
        p2_actual_action = round_score.get_player_action(p2)
        self.assertEqual(p1_action, p1_actual_action)
        self.assertEqual(p2_action, p2_actual_action)

    def test_totals_one_each(self):
        round_score = self.make_round_score(self.one_each_actions)
        round_score.calculate_totals()
        self.assertEqual(1, round_score.total_sustain)
        self.assertEqual(1, round_score.total_overharvest)
        self.assertEqual(1, round_score.total_restore)
        self.assertEqual(1, round_score.total_police)

    def test_totals_zero(self):
        round_score = RoundScore(self.game_round)
        round_score.calculate_totals()
        self.assertEqual(0, round_score.total_sustain)
        self.assertEqual(0, round_score.total_overharvest)
        self.assertEqual(0, round_score.total_restore)
        self.assertEqual(0, round_score.total_police)

    def test_totals_multiple(self):
        round_score = self.make_round_score(self.multi_actions)
        round_score.calculate_totals()
        self.assertEqual(2, round_score.total_sustain)
        self.assertEqual(4, round_score.total_overharvest)
        self.assertEqual(5, round_score.total_restore)
        self.assertEqual(3, round_score.total_police)

    def test_calculate_scores_one_each(self):
        round_score = self.make_round_score(self.one_each_actions)
        commons_index = CommonsIndex(1.0)
        round_score.set_end_of_round_scores(commons_index)
        for player_num in range(len(self.one_each_actions)):
            action = self.one_each_actions[player_num]
            action_score = commons_index.get_yield(round_score, action)
            player_score = round_score.get_player_score(player_num)
            self.assertEqual(action_score, player_score)

    def test_calculate_scores_multi_player(self):
        round_score = self.make_round_score(self.multi_actions)
        commons_index = CommonsIndex(1.0)
        round_score.set_end_of_round_scores(commons_index)
        for player_num in range(len(self.multi_actions)):
            action = self.multi_actions[player_num]
            action_score = commons_index.get_yield(round_score, action)
            player_score = round_score.get_player_score(player_num)
            self.assertEqual(action_score, player_score)

    def test_is_over(self):
        round_score = RoundScore(self.game_round)
        self.assertFalse(round_score.is_over())
        round_score.set_end_of_round_scores(CommonsIndex(1.))
        self.assertTrue(round_score.is_over())
