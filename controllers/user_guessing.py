from fuzzywuzzy import fuzz

class user_guessing_controller:
	"""
	Controller class for user guessing in the "Who's that Pokémon" game.

	Args:
		user (dict): A dictionary containing user information, including age.
		pokemon_name (str): The name of the Pokémon to be guessed.

	Attributes:
		difficulty (int): The difficulty level based on the user's age.
		pokemon_name (str): The name of the Pokémon to be guessed.

	Methods:
		get_user_guess: Prompts the user to enter their guess.
		check_guess: Checks if the user's guess is correct.

	"""

	def __init__(self, user, pokemon_name):
		"""
		Initializes a new instance of the user_guessing_controller class.

		Args:
			user (dict): A dictionary containing user information, including age.
			pokemon_name (str): The name of the Pokémon to be guessed.

		"""
		# Determine the spelling level based on the user's age
		age = user["age"]
		if age < 8:
			self.difficulty = 1
		elif age < 14:
			self.difficulty = 2
		else:
			self.difficulty = 3

		self.pokemon_name = pokemon_name

	def get_user_guess(self):
		"""
		Prompts the user to enter their guess.

		Returns:
			str: The user's guess.

		"""
		guess = input("Enter your guess: ")
		return guess

	def check_guess(self, guess):
		"""
		Checks if the user's guess is correct.

		Args:
			guess (str): The user's guess.

		Returns:
			bool: True if the guess is correct, False otherwise.

		"""
		# Use fuzzy string matching to compare the guess to the Pokemon name
		similarity = fuzz.ratio(guess.lower(), self.pokemon_name.lower())

		# Determine the threshold based on the user's age group
		if self.difficulty == 1:
			threshold = 65
		elif self.difficulty == 2:
			threshold = 90
		else:
			threshold = 95

		# If the similarity is above the threshold, consider the guess as correct
		if similarity > threshold:
			return True
		else:
			return False
