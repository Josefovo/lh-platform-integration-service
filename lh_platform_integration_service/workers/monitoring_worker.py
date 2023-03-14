from datetime import timedelta
from logging import getLogger
from os import getpid
from socket import getfqdn
from time import sleep, time, monotonic

from ..context import Context
from ..model.model import Model


logger = getLogger(__name__)

sleep_interval = timedelta(seconds=60)


def run_monitoring_worker(conf=None, context=None, should_stop=None, once=False):
    context = context or Context(conf=conf)
    model = context['model']
    system = context['system']
    assert isinstance(model, Model)
    while True:
        if should_stop and should_stop():
            break
        start_time = monotonic()
        report_data = {
            'date': system.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
            'label': {
                'agent': __name__.split('.')[0],
                'db': model.db_name,
            },
            'state': get_report_state(),
        }
        duration = monotonic() - start_time
        report_data['state']['duration'] = {
            '__value': duration,
            '__unit': 'seconds',
            '__check': {
                'state': 'green' if duration < 1 else 'red',
            }
        }
        context['overwatch_client'].post_report(report_data)
        if once:
            break

        for _ in range(int(sleep_interval.total_seconds())):
            if should_stop and should_stop():
                break
            sleep(1)


def get_report_state():
    return {
        'fqdn': getfqdn(),
        'pid': getpid(),
        'watchdog': {
            '__watchdog': {
                'deadline': int((time() + sleep_interval.total_seconds() * 2) * 1000),
            }
        },
    }
