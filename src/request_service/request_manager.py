import time

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

        self.session = requests.Session()  # create session
        self.session.headers.update({'User-Agent': fake_useragent.UserAgent().random})  # set user agent

    def __enter__(self):
        return self

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
            if http_err.response.status_code == 429:
                time.sleep(10)
                return self.get_request(url)
            elif http_err.response.status_code == 500:
                return self.get_request(url)

        except Exception as err:
            request_log.error(f'Unexpected error occurred: {err}')
            raise err
        else:
            request_log.info(f'Successfully fetched response from {url} with status code: {resp.status_code}')
            return resp

    def get_products_data(self, shard, query, page_num: int) -> requests.Response:
        """ Method for making get request and parsing data """

        resp = self.get_request((f"https://catalog.wb.ru/catalog/{shard}/"
                                 f"catalog?appType=1&{query}&curr=rub"
                                 f"&dest=-1257786&page={page_num}&sort=popular&spp=24"))
        request_log.info(f'Successfully fetched response from {resp.url} with status code: {resp.status_code}')
        return resp

    def close(self):
        """ Close current session """
        self.session.close()
