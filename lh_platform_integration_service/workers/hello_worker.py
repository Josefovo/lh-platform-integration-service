from logging import getLogger
from time import sleep


logger = getLogger(__name__)


def run_hello_worker(should_stop, conf):
    while True:
        if should_stop and should_stop():
            break
        logger.info('hello')
        sleep(1)
