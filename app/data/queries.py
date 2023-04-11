CREATE_USERS_TABLE = """
    CREATE TABLE users (
        userId VARCHAR UNIQUE,
        currentBalance INTEGER,
        createdAt TEXT,
        updatedAt TEXT
    );
"""

CREATE_BETS_TABLE = """
    CREATE TABLE bets (
        userId VARCHAR,
        amount INTEGER,
        number INTEGER,
        color TEXT,
        isActive INTEGER,
        createdAt TEXT,
        updatedAt TEXT
    );
"""

ADD_USER = "INSERT INTO users VALUES (:user_id, 100, :created_at, '')"

FETCH_USER = "SELECT * FROM users WHERE userId = :user_id"

FETCH_USERS = "SELECT * FROM users WHERE userId IN ({})"

UPDATE_USER_COINS = """
    UPDATE users
    SET currentBalance = :balance, updatedAt = :updated_at
    WHERE userId = :user_id
"""

ADD_BET = "INSERT INTO bets VALUES (:user_id, :amount, :number, :color, 1, :created_at, '')"

FETCH_ACTIVE_BETS_BY_USER = "SELECT * FROM bets WHERE userId = :user_id AND isActive = 1"

FETCH_ACTIVE_BETS_ALL = "SELECT * FROM bets WHERE isActive = 1"

UPDATE_BETS_DEACTIVATE_ALL = """
    UPDATE bets
    SET isActive = 0, updatedAt = :updated_at
    WHERE isActive = 1
"""

WIPE_USERS = "DELETE FROM users"
WIPE_BETS = "DELETE FROM bets"
