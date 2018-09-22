import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required, current_identity
from datetime import datetime
from flask import Response


class Postname:
    def __init__(self, _id, name, creator):
        self.id = _id
        self.name = name
        self.creator = creator

    @classmethod
    def find(cls,forumid,threadid):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM threads WHERE thread_id = ? and forum_id = ?"
        result = cursor.execute(query, (threadid, forumid))
        row = result.fetchone()
        connection.close()
        if row:
            return row
        return None

    @classmethod
    def get_user_id(cls, username):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT user_id FROM users where username = ?"
        result = cursor.execute(query, (username,))
        row = result.fetchone()
        if row:
            user_id = (row[0])
        else:
            user_id = None

        connection.close()
        return user_id
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
    parser.add_argument('text',
                        type=str,
                        required=True,
                        help="This field cannot be blank.")
    # parser.add_argument('creator',
    #                     type=str,
    #                     required=True,
    #                     help="This field cannot be blank.")

    def get(self,forum_id,thread_id):
        if Postname.find(forum_id,thread_id) is None:
            return {"message":"forum / thread does not exist"}, 404
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "SELECT u.username as author, p.text, p.timestamp FROM posts p, threads t, users u where t.thread_id = p.thread_id and t.thread_id = ? and t.forum_id = ?  and u.user_id  = p.user_id order by timestamp desc"
        result = cursor.execute(query, (thread_id,forum_id))
        rows = result.fetchall()
        connection.close()
        postlist = []
        if rows:
            for row in rows:
                postlist.append({"author": row[0], "text": row[1], "timestamp": row[2]})
            return postlist, 200
        return {}, 404
    @jwt_required()
    def post(self,forum_id,thread_id):
        data = Post.parser.parse_args()
        if Postname.find(forum_id,thread_id) is None:
            return {"message":"forum / thread does not exist"}, 404
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        user_id = Postname.get_user_id(current_identity.username)
        query = "INSERT INTO posts VALUES (NULL,?,?,?,?)"
        cursor.execute(query, (thread_id, user_id, data['text'], datetime.now()))
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