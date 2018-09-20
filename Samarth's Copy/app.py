from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from security import authenticate, identity
from user import UserRegister, UserUpdation
from forum import Forum
from thread import Thread
from post import Post
app = Flask(__name__)
app.secret_key = 'sam'
api = Api(app)

jwt = JWT(app, authenticate, identity) #/auth


api.add_resource(Forum,'/forums')
api.add_resource(Thread,'/forums/<forum_id>')
api.add_resource(Post,'/forums/<forum_id>/<thread_id>')
api.add_resource(UserRegister, '/users')
api.add_resource(UserUpdation, '/users/<string:username>')
app.run(port=5000,debug=True)
#Authentication using pip install Flask-JWT
#pip install Flask-RESTful