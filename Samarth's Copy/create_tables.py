import sqlite3

connection = sqlite3.connect('data.db')
cursor = connection.cursor()

create_table = "CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY, username text, password text)"
cursor.execute(create_table)

create_table_forums = "CREATE TABLE IF NOT EXISTS forums (forum_id INTEGER PRIMARY KEY, name text, user_id INTEGER)"
cursor.execute(create_table_forums)

create_table_forums = "CREATE TABLE IF NOT EXISTS threads (thread_id INTEGER PRIMARY KEY, forum_id INTEGER, title text, text text)"
cursor.execute(create_table_forums)

create_table_forums = "CREATE TABLE IF NOT EXISTS posts (id INTEGER PRIMARY KEY, thread_id INTEGER, user_id INTEGER, text text, timestamp DateTime)"
cursor.execute(create_table_forums)


connection.commit()

connection.close()
