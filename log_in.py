from datetime import datetime
from config import STORE_DOB
from controllers.database import database_controller

from rich import print
from rich.panel import Panel
from rich.prompt import Prompt

from abc import ABC, abstractmethod
import re
import inquirer

db = database_controller()

class UserAuthenticationStrategy(ABC):
    @abstractmethod
    def authenticate(self):
        pass

class SignInStrategy(UserAuthenticationStrategy):
    """
    Represents a strategy for user sign-in authentication.

    This class provides a method to authenticate a user by prompting for their
    username and password. It uses the `Prompt` class to interact with the user
    and the `db` module to check the username and authenticate the user.

    Attributes:
        username (str): The username entered by the user.
        password (str): The password entered by the user.

    Methods:
        authenticate: Authenticates the user by prompting for their username and password.

    """

    username = None
    password = None

    def authenticate(self):
        while True:
            username = Prompt.ask("Please enter your username")
            if re.match(r'^\w+$', username) and db.check_username_taken(username):
                password = Prompt.ask("Please enter a password", password=True)
                if db.authenticate_user(username, password):
                    print(Panel("Authentication successful!", title="[bold green]Success[/bold green]", border_style="bold green"))
                    print('\n')
                    break
                else:
                    print(Panel("Password is incorrect. Please try again.", title="[bold red]Error[/bold red]", border_style="bold red"))
                    print('\n')
            else:
                print(Panel("That account doesn't exist. Please try again.", title="[bold red]Error[/bold red]", border_style="bold red"))

        return db.pull_user(f'username = "{username}"')

class SignUpStrategy(UserAuthenticationStrategy):
    """
    Represents a strategy for user sign up/authentication.

    This strategy prompts the user to enter a username, password, and date of birth,
    and then creates a new user account if the provided information is valid.

    Attributes:
        None

    Methods:
        authenticate: Prompts the user for username, password, and date of birth,
                      and creates a new user account if the information is valid.
    """
    def authenticate(self):
        while True:
            username = Prompt.ask("Please enter a username")
            if re.match(r'^\w+$', username):
                if db.check_username_taken(username):
                    print('\n')
                    print(Panel("Username is already taken. Please try another username.", title="[bold red]Error[/bold red]", border_style="bold red"))
                else:
                    password = Prompt.ask("Please enter a password", password=True)
                    confirm_password = Prompt.ask("Please confirm your password", password=True)
                    if password == confirm_password:
                        if STORE_DOB:
                            dob_input = Prompt.ask("Please enter your date of birth (YYYY-MM-DD)")
                            try:
                                dob = datetime.strptime(dob_input, "%Y-%m-%d")
                                age = datetime.now().year - dob.year
                                if db.push_user(data_dict={'username': username, 'password': password, 'age': age}):
                                    print(Panel("Successfully created account!", title="[bold green]Success[/bold green]", border_style="bold green"))
                                    print('\n')
                                    break
                                else:
                                    print(Panel("Error creating account. Please try again.", title="[bold red]Error[/bold red]", border_style="bold red"))
                                    print('\n')
                            except ValueError:
                                print(Panel("Invalid date. Please try again.", title="[bold red]Error[/bold red]", border_style="bold red"))
                                print('\n')
                        else:
                              if db.push_user(data_dict={'username': username, 'password': password}):
                                print(Panel("Successfully created account!", title="[bold green]Success[/bold green]", border_style="bold green"))
                                print('\n')
                                break
                    else:
                        print(Panel("Passwords do not match. Please try again.", title="[bold red]Error[/bold red]", border_style="bold red"))
                        print('\n')
            else:
                print(Panel("Invalid username. Please try again.", title="[bold red]Error[/bold red]", border_style="bold red"))
                print('\n')
        return db.pull_user(f'username = "{username}"')

class AuthenticationContext:
    def __init__(self, strategy: UserAuthenticationStrategy):
        self._strategy = strategy

    def set_strategy(self, strategy: UserAuthenticationStrategy):
        self._strategy = strategy

    def authenticate_user(self):
        return self._strategy.authenticate()

def log_in():
    print('\n')
    print(Panel("\tWelcome to who's that Pokemon, to play the game you need an account, would you like to Sign-in or if you don't have an account Sign-up? 🔑🔐👤", padding=(1, 1),
                title="[bold]Who's that Pokemon[/bold]", border_style="bold"))
    return select_option()

def select_option():
    print('\n')
    decision = inquirer.list_input("Please select an option", choices=["Sign-in 🔑", "Sign-up 🔐"])
    print('\n')
    context = AuthenticationContext(SignInStrategy() if decision == "Sign-in 🔑" else SignUpStrategy())
    return context.authenticate_user()