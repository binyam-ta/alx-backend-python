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


seed = __import__('seed')

def stream_users_in_batches(batch_size):
    """Generator that fetches rows from user_data in batches."""
    offset = 0
    while True:
        connection = seed.connect_to_prodev()
        cursor = connection.cursor(dictionary=True)
        cursor.execute(f"SELECT * FROM user_data LIMIT {batch_size} OFFSET {offset}")
        rows = cursor.fetchall()
        cursor.close()
        connection.close()
        if not rows:
            break
        yield rows
        offset += batch_size

def batch_processing(batch_size):
    """Process each batch to filter users over the age of 25."""
    for batch in stream_users_in_batches(batch_size):
        for user in batch:
            if user['age'] > 25:
                print(user)
