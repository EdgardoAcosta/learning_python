from flask import Flask
from flask_resful import Resource, Api

app = Flask(__name__)

api =Api(app)

class Studen(Resource):
    def get(self, id):
        return {'student' : id}

api.add_resource(Student, '/student/<string:id>')


app.run(port=8080)