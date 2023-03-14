from logging import getLogger
from lhrpc import handler


logger = getLogger(__name__)


class HelloHandlers:

    def __init__(self, context):
        self.model = context['model']

    @handler
    def reverse(self, params):
        '''
        Return given text reversed

        Example: {'text': 'Foo bar'} -> reply: {'reversed': 'rab ooF'}
        '''
        reversed_text = ''.join(reversed(params['text']))
        self.model.greetings.add_greeting(reversed_text)
        self.model.welcome_queue.create_task({'text': params['text']})
        return {
            'reversed': reversed_text,
        }
