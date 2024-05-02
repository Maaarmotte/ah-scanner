import json
import sqlite3

CREATE_QUERY = """
    CREATE TABLE IF NOT EXISTS market_entry (
    id INTEGER PRIMARY KEY,
    timestamp TIMESTAMP,
    session TEXT,
    entry TEXT)"""

INSERT_QUERY = "INSERT INTO market_entry (timestamp, session, entry) VALUES (?, ?, ?)"

SELECT_ALL_JSON_QUERY = "SELECT entry FROM market_entry"


class MarketEntriesStorage:
    def __init__(self):
        self.file = 'db.sqlite'
        self.create_table()

    def create_table(self):
        conn = sqlite3.connect(self.file)
        cursor = conn.cursor()
        cursor.execute(CREATE_QUERY)
        conn.commit()
        conn.close()

    def insert_market_entry(self, timestamp: int, session: str, str_data: str):
        conn = sqlite3.connect(self.file)
        cursor = conn.cursor()
        cursor.execute(INSERT_QUERY, (timestamp, session, str_data))
        conn.commit()
        conn.close()

    def get_all_market_entries(self):
        conn = sqlite3.connect(self.file)
        cursor = conn.cursor()
        cursor.execute(SELECT_ALL_JSON_QUERY)
        rows = cursor.fetchall()
        conn.close()

        return [json.loads(row[0]) for row in rows]
