import sqlite3
from flask_restful import Resource, reqparse
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt)
from blacklist import BLACKLIST
from models.user import UserModel

_user_parser = reqparse.RequestParser()
_user_parser.add_argument('username',
                          type=str,
                          required=True,
                          help="This field cannot be left blank!"
                          )
_user_parser.add_argument('password',
                          type=str,
                          required=True,
                          help="This field cannot be left blank!"
                          )


class UserRegister(Resource):

    def post(self):

        try:
            data = _user_parser.parse_args()

            if UserModel.find_by_username(data['username']):
                return {"message": "User already exists"}, 400

            UserModel(**data).save_to_db()
            return {"message": "User created successfully."}, 201
        except TypeError:
            print("error")
            return {"message", "Error saving user"}, 400


class User(Resource):
    @classmethod
    def get(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': 'User not exist'}, 404

        return user.json()

    @classmethod
    def delete(cls, user_id):

        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': 'User not exist'}, 404

        user.delete_from_db()
        return {'message': 'User deleted'}


class UserLogin(Resource):

    @classmethod
    def post(cls):
        data = _user_parser.parse_args()

        user = UserModel.find_by_username(data['username'])

        if user and safe_str_cmp(user.password, data['password']):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return{
                'access_token': access_token,
                'refresh_token': refresh_token
            }, 200
        return {'message': 'Invalid credentials'}, 401


class UserLogout(Resource):

    @jwt_required
    def post(self):
        jti = get_jwt()['jti']
        BLACKLIST.add(jti)
        return {'message': 'Succefully logout'}, 200


class TokenRefresh(Resource):

    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt()
        print(current_user)
        new_token = create_access_token(
            identity=current_user["sub"], fresh=False)
        return{'access_token': new_token}, 200
