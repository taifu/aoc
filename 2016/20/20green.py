blacklist = set()

[blacklist.add(tuple([int(i) for i in l.strip().split('-')])) for l in open('input')]

curmax = 0
found = False
foundmin = False
whitelist = set()
while curmax <= 2**32:
    found = True
    i = curmax
    for (start,end) in list(blacklist):
        if start <= i <= end:
            curmax = max(curmax, end+1)
            blacklist.remove((start,end))
            found = False
    if found:
        if not foundmin:
            print(curmax)
            foundmin = True
        whitelist.add(curmax)
        curmax += 1
print(len(whitelist)-1)

