from logging import getLogger
from time import sleep

from ..context import Context
from ..model.model import Model


logger = getLogger(__name__)


def run_welcome_worker(conf, should_stop):
    context = Context(conf=conf)
    model = context['model']
    assert isinstance(model, Model)
    while not should_stop():
        task = model.welcome_queue.take_task()
        if task:
            with task:
                process_task(task, context)
        else:
            sleep(1)


def process_task(task, context):
    #context['mailgun_client'].send_email(...)
    logger.info('Would send email; task.payload: %r', task.payload)
