"""Maintains list of constants required across project"""

from enum import Enum


class Endpoints(Enum):
    """endpoints to be used throughout the script"""

    COMIC = "http://xkcd.com/{}/info.0.json"
