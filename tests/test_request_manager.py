import pytest


def test_request_manager():
    from src.request_service.request_manager import RequestManager
    with RequestManager() as session:
        assert session.get_request('https://www.google.com').status_code == 200

