#!/usr/bin/python3
##**Version**| [0.0.27 2021-12-14T08:23:52+01:00](14.py)
##-----------|-----------------------------------------------------------
##**Author** | Carlo ㎝ Miron, carlo&#64;miron.it

from collections import Counter

F, EXP = "input.txt", {10: 0, 40: 0}
if True:
    template, x = open(F).read().split("\n\n")
    rules = {k: v for k, v in [i.strip().split(" -> ") for i in x.strip().split("\n")]}
    pairs = Counter(["".join(i) for i in zip(template, template[1:])])
    for step in range(42):
        if step in EXP:
            polymer: Counter = Counter()
            for i in pairs:
                polymer[i[0]] += pairs[i]
            polymer[template[-1]] += 1
            got = max(polymer.values()) - min(polymer.values())
            assert EXP[step] in (got, 0), f"expected {EXP[step]}, got {got}"
            print("ok" if EXP[step] else got)
        new_pairs: Counter = Counter()
        for i in pairs:
            new_pairs[i[0] + rules[i]] += pairs[i]
            new_pairs[rules[i] + i[1]] += pairs[i]
        pairs = new_pairs

##--
##!!!! THE BEER-WARE LICENSE (Revision 42):
##    carlo&#64;miron.it wrote this file. As long as you retain this notice
##    you can do whatever you want with this stuff. If we meet some day, and
##    you think this stuff is worth it, you can buy me a beer in return. --㎝
