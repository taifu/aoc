def spinlock(n, step):
    buffer = [0]
    pos = 0
    last = None
    for cont in range(n):
        pos = (pos + step) % len(buffer) + 1
        buffer.insert(pos, cont + 1)
    return buffer[pos + 1]


def spinlock_0(n, step):
    pos = 0
    buffer_1 = None
    len_buffer = 1
    for cont in range(n):
        pos = (pos + step) % len_buffer + 1
        len_buffer += 1
        if pos == 1:
            buffer_1 = cont + 1
    return buffer_1


print(spinlock(2017, 354))
print(spinlock_0(50000000, 354))
