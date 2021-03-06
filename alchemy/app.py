from db import db
from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager
from resources.user import UserRegister, User, UserLogin, UserLogout, TokenRefresh
from resources.item import Item, ItemList
from resources.store import Store, StoreList
from blacklist import BLACKLIST

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['JWT_SECRET_KEY'] = 'salkdlsakjdlkasjdlkasj23'
app.config['JWT_BLACKLIST_ENABLE'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
app.secret_key = 'PjK2gt4alvpjZ8B23x'

api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()


jwt = JWTManager(app)


@jwt.additional_claims_loader
def add_claims_to_jwt(identity):
    if identity == 1:
        return{'is_admin': True}
    return{'is_admin': False}


@jwt.expired_token_loader
def expire_token_callback():
    return jsonify({
        'description': 'The token has expire',
        'error': 'token_expire'
    }), 401


@jwt.invalid_token_loader
def invalid_toke_callback(error):
    return jsonify({
        'description': 'Signature verification failed',
        'error': 'invalid_token'
    }), 401


@jwt.unauthorized_loader
def unauthorized_loader_callback():
    return jsonify({
        'description': 'Missing required token',
        'error': 'missing_token'
    }), 401


# @jwt.needs_fresh_token_loader
@jwt.revoked_token_loader
def revoked_token_loader_callback():
    return jsonify({
        'description': 'The token has beeen revoke',
        'error': 'revoked_token'
    }), 401


@jwt.token_in_blocklist_loader
def check_if_token_in_blacklist(decrypted_token):
    return decrypted_token['jti'] in BLACKLIST


api.add_resource(Store, '/store/<string:_id>')
api.add_resource(Item, '/item/<string:_id>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')
api.add_resource(StoreList, '/stores')
api.add_resource(User, '/user/<int:user_id>')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout, '/logout')
api.add_resource(TokenRefresh, '/refresh')

if __name__ == '__main__':
    db.init_app(app)
    app.run(debug=True, port=8080)
