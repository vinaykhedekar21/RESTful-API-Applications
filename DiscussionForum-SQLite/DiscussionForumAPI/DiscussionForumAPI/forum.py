import sqlite3
from flask_restful import Resource, reqparse
from flask import Response
from flask_jwt import jwt_required,current_identity
from DiscussionForum import get_db
from DiscussionForum import query_db

class Forumname:
    def __init__(self, _id, name, creator):
        self.id = _id
        self.name = name
        self.creator = creator

    @classmethod
    def find_by_forumname(cls, name):
        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()
        #
        # query = "SELECT * FROM forums WHERE name = ?"
        # result = cursor.execute(query, (name,))
        # row = result.fetchone()
        # if row:
        #     frm = cls(*row)
        # else:
        #     frm = None
        #
        # connection.close()
        # return frm

        rv = query_db('SELECT name FROM forum WHERE name = ?',
                      [name], one=True)
        return rv[0] if rv else None

    @classmethod
    def get_forum_id(cls):
        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()
        #
        # query = "SELECT forum_id FROM forum ORDER BY id DESC"
        # result = cursor.execute(query)
        # row = result.fetchone()
        # if row:
        #     forum_id = (row[0])
        # else:
        #     forum_id = None
        #
        # connection.close()
        # return forum_id

        rv = query_db('SELECT forum_id FROM forum ORDER BY id DESC', one=True)
        return rv[0] if rv else None


class Forum(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name',
                        type=str,
                        required=True,
                        help="This field cannot be blank.")
    # parser.add_argument('creator',
    #                     type=str,
    #                     required=True,
    #                     help="This field cannot be blank.")

    def get(self):
        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()
        # query = "SELECT * FROM forums"
        # result = cursor.execute(query)
        # rows = result.fetchall()
        # connection.close()

        rv = query_db('SELECT * FROM forum', one=False)
        return rv[0] if rv else None

        forumdic = []
        if rv:
            for row in rv:
                forumdic.append({"id":row[0], "name":row[1], "creator":row[2]})
            return forumdic, 200
        return {}, 404

    @jwt_required()
    def post(self):
        data = Forum.parser.parse_args()
        if Forumname.find_by_forumname(data['name']):
            return {"message":"forum with that name already exists"}, 409

        connection = get_db()
        cursor = connection.cursor()

        query = "INSERT INTO forum VALUES (NULL,?,?)"
        cursor.execute(query, (data['name'], current_identity.username))

        connection.commit()

        resp = Response(status=201, mimetype='application/json')

        forum_id = Forumname.get_forum_id()
        if forum_id:
            resp.headers['Location'] = 'http://127.0.0.1:5000/forums/'+str(forum_id)
        connection.close()
        return resp