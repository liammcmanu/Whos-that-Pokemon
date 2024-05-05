import inquirer

from rich.table import Table
from rich.console import Console
from rich.panel import Panel

import controllers.database as database

class leaderboard:
	"""
	Represents a leaderboard.

	Attributes:
		current_user (dict): The current user's information.
		db (database_controller): The database controller object.
		leaderboard_data (list): The leaderboard data retrieved from the database.

	Methods:
		__init__(self, current_user): Initializes the leaderboard object.
		print_user(self): Prints the current user's leaderboard stats.
		print_lb(self): Prints the leaderboard table.
	"""

	def __init__(self, current_user):
		"""
		Initializes the leaderboard object.

		Args:
			current_user (dict): The current user's information.
		"""
		print("\n"*2)
		self.current_user = current_user
		self.db = database.database_controller()
		self.leaderboard_data = self.db.get_leaderboard()

		self.print_lb()
		print("\n"*2)

		self.cmd = inquirer.list_input("Okay what now...", choices=["Who's that Pokemon 🔥🌿💧", "Exit 🏃"], default="Who's that Pokemon 🔥🌿💧")

	def print_user(self):
		"""
		Prints the current user's leaderboard stats.
		"""
		console = Console()

		current_user_rank = None
		current_user_high_score = None
		for i, user in enumerate(self.leaderboard_data, start=1):
			if user['username'] == self.current_user['username']:
				current_user_rank = i
				current_user_high_score = user['high_score']
				current_user_games_played = user['games_played']
				break

			panel = Panel(
		  		f"Current User: {self.current_user['username']}\n"
				f"Rank: {current_user_rank}\n"
				f"High Score: {current_user_high_score}\n",
				title="Your Leaderboard Stats",
				padding=(1, 2)
			)

			console.print(panel)

	def print_lb(self):
		"""
		Prints the leaderboard table.
		"""
		self.print_user()
		print()

		console = Console()

		table = Table(show_header=True, header_style="bold dim")
		table.add_column("Rank", width=12)
		table.add_column("Username", width=20)
		table.add_column("High Score", width=12)

		for i, user in enumerate(self.leaderboard_data, start=1):
			table.add_row(
				str(i),
				user['username'],
				str(user['high_score']),
			)

		console.print(table)
