start = {'hm': 1, 'lm': 1, 'hg': 2, 'lg': 3}


FINAL = set([4])

def check(position):
    

def explore(position, moves=0, seen=set(), best=None):
    if set(position.values()) == FINAL:
        if best is None or moves < best:
            print(moves, position)
            return best
    if not check(position):
        return
    current = repr(sorted(position.items()))
    if current in seen:
        return None
    seen.add(current)
    for thing, floor in position.items():
        if floor > 1:
            position[thing] = floor - 1
            best = explore(position, moves, seen, best)
            position[thing] = floor + 1
        if floor < 4:
            position[thing] = floor + 1
            best = explore(position, moves, seen, best)
            position[thing] = floor - 1
    return None

explore(start)
