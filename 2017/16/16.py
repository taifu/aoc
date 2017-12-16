instructions = open("input").read().strip().split(",")

ALPHABET = [chr(ord('a') + n) for n in range(16)]
letters = ALPHABET[:]


def run(instructions, letters):
    for instruction in instructions:
        if instruction[0] == 's':
            pos = int(instruction[1:])
            letters[:] = letters[-pos:] + letters[:-pos]
        elif instruction[0] == 'x':
            pos1, pos2 = [int(p) for p in instruction[1:].split("/")]
            letters[pos1], letters[pos2] = letters[pos2], letters[pos1]
        elif instruction[0] == 'p':
            pos1, pos2 = [letters.index(p) for p in instruction[1:].split("/")]
            letters[pos1], letters[pos2] = letters[pos2], letters[pos1]
    return letters

n = 0
while True:
    run(instructions, letters)
    if n == 0:
        print("".join(letters))
    n += 1
    if letters == ALPHABET:
        break

for n in range(1000000000 % n):
    run(instructions, letters)
print("".join(letters))
