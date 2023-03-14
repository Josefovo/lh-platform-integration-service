from lh_platform_integration_service.handlers.hello_handlers import HelloHandlers


def test_reverse(context):
    h = HelloHandlers(context)
    assert h.reverse({'text': 'ahoj'}) == {'reversed': 'joha'}
