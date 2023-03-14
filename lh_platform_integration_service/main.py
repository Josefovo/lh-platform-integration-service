from argparse import ArgumentParser
from logging import Formatter, getLogger

from lh_process_dispatcher import run_and_manage_workers

from .configuration import Configuration
from .workers import run_init_worker, run_hello_worker, run_monitoring_worker, run_service_worker, run_welcome_worker


logger = getLogger(__name__)


def platform_integration_service_main():
    p = ArgumentParser()
    p.add_argument('--verbose', '-v', action='count')
    p.add_argument('--conf')
    args = p.parse_args()
    setup_logging(args.verbose)

    conf = Configuration(args.conf)

    # TODO: pridat moznost spusteni jen services nebo workers
    workers = [
        run_hello_worker,
        run_welcome_worker,
        run_monitoring_worker,
    ]
    for _ in range(8):
        workers.append(run_service_worker)

    run_and_manage_workers(
        init_worker=run_init_worker,
        workers=workers,
        kwargs={'conf': conf},
        log_file_path=conf.log.file_path,
        log_formatter=Formatter(log_format))


log_format = '%(asctime)s [%(processName)-27s %(process)5d] %(name)-40s %(levelname)5s: %(message)s'


def setup_logging(verbosity):
    from logging import DEBUG, INFO, ERROR, Formatter, StreamHandler, getLogger
    # set root logger level
    getLogger('').setLevel(DEBUG)
    for name in 'boto3', 'botocore', 's3transfer':
        getLogger(name).setLevel(INFO)
    # log to stderr
    h = StreamHandler()
    h.setFormatter(Formatter(log_format))
    if not verbosity:
        h.setLevel(ERROR)
    elif verbosity == 1:
        h.setLevel(INFO)
    else:
        h.setLevel(DEBUG)
    getLogger('').addHandler(h)
