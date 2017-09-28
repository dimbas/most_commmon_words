from urllib.error import URLError

from nltk.downloader import Downloader


class NLTKDownloaderError(Exception):
    code = -1


class InternetError(NLTKDownloaderError):
    code = 1


class DownloadError(NLTKDownloaderError):
    code = 2


class NLTKDownloader(Downloader):
    default_data_id = 'all'

    def __init__(self, data_id=default_data_id):
        Downloader.__init__(self)
        self.data_id = data_id

    def _ask(self, yes):
        if yes:
            return 'yes'

        answer = input('For work you need installed nltk data, do you want to install it? [yes?no]: ').lower()
        while answer not in ('yes', 'no'):
            answer = input('Type yes or no: ').lower()
        return answer

    def check_installation(self, yes=False, force_download=False):
        if force_download:
            self.download(self.data_id)
            return

        try:
            is_installed = self.is_installed(self.data_id)
        except URLError as err:
            print('You need internet connection to check and download nltk data installation. Aborting!')
            raise InternetError from err

        if is_installed:
            return

        action = self._ask(yes)
        if action == 'yes':
            print('Warning, installing may take some time')
            self.download(self.data_id)
        else:
            print('Script cant work without nltk data installed. Aborting!')
            raise DownloadError
