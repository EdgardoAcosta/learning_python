from flask import Flask, jsonify, request
import uuid
app = Flask(__name__)

stores = [
    {
        'id': '1',
        'name': 'store1',
        'items': [
            {
                'name': 'item1',
                'price': 15.99,
            }
        ]
    }
]


@app.route('/')
def home():
    return jsonify({"server": "ok"})


@app.route('/store', methods=['POST'])
def creat_store():
    request_data = request.get_json()
    new_store = {
        'id': uuid.uuid1(),
        'name': request_data['name'],
        'items': []
    }
    stores.append(new_store)
    return jsonify(new_store)


@app.route('/store/<string:id>', methods=['GET'])
def get_store(id):
    for store in stores:
        if(store['id'] == id):
            return jsonify(store)
    return jsonify({'message': 'No store found'})


@app.route('/store', methods=['GET'])
def get_stores():
    return jsonify({'stores': stores})


@app.route('/store/<string:store_id>/item', methods=['POST'])
def creat_item_in_store(store_id):
    request_data = request.get_json()
    for store in stores:
        if(store['id'] == store_id):
            new_item = {
                'name' : request_data['name'],
                'price' : request_data['price']
            }
            store['items'].append(new_item)
            return jsonify(new_item)
    return jsonify({'message': 'No store found'})


@app.route('/store/<string:store_id>/item', methods=['GET'])
def get_item_in_store(store_id):
    for store in stores:
        if(store['id'] == store_id):
            return jsonify(store['items'])
    return jsonify({'message': 'No store found'})


app.run(port=8080)
