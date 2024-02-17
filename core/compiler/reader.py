import logging

from core.fs import read_file_char
from core.util import (
    seq_get,
)

logger = logging.getLogger(__name__)

class Reader:
    def __init__(self, file):
        self.file = read_file_char(file)
        self.pointer = 0
        
        logger.debug("file: %s", file)
        logger.debug("self.file: %s", self.file)

    def get(self):
        b = seq_get(self.file, self.pointer)
        if b:    
            self.pointer += 1
        return b
    
    def undo(self):
        self.pointer -= 1
    
    def peek(self):
        return seq_get(self.file, self.pointer)
    
    def peek_next(self):
        return seq_get(self.file, self.pointer + 1)

    def has_next(self):
        self.peek() != None