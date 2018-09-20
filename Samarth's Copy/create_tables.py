import sqlite3

connection = sqlite3.connect('data.db')
cursor = connection.cursor()

create_table = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username text, password text)"
cursor.execute(create_table)

create_table_forums = "CREATE TABLE IF NOT EXISTS forums (id INTEGER PRIMARY KEY, name text, creator text)"
cursor.execute(create_table_forums)

create_table_forums = "CREATE TABLE IF NOT EXISTS threads (id INTEGER PRIMARY KEY, forumid INTEGER, title text, creator text, timestamp DateTime)"
cursor.execute(create_table_forums)

create_table_forums = "CREATE TABLE IF NOT EXISTS posts (id INTEGER PRIMARY KEY, forumid INTEGER, threadid INTEGER, content text, creator text, timestamp DateTime)"
cursor.execute(create_table_forums)


connection.commit()

connection.close()
