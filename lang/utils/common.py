
def lookup_table(*coll):
    return {value: True  for i, value in enumerate(coll)}

def spit(file_path, data):
    with open(file_path, 'w', encoding='utf8') as file:
        file.write(data)

def cat(file_path):
    pass


def read_file_char(path):
    chars = []
    with open(path, 'r', encoding='utf-8') as file:
        i = 1
        while True:
            byte = file.read(1)
            if not byte:
                break
            chars.append(byte)
            i += 1
    return chars