class Item:
    dirs = set()

    def __init__(self, father=None, size = 0, directory=True):
        self.father = father
        self.size = 0
        if directory:
            self.items = {}
            self.dirs.add(self)
        else:
            self.add_size(size)

    def add_size(self, size):
        self.size += size
        if self.father:
            self.father.add_size(size)


def load(data):
    tree = Item()
    tree.dirs.clear()
    for line in data.strip().split("\n"):
        if line.startswith('$ cd'):
            name = line.split()[2]
            if name == '/':
                current = tree
            elif name == '..':
                current = current.father
            else:
                current = current.items[name]
        elif line.startswith('$ ls'):
            continue
        elif line.startswith('dir'):
            name = line.split()[1]
            current.items[name] = Item(current)
        else:
            size, name = line.split()
            current.items[name] = Item(current, int(size), False)
    return tree


def solve1(data):
    tree = load(data)
    return sum(d.size for d in tree.dirs if d.size <= 100000)


def solve2(data):
    tree = load(data)
    needed, delete = tree.size - 40000000, tree
    for directory in tree.dirs:
        if directory.size >= needed and directory.size < delete.size:
            delete = directory
    return delete.size


if __name__ == "__main__":
    data = open("input.txt").read()
    print(solve1(data))
    print(solve2(data))
