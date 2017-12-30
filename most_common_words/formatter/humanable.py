from .base import Formatter


class HumanableFormatter(Formatter):
    @property
    def path(self):
        return self.config['path']

    @property
    def project_name(self):
        return self.config['project-name']

    def format(self, data) -> str:
        indent = '\t' if self.is_pretty else ''
        target = 'project {name}'.format(name=self.project_name) if self.config.get('github') \
            else 'path {path}'.format(path=self.path)

        return 'Most common {part} in {target}\n'.format(part=self.speech_part, target=target) +\
               '\n'.join(
                   ['{indent}{word}: {times}'.format(word=word, times=count, indent=indent) for word, count in data]
               ) + '\n'
