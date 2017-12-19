def load(filename):
    return [list(l[:-1]) for l in open(filename).readlines()]

def solve(maze):
    pos = [maze[0].index('|'), 0]
    direction = [0, 1]

    letters = ""
    steps = 1

    while True:
        cur = maze[pos[1]][pos[0]]
        if cur.isalpha():
            letters += cur
            cur = next_cur
        next_pos = [pos[0] + direction[0], pos[1] + direction[1]]
        if not (0 <= next_pos[0] < len(maze[0]) and 0 <= next_pos[1] < len(maze)):
            break
        next_cur = maze[next_pos[1]][next_pos[0]]
        if next_cur == cur or next_cur.isalpha():
            pos = next_pos
            if next_cur.isalpha():
                next_cur = cur
        elif next_cur in ('-', '|'):
            pos = [next_pos[0] + direction[0], next_pos[1] + direction[1]]
            steps += 1
        elif next_cur == '+':
            if direction[0] == 0:
                direction1 = [1, 0]
                direction2 = [-1, 0]
                next_cur = '-'
            else:
                direction1 = [0, 1]
                direction2 = [0, -1]
                next_cur = '|'
            next_pos1 = [next_pos[0] + direction1[0], next_pos[1] + direction1[1]]
            next_pos2 = [next_pos[0] + direction2[0], next_pos[1] + direction2[1]]
            if (0 <= next_pos1[0] < len(maze[0])) and (0 <= next_pos1[1] < len(maze)) and (
                maze[next_pos1[1]][next_pos1[0]] == next_cur or maze[next_pos1[1]][next_pos1[0]].isalpha()):
                pos = next_pos1
                direction = direction1
            else:
                pos = next_pos2
                direction = direction2
            steps += 1
        else:
            break
        steps += 1
    return letters, steps

print(solve(load("input-test")))
print(solve(load("input")))
