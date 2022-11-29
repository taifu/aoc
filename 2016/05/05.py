import hashlib

door = u"ffykfhsq"

pwd = ""
pwd2 = [0]*8

i = 0
found = 0

while len(pwd) < 8 or found < 8:
    dig = hashlib.md5((door + str(i)).encode('utf8')).hexdigest()[:7]
    if i % 100000 == 0:
        print(pwd, i, dig, pwd2)
    if dig.startswith("00000"):
        if len(pwd) < 8:
            pwd += dig[5]
        if dig[5] in "01234567":
            pos = int(dig[5])
            if pwd2[pos] == 0:
                found += 1
                pwd2[pos] = dig[6]
    i += 1

print(pwd)
print("".join(pwd2))
