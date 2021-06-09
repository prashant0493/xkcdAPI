"""
This module defines pydantic (provides Py3 data-classes validation out of the box) models used
for validation and (de)serialization in API requests/responses.
"""

from typing import Optional
from models.basemodel import Base


class Comic(Base):
    """Pydantic model class to validate data for `Comic` object from xkcd API"""

    # attribute fields
    month: Optional[str] = ""
    link: Optional[str] = ""
    year: Optional[str] = ""
    news: Optional[str] = ""
    safe_title: Optional[str] = ""
    transcript: Optional[str] = ""
    alt: Optional[str] = ""
    img: str
    title: Optional[str] = ""
    day: Optional[str] = ""

    @property
    def image(self) -> str:
        if self.img:
            image_ = self.img.split("/")
            return image_[-1]
        return ""

    @property
    def link_(self) -> str:
        if self.num:
            return "https://www.xkcd.com/" + str(self.num)
        return ""

    # relationship attribute fields
    # [todo] add relationships if any
