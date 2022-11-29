import re
import hashlib


def md5(salt):
    return hashlib.md5(salt.encode('utf8')).hexdigest()


def md5_times(salt, times=1, seen={}):
    try:
        return seen[salt, times]
    except KeyError:
        pass
    key = salt
    for i in range(times):
        key = md5(key)
    seen[salt, times] = key
    return key


TRIPLET = re.compile(r"(.)\1{2}")


def generate(salt, times=1, how_many=64):
    found = index = 0
    while found < how_many:
        key = md5_times(salt + str(index), times)
        triplets = TRIPLET.findall(key)
        if triplets:
            quintuplet = triplets[0] * 5
            for next_index in range(index + 1, index + 1001):
                if re.findall(quintuplet, md5_times(salt + str(next_index), times)):
                    found += 1
                    break
        index += 1
    return index - 1

salt = 'qzyelonm'
print(generate(salt))
print(generate(salt, 2017))
