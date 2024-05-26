import abc
import json


class AbstractParser(abc.ABC):
    """
    Abstract class for parsing
    """

    @abc.abstractmethod
    def parse_category_urls(self, category_urls_list: list) -> list:
        """
        Abstract method for parsing list with links
        :return: list with dicts where key is category and value is category link
        """
        raise NotImplementedError


    @abc.abstractmethod
    def parse_category(self, category_page: dict, category_name: str, page_num: int) -> None:
        """
        Abstract method for parsing one category page and save it to JSON file
        """
        raise NotImplementedError

