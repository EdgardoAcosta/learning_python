from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity

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
    parser.add_argument('store_id',
                        type=str,
                        required=True,
                        help='This fields is required'
                        )

    @jwt_required
    def get(self, _id):
        item = ItemModel.find_by_id(_id)
        if item:
            return item.json(), 200

        return {'message': "Item not found"}, 400

    @jwt_required
    def post(self, _id):
        request_data = Item.parser.parse_args()

        if ItemModel.find_by_name(request_data['name']):
            return {"message": 'Name already exists'}, 400

        item = ItemModel(
            request_data['name'],
            request_data['price'],
            request_data['store_id']
        )
        try:
            result = item.save_to_db()
            return item.json(), 201
        except Exception:
            return {"message": 'Error creating item'}, 500

    @jwt_required
    def delete(self, _id):
        claims = get_jwt()
        try:
            if not claims['is_admin']:
                return {"message": 'cant access this method'}, 201
            item = ItemModel.find_by_id(_id)
            if item:
                item.delete_from_db()
            return {"message": 'Item deleted'}, 201

        except:
            return {"message": 'Error deleting item'}, 500

    def put(self):

        data = Item.parser.parse_args()

        try:
            item = ItemModel.find_by_name(data['name'])
            if item is None:
                item = ItemModel(**data)
            else:
                item.price = data['price']

            item.save_to_db()
            return item.json(), 200

        except Exception:
            return {"message": "Error saving data"}, 500


class ItemList(Resource):
    @jwt_required(optional=True)
    def get(self):
        try:
            user_id = get_jwt_identity()
            items = [item.json() for item in ItemModel.query.all()]
            if user_id:
                return {'item': items}
            return {
                'item': [item['name'] for item in ItemModel.query.all()],
                'message': 'More data only for admins'
            }
        except Exception:
            return {"message": 'Error deleting item'}, 500
