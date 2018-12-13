raw = r"""/->-\        
|   |  /----\
| /-+--+-\  |
| | |  | v  |
\-+-/  \-+--/
  \------/  """

raw = r"""/>-<\  
|   |  
| /<+-\
| | | v
\>+</ |
  |   ^
  \<->/"""

raw = open("input.txt").read()


DOWN, UP, LEFT, RIGHT = list("v^<>")
G_LEFT, G_STRAIGHT, G_RIGHT = range(3)
DELTA = {DOWN: (0, 1), UP: (0, -1), LEFT: (-1, 0), RIGHT: (1, 0)}


def read(raw):
    track = []
    cars = {}
    for y, line in enumerate(raw.split("\n")):
        row = list(line)
        for x, direction in enumerate(row):
            if direction in (DOWN, UP, LEFT, RIGHT):
                cars[len(cars)] = [x, y, direction, G_LEFT]
                if direction in (LEFT, RIGHT):
                    row[x] = "-"
                else:
                    row[x] = "|"
        track.append(row)
    return track, cars


def turn(street, direction, turning):
    if street == "+":
        if turning == G_LEFT:
            if direction == LEFT:
                direction = DOWN
            elif direction == RIGHT:
                direction = UP
            elif direction == DOWN:
                direction = RIGHT
            else:
                direction = LEFT
        elif turning == G_RIGHT:
            if direction == LEFT:
                direction = UP
            elif direction == RIGHT:
                direction = DOWN
            elif direction == DOWN:
                direction = LEFT
            else:
                direction = RIGHT
        turning = (turning + 1) % 3
    elif street == "/":
        if direction == LEFT:
            direction = DOWN
        elif direction == RIGHT:
            direction = UP
        elif direction == DOWN:
            direction = LEFT
        else:
            direction = RIGHT
    elif street == "\\":
        if direction == LEFT:
            direction = UP
        elif direction == RIGHT:
            direction = DOWN
        elif direction == DOWN:
            direction = RIGHT
        else:
            direction = LEFT
    return direction, turning


def move(car, track):
    x, y, direction, turning = car
    delta = DELTA.get(direction, (0, 0))
    x, y = x + delta[0], y + delta[1]
    street = track[y][x]
    if street in "+/\\":
        direction, turning = turn(street, direction, turning)
    car[0:4] = x, y, direction, turning


def draw(track, cars):
    print("=" * 10)
    for y, row in enumerate(track):
        line = ""
        for x, c in enumerate(row):
            for c_x, c_y, direction, turning in cars.values():
                if (c_x, c_y) == (x, y):
                    c = direction
                    break
            line += c
        print("{} {}".format(str(y).zfill(3), line))
    print("=" * 10)


track, cars = read(raw)
tick, first_crash = 0, True

while True:
    tick += 1
    positions = dict((((x, y), car) for car, (x, y, direction, turning) in cars.items()))
    to_remove = set()
    for car, (x, y, direction, turning) in cars.copy().items():
        move(cars[car], track)
        position = (cars[car][0], cars[car][1])
        if position in positions:
            if first_crash:
                print("{},{}".format(*position))
                first_crash = False
            to_remove.add(positions[position])
            to_remove.add(car)
        else:
            positions.pop((x, y))
        positions[position] = car
    for car in to_remove:
        cars.pop(car)
    if len(cars) == 1:
        print("{},{}".format(*cars.values()[0][:2]))
        break
