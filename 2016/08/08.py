ROWS, COLS = 6, 50

matrix = [[' '] * COLS for x in range(ROWS)]

for instruction in open("input").readlines():
    parts = instruction.strip().split(" ")
    if parts[0] == "rect":
        sizes = parts[1].split("x")
        for x in range(int(sizes[0])):
            for y in range(int(sizes[1])):
                matrix[y][x] = "#"
    else:
        if parts[1] == "row":
            row = int(parts[2].split("=")[-1])
            for by in range(int(parts[4])):
                matrix[row] = matrix[row][-1:] + matrix[row][:-1]
        else:
            column = int(parts[2].split("=")[-1])
            for by in range(int(parts[4])):
                last = matrix[ROWS - 1][column]
                for n in range(ROWS - 1, 0, -1):
                    matrix[n][column] = matrix[n - 1][column]
                matrix[0][column] = last

tot = 0
for line in matrix:
    print("".join(line))
    tot += sum(1 for x in line if x == '#')

print(tot)
