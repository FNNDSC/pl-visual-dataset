import functools
import re

from pydantic import BaseModel


class Matcher(BaseModel):
    key: str
    value: str
    regex: str

    @functools.cached_property
    def re(self):
        return re.compile(self.regex)

