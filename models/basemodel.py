"""
This module defines pydantic basemodel (provides Py3 data-classes validation out of the box)
used for common fields and methods used across all the datamodels.
"""

from pydantic import BaseModel
from datetime import datetime


class Base(BaseModel):
    """Base model for common dataclass attributes"""
    num: int
