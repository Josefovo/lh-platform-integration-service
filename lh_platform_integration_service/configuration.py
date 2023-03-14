from logging import getLogger
import os
from pathlib import Path
import yaml


logger = getLogger(__name__)


class Configuration:

    def __init__(self, conf_file_path):
        cfg_data = yaml.safe_load(Path(conf_file_path).read_text())
        cfg_dir = Path(conf_file_path).resolve().parent
        local_path = Path(conf_file_path).with_suffix('.local.yaml')
        if local_path.exists():
            local_data = yaml.safe_load(local_path.read_text())
            cfg_data = merge_configuration(cfg_data, local_data)
        cfg = cfg_data['lh_platform_integration_service']
        self.log = Log(cfg.get('log', {}), cfg_dir)
        self.db = MongoDB(cfg['db'], cfg_dir)
        self.service_name = 'lh_platform_integration_service'
        self.broker_address = cfg['broker_address']
        self.overwatch = Overwatch(cfg.get('overwatch') or {})


def merge_configuration(conf, update, root=None):
    '''
    Recursively merge two configuration dictionaries

    i.e.:
        lh_account_service.yaml - default configuration file:

            lh_account_service:
                gopay_cz:
                    endpoint: https://gw.sandbox.gopay.com
                    notification_url: http://dev-gopay.leadhub.cz/api/public/payments/gopay/callback

        lh_account_service.local.yaml - local configuration file:

            lh_account_service:
                gopay_cz:
                    notification_url: http://dev-josef.leadhub.cz/api/public/payments/gopay/callback

        The value of gopay_cz.notification_url will be updated with the value from local file.
        The rest remains same (gopay_cz.endpoint will be 'https://gw.sandbox.gopay.com').

    :param dict conf:   default conf to be updated with local values
    :param dict update: conf with local values
    :param str root:    root of conf (path in default dict conf, recursively goes deep)

    :return: dict with merged configuration
    '''
    # TODO: move this function to shared library - maybe lh-process-dispatcher
    conf = dict(conf) # copy before modification so we do not change the original data
    for k, v in update.items():
        if isinstance(v, dict):
            # going deep
            if k not in conf or conf[k] is None:
                logger.debug('merge_configuration: creating non existing key %s.%s', root, k)
                conf[k] = {}
            conf[k] = merge_configuration(conf[k], update[k], f'{root}.{k}' if root else k)
        else:
            logger.debug('merge_configuration: updating key %s.%s: %r => %r', root, k, conf.get(k), v)
            conf[k] = update[k]
    return conf


class Log:

    def __init__(self, data, cfg_dir):
        if os.environ.get('LOG_FILE'):
            self.file_path = Path(os.environ['LOG_FILE'])
        elif data.get('file'):
            self.file_path = cfg_dir / data['file']
        else:
            self.file_path = None


class MongoDB:

    def __init__(self, data, cfg_dir):
        self.uri = data['uri']
        self.ssl_ca_cert = None
        if data.get('ssl') and data['ssl'].get('ca_cert_file'):
            self.ssl_ca_cert = cfg_dir / data['ssl']['ca_cert_file']


class LHRPCConnection:
    '''
    Configuration for LHRPC clients
    '''

    def __init__(self, cfg, default_service_name):
        self.address = cfg.get('address')
        self.service_name = cfg.get('service_name', default_service_name)


class Overwatch:

    def __init__(self, data):
        self.report_url = data.get('report_url')
        self.report_token = data.get('report_token')
