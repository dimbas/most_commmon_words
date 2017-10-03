from .base import Formatter


class HumanableFormatter(Formatter):
    @property
    def path(self):
        return self.config['path']

    def format(self, data) -> str:
        indent = '\t' if self.is_pretty else ''
        return 'Most common {part} in path {path}\n'.format(part=self.speech_part, path=self.path) +\
               '\n'.join(
                   ['{indent}{word}: {times}'.format(word=word, times=count, indent=indent) for word, count in data]
               )
