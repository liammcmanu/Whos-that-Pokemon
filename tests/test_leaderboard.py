import unittest
from unittest.mock import patch
from io import StringIO
from leaderboard import leaderboard

class TestLeaderboard(unittest.TestCase):

    def setUp(self):
        self.current_user = {'username': 'test_user'}
        self.lb = leaderboard(self.current_user)

    def test_print_user(self):
        expected_output = "Current User: test_user\nRank: 1\nHigh Score: 100\n"
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.lb.print_user()
            self.assertEqual(fake_out.getvalue(), expected_output)

    def test_print_lb(self):
        expected_output = "Current User: test_user\nRank: 1\nHigh Score: 100\n\nRank       Username             High Score\n1          user1                100\n2          user2                90\n"
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.lb.print_lb()
            self.assertEqual(fake_out.getvalue(), expected_output)

if __name__ == '__main__':
    unittest.main()