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