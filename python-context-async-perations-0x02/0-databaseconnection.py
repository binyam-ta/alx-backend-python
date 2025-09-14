import sqlite3

class DatabaseConnection:
    """Custom class-based context manager for SQLite database connections."""
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = None

    def __enter__(self):
        # Open the connection when entering the context
        self.conn = sqlite3.connect(self.db_name)
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Commit changes if no exception occurred, otherwise rollback
        if exc_type is None:
            self.conn.commit()
        else:
            self.conn.rollback()
        # Close the connection
        self.conn.close()
        # Do not suppress exceptions
        return False

# Example usage
if __name__ == "__main__":
    with DatabaseConnection("users.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        results = cursor.fetchall()
        for row in results:
            print(row)
