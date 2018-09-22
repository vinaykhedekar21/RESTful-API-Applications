import sqlite3
from flask_restful import Resource, reqparse
from flask import Response
from flask_jwt import jwt_required,current_identity


class Forumname:
    def __init__(self, _id, name, creator):
        self.id = _id
        self.name = name
        self.creator = creator

    @classmethod
    def find_by_forumname(cls, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM forums WHERE name = ?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        if row:
            frm = cls(*row)
        else:
            frm = None

        connection.close()
        return frm

    @classmethod
    def get_forum_id(cls):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM forums ORDER BY forum_id DESC"
        result = cursor.execute(query)
        row = result.fetchone()
        if row:
            forum_id = (row[0])
        else:
            forum_id = None

        connection.close()
        return forum_id

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
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "SELECT f.forum_id as id, f.name as name, u.username as creator FROM forums f, users u where f.user_id = u.user_id"
        result = cursor.execute(query)
        rows = result.fetchall()
        connection.close()
        forumdic = []
        if rows:
            for row in rows:
                forumdic.append({"id":row[0],"name":row[1],"creator":row[2]})
            return forumdic, 200
        return {}
    @jwt_required()
    def post(self):
        data = Forum.parser.parse_args()
        if Forumname.find_by_forumname(data['name']):
            return {"message":"forum with that name already exists"}, 409
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        user_id = Forumname.get_user_id(current_identity.username)
        if user_id:
            query = "INSERT INTO forums VALUES (NULL,?,?)"
            cursor.execute(query, (data['name'], user_id))

        connection.commit()
        resp = Response(status=201, mimetype='application/json')
        forum_id = Forumname.get_forum_id()
        if forum_id:
            resp.headers['Location'] = 'http://127.0.0.1:5000/forums/'+str(forum_id)
        connection.close()
        return resp