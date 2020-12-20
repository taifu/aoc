from collections import defaultdict
import math


SIZE = 10
MONSTER = "                  # \n#    ##    ##    ###\n #  #  #  #  #  #   \n"


def get_dots(monster):
    return tuple(tuple(1 if dot == '#' else 0 for dot in line) for line in monster.split('\n') if line)


def show(tile, no_border=False):
    size = len(tile[0])
    for x in range(size):
        if no_border and x in (0, size - 1):
            continue
        print(''.join('#' if c == 1 else '.' if c == 0 else 'O' for c in (tile[x][1:-1] if no_border else tile[x])))
    print()


def flip(tile):
    new_tile = []
    size = len(tile[0])
    for x in range(size):
        new_tile.append(tuple(tile[x][size - y - 1] for y in range(size)))
    return new_tile


def rotate(tile):
    new_tile = []
    size = len(tile[0])
    for y in range(size):
        new_tile.append(list(tile[x][size - y - 1] for x in range(size)))
    return new_tile


def get_borders(tile):
    size = len(tile[0])
    return tuple(tile[0]), tuple(tile[x][size - 1] for x in range(size)), tuple(tile[size - 1]), tuple(tile[x][0] for x in range(size))


def remove_borders(key, borders):
    for k, v in borders.items():
        if key in v:
            v.remove(key)


def parse(data):
    tiles = {}
    for tile in data.strip().split('\n\n'):
        for n, line in enumerate(tile.split('\n')):
            if n == 0:
                key = int(line[-5:-1])
                space = []
            else:
                space.append(tuple(1 if c == '#' else 0 for c in line))
        tiles[key] = space
    return tiles


def get_adiajents(key, tile, borders):
    adjacents = []
    for border in get_borders(tile):
        adjacents.append(set((k for k in borders[border] if k != key)))
    return adjacents


def erase_sea(tile, monster, dx, dy):
    size_x_monster = len(monster[0])
    size_y_monster = len(monster)
    for x in range(size_x_monster):
        for y in range(size_y_monster):
            if monster[y][x] == 1:
                tile[y + dy][x + dx] = -1


def count_sea(tile, monster):
    size = len(tile[0])
    size_x_monster = len(monster[0])
    size_y_monster = len(monster)
    positions = []
    for x in range(size - size_x_monster):
        for y in range(size - size_y_monster):
            found = True
            for dx in range(size_x_monster):
                for dy in range(size_y_monster):
                    if monster[dy][dx] == 1 and tile[y + dy][x + dx] == 0:
                        found = False
                        break
                if not found:
                    break
            if found:
                positions.append((x, y))
    return positions


def solve(data, step=1):
    tiles = parse(data)
    borders = defaultdict(set)
    for key, tile in tiles.items():
        for tile1 in tile, flip(tile):
            for n in range(4):
                for border in get_borders(tile1):
                    borders[border].add(key)
                tile1 = rotate(tile1)
    uniques = defaultdict(int)
    for k, v in borders.items():
        if len(v) == 1:
            uniques[list(v)[0]] += 1
    corners = []
    sides = []
    for k, v in uniques.items():
        if v == 4:
            corners.append(k)
        elif v == 2:
            sides.append(k)
        else:
            assert False
    if step == 1:
        id = 1
        for k in corners:
            id *= k
        return id
    dimension = int(math.sqrt(len(tiles)))
    image = [[0] * dimension for n in range(dimension)]
    for row in range(dimension):
        if row == 0:
            corner = corners.pop(0)
            corner_tile = tiles.pop(corner)
            found = False
            for tile in corner_tile, flip(corner_tile):
                for n in range(4):
                    adjacents = get_adiajents(corner, tile, borders)
                    if len(adjacents[0]) == 0 and len(adjacents[3]) == 0:
                        image[0][0] = (corner, tile)
                        last_border = get_borders(tile)[1]
                        remove_borders(corner, borders)
                        found = True
                        break
                    tile = rotate(tile)
                if found:
                    break
            for col in range(1, dimension):
                assert len(borders[last_border]) == 1
                this = list(borders[last_border])[0]
                this_tile = tiles.pop(this)
                found = False
                for tile in this_tile, flip(this_tile):
                    for n in range(4):
                        if get_borders(tile)[3] == last_border:
                            image[row][col] = (this, tile)
                            last_border = get_borders(tile)[1]
                            remove_borders(this, borders)
                            found = True
                            break
                        tile = rotate(tile)
                    if found:
                        break
        else:
            for col in range(dimension):
                up, up_tile = image[row - 1][col]
                up_border = get_borders(up_tile)[2]
                assert len(borders[up_border]) == 1
                this = list(borders[up_border])[0]
                this_tile = tiles.pop(this)
                found = False
                for tile in this_tile, flip(this_tile):
                    for n in range(4):
                        if get_borders(tile)[0] == up_border:
                            image[row][col] = (this, tile)
                            remove_borders(this, borders)
                            found = True
                            break
                        tile = rotate(tile)
                    if found:
                        break
    size = dimension * (SIZE - 2)
    raster = [[0] * size for n in range(size)]
    for row in range(dimension):
        for col in range(dimension):
            tile = image[row][col][1]
            dx = row * (SIZE - 1)
            dy = col * (SIZE - 1)
            for x in range(1, SIZE - 1):
                for y in range(1, SIZE - 1):
                    raster[dx + x - row - 1][dy + y - col - 1] = tile[x][y]
    sea_monster = get_dots(MONSTER)
    for tile in raster, flip(raster):
        for n in range(4):
            positions = count_sea(tile, sea_monster)
            if len(positions) > 0:
                for x, y in positions:
                    erase_sea(tile, sea_monster, x, y)
                return sum(sum(dot for dot in line if dot == 1) for line in tile)
            tile = rotate(tile)


if __name__ == "__main__":
    data = open("input.txt").read()
    print(solve(data))
    print(solve(data, step=2))
