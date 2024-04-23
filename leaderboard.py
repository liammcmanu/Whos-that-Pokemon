import inquirer

from rich.table import Table
from rich.console import Console
from rich.panel import Panel

import controllers.database as database

class leaderboard:

    def __init__(self, current_user):
        print("\n"*2)
        self.current_user = current_user
        self.db = database.database_controller("whos_that_pokemon.db")
        self.leaderboard_data = self.db.get_leaderboard()

        self.print_lb()
        print("\n"*2)

        cmd = inquirer.list_input("Okay what now...", choices=["Who's that Pokemon 🔥🌿💧", "Exit 🏃"], default="Who's that Pokemon 🔥🌿💧")

        if cmd == "Who's that Pokemon 🔥🌿💧":
            return
        else:
            exit()

    def print_user(self):

        # Create a console for rich output
        console = Console()

        # Find the current user's rank and high score
        current_user_rank = None
        current_user_high_score = None
        for i, user in enumerate(self.leaderboard_data, start=1):
            if user['username'] == self.current_user['username']:
                current_user_rank = i
                current_user_high_score = user['high_score']
                break

        # Create a panel for the current user's high score and rank
        panel = Panel(
            f"Current User: {self.current_user['username']}\n"
            f"Rank: {current_user_rank}\n"
            f"High Score: {current_user_high_score}",
            title="Your Leaderboard Stats",
            padding=(1, 2)
        )

        # Print the panel
        console.print(panel)

    def print_lb(self):
        self.print_user()
        print()

        # Create a console for rich output
        console = Console()

        # Create a table
        table = Table(show_header=True, header_style="bold dim")
        table.add_column("Rank", width=12)
        table.add_column("Username", width=20)
        table.add_column("High Score", width=12)

        for i, user in enumerate(self.leaderboard_data, start=1):
            table.add_row(str(i), user['username'], str(user['high_score']))

        console.print(table)
