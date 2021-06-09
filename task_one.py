"""
CLI tool to fetch data from `https://xkcd.com/`, store in local database and print re-formatted.

Example,
    python task_one.py --max 87 --any 15
"""

# package imports
import json
import requests
import argparse
from multiprocessing.pool import ThreadPool
from typing import List, Dict
from collections import OrderedDict
from random import randrange
from pydantic.error_wrappers import ValidationError

# module imports
from commons.constants import Endpoints
from models.datamodels.comics import Comic
from commons.dal import (
    upsert_comics
)


def rand_set(start: int = 1, stop: int = 87, limit: int = 15) -> List[int]:
    """ creates a list of unique random integers in numerical range(start:stop)

    Args:
        start (int): first numeric value in range.
        stop (int): last numeric value in range.
        limit (int): number of results to yield.

    Returns:
        List[int]: random values in range(start:stop) with count limited to `limit`.
    """

    result_ = []
    while len(result_) < limit:
        random_ = randrange(start, stop+1)
        if random_ not in result_:
            result_.append(random_)
        else:
            continue

    return result_


def fetch_comic(comic_id: int) -> Dict:
    """fetches a comic per `comic_id`

    Args:
        comic_id (int): fetches comic id

    Returns:
        fetched_comic (dict): comic object as received from xkcd API.
    """

    endpoint = Endpoints.COMIC.value.format(comic_id)
    response = requests.get(endpoint)

    response.raise_for_status()
    print(f"\n-- data has been downloaded from ```{endpoint}``` -- {response.status_code}")

    data = json.loads(response.text, object_pairs_hook=OrderedDict)
    try:
        comic = Comic(**data)
    except ValidationError as e:
        print(f"[ Error ] fetched comic record does not meet validations. Details  -\n{e}")

    return data


def print_formatted_output(fetched_comics: List[Dict]) -> None:
    """
    pretty printing for the final output

    Args:
        fetched_comics (list): set of pre-fetch comics
    """

    comics = [Comic(**comic) for comic in fetched_comics]

    comics = [
        {
            "comic": comic.title,
            "comic_meta": {
                "alt_text": comic.alt,
                "number": comic.num,
                "link": comic.link_,
                "image": comic.image,
                "image_link": comic.img
            }
        }
        for comic in comics
    ]

    print(comics)


if __name__ == "__main__":

    example = """example:

    python task_one.py --max 87 --any 15
    """

    parser = argparse.ArgumentParser(
        description="CLI tool to fetch resource(s) from any API",
        epilog=example,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "-m", "--max",
        metavar="max",
        type=int,
        default=87,
        help="max number of resources to be fetch",
        dest="max"
    )
    parser.add_argument(
        "-a", "--any",
        metavar="any",
        type=int,
        default=15,
        help="random sized chunk of resources to fetch",
        dest="any"
    )
    args = parser.parse_args()

    comic_set = rand_set(1, args.max, args.any)
    print(f"\n[ NOTE ] LIST OF RANDOM COMIC IDs :: \n\n{comic_set}\n")
    pool_size = 5
    print(f"\n[ NOTE ] requesting comic_set urls -\n ** ThreadPool of {pool_size} at work **")

    # Thread-pool to resolve IO-intensive operation real quick.
    pool = ThreadPool(pool_size)
    fetched_comic_list = pool.map(fetch_comic, comic_set)
    upsert_comics(fetched_comic_list)
    print_formatted_output(fetched_comic_list)
