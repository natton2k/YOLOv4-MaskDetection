import sqlite3

CONNECTION_URL = "thermal.db"

def getConnection():
    return sqlite3.connect(CONNECTION_URL)
