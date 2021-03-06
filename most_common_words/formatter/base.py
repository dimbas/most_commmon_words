import abc


class Formatter(abc.ABC):
    def __init__(self, config):
        self.config = config

    @property
    def is_pretty(self):
        return self.config['pretty']

    @property
    def speech_part(self):
        return self.config['speech_part']

    @abc.abstractmethod
    def format(self, data) -> str:
        pass
