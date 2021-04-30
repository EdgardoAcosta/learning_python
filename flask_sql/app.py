from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required
import uuid


from security import authenticate, identity

app = Flask(__name__)

app.secret_key = 'PjK2gt4alvpjZ8B23x'

api = Api(app)

jwt = JWT(app, authenticate, identity)  # /auth

items = []


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help='This fields is required'
                        )

    @jwt_required()
    def get(self, _id):
        item = next(filter(lambda x: x['id'] == _id, items), None)
        return {'item': item}, 200 if item else 400

    @jwt_required()
    def post(self, _id):
        if next(filter(lambda x: x['id'] == _id, items), None):
            return {message: 'ID already exists'}, 400

        request_data = Item.parser.parse_args()
        item = {
            'id': _id,
            'name': request_data['name'],
            'price': request_data['price']
        }
        items.append(item)
        return item, 201

    def delete(self, _id):
        global items
        items = list(filter(lambda x: x['id'] != _id, items))
        return {'message': 'Item deleted'}

    def put(self, _id):

        data = Item.parser.parse_args()
        item = next(filter(lambda x: x['id'] == _id, items), None)
        if item is None:
            item = {'id': _id, 'price': data['price']}
            items.append(item)
        else:
            item.update(date)
        return item


class ItemList(Resource):
    @jwt_required()
    def get(self):
        return {'items': items}


api.add_resource(Item, '/item/<string:_id>')
api.add_resource(ItemList, '/items')


if __name__ == '__main__':
    app.run(debug=True, port=8080)
