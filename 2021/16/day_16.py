import math


class Packet:
    def __init__(self, version, typ, value=0):
        self.version = version
        self.typ = typ
        self.value = value
        self.packets = []

    def compute(self):
        value = 0
        if self.typ == 4:
            value = self.value
        elif self.typ == 0:
            value += sum(p.compute() for p in self.packets)
        elif self.typ == 1:
            value += math.prod(p.compute() for p in self.packets)
        elif self.typ == 2:
            value += min(p.compute() for p in self.packets)
        elif self.typ == 3:
            value += max(p.compute() for p in self.packets)
        elif self.typ == 5:
            value += 1 if self.packets[0].value > self.packets[1].value else 0
        elif self.typ == 6:
            value += 1 if self.packets[0].value < self.packets[1].value else 0
        elif self.typ == 7:
            value += 1 if self.packets[0].value == self.packets[1].value else 0
        else:
            raise Exception(f"packet type unknown {self.typ}")
        return value

    def versions(self):
        return self.version + sum(p.versions() for p in self.packets)

    @staticmethod
    def get(bits, n, raw=False):
        part, bits = bits[:n], bits[n:]
        if not raw:
            part = int(part[:n], 2)
        return part, bits

    @staticmethod
    def parse_value(bits):
        value = ""
        while True:
            part, bits = Packet.get(bits, 5, raw=True)
            value += part[1:]
            if part[0] == '0':
                break
        return int(value, 2), bits

    @staticmethod
    def compile(prog):
        version, prog = Packet.get(prog, 3)
        typ, prog = Packet.get(prog, 3)
        if typ == 4:
            value, prog = Packet.parse_value(prog)
            return Packet(version, typ, value), prog
        length_type, prog = Packet.get(prog, 1)
        assert length_type in (0, 1)
        length, prog = Packet.get(prog, 11 if length_type == 1 else 15)
        packet = Packet(version, typ)
        if length_type == 0:
            total_length = len(prog)
            while total_length - len(prog) < length:
                sub_packet, prog = Packet.compile(prog)
                packet.packets.append(sub_packet)
            return packet, prog
        for cont in range(length):
            sub_packet, prog = Packet.compile(prog)
            packet.packets.append(sub_packet)
        return packet, prog


def to_prog(data):
    return "".join(bin(int(c, 16))[2:].zfill(4) for c in data.strip())


def compile(data):
    return Packet.compile(to_prog(data))[0]


def solve1(data):
    return compile(data).versions()


def solve2(data):
    return compile(data).compute()


if __name__ == "__main__":
    data = open("input.txt").read()
    print(solve1(data))
    print(solve2(data))
