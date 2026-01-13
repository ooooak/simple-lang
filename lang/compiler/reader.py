import logging
from typing import List

from lang.utils import Seq

logger = logging.getLogger(__name__)


class Reader:
    """
    Simple iterating for collections
    """
    def __init__(self, coll: List):
        self.coll = coll
        self._pos = 0

    @property
    def position(self):
        return self._pos
    
    def get(self):
        b = Seq.get(self.coll, self._pos)
        if b:
            self._pos += 1
        return b

    def undo_read(self):
        self._pos -= 1

    def peek(self):
        return Seq.get(self.coll, self._pos)

    def peek_next(self):
        return Seq.get(self.coll, self._pos + 1)

    def has_next(self):
        self.peek() is not None

    def take(self, start, end):
        return self.coll[start:end]
