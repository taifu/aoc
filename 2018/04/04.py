from collections import defaultdict

all_shifts, shift, guard = defaultdict(list), None, None

for line in sorted(open("input.txt").readlines()):
    # Format:
    # [1518-08-12 23:58] Guard #2833 begins shift
    # [1518-07-31 00:35] falls asleep
    # [1518-03-07 00:57] wakes up
    parts = line.strip().lower().split(" ")
    day, time, action = parts[0][1:], parts[1][:-1], parts[3]
    if action[0] == "#":
        if shift is not None:
            all_shifts[guard].append(shift)
            minutes = sum((y - x) for x, y in shift)
        guard, shift = action[1:], []
    elif action == "asleep":
        sleep = int(time[3:])
    elif action == "up":
        shift.append((sleep, int(time[3:])))
    else:
        raise Exception(action)

minutes = defaultdict(lambda: defaultdict(int))
sleepy_guard1, most_minutes1, best_minute1 = None, 0, 0
sleepy_guard2, most_minutes2, best_minute2 = None, 0, 0

for guard, shifts in all_shifts.items():
    total_minutes = 0
    for shift in shifts:
        total_minutes += sum((y - x) for x, y in shift)
        for interval in shift:
            for minute in range(interval[0], interval[1]):
                minutes[guard][minute] += 1
    # Strategy 1
    if total_minutes > most_minutes1:
        sleepy_guard1, most_minutes1 = guard, total_minutes
        best_minute1 = max({v: k for k, v in minutes[guard].items()}.items())[1]
    # Strategy 2
    for minute, how_much in minutes[guard].items():
        if how_much > most_minutes2:
            sleepy_guard2, most_minutes2, best_minute2 = guard, how_much, minute

print(int(sleepy_guard1) * best_minute1)
print(int(sleepy_guard2) * best_minute2)
