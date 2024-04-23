import bcrypt

class user:
	def __init__(self, username, password, age, games_played, high_score, new=True):
		self.usernme = username
		self.games_played = games_played
		self.high_score = high_score

		if new:
			# Hash the password before storing it
			self.password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
		else:
			self.password = password

		# Store the user's age to determin the fuzzy string matching threshold
		# This sounds stupid but it's a cool way to make the game more accessible
        # especially for the age group that is not familiar with Pokemon
		self.age = age

	def auth_user(self, password):
		return bcrypt.checkpw(password.encode(), self.password)

	def get_username(self):
		return self.usernme

	def reset_password(self, new_password):
		self.password = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt())
