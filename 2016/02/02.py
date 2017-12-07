keys = {
    (0,0): 1, (1,0): 2, (2,0): 3,
    (0,1): 4, (1,1): 5, (2,1): 6,
    (0,2): 7, (1,2): 8, (2,2): 9,
    }

pos = [1, 1]

code = ""
for instruction in open("input", "r").readlines():
    for step in instruction:
        if step == 'U':
            pos[1] = max(0, pos[1] - 1)
        elif step == 'D':
            pos[1] = min(2, pos[1] + 1)
        elif step == 'L':
            pos[0] = max(0, pos[0] - 1)
        elif step == 'R':
            pos[0] = min(2, pos[0] + 1)
    code += str(keys[tuple(pos)])
print(code)


keys = {
                            (2,0): '1',
                (1,1): '2', (2,1): '3', (3,1): '4',
    (0,2): '5', (1,2): '6', (2,2): '7', (3,2): '8', (4,2): '9',
                (1,3): 'A', (2,3): 'B', (3,3): 'C',
                            (2,4): 'D',
    }

pos = [0, 2]

code = ""
for instruction in open("input", "r").readlines():
    for step in instruction:
        new_pos = pos.copy()
        if step == 'U':
            new_pos[1] = new_pos[1] - 1
        elif step == 'D':
            new_pos[1] = new_pos[1] + 1
        elif step == 'L':
            new_pos[0] = new_pos[0] - 1
        elif step == 'R':
            new_pos[0] = new_pos[0] + 1
        if tuple(new_pos) in keys:
            pos = new_pos
    code += str(keys[tuple(pos)])

print(code)
