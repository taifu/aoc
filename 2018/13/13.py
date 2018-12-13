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

track = []
cars = {}
chars = "v^<>"

DOWN, UP, LEFT, RIGHT = list(chars)
G_LEFT, G_STRAIGHT, G_RIGHT = range(3)

for y, line in enumerate(raw.split("\n")):
    row = list(line)
    for x, direction in enumerate(row):
        if direction in chars:
            cars[len(cars)] = [x, y, direction, G_LEFT]
            if direction in (LEFT, RIGHT):
                row[x] = "-"
            else:
                row[x] = "|"
    track.append(row)


def turn(pos, direction, turning):
    if pos == "+":
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
    elif pos == "/":
        if direction == LEFT:
            direction = DOWN
        elif direction == RIGHT:
            direction = UP
        elif direction == DOWN:
            direction = LEFT
        else:
            direction = RIGHT
    elif pos == "\\":
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
    if direction == LEFT:
        x = x - 1
    elif direction == RIGHT:
        x = x + 1
    elif direction == UP:
        y = y - 1
    elif direction == DOWN:
        y = y + 1
    pos = track[y][x]
    if pos in "+/\\":
        direction, turning = turn(pos, direction, turning)
    car[0] = x
    car[1] = y
    car[2] = direction
    car[3] = turning


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


tick = 0
first_crash = True

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
    if len(to_remove) not in (0, 2):
        raise Exception("Wrong!")
    for car in to_remove:
        cars.pop(car)
    if len(cars) == 1:
        print("{},{}".format(*cars.values()[0][:2]))
        break
