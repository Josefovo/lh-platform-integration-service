# flake8: noqa


def test_import():
    import lh_platform_integration_service


def test_db(db):
    db['foo'].insert_one({'test': 'test'})
    assert db['foo'].find_one()['test'] == 'test'
    assert db['foo'].count_documents({}) == 1


def test_db_is_isolated_between_tests(db):
    # no data is left in the test database between test_db and this test
    db['foo'].insert_one({'test': 'test'})
    assert db['foo'].count_documents({}) == 1


def test_uuid(db):
    from uuid import UUID, uuid4
    some_uuid = uuid4()
    db['foo'].insert_one({'some_uuid': some_uuid})
    assert type(db['foo'].find_one()['some_uuid']) is UUID
    assert db['foo'].find_one()['some_uuid'] == some_uuid
