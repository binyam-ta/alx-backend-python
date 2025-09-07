#!/usr/bin/python3
import mysql.connector

DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "your_mysql_password"  # replace with your MySQL password
DB_NAME = "ALX_prodev"
TABLE_NAME = "user_data"

def connect_to_prodev():
    """Connects to the ALX_prodev database."""
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

def stream_users():
    """Generator that fetches rows from the user_data table one by one."""
    connection = connect_to_prodev()
    if not connection:
        return

    cursor = connection.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM {TABLE_NAME};")

    for row in cursor:
        yield row  # yield each row one by one

    cursor.close()
    connection.close()
