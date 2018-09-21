import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required, current_identity
from datetime import datetime
from flask import Response
from DiscussionForum import query_db
from DiscussionForum import get_db

class Postname:
    def __init__(self, _id, name, creator):
        self.id = _id
        self.name = name
        self.creator = creator

    @classmethod
    def find(cls, forumid, threadid):
        rv = query_db('SELECT * FROM thread WHERE id = ? and forumid = ?',
                      [threadid], [forumid], one=True)
        return rv[0] if rv else None

        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()
        #
        # query = "SELECT * FROM threads WHERE id = ? and forumid = ?"
        # result = cursor.execute(query, (threadid, forumid))
        # row = result.fetchone()
        # connection.close()
        # if row:
        #     return row
        # return None

    # @classmethod
    # def get_Thread_id(cls):
    #     connection = sqlite3.connect('data.db')
    #     cursor = connection.cursor()
    #
    #     query = "SELECT * FROM threads ORDER BY id DESC"
    #     result = cursor.execute(query)
    #     row = result.fetchone()
    #     if row:
    #         thread_id = (row[0])
    #     else:
    #         thread_id = None
    #
    #     connection.close()
    #     return thread_id


class Post(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('content',
                        type=str,
                        required=True,
                        help="This field cannot be blank.")
    # parser.add_argument('creator',
    #                     type=str,
    #                     required=True,
    #                     help="This field cannot be blank.")

    def get(self, forum_id, thread_id):
        if Postname.find(forum_id, thread_id) is None:
            return {"message":"forum / thread does not exist"}, 404
        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()
        # query = "SELECT * FROM posts where threadid = ? and forumid = ? order by timestamp desc"
        # result = cursor.execute(query, (thread_id, forum_id))
        # rows = result.fetchall()
        # connection.close()

        rv = query_db('SELECT * FROM post where thread_id = ? and forum_id = ? order by timestamp desc',
                      [thread_id], [forum_id], one=False)
        return rv[0] if rv else None

        postlist = []
        if rv:
            for row in rv:
                postlist.append({"author": row[4], "text": row[3], "timestamp": row[5]})
            return postlist, 200
        return {}, 404


    @jwt_required()
    def post(self, forum_id, thread_id):
        data = Post.parser.parse_args()
        if Postname.find(forum_id, thread_id) is None:
            return {"message":"forum / thread does not exist"}, 404

        connection = get_db()
        cursor = connection.cursor()

        query = "INSERT INTO post VALUES (NULL,?,?,?,?,?)"
        cursor.execute(query, (forum_id, thread_id, data['content'], current_identity.username, datetime.now()))

        #
        # query = "INSERT INTO forums VALUES (NULL,?,?)"
        # cursor.execute(query, (forum_id, data['creator']))

        connection.commit()
        # thread_id = Threadname.get_Thread_id()
        # if thread_id:
        #     query = "INSERT INTO posts VALUES (NULL,?,?,?,?,?)"
        #     cursor.execute(query, (forum_id, thread_id, data['content'], data['creator'], datetime.now()))
        #     connection.commit()
        resp = Response(status=201, mimetype='application/json')
        connection.close()
        return resp