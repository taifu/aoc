def adj_cubes(cube):
    a,b,c = cube
    yield a+1,b,c
    yield a-1,b,c
    yield a,b+1,c
    yield a,b-1,c
    yield a,b,c+1
    yield a,b,c-1
with open("input.txt") as file:
    lines = file.read().splitlines()
cubes = [tuple(map(int,line.split(","))) for line in lines]
scanned_cubes = set()
p1 = 0
# +6 -2*(num_adj)
for cube in cubes:
    p1 += 6
    for adj in adj_cubes(cube):
        if adj in scanned_cubes:
            p1 -= 2
    scanned_cubes.add(cube)
print("Part 1:",p1)
p2 = p1
all_cubes = {(x,y,z) for x in range(20) for y in range(20) for z in range(20)}
empty_cubes = all_cubes-scanned_cubes
q = [(0,0,0)]
while q:
    c = q.pop()
    if c in empty_cubes:
        empty_cubes.remove(c)
        q.extend(adj_cubes(c))
for cube in empty_cubes:
    p2 += 6
    for adj in adj_cubes(cube):
        if adj in scanned_cubes:
            p2 -= 2
    scanned_cubes.add(cube)
print("Part 2:",p2)
