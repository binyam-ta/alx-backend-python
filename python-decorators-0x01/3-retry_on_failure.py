import time
import sqlite3
import functools


def with_db_connection(func):
    """Decorator to handle opening and closing DB connections automatically"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect("users.db")
        try:
            return func(conn, *args, **kwargs)
        finally:
            conn.close()
            print("🔒 Connection closed")
    return wrapper


def retry_on_failure(retries=3, delay=2):
    """Decorator to retry a function if it raises an exception"""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempt = 0
            while attempt < retries:
                try:
                    result = func(*args, **kwargs)
                    if attempt > 0:
                        print(f"✅ Succeeded on attempt {attempt + 1}")
                    return result
                except Exception as e:
                    attempt += 1
                    print(f"⚠ Attempt {attempt} failed: {e}")
                    if attempt < retries:
                        print(f"⏳ Retrying in {delay} seconds...")
                        time.sleep(delay)
                    else:
                        print("❌ All retries failed")
                        raise e
        return wrapper
    return decorator


@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()


# Example usage
if __name__ == "__main__":
    users = fetch_users_with_retry()
    print("Fetched users:", users)
