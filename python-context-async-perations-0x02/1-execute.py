import sqlite3

class ExecuteQuery:
    """Reusable context manager for executing a database query."""
    def __init__(self, db_name, query, params=None):
        self.db_name = db_name
        self.query = query
        self.params = params or ()
        self.conn = None
        self.results = None

    def __enter__(self):
        # Open the database connection
        self.conn = sqlite3.connect(self.db_name)
        cursor = self.conn.cursor()
        # Execute the query with parameters
        cursor.execute(self.query, self.params)
        self.results = cursor.fetchall()
        return self.results

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Close the connection
        if self.conn:
            self.conn.close()
        # Do not suppress exceptions
        return False

# Example usage
if __name__ == "__main__":
    query = "SELECT * FROM users WHERE age > ?"
    params = (25,)

    with ExecuteQuery("users.db", query, params) as results:
        for row in results:
            print(row)
