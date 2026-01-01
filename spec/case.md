const array = import("std/array")


fn get() {
    b = Seq.get(self.coll, self.pos)
    if b:
        self.pos += 1
    b
}

fn undo_read(){
    pos -= 1
}
    

fn peek(self):
    return (Seq.get self.coll, self.pos)

fn peek_next(self) {
    seq.get(self.coll, self.pos + 1)
}
    

fn has_next(self) {
    if !self.peek() {

    }
}
    

fn take(self, start, end){
    return self.coll[start:end]
}
    



x = "Hello world"
print(x)
