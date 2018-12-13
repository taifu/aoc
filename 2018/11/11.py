

def build_matrix(seed, size):
    matrix = [[0] * size for x in range(size)]
    for x in range(size):
        for y in range(size):
            rack_id = x + 1 + 10
            matrix[y][x] = (((rack_id * (y + 1) + seed) * rack_id) // 100 % 10) - 5
    return matrix


def find_max(matrix, size):
    size_matrix = len(matrix)
    max_power = max_x = max_y = 0
    for x in range(size_matrix - size):
        for y in range(size_matrix - size):
            power = sum(matrix[py][px] for px in range(x, x + size) for py in range(y, y + size))
            if power > max_power:
                max_x, max_y, max_power = x, y, power
    return max_x, max_y, max_power


# print(build_matrix(8, 300)[4][2])
# print(build_matrix(57, 300)[78][121])
# print(build_matrix(39, 300)[195][216])
# print(build_matrix(71, 300)[152][100])

def kadane(array):
    max_so_far = max_ending_here = 0
    max_x1 = max_x2 = 0
    for i, value in enumerate(array):
        max_ending_here = max_ending_here + value
        if max_ending_here < 0:
            max_ending_here = 0
            max_x1 = i + 1
        # Do not compare for all elements. Compare only
        # when  max_ending_here > 0
        elif (max_so_far < max_ending_here):
            max_so_far = max_ending_here
            max_x2 = i + 1
    return max_so_far, max_x1, max_x2


matrix = build_matrix(8979, 300)

print("{},{}".format(*find_max(matrix, 3)[:2]))

max_power = max_x = max_y = max_size = 0
for size in range(1, 301):
    x, y, power = find_max(matrix, size)
    if power > max_power:
        max_x, max_y, max_power, max_size = x, y, power, size
print("{},{},{}".format(max_x + 1, max_y + 1, max_size))
