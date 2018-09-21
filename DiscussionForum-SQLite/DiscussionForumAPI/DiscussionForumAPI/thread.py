import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required, current_identity
from datetime import datetime
from flask import Response
from DiscussionForum import get_db
from DiscussionForum import query_db


class Threadname:
    def __init__(self, _id, name, creator):
        self.id = _id
        self.name = name
        self.creator = creator

    @classmethod
    def find_by_forumid(cls, forumid):

        rv = query_db('select * from forum where id = ?',
                      [forumid], one=True)
        return rv[0] if rv else None

        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()
        #
        # query = "SELECT * FROM forums WHERE id = ?"
        # result = cursor.execute(query, (forumid,))
        # row = result.fetchone()
        # if row:
        #     frm = cls(*row)
        # else:
        #     frm = None
        #
        # connection.close()
        # return frm

    @classmethod
    def get_Thread_id(cls):

        rv = query_db('SELECT thread_id FROM thread ORDER BY id DESC', one=True)
        return rv[0] if rv else None

        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()
        #
        # query = "SELECT * FROM threads ORDER BY id DESC"
        # result = cursor.execute(query)
        # row = result.fetchone()
        # if row:
        #     thread_id = (row[0])
        # else:
        #     thread_id = None
        #
        # connection.close()
        # return thread_id


class Thread(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('title',
                        type=str,
                        required=True,
                        help="This field cannot be blank.")
    parser.add_argument('content',
                        type=str,
                        required=True,
                        help="This field cannot be blank.")
    # parser.add_argument('creator',
    #                     type=str,
    #                     required=True,
    #                     help="This field cannot be blank.")

    def get(self, forum_id):

        rv = query_db('SELECT * FROM thread t where t.forumid = ?',
                      [forum_id], one=False)
        return rv[0] if rv else None

        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()
        # query = "SELECT * FROM threads t where t.forumid = ?"
        # result = cursor.execute(query, (forum_id,))
        # rows = result.fetchall()
        # connection.close()

        threadlist = []
        if rv:
            for row in rv:
                threadlist.append({"id": row[0], "title": row[2], "creator": row[3]})
            return threadlist, 200
        return {}, 404

    @jwt_required()
    def post(self, forum_id):
        data = Thread.parser.parse_args()
        if Threadname.find_by_forumid(forum_id) is None:
            return {"message":"forum does not exist"}, 404

        connection = get_db()
        cursor = connection.cursor()

        query = "INSERT INTO thread VALUES (NULL,?,?,?,?)"
        cursor.execute(query, (forum_id, data['title'], current_identity.username, datetime.now()))
        #
        # query = "INSERT INTO forums VALUES (NULL,?,?)"
        # cursor.execute(query, (forum_id, data['creator']))

        connection.commit()
        thread_id = Threadname.get_Thread_id()
        if thread_id:
            query = "INSERT INTO post VALUES (NULL,?,?,?,?,?)"
            cursor.execute(query, (forum_id, thread_id, data['content'], current_identity.username, datetime.now()))
            connection.commit()
            resp = Response(status=201, mimetype='application/json')
            resp.headers['Location'] = 'http://127.0.0.1:5000/forums/' + str(forum_id) +'/'+str(thread_id)

        connection.close()
        return resp