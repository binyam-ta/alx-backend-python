import sqlite3
import functools
import datetime

# decorator to log SQL queries
def log_queries(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        query = kwargs.get("query") or (args[0] if args else None)
        if query:
            log_entry = f"[{datetime.datetime.now()}] Executing SQL Query: {query}\n"
            # Print to console
            print(log_entry.strip())
            # Write to log file
            with open("queries.log", "a") as log_file:
                log_file.write(log_entry)
        return func(*args, **kwargs)
    return wrapper


@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results


# fetch users while logging the query
if __name__ == "__main__":
    users = fetch_all_users(query="SELECT * FROM users")
    print(users)
