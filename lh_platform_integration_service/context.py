from datetime import datetime

from .clients import OverwatchClient
from .model import get_model_from_conf


factories = {
    'model': lambda context: get_model_from_conf(context['conf']),
    'overwatch_client': lambda context: OverwatchClient(context['conf']),
    'system': lambda context: System(),
}


class Context:
    '''
    Context objekt má úmyslně stejné API jako dict, aby se místo něj dal
    v testech použít prostě dict.
    '''

    def __init__(self, conf):
        self._items = {
            'conf': conf,
        }

    def __getitem__(self, key):
        '''
        Tato metoda umožňuje vzít si objekt z kontextu tímto způsobem: context['model']
        '''
        if key not in self._items:
            self._items[key] = factories[key](self)
        return self._items[key]


class System:

    def utcnow(self):
        return datetime.utcnow()
