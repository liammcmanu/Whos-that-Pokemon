import random
import requests

class poke_api_controller:
	"""
	A class that interacts with the PokeAPI to retrieve Pokemon data.

	Attributes:
		base_url (str): The base URL of the PokeAPI.
	"""

	def __init__(self):
		self.base_url = "https://pokeapi.co/api/v2/"

	def get_pokemon(self, limit):
		"""
		Retrieves a random Pokemon from the PokeAPI.

		Args:
			limit (int): The maximum ID of the Pokemon to retrieve.

		Returns:
			tuple: A tuple containing the name and sprite URL of the Pokemon.
				   If the request fails or the Pokemon is not found, returns (None, None).
		"""

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
		"""
		Retrieves a random Pokemon from the PokeAPI.

		Args:
			limit (int, optional): The maximum ID of the Pokemon to retrieve. Defaults to 151.

		Returns:
			tuple: A tuple containing the name and sprite URL of the Pokemon.
				   If the request fails or the Pokemon is not found, returns (None, None).
		"""
		return self.get_pokemon(limit)
