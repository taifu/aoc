def next_gen(gen, mult, mod):
    while True:
        gen = (gen * mult) % 2147483647
        if gen % mod == 0:
            return gen


def judge(gen_a, gen_b, pairs, mod_a=1, mod_b=1):
    vote = 0
    while pairs > 0:
        gen_a = next_gen(gen_a, 16807, mod_a)
        gen_b = next_gen(gen_b, 48271, mod_b)
        if (gen_a & 65535) == (gen_b & 65535):
            vote += 1
        pairs -= 1
    return vote


# print(judge(65, 8921, 40000000))

print(judge(883, 879, 40000000))
print(judge(883, 879, 5000000, 4, 8))
