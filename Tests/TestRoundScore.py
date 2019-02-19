import unittest

from GameLogic.CommonsIndex import CommonsIndex
from GameLogic.RoundScore import RoundScore
from GameLogic.PlayerActions import PlayerActions


class TestRoundScore(unittest.TestCase):

    def setUp(self):
        self.players = {i: i for i in range(4)}
        self.game_round = 1

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

    def test_totals_and_score_one_each(self):
        round_score = RoundScore(self.game_round)
        round_score.set_player_action(0, PlayerActions.OVERHARVEST)
        round_score.set_player_action(1, PlayerActions.RESTORE)
        round_score.set_player_action(2, PlayerActions.SUSTAIN)
        round_score.set_player_action(3, PlayerActions.POLICE)
        round_score.calculate_totals()
        self.assertEqual(1, round_score.total_sustain)
        self.assertEqual(1, round_score.total_overharvest)
        self.assertEqual(1, round_score.total_restore)
        self.assertEqual(1, round_score.total_police)
        commons_index = CommonsIndex(7.0)
        round_score.set_end_of_round_scores(commons_index)
        overharvest_score = commons_index.get_yield(round_score, PlayerActions.OVERHARVEST)
        sustain_score = commons_index.get_yield(round_score, PlayerActions.SUSTAIN)
        restore_score = commons_index.get_yield(round_score, PlayerActions.RESTORE)
        police_score = commons_index.get_yield(round_score, PlayerActions.POLICE)
        self.assertEqual(overharvest_score, round_score.player_scores[0])
        self.assertEqual(restore_score, round_score.player_scores[1])
        self.assertEqual(sustain_score, round_score.player_scores[2])
        self.assertEqual(police_score, round_score.player_scores[3])

    def test_totals_none(self):
        round_score = RoundScore(self.game_round)
        round_score.calculate_totals()
        self.assertEqual(0, round_score.total_sustain)
        self.assertEqual(0, round_score.total_overharvest)
        self.assertEqual(0, round_score.total_restore)
        self.assertEqual(0, round_score.total_police)

    def test_totals_multiple(self):
        round_score = RoundScore(self.game_round)
        round_score.set_player_action(0, PlayerActions.OVERHARVEST)
        round_score.set_player_action(1, PlayerActions.OVERHARVEST)
        round_score.set_player_action(2, PlayerActions.OVERHARVEST)
        round_score.set_player_action(3, PlayerActions.OVERHARVEST)
        round_score.set_player_action(4, PlayerActions.RESTORE)
        round_score.set_player_action(5, PlayerActions.RESTORE)
        round_score.set_player_action(6, PlayerActions.RESTORE)
        round_score.set_player_action(7, PlayerActions.RESTORE)
        round_score.set_player_action(8, PlayerActions.RESTORE)
        round_score.set_player_action(9, PlayerActions.SUSTAIN)
        round_score.set_player_action(10, PlayerActions.SUSTAIN)
        round_score.set_player_action(11, PlayerActions.POLICE)
        round_score.set_player_action(12, PlayerActions.POLICE)
        round_score.set_player_action(13, PlayerActions.POLICE)
        round_score.calculate_totals()
        self.assertEqual(2, round_score.total_sustain)
        self.assertEqual(4, round_score.total_overharvest)
        self.assertEqual(5, round_score.total_restore)
        self.assertEqual(3, round_score.total_police)
