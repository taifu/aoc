from collections import Counter


class Image:
    def __init__(self, width, height, pixels):
        self.width = width
        self.height = height
        self.size = width * height
        self.pixels = pixels.strip()
        self.decode()

    def decode(self):
        self.layers = [self.pixels[n * self.size:(n + 1) * self.size] for n in range(len(self.pixels) // self.size)]
        final = [None for n in range(self.size)]
        for layer in self.layers:
            for n, pixel in enumerate(layer):
                if pixel in ('0', '1'):
                    if final[n] is None:
                        final[n] = "#" if pixel == '1' else " "
        self.final = ''.join(pixel or '2' for pixel in final)

    def check(self):
        self.counters = []
        min_0 = {'0': len(self.pixels)}
        for layer in self.layers:
            counter = Counter(layer)
            if counter['0'] < min_0['0']:
                min_0 = counter
        return min_0['1'] * min_0['2']

    def show(self):
        for n in range(self.height):
            print(self.final[n * self.width:(n + 1) * self.width])


def test():
    image = Image(3, 2, "123456789012")
    assert image.layers == ["123456", "789012"]
    image = Image(2, 2, "0222112222120000")
    assert image.final == " ## "


if __name__ == "__main__":
    image = Image(25, 6, open("input.txt").read())
    print(image.check())
    image.show()
