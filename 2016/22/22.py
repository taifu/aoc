from collections import deque

data = [[parts.split("-")[-2:] if i == 0 else parts for i, parts in enumerate(l.strip().split())] for l in open("input").readlines()[2:]]

disks = dict(((int(x[1:]), int(y[1:])), [int(used[:-1]), int(avail[:-1])]) for [x, y], _, used, avail, _ in data)

size_x = max(k[0] for k in disks.keys()) + 1
size_y = max(k[1] for k in disks.keys()) + 1

viable = 0

for x1 in range(size_x):
    for y1 in range(size_y):
        disks[x1, y1].append(False)
        for x2 in range(size_x):
            for y2 in range(size_y):
                if x1 != x2 or y1 != y2:
                    if 0 < disks[x1, y1][0] <= disks[x2, y2][1]:
                        viable += 1

disks[size_x - 1, 0][-1] = True
print(viable)

def minimum_path_bfs(disks, size_x, size_y):
    queue = deque()
    while True:
        for x in range(size_x):
            for y in range(size_y):
                for dx in (-1, 0, 1):
                    if x + dx < 0 or x + dx == size_x:
                        continue
                    for dy in (-1, 0, 1):
                        if dx == 0 and dy == 0:
                            continue
                        if y + dy < 0 or y + dy == size_y:
                            continue
                        if 0 < disks[x, y][0] <= disks[x + dx, y + dy][1]:
                            queue.append((x, y, x + dx, y + dy, disks[x, y][0], disks[x, y][2]))

        print(queue)
        break
        #path, current = queue.popleft()
        #if current == target:
        #    if not longest:
        #        return path
        #    if len(path) > len(longest_path):
        #        longest_path = path
        #    continue
        #for new_path, d_x, d_y in get_doors(current, size, passcode + path):
        #    queue.append((path + new_path, (current[0] + d_x, current[1] + d_y)))
    #return longest_path

print(minimum_path_bfs(disks, size_x, size_y))
