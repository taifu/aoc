from collections import defaultdict


def parse(data):
    step, rules = 0, {}
    your_ticket, nearby_tickets = [], []
    for line in data.strip().split('\n'):
        if not line:
            step += 1
            continue
        if step == 0:
            parts = line.split(': ')
            rules[parts[0]] = [int(p) for p in parts[1].replace(' or ', '-').split('-')]
        elif line[0].isdigit():
            values = [int(p) for p in line.split(',')]
            if step == 1:
                your_ticket = values
            else:
                nearby_tickets.append(values)
    return rules, your_ticket, nearby_tickets


def solve(data, second_part=True):
    rules, your_ticket, nearby_tickets = parse(data)
    scanning_rate, all_tickets_positions = 0, {}
    for ticket in nearby_tickets:
        valid_ticket, this_ticket_positions = True, defaultdict(set)
        for position, value in enumerate(ticket):
            valid = False
            for rule, (min1, max1, min2, max2) in rules.items():
                if not (value < min1 or max1 < value < min2 or max2 < value):
                    valid = True
                    this_ticket_positions[rule].add(position)
            if not valid:
                scanning_rate += value
                valid_ticket = False
        if valid_ticket:
            for rule, positions in this_ticket_positions.items():
                try:
                    all_tickets_positions[rule] = all_tickets_positions[rule].intersection(positions)
                except KeyError:
                    all_tickets_positions[rule] = positions
    your_ticket_id, right_positions = 1, {}
    if second_part:
        while all_tickets_positions:
            for rule, positions in all_tickets_positions.copy().items():
                if len(positions) == 1:
                    right_position = positions.pop()
                    right_positions[rule] = right_position
                    del all_tickets_positions[rule]
                    for rule, positions in all_tickets_positions.items():
                        positions.remove(right_position)
        for rule, position in right_positions.items():
            if rule.startswith('departure'):
                your_ticket_id *= your_ticket[position]
    return scanning_rate, your_ticket_id, right_positions


if __name__ == "__main__":
    data = open("input.txt").read()
    part1, part2, _ = solve(data)
    print(part1)
    print(part2)
