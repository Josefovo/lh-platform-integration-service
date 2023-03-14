from os import getpid
from socket import getfqdn

from lh_platform_integration_service.workers.monitoring_worker import run_monitoring_worker


def test_monitoring_worker(context, overwatch_client, db):
    run_monitoring_worker(context=context, once=True)
    assert overwatch_client.last_report == {
        'date': '2023-01-10T12:30:01.123456Z',
        'label': {
            'agent': 'lh_platform_integration_service',
            'db': db.name,
        },
        'state': {
            'duration': {
                '__check': {'state': 'green'},
                '__unit': 'seconds',
                '__value': overwatch_client.last_report['state']['duration']['__value'],
            },
            'fqdn': getfqdn(),
            'pid': getpid(),
            'watchdog': {
                '__watchdog': {
                    'deadline': overwatch_client.last_report['state']['watchdog']['__watchdog']['deadline'],
                },
            },
        },
    }
