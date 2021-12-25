class Cucumbers:
    def __init__(self, data):
        raw_data = data.strip().split('\n')
        self.cucumbers = dict(((x, y), c) for y, line in enumerate(raw_data) for x, c in enumerate(line) if c in 'v>')
        self.size = (len(raw_data[0]), len(raw_data))

    def move(self):
        steps = 0
        while True:
            steps += 1
            moved = 0
            for direction, dx, dy in (('>', 1, 0), ('v', 0, 1)):
                moving = set()
                for y in range(self.size[1]):
                    for x in range(self.size[0]):
                        cucumber = self.cucumbers.get((x, y), '.')
                        if cucumber != direction:
                            continue
                        next_x = (x + dx) % self.size[0]
                        next_y = (y + dy) % self.size[1]
                        if (next_x, next_y) not in self.cucumbers:
                            moving.add((cucumber, x, y, next_x, next_y))
                if moving:
                    moved += len(moving)
                    for cucumber, x, y, next_x, next_y in moving:
                        del self.cucumbers[x, y]
                        self.cucumbers[next_x, next_y] = cucumber
            if moved == 0:
                break
        return steps


def solve1(data):
    return Cucumbers(data).move()


if __name__ == "__main__":
    data = open("input.txt").read()
    print(solve1(data))
