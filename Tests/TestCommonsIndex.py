import unittest
from unittest.mock import MagicMock

from GameLogic.CommonsIndex import CommonsIndex
from GameLogic.PlayerActions import PlayerActions


class TestCommonsIndex(unittest.TestCase):

    def setUp(self):
        self.start_index = 1.5

    def test_get_yield(self):
        commons_index = CommonsIndex(self.start_index)
        sustain = 5
        restore = 4
        police = 2
        mock_score = MagicMock()
        mock_score.total_sustain = sustain
        mock_score.total_restore = restore
        mock_score.total_police = police
        # Test restore
        action = PlayerActions.RESTORE
        expected_yield = -CommonsIndex.RESTORE_COST / restore
        actual_yield = commons_index.get_yield(mock_score, action)
        self.assertEqual(expected_yield, actual_yield)
        # Test police
        action = PlayerActions.POLICE
        expected_yield = -CommonsIndex.POLICE_COST / police
        actual_yield = commons_index.get_yield(mock_score, action)
        self.assertEqual(expected_yield, actual_yield)
        # Test overharvest with police
        action = PlayerActions.OVERHARVEST
        expected_yield = -CommonsIndex.OVERHARVEST_FINE
        actual_yield = commons_index.get_yield(mock_score, action)
        self.assertEqual(expected_yield, actual_yield)
        # Test overharvest no police
        mock_score.total_police = 0
        action = PlayerActions.OVERHARVEST
        expected_yield = 35
        actual_yield = commons_index.get_yield(mock_score, action)
        self.assertEqual(expected_yield, actual_yield)
        # Test sustain
        action = PlayerActions.SUSTAIN
        expected_yield = 20
        actual_yield = commons_index.get_yield(mock_score, action)
        self.assertEqual(expected_yield, actual_yield)

    def test_get_sustain_yield(self):
        commons_index = CommonsIndex(self.start_index)
        # Test no sustain
        sustain_num = 0
        expected_yield = 15
        actual_yield = commons_index.get_sustain_yield(sustain_num)
        self.assertEqual(expected_yield, actual_yield)
        # Test multiple sustain
        sustain_num = 3
        expected_yield = 18
        actual_yield = commons_index.get_sustain_yield(sustain_num)
        self.assertEqual(expected_yield, actual_yield)

    def test_get_overharvest_yield(self):
        commons_index = CommonsIndex(self.start_index)
        # No police or sustain
        expected_yield = 30
        actual_yield = commons_index.get_overharvest_yield(0, 0)
        self.assertEqual(expected_yield, actual_yield)
        # No police some sustain
        expected_yield = 33
        actual_yield = commons_index.get_overharvest_yield(3, 0)
        self.assertEqual(expected_yield, actual_yield)
        # One police
        expected_yield = -CommonsIndex.OVERHARVEST_FINE
        actual_yield = commons_index.get_overharvest_yield(1, 1)
        self.assertEqual(expected_yield, actual_yield)
        # Multiple police
        expected_yield = -CommonsIndex.OVERHARVEST_FINE
        actual_yield = commons_index.get_overharvest_yield(1, 3)
        self.assertEqual(expected_yield, actual_yield)

    def test_get_restore_yield(self):
        commons_index = CommonsIndex(self.start_index)
        # No restore
        restore = 0
        expected = 0
        actual = commons_index.get_restore_yield(restore)
        self.assertEqual(expected, actual)
        # 1 restore
        restore = 1
        expected = -CommonsIndex.RESTORE_COST
        actual = commons_index.get_restore_yield(restore)
        self.assertEqual(expected, actual)
        # Multiple restore
        restore = 4
        expected = -CommonsIndex.RESTORE_COST / restore
        actual = commons_index.get_restore_yield(restore)
        self.assertEqual(expected, actual)

    def test_get_police_yield(self):
        commons_index = CommonsIndex(self.start_index)
        # No police
        police = 0
        expected = 0
        actual = commons_index.get_police_yield(police)
        self.assertEqual(expected, actual)
        # 1 police
        police = 1
        expected = -CommonsIndex.POLICE_COST
        actual = commons_index.get_police_yield(police)
        self.assertEqual(expected, actual)
        # Multiple police
        police = 3
        expected = -CommonsIndex.POLICE_COST / 3
        actual = commons_index.get_police_yield(police)
        self.assertEqual(expected, actual)

    def test_update_indices(self):
        # Test multiple overharvest no restore
        self.do_update_index_test(3, 0, 1.2)
        # Test one overharvest one restore
        self.do_update_index_test(1, 1, 1.4)
        # Test multiple overharvest multiple restore
        self.do_update_index_test(3, 2, 1.2)
        # Test negative commons index
        self.do_update_index_test(30, 0, 0)
        # Test multiple restore no overharvest
        self.do_update_index_test(0, 3, 1.8)
        # Test multiple updates
        self.do_multiple_updates_test()

    def do_multiple_updates_test(self):
        commons_index = CommonsIndex(self.start_index)
        overharvest = 2
        restore = 3
        commons_index.update_index(overharvest, restore)
        index = commons_index.index
        self.assertEqual(1.3, index)
        commons_index.update_index(overharvest, restore)
        index = commons_index.index
        self.assertEqual(1.1, index)
        commons_index.update_index(0, restore)
        index = commons_index.index
        self.assertAlmostEqual(1.4, index, 1)  # 1.4 != 1.400001 otherwise

    def do_update_index_test(self, overharvest, restore, expected_index):
        actual_index = self.get_index(overharvest, restore)
        self.assertEqual(expected_index, actual_index)

    def get_index(self, overharvest, restore):
        commons_index = CommonsIndex(self.start_index)
        commons_index.update_index(overharvest, restore)
        return commons_index.index
