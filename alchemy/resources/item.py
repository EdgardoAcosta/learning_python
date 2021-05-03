import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help='This fields is required'
                        )
    parser.add_argument('name',
                        type=str,
                        required=True,
                        help='This fields is required'
                        )

    @jwt_required()
    def get(self, _id):
        item = ItemModel.find_by_id(_id)
        if item:
            return item.json(), 200

        return {'message': "Item not found"}, 400

    @jwt_required()
    def post(self, _id):
        request_data = Item.parser.parse_args()

        if ItemModel.find_by_name(request_data['name']):
            return {"message": 'Name already exists'}, 400

        item = ItemModel(
            request_data['name'],
            request_data['price']
        )
        try:
            result = item.insert()
            return item.json(), 201
        except Exception:
            return {"message": 'Error creating item'}, 500

    def delete(self, _id):
        try:
            connection = sqlite3.connect('data.db')
            cursor = connection.cursor()
            query = "DELETE FROM items WHERE id =?"
            result = cursor.execute(query, (_id,))
            connection.commit()
            connection.close()
            return {"message": 'Item deleted'}, 201

        except:
            return {"message": 'Error deleting item'}, 500

    def put(self):

        data = Item.parser.parse_args()
        updated_item = ItemModel(data['name'], data['price'])

        try:
            item = ItemModel.find_by_name(data['name'])
            if item is None:
                updated_item.insert()
            else:
                updated_item.update()
            return {"message": "Item updated"}, 200

        except Exception:
            return {"message": "Error saving data"}, 500


class ItemList(Resource):
    @jwt_required()
    def get(self):
        try:
            connection = sqlite3.connect('data.db')
            cursor = connection.cursor()
            query = "SELECT * FROM items"
            result = cursor.execute(query)
            connection.commit()
            connection.close()
            items = []
            for row in result:
                items.append({
                    "id": row[0],
                    "name": row[1],
                    "price": row[2],
                })
            return {"items": items}, 201

        except Exception:
            return {"message": 'Error deleting item'}, 500
