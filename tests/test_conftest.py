from datetime import datetime


def test_system(system):
    assert system.utcnow() == datetime(2023, 1, 10, 12, 30, 1, 123456)
