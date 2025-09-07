## How it works:

connect_db() → connects to MySQL server.

create_database() → ensures ALX_prodev exists.

connect_to_prodev() → connects to that database.

create_table() → ensures the user_data table exists.

insert_data() → populates the table from user_data.csv, avoiding duplicates.

stream_rows() → generator that streams rows one by one (useful for large datasets).

Example usage of the generator:
```bash
connection = connect_to_prodev()
for row in stream_rows(connection):
    print(row)
connection.close()
````