from datetime import datetime
from loguru import logger
import sys

import sqlite3
from sqlite3 import IntegrityError
import atexit

from app.common.decorators import singleton
from app.config import DB_NAME, DATETIME_FORMAT
from app.data.queries import (CREATE_USERS_TABLE,
                              CREATE_BETS_TABLE,
                              ADD_USER,
                              FETCH_USER,
                              FETCH_USERS,
                              ADD_BET,
                              FETCH_ACTIVE_BETS_BY_USER,
                              UPDATE_USER_COINS,
                              FETCH_ACTIVE_BETS_ALL,
                              UPDATE_BETS_DEACTIVATE_ALL)

CONN = sqlite3.connect(DB_NAME)

def cleanup():
    if CONN:
        CONN.close()
        logger.info("DB closed")

atexit.register(cleanup)

@singleton
class SQLiteClient():

    def __init__(self):
        self.db = CONN.cursor()
        self.initialize()

    def initialize(self):
        existing_tables = []
        res = self.get_all_tables()
        for entry in res:
            existing_tables.append(entry[0])
        if "users" not in existing_tables:
            logger.warning("Creating 'users' table")
            self.db.execute(CREATE_USERS_TABLE)
        if "bets" not in existing_tables:
            logger.warning("Creating 'bets' table")
            self.db.execute(CREATE_BETS_TABLE)

    def get_all_tables(self):
        return self.db.execute("SELECT name FROM sqlite_master").fetchall()

    def add_user(self, user_id):
        created_at = datetime.now().strftime(DATETIME_FORMAT)
        data = {"user_id": user_id, "created_at": created_at}
        try:
            self.db.execute(ADD_USER, data)
        except IntegrityError as ie:
            logger.warning(f"User '{user_id}' is already registered")
            return ie
        CONN.commit()
        logger.debug(f"User {user_id} created!")

    def fetch_user_by_id(self, user_id):
        data = {"user_id": user_id}
        try:
            res = self.db.execute(FETCH_USER, data).fetchone()
        except Exception as e:
            logger.error(str(e))
            return None, e
        logger.debug(f"User {user_id} fetched: {res}")
        return res, None

    def fetch_users_by_id(self, user_ids):
        prep_query = FETCH_USERS.format(", ".join("?" * len(user_ids)))
        try:
            res = self.db.execute(prep_query, user_ids).fetchall()
        except Exception as e:
            logger.error(str(e))
            return None, e
        logger.debug(f"Users fetched: {res}")
        return res, None
    
    def add_bet(self, data):
        data["created_at"] = datetime.now().strftime(DATETIME_FORMAT)
        try:
            self.db.execute(ADD_BET, data)
        except Exception as e:
            logger.error(e)
            return e
        CONN.commit()
        logger.debug(f"Bet created")
    
    def fetch_active_bets_by_user(self, user_id):
        try:
            res = self.db.execute(FETCH_ACTIVE_BETS_BY_USER, {"user_id": user_id}).fetchall()
        except Exception as e:
            logger.error(str(e))
            return None, e
        logger.debug(f"Active bets of {user_id} fetched: {res}")
        return res, None
    
    def update_user_coins(self, user_id, balance):
        updated_at = datetime.now().strftime(DATETIME_FORMAT)
        data = {"user_id": user_id, "balance": balance, "updated_at": updated_at}
        try:
            self.db.execute(UPDATE_USER_COINS, data)
        except Exception as e:
            logger.error(str(e))
            return e
        CONN.commit()
        logger.debug(f"User coins updated")

    def update_user_coins_batch(self, data):
        updated_at = datetime.now().strftime(DATETIME_FORMAT)
        for d in data:
            d["updated_at"] = updated_at
        logger.debug(f"Updating user coins with data>>>{data}")
        try:
            self.db.executemany(UPDATE_USER_COINS, data)
        except Exception as e:
            logger.error(str(e))
            return e
        CONN.commit()
        logger.debug(f"User coins batch updated")

    def fetch_active_bets_all(self):
        updated_at = datetime.now().strftime(DATETIME_FORMAT)
        try:
            res = self.db.execute(FETCH_ACTIVE_BETS_ALL, {"updated_at": updated_at}).fetchall()
        except Exception as e:
            logger.error(str(e))
            return None, e
        logger.debug(f"All active bets fetched>>>{res}")
        return res, None

    def update_bets_deactivate_all(self):
        updated_at = datetime.now().strftime(DATETIME_FORMAT)
        try:
            self.db.execute(UPDATE_BETS_DEACTIVATE_ALL, {"updated_at": updated_at})
        except Exception as e:
            logger.error(str(e))
            return e
        CONN.commit()
        logger.debug("All active bets were deactivated")
