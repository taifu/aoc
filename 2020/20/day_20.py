import math
import operator
import functools
from collections import defaultdict


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


def get_borders(tile):
    size = len(tile[0])
    return tuple(tile[0]), tuple(tile[x][size - 1] for x in range(size)), tuple(tile[size - 1]), tuple(tile[x][0] for x in range(size))


def remove_borders(key, borders):
    for k, v in borders.items():
        if key in v:
            v.remove(key)


def rotate(tile):
    new_tile = []
    size = len(tile[0])
    for y in range(size):
        new_tile.append(list(tile[x][size - y - 1] for x in range(size)))
    return new_tile


def rotate_flip(tile):
    for rf_tile in tile, flip(tile):
        for n in range(4):
            yield(rf_tile)
            rf_tile = rotate(rf_tile)


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


def get_adjacents(key, tile, borders):
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


def get_all_borders(tiles):
    all_borders = defaultdict(set)
    for key, tile in tiles.items():
        for rf_tile in rotate_flip(tile):
            for border in get_borders(rf_tile):
                all_borders[border].add(key)
    return all_borders


def find_corners(tiles, all_borders):
    # Solo i tile agli angoli e ai lati hanno bordi che non confinano con alcun tile
    uniques = defaultdict(int)
    for k, v in all_borders.items():
        if len(v) == 1:
            uniques[list(v)[0]] += 1
    corners = []
    for k, v in uniques.items():
        if v == 4:
            corners.append(k)
        elif v != 2:
            assert False
    return corners


class Image:
    def __init__(self, data):
        tiles = parse(data)
        all_borders = get_all_borders(tiles)
        self.corners = find_corners(tiles, all_borders)
        self.dimension = int(math.sqrt(len(tiles)))
        self.image = [[0] * self.dimension for n in range(self.dimension)]
        for row in range(self.dimension):
            for col in range(0, self.dimension):
                if row == 0 and col == 0:
                    this = self.corners[0]
                    this_tile = tiles[this]
                    for tile in rotate_flip(this_tile):
                        adjacents = get_adjacents(this, tile, all_borders)
                        if len(adjacents[0]) == 0 and len(adjacents[3]) == 0:
                            self.image[0][0] = (this, tile)
                            last_border = get_borders(tile)[1]
                            remove_borders(this, all_borders)
                            break
                    d_row, d_col = 0, -1
                    n_last_border, n_next_border = 1, 3
                else:
                    if row == 1 and col == 0:
                        d_row, d_col = -1, 0
                        n_last_border, n_next_border = 2, 0

                    last_tile = self.image[row + d_row][col + d_col][1]
                    last_border = get_borders(last_tile)[n_last_border]
                    assert len(all_borders[last_border]) == 1
                    this = list(all_borders[last_border])[0]
                    this_tile = tiles[this]
                    for tile in rotate_flip(this_tile):
                        if get_borders(tile)[n_next_border] == last_border:
                            self.image[row][col] = (this, tile)
                            remove_borders(this, all_borders)
                            break
        self.raster = self.rasterize()

    def rasterize(self):
        size = self.dimension * (SIZE - 2)
        raster = [[0] * size for n in range(size)]
        for row in range(self.dimension):
            for col in range(self.dimension):
                tile = self.image[row][col][1]
                dx = row * (SIZE - 1)
                dy = col * (SIZE - 1)
                for x in range(1, SIZE - 1):
                    for y in range(1, SIZE - 1):
                        raster[dx + x - row - 1][dy + y - col - 1] = tile[x][y]
        return raster

    def count_sea_monster(self, sea_monster):
        for tile in rotate_flip(self.raster):
            positions = count_sea(tile, sea_monster)
            if len(positions) > 0:
                for x, y in positions:
                    erase_sea(tile, sea_monster, x, y)
                return sum(sum(dot for dot in line if dot == 1) for line in tile)


def solve(data, step=1):
    image = Image(data)
    if step == 1:
        return functools.reduce(operator.mul, image.corners, 1)
    return image.count_sea_monster(get_dots(MONSTER))


if __name__ == "__main__":
    data = open("input.txt").read()
    print(solve(data))
    print(solve(data, step=2))
