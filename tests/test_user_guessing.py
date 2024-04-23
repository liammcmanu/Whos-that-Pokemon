import unittest
from unittest.mock import patch
from controllers.user_guessing import user_guessing_controller

class UserGuessingControllerTests(unittest.TestCase):
    def setUp(self):
        self.user = {"age": 10}
        self.pokemon_name = "Pikachu"
        self.controller = user_guessing_controller(self.user, self.pokemon_name)

    def test_get_user_guess(self):
        with patch('builtins.input', return_value='Pikachu'):
            guess = self.controller.get_user_guess()
            self.assertEqual(guess, 'Pikachu')

    def test_check_guess_correct(self):
        guess = "Pikachu"
        result = self.controller.check_guess(guess)
        self.assertTrue(result)

    def test_check_guess_incorrect(self):
        guess = "Charmander"
        result = self.controller.check_guess(guess)
        self.assertFalse(result)

if __name__ == '__main__':
    unittest.main()