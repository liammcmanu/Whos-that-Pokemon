import sqlite3
import hashlib

from config import DEFAULT_DB_NAME, STORE_DOB

class database_controller:
    """
    A class that represents a database controller for user data.

    Attributes:
    - conn: The connection to the SQLite database.
    - cursor: The cursor object to execute SQL queries.

    Methods:
    - __init__(self, db_name): Initializes the database controller with the specified database name.
    - push_user(self, data_dict): Inserts a new user into the database.
    - pull_user(self, condition=None): Retrieves a user from the database based on the given condition.
    - authenticate_user(self, username, password): Authenticates a user based on the given username and password.
    - check_username_taken(self, username): Checks if a username is already taken in the database.
    - get_leaderboard(self): Retrieves the leaderboard from the database.
    - update_after_game(self, username, score): Updates the user's high score and games played after a game.

    """

    def __init__(self, db_name=DEFAULT_DB_NAME):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS user (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            age INTEGER,
            high_score INTEGER DEFAULT 0,
            games_played INTEGER DEFAULT 0
            )
        ''')

        self.conn.commit()

    def push_user(self, data_dict):
        """
        Inserts a new user into the database.

        Args:
        - data_dict: A dictionary containing the user data.

        Returns:
        - True if the user was successfully inserted, False otherwise.

        """
        try:
            # Hash the password before storing it
            password = data_dict['password']
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            data_dict['password'] = hashed_password

            if not STORE_DOB:
                data_dict['age'] = 20

            if 'high_score' not in data_dict:
                data_dict['high_score'] = 0

            if 'games_played' not in data_dict:
                data_dict['games_played'] = 0

            columns = ', '.join(data_dict.keys())
            placeholders = ', '.join('?' * len(data_dict))
            sql = f'INSERT INTO user ({columns}) VALUES ({placeholders})'
            self.cursor.execute(sql, list(data_dict.values()))
            self.conn.commit()
            return True
        except Exception as er:
            print(er)
            return False

    def pull_user(self, condition=None):
        """
        Retrieves a user from the database based on the given condition.

        Args:
        - condition: The condition to filter the user data (optional).

        Returns:
        - A dictionary containing the user data if found, None otherwise.

        """
        sql = 'SELECT * FROM user'
        if condition:
            sql += f' WHERE {condition}'
        self.cursor.execute(sql)
        raw = self.cursor.fetchall()
        if raw:
            return {"username": raw[0][1], "password": raw[0][2], "age": raw[0][3], "high_score": raw[0][4], "games_played": raw[0][5]}
        else:
            return None

    def authenticate_user(self, username, password):
        """
        Authenticates a user based on the given username and password.

        Args:
        - username: The username of the user.
        - password: The password of the user.

        Returns:
        - True if the user is authenticated, False otherwise.

        """
        user = self.pull_user(f'username = "{username}"')
        if user:
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            return user["password"] == hashed_password
        else:
            return False

    def check_username_taken(self, username):
        """
        Checks if a username is already taken in the database.

        Args:
        - username: The username to check.

        Returns:
        - True if the username is taken, False otherwise.

        """
        user = self.pull_user(f'username = "{username}"')
        return bool(user)

    def get_leaderboard(self):
        """
        Retrieves the leaderboard from the database.

        Returns:
        - A list of dictionaries containing the usernames, high scores, and games played of the users in descending order of high score.

        """
        self.cursor.execute('SELECT * FROM user ORDER BY high_score DESC')
        raw = self.cursor.fetchall()
        if raw:
            return [{"username": user[1], "high_score": user[4], "games_played": user[5]} for user in raw]
        else:
            return None

    def update_after_game(self, username, score):
        """
        Updates the user's high score and games played after a game.

        Args:
        - username: The username of the user.
        - score: The score achieved in the game.

        Returns:
        - True if the user's high score and games played were successfully updated, False otherwise.

        """
        user = self.pull_user(f'username = "{username}"')
        if user:
            current_score = user["high_score"]
            if score > current_score:
                self.cursor.execute(f'UPDATE user SET high_score = {score} WHERE username = "{username}"')
                self.conn.commit()
            self.cursor.execute(f'UPDATE user SET games_played = games_played + 1 WHERE username = "{username}"')
            self.conn.commit()
            return True
        else:
            return False
