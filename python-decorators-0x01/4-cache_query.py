import sqlite3
import functools
import time

# Global dictionary to store cached queries
query_cache = {}

def with_db_connection(func):
    """Decorator to automatically open and close DB connection"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect("users.db")
        try:
            return func(conn, *args, **kwargs)
        finally:
            conn.close()
            print("🔒 Connection closed")
    return wrapper

def cache_query(func):
    """Decorator to cache query results based on the query string"""
    @functools.wraps(func)
    def wrapper(conn, query, *args, **kwargs):
        if query in query_cache:
            print("🟢 Returning cached result")
            return query_cache[query]
        print("🟡 Executing query and caching result")
        result = func(conn, query, *args, **kwargs)
        query_cache[query] = result
        return result
    return wrapper

# Example usage
@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

if __name__ == "__main__":
    # First call will execute and cache
    users = fetch_users_with_cache(query="SELECT * FROM users")
    print(users[:2])  # Print first 2 rows

    # Second call will use cache
    users_again = fetch_users_with_cache(query="SELECT * FROM users")
    print(users_again[:2])
