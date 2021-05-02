import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required


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
        item = self.find_by_id(_id)
        if item:
            return {'item': item}, 200

        return {'message': "Item not found"}, 400

    @classmethod
    def find_by_id(cls, _id):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "SELECT * FROM items WHERE id =?"
        result = cursor.execute(query, (_id,))
        row = result.fetchone()
        connection.close()
        print(row)
        return row

    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "SELECT * FROM items WHERE name =?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()
        return row

    @jwt_required()
    def post(self, _id):
        request_data = Item.parser.parse_args()

        if self.find_by_name(request_data['name']):
            return {"message": 'Name already exists'}, 400

        item = {
            "name": request_data['name'],
            "item": request_data['price']
        }
        try:
            result = self.insert(item)
            return {"message": 'Item created'}, 201
        except Exception:
            return {"message": 'Error creating item'}, 500

    @classmethod
    def insert(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "INSERT INTO items VALUES (NULL, ?,?)"
        result = cursor.execute(query, (item['name'], item['price']))

        connection.commit()
        connection.close()
        return result

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

    def put(self, _id):

        data = Item.parser.parse_args()
        updated = {
            "name": data['name'],
            "item": data['price']
        }

        try:
            item = self.find_by_id(_id)
            if item is None:
                self.insert(updated)
            else:
                self.update(_id, updated)
            return {"message": "Item updated"}, 200

        except Exception:
            return {"message": "Error saving data"}, 500

    @classmethod
    def update(cls, _id, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "UPDATE items SET price = ? WHERE id =?"
        result = cursor.execute(query, (item["price"], _id))
        connection.commit()
        connection.close()


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
