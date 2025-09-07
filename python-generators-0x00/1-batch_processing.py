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

def stream_users_in_batches(batch_size):
    """Generator that fetches rows in batches from the user_data table."""
    connection = connect_to_prodev()
    if not connection:
        return

    cursor = connection.cursor(dictionary=True)
    offset = 0

    while True:
        cursor.execute(
            f"SELECT * FROM {TABLE_NAME} LIMIT %s OFFSET %s", (batch_size, offset)
        )
        batch = cursor.fetchall()
        if not batch:
            break
        for row in batch:
            yield row
        offset += batch_size

    cursor.close()
    connection.close()

def batch_processing(batch_size):
    """Processes each batch to filter users over age 25."""
    batch_gen = stream_users_in_batches(batch_size)
    for user in batch_gen:
        if user['age'] > 25:
            print(user)
