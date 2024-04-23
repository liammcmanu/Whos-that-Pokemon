import sqlite3
import hashlib

class database_controller:
    def __init__(self, db_name):
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
        try:
            # Hash the password before storing it
            password = data_dict['password']
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            data_dict['password'] = hashed_password

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
        user = self.pull_user(f'username = "{username}"')
        if user:
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            return user["password"] == hashed_password
        else:
            return False

    def check_username_taken(self, username):
        user = self.pull_user(f'username = "{username}"')
        return bool(user)

    def get_leaderboard(self):
        self.cursor.execute('SELECT * FROM user ORDER BY high_score DESC')
        raw = self.cursor.fetchall()
        if raw:
            return [{"username": user[1], "high_score": user[4]} for user in raw]
        else:
            return None

    def update_after_game(self, username, score):
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