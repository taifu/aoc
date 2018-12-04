import copy

def getHash(elevator, floors):
    return str(elevator) + str([(len(floors[i]), sum(x < 0 for x in floors[i])) for i in range(4)])

def move(elevator, floors, direction, from_index, to_index):
    if from_index != None and to_index != None:
        floors[elevator + direction].insert(to_index, floors[elevator].pop(from_index))

def exploreState(req, elevator, floors, states, queue, direction, moves, index1, index2 = None):
    if direction * elevator < req:
        move(elevator, floors, direction, index2, 0)
        move(elevator, floors, direction, index1, 0)

        next_hash = getHash(elevator + direction, floors)

        if next_hash not in states and floors[elevator + direction] and isValidState(floors[elevator + direction]) and isValidState(floors[elevator]):
            queue.append([elevator + direction, copy.deepcopy(floors), moves + 1, next_hash])

        move(elevator + direction, floors, -direction, 0, index1)
        move(elevator + direction, floors, -direction, 0, index2)

def isValidState(floor):
    hasGen   = sum(x < 0 for x in floor)
    unpaired = sum(x > 0 and -x not in floor for x in floor)

    return not (hasGen and unpaired)

def explore(start):
    end_hash = getHash(3, [[], [], [], sum(start, [])])
    states   = set()
    queue    = []

    queue.append([0, start, 0, getHash(0, start)])

    while True:
        elevator, floors, moves, cur_hash = queue.pop(0)

        if cur_hash not in states:
            states.add(cur_hash)

            if cur_hash == end_hash:
                print("moves:", moves)
                break

            for index1 in range(len(floors[elevator])):
                for index2 in range(index1 + 1, len(floors[elevator])):
                    exploreState(3, elevator, floors, states, queue, 1, moves, index1, index2)
                    exploreState(0, elevator, floors, states, queue, -1, moves, index1, index2)

                exploreState(3, elevator, floors, states, queue, 1, moves, index1)
                exploreState(0, elevator, floors, states, queue, -1, moves, index1)

explore([[-1, 1, -2, -3], [2, 3], [-4, 4, -5, 5], []])
explore([[-1, 1, -2, -3, -6, 6, -7, 7], [2, 3], [-4, 4, -5, 5], []])
