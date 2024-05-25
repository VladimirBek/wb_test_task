import fake_useragent
import requests
from requests import HTTPError, Response

from logs import request_log
from src.request_service import AbstractRequestManager


class RequestManager(AbstractRequestManager):

    """
    Class for making requests via requests python library
    """

    def __init__(self) -> None:

        self.session = requests.Session()
        self.session.headers.update({'User-Agent': fake_useragent.UserAgent().random})

    def __enter__(self):
        return self.session

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


    def get_request(self, url: str) -> requests.Response:
        """
        Method for making get request

        :param url: target url for get request
        :return: requests.Response object
        """
        try:
            resp: Response = self.session.get(url, timeout=10)
            resp.raise_for_status()
        except HTTPError as http_err:
            request_log.error(f'HTTP error occurred: {http_err}')
        except Exception as err:
            request_log.error(f'Other error occurred: {err}')
        else:
            request_log.info(f'Successfully fetched {url} with status code: {resp.status_code}')
            return resp

    def close(self):
        """ Close current session """
        self.session.close()
