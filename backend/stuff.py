# Where processing logic lives.

import sqlite3


def create_user(database, username):
    """Create a new player."""
    pass


def get_user_id_from_username(database: sqlite3.Connection, username):
    """Get the user_id from a username."""
    return database.execute(
        "SELECT user_id FROM users WHERE name = ?", (username,)
    ).fetchone()
