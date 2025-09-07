#!/usr/bin/python3
import mysql.connector
import csv
import uuid

DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "your_mysql_password"  # replace with your MySQL password
DB_NAME = "ALX_prodev"
TABLE_NAME = "user_data"

def connect_db():
    """Connects to the MySQL server."""
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

def create_database(connection):
    """Creates ALX_prodev database if it does not exist."""
    cursor = connection.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME};")
    cursor.close()
    print(f"Database {DB_NAME} ensured.")

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

def create_table(connection):
    """Creates the user_data table if it does not exist."""
    cursor = connection.cursor()
    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
            user_id CHAR(36) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            age DECIMAL NOT NULL
        );
    """)
    cursor.close()
    print(f"Table {TABLE_NAME} created successfully")

def insert_data(connection, csv_file):
    """Inserts data from CSV file into the user_data table."""
    cursor = connection.cursor()
    with open(csv_file, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Avoid duplicates
            cursor.execute(f"SELECT * FROM {TABLE_NAME} WHERE email = %s", (row['email'],))
            if cursor.fetchone() is None:
                cursor.execute(f"""
                    INSERT INTO {TABLE_NAME} (user_id, name, email, age)
                    VALUES (%s, %s, %s, %s)
                """, (str(uuid.uuid4()), row['name'], row['email'], row['age']))
    connection.commit()
    cursor.close()
    print(f"Data from {csv_file} inserted successfully")

def stream_rows(connection):
    """Generator to yield rows from the user_data table one by one."""
    cursor = connection.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM {TABLE_NAME};")
    for row in cursor:
        yield row
    cursor.close()
