from bson import ObjectId
from datetime import datetime
from instant_mongo import InstantMongoDB
import os
from pathlib import Path
from pymongo import MongoClient
from pytest import fixture

from lh_test_helpers.deterministic import DeterministicTime

from lh_platform_integration_service.model.model import Model


@fixture
def temp_dir(tmpdir):
    return Path(tmpdir)


@fixture
def db(mongo_client):
    db_name = f'test_{ObjectId()}'
    yield mongo_client[db_name]
    mongo_client.drop_database(db_name)


@fixture(scope='session')
def mongo_client(tmpdir_factory):
    if os.environ.get('TEST_MONGO_PORT'):
        yield MongoClient(
            port=int(os.environ['TEST_MONGO_PORT']),
            uuidRepresentation='pythonLegacy')
    else:
        temp_dir = tmpdir_factory.mktemp('instant-mongo')
        with InstantMongoDB(data_parent_dir=temp_dir) as im:
            yield im.get_client(uuidRepresentation='pythonLegacy')


@fixture
def deterministic_time():
    return DeterministicTime(datetime.strptime('2023-01-10 12:30:01.123456', '%Y-%m-%d %H:%M:%S.%f'))


@fixture
def advance_time(deterministic_time):
    return deterministic_time.advance


@fixture
def model(db):
    return Model(db)


@fixture
def overwatch_client():
    class MockOverwatchClient:

        def __init__(self):
            self.last_report = None

        def post_report(self, report_data):
            self.last_report = report_data

    return MockOverwatchClient()


@fixture
def system(deterministic_time):
    class MockSystem:

        def utcnow(self):
            return deterministic_time.datetime()

    return MockSystem()


@fixture
def context(model, overwatch_client, system):
    return {
        'model': model,
        'overwatch_client': overwatch_client,
        'system': system,
    }
