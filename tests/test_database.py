import unittest
from unittest.mock import patch
from controllers.database import database_controller

class TestDatabaseController(unittest.TestCase):
    def setUp(self):
        self.db = database_controller(':memory:')

    def tearDown(self):
        self.db.conn.close()

    def test_push_user(self):
        data_dict = {
            'username': 'test_user',
            'password': 'test_password',
            'age': 30,
            'high_score': 100,
            'games_played': 5
        }
        self.assertTrue(self.db.push_user(data_dict))

    def test_pull_user(self):
        data_dict = {
            'username': 'test_user',
            'password': 'test_password',
            'age': 30,
            'high_score': 100,
            'games_played': 5
        }
        self.db.push_user(data_dict)
        user = self.db.pull_user('username = "test_user"')
        self.assertEqual(user['username'], 'test_user')
        self.assertEqual(user['age'], 30)
        self.assertEqual(user['high_score'], 100)
        self.assertEqual(user['games_played'], 5)

    def test_authenticate_user(self):
        data_dict = {
            'username': 'test_user',
            'password': 'test_password',
            'age': 30,
            'high_score': 100,
            'games_played': 5
        }
        self.db.push_user(data_dict)
        self.assertTrue(self.db.authenticate_user('test_user', 'test_password'))
        self.assertFalse(self.db.authenticate_user('test_user', 'wrong_password'))

    def test_check_username_taken(self):
        data_dict = {
            'username': 'test_user',
            'password': 'test_password',
            'age': 30,
            'high_score': 100,
            'games_played': 5
        }
        self.db.push_user(data_dict)
        self.assertTrue(self.db.check_username_taken('test_user'))
        self.assertFalse(self.db.check_username_taken('non_existing_user'))

    def test_get_leaderboard(self):
        data_dict1 = {
            'username': 'user1',
            'password': 'password1',
            'age': 25,
            'high_score': 200,
            'games_played': 10
        }
        data_dict2 = {
            'username': 'user2',
            'password': 'password2',
            'age': 35,
            'high_score': 150,
            'games_played': 8
        }
        self.db.push_user(data_dict1)
        self.db.push_user(data_dict2)
        leaderboard = self.db.get_leaderboard()
        self.assertEqual(len(leaderboard), 2)
        self.assertEqual(leaderboard[0]['username'], 'user1')
        self.assertEqual(leaderboard[0]['high_score'], 200)
        self.assertEqual(leaderboard[1]['username'], 'user2')
        self.assertEqual(leaderboard[1]['high_score'], 150)

    def test_update_after_game(self):
        data_dict = {
            'username': 'test_user',
            'password': 'test_password',
            'age': 30,
            'high_score': 100,
            'games_played': 5
        }
        self.db.push_user(data_dict)
        self.assertTrue(self.db.update_after_game('test_user', 150))
        user = self.db.pull_user('username = "test_user"')
        self.assertEqual(user['high_score'], 150)
        self.assertEqual(user['games_played'], 6)
        self.assertFalse(self.db.update_after_game('non_existing_user', 200))

if __name__ == '__main__':
    unittest.main()