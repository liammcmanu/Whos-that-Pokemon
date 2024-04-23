import unittest
from unittest.mock import patch
from controllers.poke_api import poke_api_controller

class TestPokeAPIController(unittest.TestCase):

    def setUp(self):
        self.poke_api = poke_api_controller()

    @patch('controllers.poke_api.requests.get')
    def test_get_pokemon_success(self, mock_get):
        mock_response = mock_get.return_value
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'name': 'pikachu',
            'sprites': {
                'other': {
                    'official-artwork': {
                        'front_default': 'https://pokeapi.co/media/sprites/pokemon/other/official-artwork/25.png'
                    }
                }
            }
        }

        pokemon_name, pokemon_sprite = self.poke_api.get_pokemon(151)

        self.assertEqual(pokemon_name, 'pikachu')
        self.assertEqual(pokemon_sprite, 'https://pokeapi.co/media/sprites/pokemon/other/official-artwork/25.png')

    @patch('controllers.poke_api.requests.get')
    def test_get_pokemon_failure(self, mock_get):
        mock_response = mock_get.return_value
        mock_response.status_code = 404

        pokemon_name, pokemon_sprite = self.poke_api.get_pokemon(151)

        self.assertIsNone(pokemon_name)
        self.assertIsNone(pokemon_sprite)

    def test_get_whos_that_pokemon(self):
        with patch('controllers.poke_api.poke_api_controller.get_pokemon') as mock_get_pokemon:
            mock_get_pokemon.return_value = ('pikachu', 'https://pokeapi.co/media/sprites/pokemon/other/official-artwork/25.png')

            pokemon_name, pokemon_sprite = self.poke_api.get_whos_that_pokemon()

            self.assertEqual(pokemon_name, 'pikachu')
            self.assertEqual(pokemon_sprite, 'https://pokeapi.co/media/sprites/pokemon/other/official-artwork/25.png')

if __name__ == '__main__':
    unittest.main()