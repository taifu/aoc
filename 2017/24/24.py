class Port:
    def __init__(self, pin1, pin2):
        self.pin1 = pin1
        self.pin2 = pin2

    def other_pin(self, pin):
        if pin == self.pin1:
            return self.pin2
        return self.pin1


def load(filename):
    ports = set()
    for l in open(filename).readlines():
        pin1, pin2 = tuple(int(p) for p in l.strip().split("/"))
        ports.add(Port(pin1, pin2))
    return ports


def all_bridges(ports, path=None, bridges=None):
    if bridges is None:
        bridges = set()
    if path is None:
        path = (0,)
    last_pin = path[-1]
    availables = [p for p in ports if p.pin1 == last_pin or p.pin2 == last_pin]
    if not availables:
        bridges.add(path)
        return bridges
    else:
        for port in availables:
            ports.remove(port)
            all_bridges(ports, path + (port.other_pin(last_pin),), bridges)
            ports.add(port)
        return bridges

ports = load("input")
bridges = all_bridges(ports)

print(max(sum(bridge[:-1]) * 2 + bridge[-1] for bridge in bridges))
longest = max(len(bridge) for bridge in bridges)
print(max(sum(bridge[:-1]) * 2 + bridge[-1] for bridge in bridges if len(bridge) == longest))
