import bcrypt

class user:
	"""
	Represents a user in the game.

	Attributes:
		username (str): The username of the user.
		password (str): The hashed password of the user.
		age (int): The age of the user.
		games_played (int): The number of games played by the user.
		high_score (int): The high score achieved by the user.
		new (bool): Indicates whether the user is new or not.

	Methods:
		__init__(self, username, password, age, games_played, high_score, new=True):
			Initializes a new user object.
		auth_user(self, password):
			Authenticates the user by checking the provided password.
		get_username(self):
			Returns the username of the user.
		reset_password(self, new_password):
			Resets the user's password to a new hashed password.
	"""

	def __init__(self, username, password, games_played, high_score, age=20, new=True):
		self.usernme = username
		self.games_played = games_played
		self.high_score = high_score

		if new:
			# Hash the password before storing it
			self.password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
		else:
			self.password = password

		# Store the user's age to determine the fuzzy string matching threshold
		# This sounds stupid but it's a cool way to make the game more accessible
		# especially for the age group that is not familiar with Pokemon
		self.age = age

	def auth_user(self, password):
		"""
		Authenticates the user by checking the provided password.

		Args:
			password (str): The password to be checked.

		Returns:
			bool: True if the password is correct, False otherwise.
		"""
		return bcrypt.checkpw(password.encode(), self.password)

	def get_username(self):
		"""
		Returns the username of the user.

		Returns:
			str: The username of the user.
		"""
		return self.usernme

	def reset_password(self, new_password):
		"""
		Resets the user's password to a new hashed password.

		Args:
			new_password (str): The new password to be set.
		"""
		self.password = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt())
