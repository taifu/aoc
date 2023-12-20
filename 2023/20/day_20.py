from math import lcm, prod
from collections import deque


FF, CON, END = 0, 1, 2
OFF_LOW, ON_HIGH = 0, 1


class Node:
    def __init__(self, label: str, node_type: int, node_labels: list[str]):
        self.label = label
        self.type = node_type
        self.output_labels = node_labels
        self.output_nodes: list[Node] = []
        self.received: dict[str, int] = {}
        self.state = OFF_LOW

    def __repr__(self) -> str:
        descr, state = (("END", None) if self.type == END else (("F&F", self.state) if self.type == FF else
                        ("CON", f"{(','.join(f'{label}={val}' for label, val in self.received.items()))}")))
        return f"<Node:{self.label} type:{descr} state:{state}>"


class Modules:
    def __init__(self, raw: str):
        self.nodes: dict[str, Node] = {}
        self.cycles: dict[str, int] = {}
        self.stop = self.before_stop = None
        self.cycles = {}
        for line in raw.splitlines():
            parts = line.split(' -> ')
            node_type, label, node_labels = (FF if parts[0][0] == '%' else CON), parts[0][1:], parts[1].split(', ')
            if label == 'roadcaster':
                self.broadcaster = node_labels
            else:
                self.nodes[label] = Node(label, node_type, node_labels)
        for node_key in list(self.nodes.keys()):
            node = self.nodes[node_key]
            for label_node_out in node.output_labels:
                if label_node_out not in self.nodes:
                    assert self.stop is None
                    self.before_stop = node
                    self.stop = Node(label_node_out, END, [])
                    self.nodes[label_node_out] = self.stop
                node.output_nodes.append(self.nodes[label_node_out])
                self.nodes[label_node_out].received[node.label] = OFF_LOW
        self.before_before_stop = [self.nodes[label] for label in self.before_stop.received] if self.before_stop else []

    def push(self, loop: int = 0) -> list[int]:
        #  HIGH -> FF = ignored
        #  LOW -> FF OFF -> ON & send HIGH
        #  LOW -> FF ON -> OFF & send LOW
        #  any -> CON = update state -> if all(HIGH) send LOW else send HIGH
        pulses = deque((OFF_LOW, self.nodes[label]) for label in self.broadcaster)
        lows_highs = [len(self.broadcaster) + 1, 0]
        while pulses:
            pulse, node = pulses.popleft()
            if node.type == FF:
                # FF receive always low
                node.state = OFF_LOW if node.state == ON_HIGH else ON_HIGH
                pulse = node.state
            else:
                pulse = OFF_LOW if all(state == ON_HIGH for state in node.received.values()) else ON_HIGH
                if pulse == ON_HIGH and node in self.before_before_stop and node.label not in self.cycles:
                    self.cycles[node.label] = loop
            for node_out in node.output_nodes:
                if node_out.type == CON:
                    node_out.received[node.label] = pulse
                lows_highs[pulse] += 1
                # Ignore HIGH sent to FF
                if node_out.type == FF and pulse == ON_HIGH:
                    continue
                pulses.append((pulse, node_out))
        return lows_highs

    def total(self, part2: bool = False) -> int:
        n, tot_lows_highs = 0, [0, 0]
        while True:
            n += 1
            lows_highs = self.push(n)
            if part2:
                if len(self.cycles) == len(self.before_before_stop):
                    return lcm(*self.cycles.values())
            else:
                for m in (0, 1):
                    tot_lows_highs[m] += lows_highs[m]
                if n == 1000:
                    break
        return prod(tot_lows_highs)


def solve1(data: str) -> int:
    return Modules(data).total()


def solve2(data: str) -> int:
    return Modules(data).total(True)


if __name__ == "__main__":
    import sys
    data = open((sys.argv + ["input.txt"])[1]).read()
    print(solve1(data))
    print(solve2(data))
