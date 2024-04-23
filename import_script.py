import random
from controllers.database import database_controller
import requests

def generate_random_users(n):
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

db = database_controller('whos_that_pokemon.db')
populate_database()