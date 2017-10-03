from . import formatter, writer


class Printer:
    def __init__(self, config):
        self.config = config

    @property
    def formatter(self):
        name = self.config['format'].capitalize() + 'Formatter'
        return getattr(formatter, name)(self.config)

    @property
    def writer(self):
        if self.config['writer']:
            return self.config['writer']

        if self.config['output']:
            return writer.FileWriter(self.config['output'])

        name = self.config['console'].capitalize() + 'Writer'
        return getattr(writer, name)()

    def print(self, data):
        message = self.formatter.format(data)
        self.writer.write(message)
