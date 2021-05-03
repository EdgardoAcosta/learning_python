import sqlite3

connection = sqlite3.connect("data.db")
cursor = connection.cursor()


cursor.execute("CREATE TABLE user (id int, username text, password text)")


connection.commit


connection.close()
