import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required, current_identity
from datetime import datetime
from flask import Response

class Threadname:
    def __init__(self, _id, name, creator):
        self.id = _id
        self.name = name
        self.creator = creator

    @classmethod
    def find_by_forumid(cls, forumid):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT forum_id FROM forums WHERE forum_id = ?"
        result = cursor.execute(query, (forumid,))
        row = result.fetchone()
        if row:
            frm = (row[0])
        else:
            frm = None

        connection.close()
        return frm

    @classmethod
    def get_Thread_id(cls):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT thread_id FROM threads ORDER BY thread_id DESC"
        result = cursor.execute(query)
        row = result.fetchone()
        if row:
            thread_id = (row[0])
        else:
            thread_id = None

        connection.close()
        return thread_id

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
class Thread(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('title',
                        type=str,
                        required=True,
                        help="This field cannot be blank.")
    parser.add_argument('text',
                        type=str,
                        required=True,
                        help="This field cannot be blank.")
    # parser.add_argument('creator',
    #                     type=str,
    #                     required=True,
    #                     help="This field cannot be blank.")

    def get(self,forum_id):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "select t.thread_id as id,t.title as title, (select p.timestamp from posts p, threads t WHERE t.thread_id = p.thread_id and t.forum_id = ? order by p.id desc) as timestamp, (select u.username from posts p, threads t, users u WHERE t.thread_id = p.thread_id and t.forum_id = ?  and p.user_id = u.user_id order by p.id asc) as creator, t.title from threads t"
        result = cursor.execute(query, (forum_id,forum_id))
        rows = result.fetchall()
        connection.close()
        threadlist = []
        if rows:
            for row in rows:
                threadlist.append({"id": row[0], "title": row[1], "creator": row[3], "timestamp": row[2]})
            return threadlist, 200
        return {}, 404
    @jwt_required()
    def post(self,forum_id):
        data = Thread.parser.parse_args()
        if Threadname.find_by_forumid(forum_id) is None:
            return {"message":"forum does not exist"}, 404
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "INSERT INTO threads VALUES (NULL,?,?,?)"
        cursor.execute(query, (forum_id, data['title'],data['text']))
        #
        # query = "INSERT INTO forums VALUES (NULL,?,?)"
        # cursor.execute(query, (forum_id, data['creator']))

        connection.commit()
        thread_id = Threadname.get_Thread_id()
        user_id = Threadname.get_user_id(current_identity.username)
        if thread_id:
            query = "INSERT INTO posts VALUES (NULL,?,?,?,?)"
            cursor.execute(query, (thread_id, user_id, data['text'], datetime.now()))
            connection.commit()
            resp = Response(status=201, mimetype='application/json')
            resp.headers['Location'] = 'http://127.0.0.1:5000/forums/' + str(forum_id) +'/'+str(thread_id)

        connection.close()
        return resp