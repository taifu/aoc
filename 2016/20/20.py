blocked = [[int(n) for n in l.strip().split("-")] for l in open("input").readlines()]

max_last = good_ip = 0

for blocked_from, blocked_to in sorted(blocked):
    if blocked_from > max_last + 1:
        if good_ip == 0:
            print(max_last + 1)
        good_ip += blocked_from - (max_last + 1)
    max_last = max(max_last, blocked_to)

print(good_ip + max_last - min(4294967295, max_last))
