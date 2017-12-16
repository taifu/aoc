# The Josephus Problem 
# https://en.wikipedia.org/wiki/Josephus_problem
# https://www.youtube.com/watch?v=uCsD3ZGzMgE

def josephus_n(n_elfs):
    n = 1
    while n < n_elfs:
        n = n * 2
    n = n / 2
    return 1 + (n_elfs - n) * 2

print(josephus_n(3017957))

def josephus(n, k):
    r = 0
    for i in xrange(1, n+1):
        r = (r+k)%i
    return r + 1

print(josephus(3017957, 2))

def josephus_across(n):
    p = 1
    while 3 * p <= n:
        p*=3
    if n == p:
        return n
    return n - p + max(n - 2 * p, 0)

print(josephus_across(3017957))
