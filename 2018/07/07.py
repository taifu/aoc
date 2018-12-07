from collections import defaultdict


def read_tasks(data, load):
    tasks = set()
    deps = defaultdict(list)
    for k, v in [(p.split(" ")[1], p.split(" ")[7]) for p in data.split("\n") if p]:
        deps[v].append(k)
        tasks.add(k)
        tasks.add(v)
    tasks = [[task, ord(task) - ord('A') + 1 + load] for task in sorted(tasks)]
    return deps, tasks


def update_deps(deps, done):
    for task in done:
        for k, v in deps.copy().items():
            if task in v:
                deps[k].remove(task)
                if len(deps[k]) == 0:
                    del deps[k]


workers = 5
load = 60
data = open("input.txt").read()

# workers = 2
# load = 0
# data = """Step C must be finished before step A can begin.
# Step C must be finished before step F can begin.
# Step A must be finished before step B can begin.
# Step A must be finished before step D can begin.
# Step B must be finished before step E can begin.
# Step D must be finished before step E can begin.
# Step F must be finished before step E can begin."""

# Star 1
deps, tasks = read_tasks(data, load)
order = []
while deps:
    done = None
    for task, dur in tasks:
        if task not in deps:
            done = task
            tasks.remove([task, dur])
            break
    order.append(done)
    update_deps(deps, done)

order.append(tasks.pop()[0])
print("".join(order))

# Star 1
deps, tasks = read_tasks(data, load)
doing = {}
tick = 0
while deps or tasks or doing:
    for task, dur in tasks[:]:
        if task not in deps and task not in doing:
            if len(doing) < workers:
                doing[task] = dur
                tasks.remove([task, dur])
    tick += 1
    for to_do, dur in sorted(doing.items()):
        doing[to_do] -= 1
        if doing[to_do] == 0:
            update_deps(deps, [to_do])
            del doing[to_do]
print(tick)
