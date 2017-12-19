
start = 20151125


def next(x):
    return (x * 252533) % 33554393

def count(row, col):
    x = y = 1
    while y != row:
        x += y
        y += 1
    n = 1
    y = row + 1
    while n != col:
        x += y
        n += 1
        y += 1
    return x

n = count(3, 4)
x = start
for i in xrange(n - 1):
    x = next(x)

n = count(2947, 3029)

x = start
for i in xrange(n - 1):
    x = next(x)
print x


