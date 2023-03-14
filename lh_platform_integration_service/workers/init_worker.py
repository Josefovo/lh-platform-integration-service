from logging import getLogger
from time import sleep


logger = getLogger(__name__)


def run_init_worker(should_stop, conf):
    logger.info('inside init worker')
    sleep(2)
    logger.info('init worker done')
