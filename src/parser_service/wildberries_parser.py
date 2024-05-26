import json
import os

from core.config import settings
from logs import parser_log
from src.parser_service import AbstractParser


class WildberriesParser(AbstractParser):
    """
    Class for parsing Wildberries category pages
    """
    categories = {}

    def __init__(self):
        self.root_url = settings.ROOT_URLS['wildberries'][0]

    def parse_category_urls(self, category_urls_list: list) -> dict:
        """
        Method for parsing list with links of wildberries category pages
        :return: list with dicts where key is category and value is category link
        """
        for category in category_urls_list:
            category_name = category.get('seo') or category.get('name')
            if not category_name:
                parser_log.error(f'Category name not found: {category}')
                continue
            self.categories[category_name] = (category.get('shard'), category.get('query'))
            parser_log.info(
                f'got category attributes ({category_name}) from catalog: {category}, {category.get("shard")}, '
                f'{category.get("query")}')
            if category.get('childs'):
                self.parse_category_urls(category.get('childs'))
        return self.categories

    def parse_category(self, category_json: dict, category_name: str, page_num: int) -> None:
        """
        Method for parsing one wildberries category page and save it to JSON file
        category_page: JSON object with data of one category
        :return: None
        """
        products_on_page = []
        for item in category_json['data']['products']:
            products_on_page.append({
                'title': item['name'],
                'price': int(item['priceU'] / 100),
                'link': f"{self.root_url}/"
                        f"{item['id']}/detail.aspx"
            })

        path_to_results = os.path.join("results", category_name)
        with open(f'{os.path.join(path_to_results, str(page_num))}.json', 'w', encoding='utf-8') as f:
            json.dump(products_on_page, f, ensure_ascii=False)

        parser_log.info(f'Category {category_name} (page: {page_num}) parsed')
