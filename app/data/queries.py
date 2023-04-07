CREATE_USERS_TABLE = """
    CREATE TABLE users (
        userId VARCHAR UNIQUE,
        currentBalance INTEGER,
        hasActiveBets INTEGER,
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
        createdAt TEXT
    );
"""

ADD_USER = "INSERT INTO users VALUES (:user_id, 100, 0, :created_at, '')"

FETCH_USER = "SELECT * FROM users WHERE userId = :user_id"

ADD_BET = "INSERT INTO bets VALUES (:user_id, :amount, :number, :color, 1, :created_at)"

FETCH_ACTIVE_BETS_BY_USER = "SELECT * FROM bets WHERE userId = :user_id AND isActive = 1"
