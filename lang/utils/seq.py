
class Seq:
    @staticmethod
    def get(data, index, default=None):
        if not data:
            return default
        if index < len(data):
            return data[index]
        return default