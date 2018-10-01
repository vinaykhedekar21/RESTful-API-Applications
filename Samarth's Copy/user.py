import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required, current_identity
from flask import Response


class User:
    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls, username):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE username = ?"
        result = cursor.execute(query, (username,))
        row = result.fetchone()
        if row:
            user = cls(*row)
        else:
            user = None

        connection.close()
        return user

    @classmethod
    def find_by_id(cls, _id):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE user_id = ?"
        result = cursor.execute(query, (_id,))
        row = result.fetchone()
        if row:
            user = cls(*row)
        else:
            user = None

        connection.close()
        return user


class UserUpdation(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="This field cannot be blank.")
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="This field cannot be blank.")

    @jwt_required()
    def put(self, username):
        data = UserUpdation.parser.parse_args()
        if User.find_by_username(username) is None:
            return {"message": "user with that name not found"}, 404
        if (current_identity.username != username):
            return {"message": "not authenticated user"}, 409

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "update users set username = ?, password = ? where username = ?"
        cursor.execute(query, (data['username'], data['password'], username))

        connection.commit()
        connection.close()

        return {"message": "user updated successfully"}, 200


class UserRegister(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type = str,
                        required=True,
                        help="This field cannot be blank.")
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="This field cannot be blank.")

    def post(self):
        data = UserRegister.parser.parse_args()

        if User.find_by_username(data['username']):
            return {"message":"user with that name already exists"}, 409

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "INSERT INTO users VALUES (NULL,?,?)"
        cursor.execute(query, (data['username'], data['password']))

        connection.commit()
        connection.close()
        resp = Response(status=201, mimetype='application/json')
        return resp
