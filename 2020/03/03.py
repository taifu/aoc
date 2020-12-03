WOOD = """..##.......
#...#...#..
.#....#..#.
..#.#...#.#
.#...##..#.
..#.##.....
.#.#.#....#
.#........#
#.##...#...
#...##....#
.#..#...#.#"""


def slope(wood, right, down):
    wood = [[1 if square == '#' else 0 for square in line] for line in wood.strip().split('\n')]
    start, trees, depth, width = [0, 0], 0, len(wood), len(wood[0])
    while start[0] < depth:
        trees += wood[start[0]][start[1]]
        start = [start[0] + down, (start[1] + right) % width]
    return trees

print(slope(WOOD, 3, 1))
wood = open("input.txt").read()
print(slope(wood, 3, 1))

tot = 1
for right, down in ((1, 1), (3, 1), (5, 1), (7, 1), (1, 2)):
    tot *= slope(wood, right, down)
print(tot)
