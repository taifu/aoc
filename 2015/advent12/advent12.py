import json

def deep_sum(struct, skip_red=False):
    tot = 0
    if isinstance(struct, unicode):
        pass
    elif isinstance(struct, int):
        tot = struct
    elif isinstance(struct, dict):
        if not skip_red or not "red" in struct.values():
            for k, v in struct.items():
                if isinstance(v, int):
                    tot += v
                else:
                    tot += deep_sum(v, skip_red)
    elif isinstance(struct, tuple) or isinstance(struct, list):
        for v in struct:
            tot += deep_sum(v, skip_red)
    else:
        print("Boh", struct)

    return tot

if __name__ == "__main__":
    import sys
    struct = json.loads(file(sys.argv[1]).read())
    print(deep_sum(struct))
    print(deep_sum(struct, True))
