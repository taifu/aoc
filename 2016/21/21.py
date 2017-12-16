def scramble(password, instructions, unscramble=False):
    letters = list(password)
    for instruction in instructions:
        # Invariant
        if instruction[0] == "swap":
            if instruction[1] == "position":
                pos1, pos2 = int(instruction[2]), int(instruction[5])
                letters[pos1], letters[pos2] = letters[pos2], letters[pos1]
            else:
                pos1, pos2 = letters.index(instruction[2]), letters.index(instruction[5])
                letters[pos1], letters[pos2] = letters[pos2], letters[pos1]
        # Need unscramble
        elif instruction[0] == "rotate":
            if instruction[1] == "based":
                if unscramble:
                    cont = 1
                    while True:
                        letters = letters[1:] + letters[:1]
                        pos = letters.index(instruction[6])
                        if cont == pos + 1 + (0 if pos < 4 else 1):
                            break
                        cont += 1
                else:
                    times = letters.index(instruction[6])
                    for i in range(times + 1 + (0 if times < 4 else 1)):
                        letters = letters[-1:] + letters[:-1]
            else:
                times = int(instruction[2])
                if (instruction[1] == "right" and not unscramble) or (instruction[1] == "left" and unscramble):
                    for i in range(times):
                        letters = letters[-1:] + letters[:-1]
                else:
                    for i in range(times):
                        letters = letters[1:] + letters[:1]
        # Need unscramble
        elif instruction[0] == "move":
            pos1, pos2 = int(instruction[2]), int(instruction[5])
            if unscramble:
                pos2, pos1 = pos1, pos2
            letter = letters.pop(pos1)
            letters.insert(pos2, letter)
        # Invariant
        elif instruction[0] == "reverse":
            pos1, pos2 = int(instruction[2]), int(instruction[4])
            letters[pos1:pos2 + 1] = letters[pos2:None if pos1 == 0 else pos1 - 1:-1]
        else:
            raise Exception("Not managed {}".format(instruction))

    return "".join(letters)


instructions = [l.strip().split() for l in open("input").readlines()]

print(scramble("abcdefgh", instructions))
print(scramble("fbgdceah", instructions[::-1], True))
