

def hello() {
    let x = hello
}


import Seq

logger = logging.getLogger(__name__)

struct Peekable {
    coll: coll
    pos: int = 0
}

def get_pos() {
    return self.pos
}
    
def get() {
    b = Seq.get(self.coll, self.pos)
    if b:
        self.pos += 1
    b
}
    

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
}



x = "Hello world"
print(x)
