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
    connect = getConnection()
    cursor = connect.cursor(dictionary=True)
    try:
        cursor.execute(query, params or ())
        if fetch_one:
            return cursor.fetchone()
        if fetch:
            return cursor.fetchall()
        connect.commit()
        return cursor.lastrowid
    except Error as e:
        connect.rollback()
        raise RuntimeError(str(e))
    finally:
        cursor.close()
        connect.close()