import os

import pymongo
from bson import ObjectId
from flask import g

from team.model.player import Player
from team.model.captain import Captain


class MongoDatabase:
    @staticmethod
    def __get_db():
        if 'db' not in g:
            user = os.getenv('MONGODB_USER', default='usr')
            password = os.getenv('MONGODB_PASSWD', default='passwd')
            host = os.getenv('MONGODB_ADDR', default='127.0.0.1')
            port = os.getenv('MONGODB_PORT', default='27017')
            database = os.getenv('MONGODB_DBNAME', default='db')

            g.db_connect = pymongo.MongoClient(f"mongodb://{user}:{password}@{host}:{port}/")
            g.db = g.db_connect[database]
            g.dbc = g.db['teams']
        return g.dbc

    @staticmethod
    def close_db():
        if 'db_connect' in g and (db_connect := g.db_connect) is not None:
            db_connect.close()

    @staticmethod
    def reset():
        dbc = MongoDatabase.__get_db()
        dbc.drop()

    @staticmethod
    def get_record(id):
        dbc = MongoDatabase.__get_db()

        data = dbc.find_one({'_id': ObjectId(str(id))})

        record = Captain() if 'grade' in data else Player()
        data['id'] = data.pop('_id')
        record.input(data)

        return record

    @staticmethod
    def get_records():
        dbc = MongoDatabase.__get_db()
        for data in dbc.find():
            record = Captain() if 'grade' in data else Player()
            data['id'] = data.pop('_id')
            record.input(data)
            yield record

    @staticmethod
    def add_record(item):
        dbc = MongoDatabase.__get_db()
        data = item.__dict__
        del data['id']
        dbc.insert_one(data)

    @staticmethod
    def edit_record(item):
        dbc = MongoDatabase.__get_db()
        data = item.__dict__
        id = data.pop('id')
        dbc.update_one({'_id': ObjectId(id)}, {'$set': data})

    @staticmethod
    def delete_record(id):
        dbc = MongoDatabase.__get_db()
        dbc.delete_one({'_id': ObjectId(str(id))})

    @classmethod
    def init_db(cls):
        pass
