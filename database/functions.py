from database.base import Database
import logging


def create_user(telegram_id):
    db = Database("lol")
    result = db.query("SELECT * FROM users WHERE tg_id = %s;", [telegram_id], fetchone=True)
    if result is not None:
        return 1
    db.query("INSERT INTO users (tg_id) VALUES (%s);", [telegram_id])
    return 0