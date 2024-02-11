def seq_get(data, index, default=None):
    if not data:
        return default
    if index < len(data):
        return data[index]
    return default

def map_get(data, index, default=None):
    if index in data:
        return data[index]
    return default

def map_has(data, index):
    return index in data

def into_lookup_tbl(*coll):
    return {value: True  for i, value in enumerate(coll)}
