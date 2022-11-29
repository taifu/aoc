d = 312051

class Matrix:
    def next(self):
        step_even = (self.step % 2) == 0
        times_even = (self.times % 2) == 0
        if times_even:
            if step_even:
                self.x -= 1
            else:
                self.x += 1
        else:
            if step_even:
                self.y -= 1
            else:
                self.y += 1

    def reset(self):
        self.step = 1
        self.move = 0
        self.times = 0
        self.current = 1
        self.x, self.y = 0, 0
        self.board = {(0, 0): self.current}

    def cycle(self):
        if self.move == self.step:
            self.times += 1
            self.move = 0
        if self.times == 2:
            self.times = 0
            self.step += 1
        self.next()

    def around(self):
        t = 0
        for i in (-1, 0, 1):
            for j in (-1, 0, 1):
                if i == j == 0:
                    continue
                pos = (self.x + i, self.y + j)
                t += self.board.get(pos, 0)
        return t

    def compute(self):
        self.board[(self.x, self.y)] = self.current
        self.move += 1

    def coordinates(self, p):
        self.reset()
        while self.current < p:
            self.cycle()
            self.current += 1
            self.compute()
        return self.x, self.y

    def larger(self, p):
        self.reset()
        while self.current <= p:
            self.cycle()
            self.current = self.around()
            self.compute()
        return self.current

matrix = Matrix()

print(d, sum(abs(a) for a in matrix.coordinates(d)))
print(d, matrix.larger(d))
