import mysql.connector
from mysql.connector import Error
from config import DB_CONFIG

def getConnection():
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except Error as e:
        raise RuntimeError(f"DB connection failed")

def executeQuery(query, params=None, fetch=False, fetch_one=False):
    conn = getConnection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(query, params or ())
        if fetch_one:
            return cursor.fetchone()
        if fetch:
            return cursor.fetchall()
        conn.commit()
        return cursor.lastrowid
    except Error as e:
        conn.rollback()
        raise RuntimeError(str(e))
    finally:
        cursor.close()
        conn.close()