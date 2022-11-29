freqs = [int(x.strip()) for x in open("input.txt").readlines()]
print(sum(freqs))
curr_freq = 0
seen = set([0])
n = 0
while True:
    curr_freq += freqs[n % len(freqs)]
    if curr_freq in seen:
        print(curr_freq)
        break
    seen.add(curr_freq)
    n += 1
