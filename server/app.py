#!/usr/bin/env python3

from flask import request, session
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError

from config import app, db, api
from models import User, Recipe

class Signup(Resource):
    def post(self):
        if not request.json or 'username' not in request.json or 'password' not in request.json:
            return {'message': 'Missing username or password'}, 422

        username = request.json['username']
        password = request.json['password']

        if not username or not password:
            return {'message': 'Missing username or password'}, 400

        try:
            user = User(username=username)
            user.set_password(password)  # Assuming you have a method to hash and set the password

            db.session.add(user)
            db.session.commit()

            session['user_id'] = user.id
            return {'message': 'User created'}, 201

        except IntegrityError:
            db.session.rollback()
            return {'message': 'User already exists'}, 409
class CheckSession(Resource):
     def get(self):
        if 'user_id' in session:
            user = User.query.get(session['user_id'])
            return {
                'user_id': user.id,
                'username': user.username,
                'image_url': user.image_url,
                'bio': user.bio
            }, 
        else:
            return {'message': 'Unauthorized'}, 401

class Login(Resource):
    pass

class Logout(Resource):
    pass

class RecipeIndex(Resource):
    pass

api.add_resource(Signup, '/signup', endpoint='signup')
api.add_resource(CheckSession, '/check_session', endpoint='check_session')
api.add_resource(Login, '/login', endpoint='login')
api.add_resource(Logout, '/logout', endpoint='logout')
api.add_resource(RecipeIndex, '/recipes', endpoint='recipes')


if __name__ == '__main__':
    app.run(port=5555, debug=True)