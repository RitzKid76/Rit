from collections import deque


class ByteStream:

    def __init__(self, data: bytes = b""):
        self.buffer = deque(data)

    def read(self, n: int) -> bytes:
        count = min(n, self.size())
        return bytes(self.buffer.popleft() for _ in range(count))

    def write(self, data: bytes):
        self.buffer.extend(data)

    def read_to_delimiter(self, delimiter: bytes) -> bytes:
        if len(delimiter) > 1:
            raise ValueError(f"delimiter {delimiter.hex()} must be single byte. found length {len(delimiter)}")

        delimiter_byte = delimiter[0]

        collected = []

        while True:
            byte = self.buffer.popleft()

            if byte == delimiter_byte:
                break

            collected.append(byte)

        return bytes(collected)

    def has_data(self) -> bool:
        return self.size() > 0

    def size(self) -> int:
        return len(self.buffer)

    def bytes(self) -> bytes:
        return bytes(self.buffer)

    def __len__(self) -> int:
        return self.size()

    def __bool__(self) -> bool:
        return self.has_data()
