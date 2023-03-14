from lh_platform_integration_service.configuration import Configuration, merge_configuration


def test_merge_configuration():
    assert merge_configuration({'foo': 'bar'}, {'foo': 'baz'}) == {'foo': 'baz'}
    assert merge_configuration({'foo': {'bar': 10}}, {'foo': {'bar': 20}}) == {'foo': {'bar': 20}}


def test_load_configuration(temp_dir):
    conf_file_path = temp_dir / 'test.yaml'
    conf_file_path.write_text('''
        lh_platform_integration_service:
          log:
            file: test.log
          db:
            uri: mongodb://test:27027
          broker_address: tcp://127.0.0.1:3334
    ''')
    conf = Configuration(conf_file_path)
    assert conf.log.file_path == temp_dir / 'test.log'
    assert conf.broker_address == 'tcp://127.0.0.1:3334'


def test_load_local_configuration(temp_dir):
    conf_file_path = temp_dir / 'test.yaml'
    conf_file_path.write_text('''
        lh_platform_integration_service:
          log:
            file: test.log
          db:
            uri: mongodb://test:27027
          broker_address: tcp://127.0.0.1:3334
    ''')
    local_file_path = temp_dir / 'test.local.yaml'
    local_file_path.write_text('''
        lh_platform_integration_service:
          broker_address: tcp://127.0.0.1:9999
    ''')
    conf = Configuration(conf_file_path)
    assert conf.log.file_path == temp_dir / 'test.log'
    assert conf.broker_address == 'tcp://127.0.0.1:9999'
