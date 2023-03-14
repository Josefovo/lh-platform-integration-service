from logging import getLogger
import requests


logger = getLogger(__name__)


class OverwatchClient:

    def __init__(self, conf):
        self.ow_conf = conf.overwatch
        self.session = requests.Session()

    def post_report(self, report_data):
        '''
        Post data to Overwatch report endpoint.

        Does nothing if Overwatch URL or token is not configured - which is preferred in dev and test environment.
        '''
        if not self.ow_conf.report_url or not self.ow_conf.report_token:
            logger.info('Overwatch monitoring report_url or report_token is not configured')
            return
        try:
            r = self.session.post(
                self.ow_conf.report_url,
                json=report_data,
                headers={'Authorization': 'token ' + self.ow_conf.report_token},
                timeout=30)
            logger.debug('Report response: %s', r.text[:100])
            r.raise_for_status()
        except Exception as e:
            logger.error('Failed to post report to %r: %r', self.ow_conf.report_url, e)
            #logger.info('Report token: %s...%s', self.ow_conf.report_token[:3], self.ow_conf.report_token[-3:])
            logger.info('Report data: %r', report_data)
