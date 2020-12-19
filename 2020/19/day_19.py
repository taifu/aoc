def parse(data):
    raw_rules, messages = list(map(lambda part: part.splitlines(), data.split('\n\n')))
    rules = {}
    chars = set()
    for raw_rule in raw_rules:
        rule, parts = raw_rule.split(": ")
        if parts[0] == '"':
            char = parts[1][-1]
            rules[int(rule)] = char
            chars.add(char)
        else:
            rules[int(rule)] = [[int(r) for r in part.split(' ')] for part in parts.split(' | ')]
    return rules, messages, chars


def find_root(rules):
    # In realtà questa è inutile (lo dice già il testo che la regola princilare è la '0'
    keys = set(rules.keys())
    for rule, matches in rules.items():
        for match in matches:
            for part in match:
                if part in keys:
                    keys.remove(part)
    assert len(keys) == 1
    root = keys.pop()
    assert len(rules[root]) == 1
    return root


def check_valid(message, rules, chars, matching):
    part = matching.pop(0)
    if part in chars:
        if message[0] == part:
            if len(message) == 1:
                # Deve combaciare alla perfezione senza che rimanga fuori nulla
                return len(matching) == 0
            elif len(matching) == 0:
                return False
            else:
                return check_valid(message[1:], rules, chars, matching)
    else:
        for rule in rules[part]:
            if check_valid(message, rules, chars, list(rule) + matching):
                return True
    return False


def solve(data, substitute=False):
    rules, messages, chars = parse(data)
    if substitute:
        rules.update(substitute)
    root_rule = rules.pop(find_root(rules))[0]
    return sum(1 if check_valid(message, rules, chars, root_rule[:]) else 0 for message in messages)


if __name__ == "__main__":
    data = open("input.txt").read()
    print(solve(data))
    print(solve(data, {8: [[42], [42, 8]], 11: [[42, 31], [42, 11, 31]]}))
