from rich import print
from rich.panel import Panel
from rich.prompt import Prompt

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

def selectGeneration():
    generations = [
        "Gen 1: Red, Green and Blue 🐐",
        "Gen 2: Gold, Silver and Crystal 🥉🥈💎",
        "Gen 3: Ruby, Sapphire and Emerald 🔴🔵🟢",
        "Gen 4: Diamond, Pearl and Platinum 💎💎💎",
        "Gen 5: Black, White ⚫⚪", 
        "Gen 6: X and Y 🔵🔴",
        "Gen 7: Sun, Moon and Ultra Sun, Ultra Moon 🌞🌚",
        "Gen 8: Sword, Shield 🗡🛡"
    ]
    generation = inquirer.list_input("What Generation do you want to take a guess at: 🧐", choices=generations)

    if generation == "Gen 1: Red, Green and Blue 🐐":
        return 151
    elif generation == "Gen 2: Gold, Silver and Crystal 🥉🥈💎":
        return 251
    elif generation == "Gen 3: Ruby, Sapphire and Emerald 🔴🔵🟢":
        return 386
    elif generation == "Gen 4: Diamond, Pearl and Platinum 💎💎💎":
        return 493
    elif generation == "Gen 5: Black, White ⚫⚪":
        return 649
    elif generation == "Gen 6: X and Y 🔵🔴":
        return 721
    elif generation == "Gen 7: Sun, Moon and Ultra Sun, Ultra Moon 🌞🌚":
        return 809
    elif generation == "Gen 8: Sword, Shield 🗡🛡":
        return 898
    else :
        return 151

def game_loop(start_game, current_user):
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

                while count < 3:

                    guess = Prompt.ask("Enter your guess")

                    # Check if the guess is correct
                    if user_guessing.check_guess(guess):
                        print(Panel("Congratulations! You guessed it right!", style="bold green"))
                        score += 1
                        break
                    else:
                        count += 1
                        if (count < 2):
                            print(Panel(f"Try again! You have {3 - count} attempts left", style="bold red"))
                        else:
                            if (score < 10):
                                print(Panel(f"Sorry, the correct answer was {pokemon_name}, score: {score}", style="bold red"))
                            elif (score <= 30):
                                print(Panel(f"Unclucky, the correct answer was {pokemon_name}, Holy shit that's a high score: {score}", style="bold yellow"))
                            elif (score > 30):
                                print(Panel(f"Oooff unlucky, the correct answer was {pokemon_name} but my god look at that score: {score}", style="bold green"))
                            print('\n'*3)
                            db = database_controller('whos_that_pokemon.db')
                            db.update_after_game(current_user['username'], score)
                            start_game = inquirer.list_input("Okay what's next?", choices=["Who's that Pokemon 🔥🌿💧", "Leaderboard 🏆💪🎉", "Exit 🏃"], default="Leaderboard 🏆💪🎉")
                            game_loop(start_game, current_user)
                            break
        elif start_game == "Leaderboard 🏆💪🎉":
            leaderboard(current_user)
        else:
            quit()
