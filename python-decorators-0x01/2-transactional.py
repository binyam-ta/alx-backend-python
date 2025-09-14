import sqlite3
import functools


def with_db_connection(func):
    """Decorator that opens and closes a database connection automatically"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect("users.db")
        try:
            return func(conn, *args, **kwargs)
        finally:
            conn.close()
            print("🔒 Connection closed")
    return wrapper


def transactional(func):
    """Decorator that wraps a function inside a transaction"""
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        try:
            result = func(conn, *args, **kwargs)
            conn.commit()   # commit if no errors
            print("✅ Transaction committed")
            return result
        except Exception as e:
            conn.rollback()  # rollback if an error occurs
            print("❌ Transaction rolled back due to error:", e)
            raise e
    return wrapper


@with_db_connection
@transactional
def update_user_email(conn, user_id, new_email):
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id))


# Example usage
if __name__ == "__main__":
    try:
        update_user_email(user_id=1, new_email="Crawford_Cartwright@hotmail.com")
        print("User email updated successfully ✅")
    except Exception as e:
        print("Update failed ❌:", e)
