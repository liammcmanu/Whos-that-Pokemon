import unittest
from classes.user_class import user

class UserTests(unittest.TestCase):
    def setUp(self):
        self.username = "test_user"
        self.password = "test_password"
        self.age = 30
        self.games_played = 10
        self.high_score = 100
        self.new_user = user(self.username, self.password, self.age, self.games_played, self.high_score, new=True)
        self.existing_user = user(self.username, self.password, self.age, self.games_played, self.high_score, new=False)

    def test_get_username(self):
        self.assertEqual(self.new_user.get_username(), self.username)
        self.assertEqual(self.existing_user.get_username(), self.username)

    def test_reset_password(self):
        new_password = "new_password"
        self.new_user.reset_password(new_password)
        self.assertTrue(self.new_user.auth_user(new_password))

if __name__ == '__main__':
    unittest.main()