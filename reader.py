def to_int(raw_data, signed=True):
    return int.from_bytes(raw_data, byteorder='big', signed=signed)


class BufferReader:
    def __init__(self, raw_data):
        self.raw_data = raw_data
        self.index = 0

    def bytes(self, count) -> bytes:
        if count == 0:
            return b''

        self.index += count
        return self.raw_data[self.index-count:self.index]

    def byte(self) -> int:
        return self.bytes(1)[0]

    def short(self) -> int:
        return to_int(self.bytes(2))

    def integer(self) -> int:
        return to_int(self.bytes(4))

    def long(self) -> int:
        return to_int(self.bytes(8))

    def string(self) -> str:
        return self.bytes(self.short()).decode('utf-8')

    def remaining(self) -> bytes:
        if self.index >= len(self.raw_data):
            return b''

        return self.raw_data[self.index:]
