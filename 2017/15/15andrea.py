from itertools import izip

A = 116
B = 299

Af = 16807
Bf = 48271

def gen(start, factor):
    cur = start
    mask = (2**16 - 1)
    while True:
        cur = (cur * factor)  % 2147483647
        yield cur & mask

def gen2(start, factor, filt):
    cur = start
    mask = (2**16 - 1)
    while True:
        cur = (cur * factor)  % 2147483647
        if cur % filt == 0:
            yield cur & mask

def count_matches(a, b, max_p):
  points = 0
  for n, (x, y) in enumerate(izip(a, b)):
      if n >= max_p:
          break
      if x == y:
          points += 1
  return points

a = gen(A, Af)
b = gen(B, Bf)

#print count_matches(a, b, 40000000)

a = gen2(A, Af, 4)
b = gen2(B, Bf, 8)

#print count_matches(a, b, 5000000)

def puppyfriendly1(A, B):
    a, b = A, B
    mask = (2**16 - 1)
    total = 0
    part1 = 0
    while total < 40000000:
        total += 1
        a = (a * Af) % 2147483647
        b = (b * Bf) % 2147483647
        if (a & mask) == (b & mask):
            part1 += 1
    return part1

def puppyfriendly2(A, B):
    a, b = A, B
    mask = (2**16 - 1)
    total = 0
    result = 0
    while total < 5000000:
        total += 1
        a = (a * Af) % 2147483647
        while a % 4 != 0:
          a = (a * Af) % 2147483647
        b = (b * Bf) % 2147483647
        while b % 8 != 0:
          b = (b * Bf) % 2147483647
        if (a & mask) == (b & mask):
            result += 1
    return result

print puppyfriendly1(A, B)
print puppyfriendly2(A, B)
