import sqlite3
import hashlib
import os
import hmac

class AuthManager:
    def __init__(self, db_path="users.db"):
        self.conn = sqlite3.connect(db_path)
        self.create_user_table()
        self.create_password_table()

    def create_user_table(self):
        with self.conn:
            self.conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY,
                password_hash TEXT NOT NULL,
                salt TEXT NOT NULL
            )
            """)

    def create_password_table(self):
        with self.conn:
            self.conn.execute("""
            CREATE TABLE IF NOT EXISTS passwords (
                user_id TEXT NOT NULL,
                email TEXT NOT NULL,
                password TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users (username),
                PRIMARY KEY (user_id, email)
            )
            """)

    def register(self, username, password):
        if self.user_exists(username):
            return False

        salt = os.urandom(16).hex()
        password_hash = self.hash_password(password, salt)

        with self.conn:
            self.conn.execute("""
            INSERT INTO users (username, password_hash, salt) VALUES (?, ?, ?)
            """, (username, password_hash, salt))

        return True

    def login(self, username, password):
        user = self.get_user(username)
        if not user:
            return False

        password_hash = self.hash_password(password, user["salt"])
        return hmac.compare_digest(password_hash, user["password_hash"])

    def user_exists(self, username):
        return self.get_user(username) is not None

    def get_user(self, username):
        cursor = self.conn.cursor()
        cursor.execute("SELECT username, password_hash, salt FROM users WHERE username = ?", (username,))
        row = cursor.fetchone()
        if row:
            return {"username": row[0], "password_hash": row[1], "salt": row[2]}
        return None

    def hash_password(self, password, salt):
        return hashlib.sha256((salt + password).encode()).hexdigest()
