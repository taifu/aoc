from collections import defaultdict

data = open("input.txt").read()

data = """Step C must be finished before step A can begin.
Step C must be finished before step F can begin.
Step A must be finished before step B can begin.
Step A must be finished before step D can begin.
Step B must be finished before step E can begin.
Step D must be finished before step E can begin.
Step F must be finished before step E can begin."""

raw_tasks = [(p.split(" ")[1], p.split(" ")[7]) for p in data.split("\n") if p]

deps = defaultdict(list)
tasks = set()

for k, v in raw_tasks:
    deps[v].append(k)
    tasks.add(k)
    tasks.add(v)

tasks = sorted(tasks)

order = []

while deps:
    done = None
    for task in tasks:
        if task not in deps:
            done = task
            tasks.remove(task)
            break
    order.append(done)
    for task in done:
        for k, v in deps.items()[:]:
            if task in v:
                deps[k].remove(task)
                if len(deps[k]) == 0:
                    del deps[k]

order.append(tasks.pop())
print("".join(order))

