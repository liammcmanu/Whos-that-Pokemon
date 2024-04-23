import random
import requests

class poke_api_controller:
	def __init__(self):
		self.base_url = "https://pokeapi.co/api/v2/"

	def get_pokemon(self, limit):

		random_pokemon_id = random.randint(1, limit)
		url = 'https://pokeapi.co/api/v2/pokemon/{random_pokemon_id}/'.format(random_pokemon_id=random_pokemon_id)
		if not url:
			return None, None

		response = requests.get(url)
		if response.status_code == 200:
			pokemon_data = response.json()
			pokemon_name = pokemon_data['name']
			pokemon_sprite = pokemon_data['sprites']['other']['official-artwork']['front_default']
			return pokemon_name, pokemon_sprite
		else:
			return None, None

	def get_whos_that_pokemon(self, limit=151):
		return self.get_pokemon(limit)
