import unittest
from unittest.mock import patch
from leaderboard import leaderboard
from rich.console import Console

class TestLeaderboard(unittest.TestCase):

    @patch('inquirer.list_input')
    @patch('controllers.database.database_controller')
    def test_init(self, mock_db, mock_inquirer):
        mock_db.return_value.get_leaderboard.return_value = [{'username': 'test_user', 'high_score': 100}]
        mock_inquirer.return_value = "Who's that Pokemon 🔥🌿💧"
        lb = leaderboard({'username': 'test_user'})
        mock_db.assert_called_once_with("whos_that_pokemon.db")
        mock_db.return_value.get_leaderboard.assert_called_once()
        mock_inquirer.assert_called_once_with("Okay what now...", choices=["Who's that Pokemon 🔥🌿💧", "Exit 🏃"], default="Who's that Pokemon 🔥🌿💧")

    @patch('inquirer.list_input')
    @patch('controllers.database.database_controller')
    def test_init_with_exit_cmd(self, mock_db, mock_inquirer):
        mock_db.return_value.get_leaderboard.return_value = [{'username': 'test_user', 'high_score': 100}]
        mock_inquirer.return_value = "Exit 🏃"
        with self.assertRaises(SystemExit):
            lb = leaderboard({'username': 'test_user'})

if __name__ == '__main__':
    unittest.main()
