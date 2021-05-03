from db import db
from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList

from security import authenticate, identity

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'PjK2gt4alvpjZ8B23x'

api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()


# app.config['JWT_AUTH_URL_RULE'] = '/login'
# app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=1800)
jwt = JWT(app, authenticate, identity)  # /auth

# @jwt.error_handler
# def customized_error_handler(error):
#     return jsonify(
#         {'message': error.description, 'code': error.status_code}), error.status_code


api.add_resource(Store, '/store/<string:_id>')
api.add_resource(Item, '/item/<string:_id>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')
api.add_resource(StoreList, '/stores')

if __name__ == '__main__':
    db.init_app(app)
    app.run(debug=True, port=8080)
