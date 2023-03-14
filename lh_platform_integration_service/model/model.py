
from pathlib import Path
from pymongo import MongoClient
from pymongo.uri_parser import parse_uri as parse_mongo_uri
import re

from lh_mongo_queue import MongoQueue


def get_model_from_conf(conf, system):
    db = connect_to_mongodb(conf.db.uri, conf.db.ssl_ca_cert)
    return Model(db, system)


def connect_to_mongodb(mongo_uri, ssl_ca_cert):
    assert isinstance(mongo_uri, str)
    assert mongo_uri.startswith('mongodb://')
    mongo_uri_safe = _strip_password(mongo_uri)
    db_name = parse_mongo_uri(mongo_uri)['database']
    mc_kwargs = {}
    if ssl_ca_cert:
        assert Path(ssl_ca_cert).is_file(), ssl_ca_cert
        mc_kwargs['tlsCAFile'] = str(ssl_ca_cert)
    try:
        client = MongoClient(
            mongo_uri,
            connect=True,
            connectTimeoutMS=3 * 1000,
            serverSelectionTimeoutMS=5 * 1000,
            uuidRepresentation='pythonLegacy', # or 'standard'
            #w='majority',
            **mc_kwargs)
        db = client[db_name]
        # fire some operation to ensure we are really connected
        list(db['something_that_does_not_exist'].find())
    except Exception as e:
        raise Exception(f'Failed to connect to {mongo_uri_safe!r}: {e!r}') from None
    return db


def _strip_password(uri):
    m = re.match(r'^(.+):.*@(.+)$', uri)
    if m:
        return m.group(1) + ':xxx@' + m.group(2)
    else:
        return uri


class Model:

    def __init__(self, db):
        '''
        db: MongoDB Database
        '''
        self.db_name = db.name # accessed by monitoring worker
        self.greetings = Greetings(db)
        self.welcome_queue = MongoQueue(db['queues.welcome'])


class Greetings:

    def __init__(self, db):
        self._collection_greetings = db['greetings']

    def add_greeting(self, text):
        self._collection_greetings.insert_one({
            'text': text,
        })
