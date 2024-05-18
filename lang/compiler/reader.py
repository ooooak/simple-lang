import logging
from typing import List

from lang.utils import Seq

logger = logging.getLogger(__name__)

class Reader:
    def __init__(self, coll: List):
        self.coll = coll
        self.pos = 0

    def get_pos(self):
        return self.pos
    
    def get(self):
        b = Seq.get(self.coll, self.pos)
        if b:
            self.pos += 1
        return b

    def undo_read(self):
        self.pos -= 1

    def peek(self):
        return Seq.get(self.coll, self.pos)

    def peek_next(self):
        return Seq.get(self.coll, self.pos + 1)

    def has_next(self):
        self.peek() != None

    def take(self, start, end):
        return self.coll[start:end]