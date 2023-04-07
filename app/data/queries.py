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
