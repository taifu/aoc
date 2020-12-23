def solve(data, moves=100, n_cups=9):
    cups = [int(cup) for cup in data] + [int(cup) for cup in range(len(data) + 1, n_cups + 1)]
    following = {}
    for n, cup in enumerate(cups):
        following[cup] = cups[(n + 1) % n_cups]
    current = cups[0]
    for move in range(moves):
        pick_up_1 = following[current]
        pick_up_2 = following[pick_up_1]
        pick_up_3 = following[pick_up_2]
        next_current = following[pick_up_3]
        following[current] = next_current
        destination = current
        while True:
            destination -= 1
            if destination == 0:
                destination = n_cups
            if destination not in (pick_up_1, pick_up_2, pick_up_3):
                break
        following[pick_up_3] = following[destination]
        following[destination] = pick_up_1
        current = next_current
    cups = []
    next_1 = 1
    for n in range(1, n_cups):
        cups.append(following[next_1])
        next_1 = cups[-1]
    if n_cups == 9:
        return "".join(str(cup) for cup in cups)
    return cups[0] * cups[1]


if __name__ == "__main__":
    data = "123487596"
    print(solve(data))
    print(solve(data, moves=10000000, n_cups=1000000))
