import json

from .base import Formatter


class JsonFormatter(Formatter):
    def format(self, data) -> str:
        indent = 4 if self.is_pretty else None
        reformatted_data = [{'word': word, 'count': count} for word, count in data]
        return json.dumps(reformatted_data, indent=indent)
