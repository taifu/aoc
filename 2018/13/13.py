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
    carts = {}
    for y, line in enumerate(raw.split("\n")):
        row = list(line)
        for x, direction in enumerate(row):
            if direction in (DOWN, UP, LEFT, RIGHT):
                carts[len(carts)] = [x, y, direction, G_LEFT]
                if direction in (LEFT, RIGHT):
                    row[x] = "-"
                else:
                    row[x] = "|"
        track.append(row)
    return track, carts


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


def move(cart, track):
    x, y, direction, turning = cart
    delta = DELTA.get(direction, (0, 0))
    x, y = x + delta[0], y + delta[1]
    street = track[y][x]
    if street in "+/\\":
        direction, turning = turn(street, direction, turning)
    cart[0:4] = x, y, direction, turning


def draw(track, carts):
    print("=" * 10)
    for y, row in enumerate(track):
        line = ""
        for x, c in enumerate(row):
            for c_x, c_y, direction, turning in carts.values():
                if (c_x, c_y) == (x, y):
                    c = direction
                    break
            line += c
        print("{} {}".format(str(y).zfill(3), line))
    print("=" * 10)


track, carts = read(raw)
tick, first_crash = 0, True

while True:
    tick += 1
    positions = dict((((x, y), cart) for cart, (x, y, direction, turning) in carts.items()))
    to_remove = set()
    carts_order = sorted([(y, x, cart, direction, turning) for cart, (x, y, direction, turning) in carts.items()])
    for y, x, cart, direction, turning in carts_order:
        move(carts[cart], track)
        position = (carts[cart][0], carts[cart][1])
        if position in positions:
            if first_crash:
                print("{},{}".format(*position))
                first_crash = False
            to_remove.add(positions[position])
            to_remove.add(cart)
        else:
            positions.pop((x, y))
        positions[position] = cart
    for cart in to_remove:
        carts.pop(cart)
    if len(carts) == 1:
        print("{},{}".format(*carts.values()[0][:2]))
        break
