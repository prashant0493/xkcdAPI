import json
import pytest
import requests

from commons.db_con_helper import get_sql_db_connection
from commons.dal import build_upsert_sql_query


class MockResponse:

    status_code = 200
    text = """{
        "month": "1",
        "num": 1,
        "link": "",
        "year": "2021",
        "news": "",
        "safe_title": "MOCK Fuzzy Blob",
        "transcript": "",
        "alt": "MOCK simple alt_text",
        "img": "https://imgs.xkcd.com/comics/fuzzy_blob.png",
        "title": "MOCK Fuzzy Blob",
        "day": "4"
    }"""

    @staticmethod
    def json():
        return json.loads(MockResponse.raw)

    @staticmethod
    def raise_for_status():
        return b""


# monkey-patched requests.get moved to a fixture
@pytest.fixture
def mock_response(monkeypatch):
    """Requests.get() mocked to return {'mock_key':'mock_response'}."""

    def mock_get(*args, **kwargs):
        return MockResponse()

    monkeypatch.setattr(requests, "get", mock_get)


@pytest.fixture
def setup_database():
    """Fixture to set up the in-memory database with test data"""
    conn = get_sql_db_connection()
    cursor = conn.cursor()
    cursor.execute("truncate xkcdDB.comics;")
    yield conn


@pytest.fixture
def setup_test_data1(setup_database):
    conn = setup_database
    cursor = conn.cursor()

    sample_keys = [
        "num",
        "month",
        "link",
        "year",
        "news",
        "safe_title",
        "transcript",
        "alt",
        "img",
        "title",
        "day",
    ]

    sample_data = [
        (11, "11", "11", "11", "11", "11", "11", "11", "11", "11", "11"),
        (33, "11", "99", "99", "99", "99", "99", "99", "99", "99", "99"),
    ]
    cursor.execute(
        build_upsert_sql_query(
            "xkcdDB.comics", keys_=sample_keys, value_set_=sample_data
        )
    )
    yield cursor


@pytest.fixture
def setup_for_upsert(setup_database, setup_test_data1):
    conn = setup_database
    conn.commit()
    cursor = setup_test_data1
    conn.commit()
    yield cursor
    conn.close()
