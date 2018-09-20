import flask
import sqlite3
from flask import g

app = flask.Flask('DiscussionForumAPI')
app.config.from_object(__name__)
app.config.from_envvar('DISCUSSIONFORUMAPI_SETTINGS', silent=True)
app.config["DEBUG"] = True

DATABASE = '/tmp/DiscussionForum.db'


# create database connection
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


# close connection when not in use
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


# create initial schema's
def create_schema():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


@app.cli.command('createschema')
def create_schema_command():
    """Initializes the database. and create schema"""
    create_schema()
    print('Database Schema Created')


# Insert dummy data into database
def insert_data():
    with app.app_context():
        db = get_db()
        with app.open_resource('insertScript.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


@app.cli.command('insertdata')
def insert_data_command():
    """Insert dummy data to database"""
    insert_data()
    print('Dummy data inserted to database')

# Initial operations completed ###


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


# common query function
def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


for user in query_db('select * from user'):
    print(user['username'], 'has Id', user['user_id'])


app.run()
