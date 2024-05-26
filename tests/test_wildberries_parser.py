import pytest

from core.config import settings
from src.request_service import RequestManager


@pytest.fixture
def raw_category_data():
    with RequestManager() as session:
        raw_category_data = session.get_request(settings.ROOT_URLS['wildberries'][1]).json()
    return raw_category_data


def test_wildberries_parser(raw_category_data):
    from src.parser_service.wildberries_parser import WildberriesParser
    parser = WildberriesParser()
    result = parser.parse_category_urls(raw_category_data)
    for cat_name, attributes in result.items():
        assert isinstance(cat_name, str)
        assert isinstance(attributes, tuple)
        assert len(attributes) == 2
