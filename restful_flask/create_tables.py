import sqlite3


if __name__ == '__main__':
    connection = sqlite3.connect("data.db")

    cursor = connection.cursor()

    create_table_users = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username text UNIQUE , password text)"
    create_table_items = "CREATE TABLE IF NOT EXISTS items (id INTEGER PRIMARY KEY, name text UNIQUE , price real)"

    cursor.execute(create_table_users)
    cursor.execute(create_table_items)

    connection.commit()

    connection.close()
