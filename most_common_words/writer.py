import sys
from pathlib import Path


class FileWriter:
    def __init__(self, file: Path):
        self.file_descriptor = file.open('w')

    def write(self, data):
        self.file_descriptor.write(data)
        self.file_descriptor.close()


class StdoutWriter(FileWriter):
    def __init__(self):
        self.file_descriptor = sys.stdout

    def write(self, data):
        self.file_descriptor.write(data)


class StderrWriter(StdoutWriter):
    def __init__(self):
        self.file_descriptor = sys.stderr
