# http://www.euclideanspace.com/maths/algebra/matrix/transforms/examples/index.htm

rotations_raw_matrices = """
1 0 0
0 1 0
0 0 1

0 0 1
0 1 0
-1 0 0

-1 0 0
0 1 0
0 0 -1

0 0 -1
0 1 0
1 0 0

0 -1 0
1 0 0
0 0 1

0 0 1
1 0 0
0 1 0

0 1 0
1 0 0
0 0 -1

0 0 -1
1 0 0
0 -1 0

0 1 0
-1 0 0
0 0 1

0 0 1
-1 0 0
0 -1 0

0 -1 0
-1 0 0
0 0 -1

0 0 -1
-1 0 0
0 1 0

1 0 0
0 0 -1
0 1 0

0 1 0
0 0 -1
-1 0 0

-1 0 0
0 0 -1
0 -1 0

0 -1 0
0 0 -1
1 0 0

1 0 0
0 -1 0
0 0 -1

0 0 -1
0 -1 0
-1 0 0

-1 0 0
0 -1 0
0 0 1

0 0 1
0 -1 0
1 0 0

1 0 0
0 0 1
0 -1 0

0 -1 0
0 0 1
-1 0 0

-1 0 0
0 0 1
0 1 0

0 1 0
0 0 1
1 0 0
"""


base = [1, 2, 4]
results = set()
for raw_matrix in rotations_raw_matrices.strip().split('\n\n'):
    matrix = [[int(s) for s in line.split(' ')] for line in raw_matrix.split('\n')]
    results.add(tuple(sum(base[m] * matrix[n][m] for m in range(3)) for n in range(3)))
for a, b, c in results:
    print(f"    lambda x, y, z: ({a}, {b}, {c}),".replace('1', 'x').replace('2', 'y').replace('4', 'z'))
