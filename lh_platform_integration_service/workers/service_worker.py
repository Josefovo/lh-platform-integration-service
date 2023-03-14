from logging import getLogger
from lhrpc import Blueprint, BrokerWorker

from ..context import Context
from ..handlers import HelloHandlers


logger = getLogger(__name__)


def run_service_worker(conf, should_stop):
    context = Context(conf=conf)
    bp = get_blueprint(conf, context)
    bw = BrokerWorker(conf.broker_address, blueprint=bp, should_stop=should_stop)
    logger.info(
        'Running service worker - service name: %r broker address: %r',
        conf.service_name, conf.broker_address)
    bw.run()


def get_blueprint(conf, context):
    bp = Blueprint(conf.service_name)
    bp.load_from(HelloHandlers(context))
    return bp
