import shutil
from zipfile import ZipFile

import requests
from github3 import GitHub, repository

from .formatter.base import Formatter
from .writer import StdoutWriter
from .printer import Printer


class _Formatter(Formatter):
    def format(self, data):
        return data


class GitHubClient:
    def __init__(self, config):
        self.config = config
        self._client = GitHub(login=self.login, password=self.secret, token=self.token)
        self.found_project = None

        printer_config = self.config.copy()
        printer_config['formatter'] = _Formatter
        printer_config['writer'] = StdoutWriter

        self.printer = Printer(printer_config)

    def find_project(self):
        if self.project_owner:
            project = repository(repository=self.project_name, owner=self.project_owner)
            if project:
                self.found_project = project
                return
            self._error_nothing_found(True)

        search_result = list(self._client.search_repositories(
            'language:python {}'.format(self.project_name), number=10))

        repositories_count = len(search_result)

        if repositories_count == 1:
            self.found_project = search_result[0].repository
            self.printer.print('Found {}'.format(self.found_project))
            return

        if repositories_count == 0:
            self._error_nothing_found()

        repos = '\n'.join(['[{}]{}/{}'.format(i, r.repository.owner.login, r.repository.name)
                           for i, r in enumerate(search_result, start=1)])
        message = 'Found {count} projects:\n{repos}\n'.format(count=repositories_count, repos=repos)

        self.printer.print(message)
        self.found_project = search_result[self._ask(repos)].repository

    def _error_nothing_found(self, with_owner=False):
        msg = 'Nothing was found! Check project name '
        if with_owner:
            msg += 'and repository owner '
        msg += 'you are looking for!'

        self.printer.print(msg)
        exit(5)

    def _ask(self, repos):
        repositories_count = len(repos)

        answer = None
        while not answer:
            tmp = input('Choose one of them or write "NO" to stop: ')
            if tmp == 'NO':
                exit(3)

            try:
                answer = int(tmp)
            except ValueError:
                self.printer.print('Write only "NO" or repo number!')
                continue

            if not (0 < answer <= repositories_count):
                self.printer.print('Incorrect number!')
                continue

            return answer - 1

    def download_project(self, archive_fd):
        url = self.found_project.archive_urlt.expand(archive_format='zipball')
        response = requests.get(url, stream=True)
        shutil.copyfileobj(response.raw, archive_fd)

    def unzip_project(self, archive_fd, project_folder):
        with ZipFile(archive_fd) as zip:
            zip.extractall(path=project_folder)

    @property
    def project_name(self):
        return self.config['project-name']

    @property
    def project_owner(self):
        return self.config.get('user')

    @property
    def login(self):
        return self.config.get('login')

    @property
    def secret(self):
        return self.config.get('secret')

    @property
    def token(self):
        return self.config.get('token')
