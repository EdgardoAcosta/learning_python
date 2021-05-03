from flask import Flask,jsonify
from flask_restful import Api
from flask_jwt import JWT
from user import UserRegister
from item import Item, ItemList

from security import authenticate, identity

app = Flask(__name__)

app.secret_key = 'PjK2gt4alvpjZ8B23x'

api = Api(app)

app.config['JWT_AUTH_URL_RULE'] = '/login'
# app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=1800)
jwt = JWT(app, authenticate, identity)  # /auth


# @jwt.error_handlerdef
# def customized_error_handler(error):
#     return jsonify(
#         {'message': error.description, 'code': error.status_code}), error.status_code


api.add_resource(Item, '/item/<string:_id>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':

    app.run(debug=True, port=8080)
