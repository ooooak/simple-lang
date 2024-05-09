class Map:
    @staticmethod
    def has(data, index):
        return index in data

    @staticmethod
    def get(data, index, default=None):
        if index in data:
            return data[index]
        return default