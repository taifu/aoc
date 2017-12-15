from collections import deque
import hashlib


def get_doors(pos, size, salt):
    hash_doors = hashlib.md5(salt.encode('utf8')).hexdigest()[:4]
    doors = []
    for n, (d, d_x, d_y) in enumerate((("U", 0, -1), ("D", 0, 1), ("L", -1, 0), ("R", 1, 0))):
        if hash_doors[n] > 'a':
            if 0 <= pos[0] + d_x < size[0] and 0 <= pos[1] + d_y < size[1]:
                doors.append((d, d_x, d_y))
    return doors


def minimum_path_bfs(pos, size, passcode, longest=False):
    target = (size[0] - 1, size[1] - 1)
    queue = deque([("", pos)])
    longest_path = ""
    while queue:
        path, current = queue.popleft()
        if current == target:
            if not longest:
                return path
            if len(path) > len(longest_path):
                longest_path = path
            continue
        for new_path, d_x, d_y in get_doors(current, size, passcode + path):
            queue.append((path + new_path, (current[0] + d_x, current[1] + d_y)))
    return longest_path

path = minimum_path_bfs((0, 0), (4, 4), "gdjjyniy")
print(path)

path = minimum_path_bfs((0, 0), (4, 4), "gdjjyniy", longest=True)
print(len(path))


