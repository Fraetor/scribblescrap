# Where processing logic lives.

import sqlite3
import secrets


def create_user(database: sqlite3.Connection, username):
    """Create a new player."""
    user_id = secrets.randbits(63)
    database.execute("INSERT INTO users VALUES(user_id, username)", (user_id, username))
    return user_id


def get_user_id_from_username(database: sqlite3.Connection, username):
    """Get the user_id from a username."""
    return database.execute(
        "SELECT user_id FROM users WHERE username = ?", (username,)
    ).fetchone()
