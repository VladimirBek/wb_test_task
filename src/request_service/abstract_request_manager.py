import abc

import requests


class AbstractRequestManager(abc.ABC):
    """ Abstract class for making requests """
    @abc.abstractmethod
    def get_request(self, url: str) -> requests.Response:
        """ Abstract method for making get request """
        raise NotImplementedError