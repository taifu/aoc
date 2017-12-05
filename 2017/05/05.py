for times in range(2):
    maze = [int(l.strip()) for l in open("input", "r").readlines()]
    l = len(maze)

    pos = steps = 0

    while pos >= 0 and pos < l:
        if times == 0:
            inc = 1
        else:
            inc = -1 if maze[pos] >= 3 else 1
        maze[pos] += inc
        pos += maze[pos] - inc
        steps += 1

    print(steps)
