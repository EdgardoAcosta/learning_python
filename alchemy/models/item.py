import sqlite3
from db import db


class ItemModel(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))

    def __init__(self, name, price):
        self.name = name
        self.price = price

    def json(self):
        return {"id": self.id, "name": self.name, "price": self.price}

    @classmethod
    def find_by_id(cls, _id):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "SELECT name, price FROM items WHERE id =?"
        result = cursor.execute(query, (_id,))
        row = result.fetchone()
        connection.close()
        return cls(*row)

    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "SELECT name, price FROM items WHERE name =?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()
        return cls(*row)

    def insert(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "INSERT INTO items VALUES (NULL, ?,?)"
        result = cursor.execute(query, (self.name, self.price))

        connection.commit()
        connection.close()
        return result

    def update(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "UPDATE items SET price = ? WHERE name =?"
        result = cursor.execute(query, (self.price, self.name))
        connection.commit()
        connection.close()
