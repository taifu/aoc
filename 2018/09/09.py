# 400 players; last marble is worth 71864 points

players = 400
m_last = 71864


class Marble:
    def __init__(self, value, previous=None, next=None, inserting=False):
        self.value = value
        self.next = next or self
        self.previous = previous or self
        if inserting:
            self.previous.next = self.next.previous = self

    def remove(self):
        self.previous.next, self.next.previous = self.next, self.previous
        return self.next

    def output(self):
        n = self
        while True:
            print(n.value, end=' ')
            n = n.next
            if n == self:
                break
        print()


for last in (m_last, m_last * 100):
    points, player, current = [0] * players, 0, Marble(0)
    for m in range(1, last + 1):
        if m % 23 == 0:
            for step in range(7):
                current = current.previous
            points[player] += m + current.value
            current = current.remove()
        else:
            current = Marble(m, current.next, current.next.next, inserting=True)
        player = (player + 1) % players
    print(max(points))
