import random
from controllers.database import database_controller
import requests

def generate_random_users(n):
	"""
	Generate a list of random user data, mostly just used to make it look like its live.

	Args:
		n (int): The number of random users to generate.

	Returns:
		list: A list of dictionaries, where each dictionary represents a random user.
			  Each dictionary contains the following keys:
			  - 'username': The username of the user.
			  - 'password': The password of the user.
			  - 'age': The age of the user.
			  - 'high_score': A random high score between 1 and 63.
			  - 'games_played': A random number of games played between 1 and 234.
	"""
	response = requests.get(f'https://randomuser.me/api/?results={n}')
	data = response.json()
	users = [
		{
			'username': user['login']['username'],
			'password': user['login']['password'],
			'age': user['dob']['age'],
			'high_score': random.randint(1, 63),
			'games_played': random.randint(1, 234)
		}
		for user in data['results']
	]
	return users

def populate_database():
	users = generate_random_users(62)

	for user in users:
		if not db.check_username_taken(user['username']):
			db.push_user(user)
		else:
			print(f"Username '{user['username']}' is already taken.")

db = database_controller()
populate_database()