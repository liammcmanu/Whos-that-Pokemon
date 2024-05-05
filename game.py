from rich import print
from rich.panel import Panel
from rich.prompt import Prompt

from config import AMOUNT_OF_GUESSES
from controllers.user_guessing import user_guessing_controller
from controllers.poke_api import poke_api_controller

from PIL import Image
import ascii_magic
import tempfile
import inquirer

import requests
from io import BytesIO

from leaderboard import leaderboard

from controllers.database import database_controller

generations_list = {
		"Gen 1: Red, Green and Blue 🐐": 151,
		"Gen 2: Gold, Silver and Crystal 🥉🥈💎": 251,
		"Gen 3: Ruby, Sapphire and Emerald 🔴🔵🟢": 386,
		"Gen 4: Diamond, Pearl and Platinum 💎💎💎": 493,
		"Gen 5: Black, White ⚫⚪": 649,
		"Gen 6: X and Y 🔵🔴": 621,
		"Gen 7: Sun, Moon and Ultra Sun, Ultra Moon 🌞🌚": 809,
		"Gen 8: Sword, Shield 🗡🛡": 898,
	}

def selectGeneration():
	"""
	Prompts the user to select a Pokémon generation and returns the total number of Pokémon in that generation.

	Returns:
		int: The total number of Pokémon in the selected generation.

	"""
	selected_generation = inquirer.list_input("What Generation do you want to take a guess at: 🧐", choices=generations_list.keys())
	return generations_list[selected_generation]

def game_loop(start_game, current_user):
	"""
	Main game loop for "Who's that Pokemon".

	Args:
		start_game (str): The selected game mode.
		current_user (dict): The current user's information.

	Returns:
		None
	"""
	while True:
		if start_game == "Who's that Pokemon 🔥🌿💧":

			# Initialize the controllers
			poke_api = poke_api_controller()

			print('\n')
			limit = selectGeneration()
			print('\n')

			score = 0
			count = 0

			while True:
				# Get a random Pokemon
				pokemon_name, pokemon_sprite = poke_api.get_pokemon(int(limit))

				# Initialize the controllers
				user_guessing = user_guessing_controller(current_user, pokemon_name)

				# Download the image
				response = requests.get(pokemon_sprite)
				image = Image.open(BytesIO(response.content))

				# Resize the image
				max_size = (80, 80)  # Change these numbers to adjust the size
				image.thumbnail(max_size)

				# Save the image to a temporary file
				with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp:
					image.save(temp.name)

				# Convert the sprite to ASCII with the specified options
				output = ascii_magic.from_image(temp.name)

				print('\n')
				print(Panel(
					f"Guess the Pokemon! Here is the sprite:", style="bold blue"
				))

				output.to_terminal()

				while count < AMOUNT_OF_GUESSES + 1:

					guess = Prompt.ask("Enter your guess")

					# Check if the guess is correct
					if user_guessing.check_guess(guess):
						print(Panel("Congratulations! You guessed it right!", style="bold green"))
						score += 1
						break
					else:
						count += 1
						if (count < AMOUNT_OF_GUESSES + 1):
							print(Panel(f"Try again! You have {AMOUNT_OF_GUESSES + 1 - count} attempts left", style="bold red"))
						else:
							if (score < 10):
								print(Panel(f"Sorry, the correct answer was {pokemon_name}, score: {score}", style="bold red"))
							elif (score <= 30):
								print(Panel(f"Unclucky, the correct answer was {pokemon_name}, Holy shit that's a high score: {score}", style="bold yellow"))
							elif (score > 30):
								print(Panel(f"Oooff unlucky, the correct answer was {pokemon_name} but my god look at that score: {score}", style="bold green"))
							print('\n'*3)
							db = database_controller()
							db.update_after_game(current_user['username'], score)
							start_game = inquirer.list_input("Okay what's next?", choices=["Who's that Pokemon 🔥🌿💧", "Leaderboard 🏆💪🎉", "Exit 🏃"], default="Leaderboard 🏆💪🎉")
							game_loop(start_game, current_user)
							break
		elif start_game == "Leaderboard 🏆💪🎉":
			start_game = leaderboard(current_user).cmd
		else:
			quit()
