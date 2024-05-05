from rich import print
from rich.panel import Panel

from PIL import Image
import ascii_magic
import tempfile
import inquirer

from game import game_loop
from log_in import log_in

current_user = None

print('\n')

from PIL import Image
import tempfile
import ascii_magic

def opening_screen():
	"""
	Displays the opening screen of the game.

	This function opens the Pokemon logo image, converts it to RGBA format,
	saves it to a temporary file, and then converts the sprite to ASCII
	using the specified options. The resulting ASCII art is displayed on the terminal.
	"""
	# Get the path of the Pokemon logo image
	logo_path = r"images\Pokemon-Logo.png"
	# Open the image and convert it to RGBA
	image = Image.open(logo_path).convert("RGBA")
	# Save the image to a temporary file
	with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp:
		image.save(temp.name)
		temp_path = temp.name
	# Convert the sprite to ASCII with the specified options
	output = ascii_magic.from_image(temp_path)
	output.to_terminal()

opening_screen()
current_user = log_in()

print('\n')
print(Panel (f"\tWelcome back {current_user['username']} are you ready to guess em' all! 🤔", padding=(1, 1),
                title="[bold]Who's that Pokemon[/bold]", border_style="bold"))
print('\n'*3)
start_game = inquirer.list_input("What's the plan?", choices=["Who's that Pokemon 🔥🌿💧", "Leaderboard 🏆💪🎉", "Exit 🏃"], default="Who's that Pokemon 🔥🌿💧")
print('\n')
game_loop(start_game, current_user)
