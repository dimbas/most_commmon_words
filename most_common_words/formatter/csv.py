from .base import Formatter


class CsvFormatter(Formatter):
    def format(self, data) -> str:
        header = 'word,count'
        formatted_data = '\n'.join(['{word},{times}'.format(word=word, times=count) for word, count in data])
        return '\n'.join([header, formatted_data])
