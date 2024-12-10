from typing import TypeAlias, List


CompressedDisk: TypeAlias = List[int]
RawDisk: TypeAlias = List[int | None]


class Disk:
    def __init__(self, data: str) -> None:
        parts = [int(x) for x in data.strip()]
        self.files = []
        self.space = []
        for n, f in enumerate(parts):
            if n % 2 == 0:
                self.files.append((n // 2, f))
            else:
                self.space.append(f)

    def compress(self) -> CompressedDisk:
        compressed = [0 for n in range(self.files[0][1])]
        left_files = self.files[-1:0:-1]
        spaces = self.space[:]
        space = spaces.pop(0)
        while left_files:
            file_id, size = left_files.pop(0)
            while size:
                while size and space:
                    compressed.append(file_id)
                    space -= 1
                    size -= 1
                if not space:
                    space = spaces.pop(0)
                    if left_files:
                        left_file_id, left_size = left_files.pop(-1)
                        for n in range(left_size):
                            compressed.append(left_file_id)
        return compressed

    def compress2(self) -> RawDisk:
        disk: RawDisk = []
        files_pos, spaces_pos = {}, []
        # Build raw disk as a list: [0, 0, None, None, None, 1, 1, 1 ... etc. ]
        for n in range(len(self.files)):
            # Save file starting position
            files_pos[self.files[n][0]] = len(disk)
            for s in range(self.files[n][1]):
                # Write file
                disk.append(self.files[n][0])
            pos = len(disk)
            if n != len(self.files) - 1:
                for s in range(self.space[n]):
                    # Write empty space
                    disk.append(None)
                # Save empty space in a list
                spaces_pos.append((self.space[n], pos))
        # Try to move files starting from the last one (and skipping the first)
        for file_id, size in self.files[-1:0:-1]:
            # Search for first good empty space (starting from left)
            for n, (space, pos) in enumerate(spaces_pos):
                if space >= size:
                    break
            else:
                # If not found skip the file
                continue
            file_pos = files_pos[file_id]
            if pos > file_pos:
                # Skip the file if the first empty space is at rightmost position of the file
                continue
            # Move the file
            for p in range(size):
                disk[p + pos], disk[p + file_pos] = file_id, None
            # Adjust empty spaces
            if space == size:
                # Detele if filled
                spaces_pos.pop(n)
            else:
                # Adjust if partially filled
                spaces_pos[n] = (space - size, pos + size)
        return disk

    def count(self) -> int:
        checksum = 0
        for n, file_id in enumerate(self.compress()):
            checksum += n * file_id
        return checksum

    def count2(self) -> int:
        checksum = 0
        for n, file_id in enumerate(self.compress2()):
            checksum += n * (file_id or 0)
        return checksum


def solve1(data: str) -> int:
    return Disk(data).count()


def solve2(data: str) -> int:
    return Disk(data).count2()


if __name__ == "__main__":
    import sys, os  # noqa: E401
    data = open((sys.argv + [os.path.dirname(__file__) + "/input.txt"])[1]).read()
    print(solve1(data))
    print(solve2(data))
