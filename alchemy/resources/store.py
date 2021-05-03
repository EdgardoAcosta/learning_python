from flask_restful import Resource
from models.store import StoreModel


class Store(Resource):
    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        return {'message': 'Store not found'}, 404

    def post(self, name):
        if StoreModel.find_by_name(name):
            return {'message': 'Store already exist'}, 400

        store = StoreModel(name)
        try:
            store.save_to_db()
        except:
            return {'message': 'Error creating store'}, 500

        return store.json()

    def delete(self, _id):
        store = StoreModel.find_by_id(_id)
        if store:
            store.delete_from_db()
        return {'message': 'Store deleted'}


class StoreList(Resource):
    def get(self):
        return {'store': [store.json() for store in StoreModel.query.all()]}
