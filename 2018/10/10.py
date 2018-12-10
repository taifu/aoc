raw = """position=< 9,  1> velocity=< 0,  2>
position=< 7,  0> velocity=<-1,  0>
position=< 3, -2> velocity=<-1,  1>
position=< 6, 10> velocity=<-2, -1>
position=< 2, -4> velocity=< 2,  2>
position=<-6, 10> velocity=< 2, -2>
position=< 1,  8> velocity=< 1, -1>
position=< 1,  7> velocity=< 1,  0>
position=<-3, 11> velocity=< 1, -2>
position=< 7,  6> velocity=<-1, -1>
position=<-2,  3> velocity=< 1,  0>
position=<-4,  3> velocity=< 2,  0>
position=<10, -3> velocity=<-1,  1>
position=< 5, 11> velocity=< 1, -2>
position=< 4,  7> velocity=< 0, -1>
position=< 8, -2> velocity=< 0,  1>
position=<15,  0> velocity=<-2,  0>
position=< 1,  6> velocity=< 1,  0>
position=< 8,  9> velocity=< 0, -1>
position=< 3,  3> velocity=<-1,  1>
position=< 0,  5> velocity=< 0, -1>
position=<-2,  2> velocity=< 2,  0>
position=< 5, -2> velocity=< 1,  2>
position=< 1,  4> velocity=< 2,  1>
position=<-2,  7> velocity=< 2, -2>
position=< 3,  6> velocity=<-1, -1>
position=< 5,  0> velocity=< 1,  0>
position=<-6,  0> velocity=< 2,  0>
position=< 5,  9> velocity=< 1, -2>
position=<14,  7> velocity=<-2,  0>
position=<-3,  6> velocity=< 2, -1>""".split("\n")


raw = open("input.txt").readlines()


points = []
for line in raw:
    parts = line.replace("<", " ").replace(">", " ").replace(",", " ").split()
    points.append([int(parts[1]), int(parts[2]), int(parts[4]), int(parts[5])])


def get_size(points):
    min_x = min_y = max_x = max_y = None
    for p in points:
        min_x = min(min_x, p[0]) if min_x is not None else p[0]
        min_y = min(min_y, p[1]) if min_y is not None else p[1]
        max_x = max(max_x, p[0]) if max_x is not None else p[0]
        max_y = max(max_y, p[1]) if max_y is not None else p[1]
    size_x = max_x - min_x + 1
    size_y = max_y - min_y + 1
    return min_x, min_y, max_x, max_y, size_x, size_y


def draw(points, size_x, size_y):
    min_x, min_y, max_x, max_y, size_x, size_y = get_size(points)
    if size_x < 250 and size_y < 250:
        matrix = [[" "] * size_x for y in range(size_y)]
        for point in points:
            matrix[point[1] - min_y][point[0] - min_x] = "#"
        print("")
        for line in matrix:
            print("".join(line))
        print("")
    for point in points:
        point[0] += point[2]
        point[1] += point[3]
    min_x, min_y, max_x, max_y, size_x, size_y = get_size(points)
    return size_x, size_y


size_x = size_y = None
seconds = 0
while True:
    new_size_x, new_size_y = draw(points, size_x, size_y)
    if size_x and new_size_x > size_x and new_size_y > size_y:
        print(seconds)
        break
    seconds += 1
    size_x, size_y = new_size_x, new_size_y
