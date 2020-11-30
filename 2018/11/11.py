

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
    return max_x + 1, max_y + 1, max_power


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


def find_max_sub(matrix):
    L = R = cur_sum = max_x1 = max_x2 = max_y1 = max_y2 = 0
    max_sum = -float('inf')

    for L in range(len(matrix[0])):
        tmp = [0] * len(matrix)
        for R in range(L, len(matrix[0])):
            for n in range(len(matrix)):
                tmp[n] += matrix[n][R]
            cur_sum, y1, y2 = kadane(tmp)
            if cur_sum > max_sum:
                max_sum = cur_sum
                max_x1 = L
                max_x2 = R
                max_y1 = y1
                max_y2 = y2
    return max_sum, max_x1, max_x2, max_y1, max_y2


def find_max_square_sub(matrix):
    # cs[(x, y)] is the cumulative sum of d[(i, j)] for all i <= x and j <= y
    cs = {}
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            cs[(i, j)] = matrix[i][j] + cs.get((i - 1, j), 0) + cs.get((i, j - 1), 0) - cs.get((i - 1, j - 1), 0)
    m = -100
    mxy = 0
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            for s in range(len(matrix) - max(i, j)):
                k = cs[(i + s, j + s)] + cs[(i, j)] - cs[(i + s, j)] - cs[(i, j + s)]
                if k > m:
                    m = k
                    mxy = (j + 2, i + 2, s)
    return m, mxy


matrix = build_matrix(8979, 300)
print("{},{}".format(*find_max(matrix, 3)[:2]))

m, mxy = find_max_square_sub(matrix)
print("{},{},{}".format(*mxy))

# Brute force (sloooowwwww)
# max_power = max_x = max_y = max_size = 0
# for size in range(1, 301):
#     x, y, power = find_max(matrix, size)
#     if power > max_power:
#         max_x, max_y, max_power, max_size = x, y, power, size
# print("{},{},{}".format(max_x + 1, max_y + 1, max_size))
