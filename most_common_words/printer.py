from most_common_words import formatter


class Printer:
    def __init__(self, config):
        self.config = config
        self.formatter = self.formatter_cls(config)

    @property
    def formatter_cls(self):
        name = self.config['format'].capitalize() + 'Formatter'
        return getattr(formatter, name)

    def print(self, data):
        message = self.formatter.format(data)
        print(message)
