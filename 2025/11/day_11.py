from collections import defaultdict


class Server:
    def __init__(self, data: str) -> None:
        self.graph: dict[str, list[str]] = defaultdict(list)
        for line in data.strip().splitlines():
            root, branches = line.split(':')
            for branch in branches.split():
                self.graph[root].append(branch.strip())

    def ways(self, root: str, target: str) -> int:
        memo: dict[str, int] = {}
        def dfs(node: str) -> int:
            if node == target:
                return 1
            if node in memo:
                return memo[node]
            total = 0
            for nxt in self.graph[node]:
                total += dfs(nxt)
            memo[node] = total
            return total
        return dfs(root)


def load(data: str) -> Server:
    return Server(data)


def solve1(data: str) -> int:
    return load(data).ways('you', 'out')


def solve2(data: str) -> int:
    server = load(data)
    return (server.ways('svr' ,'fft')*server.ways('fft', 'dac')*server.ways('dac', 'out') + 
            server.ways('svr' ,'dac')*server.ways('dac', 'fft')*server.ways('fft', 'out'))


if __name__ == "__main__":
    import sys, os  # noqa: E401
    data = open((sys.argv + [os.path.dirname(__file__) + "/input.txt"])[1]).read()
    print(solve1(data))
    print(solve2(data))
