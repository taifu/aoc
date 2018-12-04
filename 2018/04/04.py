from collections import defaultdict

guards = defaultdict(list)
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
            guards[guard].append(minutes)
        guard, shift = action[1:], []
    elif action == "asleep":
        sleep = int(time[3:])
    elif action == "up":
        shift.append((sleep, int(time[3:])))
    else:
        raise Exception(action)

sleepy_guard, minutes = None, 0
for guard, intervals in guards.items():
    total = sum(intervals)
    if total > minutes:
        sleepy_guard, minutes = guard, total

minutes = defaultdict(lambda: defaultdict(int))
for guard, shifts in all_shifts.items():
    for shift in shifts:
        for interval in shift:
            for minute in range(interval[0], interval[1]):
                minutes[guard][minute] += 1

most_minute, most_how_much = 0, 0
for minute, how_much in minutes[sleepy_guard].items():
    if how_much > most_how_much:
        most_minute, most_how_much = minute, how_much

print(int(sleepy_guard) * most_minute)

most_guard, most_minute, most_how_much = 0, 0, 0
for guard, guard_minutes in minutes.items():
    for minute, how_much in guard_minutes.items():
        if how_much > most_how_much:
            most_guard, most_minute, most_how_much = guard, minute, how_much

print(int(most_guard) * most_minute)
