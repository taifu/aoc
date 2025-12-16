class Tree:
    def __init__(self, data: str) -> None:
        self.presents: dict[int, list[list[int]]] = {}
        self.boards: list[tuple[tuple[int, int], tuple[int, ...]]] = []
        for line in data.strip().split('\n\n'):
            parts = line.split(':')
            if len(parts) == 2:
                self.presents[int(parts[0])] = [[0 if pos == '.' else 1 for pos in line] for line in parts[1][1:].split('\n')]
            else:
                for board in line.split('\n'):
                    raw_xy, presents = board.split(':')
                    xy = raw_xy.split('x')
                    self.boards.append(((int(xy[0]), int(xy[1])), tuple(int(p) for p in presents.strip().split(' '))))
                break

    def how_many_fills(self) -> int:
        cont = 0
        for (x, y), presents in self.boards:
            tot_presents = sum(presents)
            tot_tiles_presents = sum(sum(sum(row) for row in self.presents[n]) * p for n, p in enumerate(presents))

            if tot_presents <= (x // 3) * (y // 3):
                cont += 1
                continue
            if tot_tiles_presents > x * y:
                continue
            raise Exception("Use DXF")
        return cont


def load(data: str) -> Tree:
    return Tree(data)


def solve1(data: str) -> int:
    return load(data).how_many_fills()


#def solve2(data: str) -> int:
    #server = load(data)
    #return (server.ways('svr' ,'fft')*server.ways('fft', 'dac')*server.ways('dac', 'out') + 
            #server.ways('svr' ,'dac')*server.ways('dac', 'fft')*server.ways('fft', 'out'))


if __name__ == "__main__":
    import sys, os  # noqa: E401
    data = open((sys.argv + [os.path.dirname(__file__) + "/input.txt"])[1]).read()
    print(solve1(data))
    #print(solve2(data))
