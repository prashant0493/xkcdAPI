"""Test suite to test all functionalities end-to-end under `task_one.py` module"""

from task_one import (
    rand_set,
    fetch_comic,
    upsert_comics
)


def test_fetch_comic(mock_response):
    """Test to ensure API call over network"""

    result = fetch_comic(1)
    assert result["num"] == 1


def test_rand_set():
    """Test to ensure random number generator results"""

    assert len(rand_set()) == 15
    assert len(rand_set(start=1, stop=10, limit=2)) == 2


def test_with_sample_data1(setup_test_data1):
    # Test to make sure that there are 2 items in the database

    cursor = setup_test_data1
    assert cursor.execute("SELECT * FROM xkcdDB.comics;") == 2


def test_upsert_comics(setup_for_upsert):
    """Test to ensure results end-to-end fetching & inserting into database"""

    first_record = fetch_comic(11)
    first_record.update({'num': 11})
    second_record = fetch_comic(1)
    second_record.update({'num': 1})

    result = [first_record, second_record]
    cursor = setup_for_upsert
    upsert_comics(result)
    assert cursor.execute("SELECT * FROM xkcdDB.comics;") == 3
