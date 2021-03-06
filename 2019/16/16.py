class FFT:
    def __init__(self, raw_data, pattern):
        self.data = [int(n) for n in raw_data.strip()]
        self.length = len(self.data)
        self.pattern = pattern
        self.pattern_length = len(self.pattern)

    def process(self, n_loops):
        for loop in range(n_loops):
            self.data = [abs(sum(self.data[i] * self.pattern[((1 + i) // (n + 1)) % self.pattern_length] for i in range(self.length))) % 10 for n in range(self.length)]
        return "".join(str(v) for v in self.data)

    def fast_process(self, n_loops, first_digit):
        """
        Pattern of last n/2 digits:

        1234567812345678
                |||||||8+0=8
                |||||||8
                ||||||7+8=15 % 10 = 5
                ||||||5
                |||||6+5=11 % 10 = 1
                |||||1
                ||||5+1=6
                ||||6
                |||4+6=10 % 10 = 0
                |||0
                ||3+0=3
                ||3
                |2+3=5
                |5
                1+5=6
                6
        ........65306158

        """
        skip = int("".join(str(d) for d in self.data[:first_digit]))
        assert skip > self.length / 2  # This doesn't work for first n/2 digits
        data = self.data[skip:]
        length = len(data)
        for loop in range(n_loops):
            new_data = data[:]
            for n in range(length - 2, -1, -1):
                new_data[n] = (data[n] + new_data[n + 1]) % 10
            data = new_data
        return "".join(str(d) for d in new_data[:8])


def test_fft():
    assert FFT("12345678", [0, 1, 0, -1]).process(1) == "48226158"
    assert FFT("12345678", [0, 1, 0, -1]).process(2) == "34040438"
    assert FFT("12345678", [0, 1, 0, -1]).process(3) == "03415518"
    assert FFT("12345678", [0, 1, 0, -1]).process(4) == "01029498"
    assert FFT("80871224585914546619083218645595", [0, 1, 0, -1]).process(100)[:8] == "24176176"
    assert FFT("19617804207202209144916044189917", [0, 1, 0, -1]).process(100)[:8] == "73745418"
    assert FFT("69317163492948606335995924319873", [0, 1, 0, -1]).process(100)[:8] == "52432133"
    assert FFT("03036732577212944063491565474664" * 10000, [0, 1, 0, -1]).fast_process(100, 7) == "84462026"
    assert FFT("02935109699940807407585447034323" * 10000, [0, 1, 0, -1]).fast_process(100, 7) == "78725270"
    assert FFT("03081770884921959731165446850517" * 10000, [0, 1, 0, -1]).fast_process(100, 7) == "53553731"


if __name__ == "__main__":
    print(FFT(open("input.txt").read(), [0, 1, 0, -1]).process(100)[:8])
    print(FFT(open("input.txt").read().strip() * 10000, [0, 1, 0, -1]).fast_process(100, 7)[:8])
