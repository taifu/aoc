from collections import defaultdict


def parse(data):
    ingredients = defaultdict(set)
    contained = defaultdict(set)
    ingredients_list = []
    for line in data.strip().split('\n'):
        p1, p2 = line.split("(contains ")
        ings, alls = p1.strip().split(" "), p2[:-1].split(", ")
        for ing in ings:
            ingredients_list.append(ing)
        for allergen in alls:
            first = allergen not in contained
            for ing in ings:
                ingredients[ing].add(allergen)
            if first:
                contained[allergen] = set(ings)
            else:
                contained[allergen] = contained[allergen].intersection(set(ings))
    return ingredients_list, ingredients, contained


def solve(data, step=1):
    ingredients_list, ingredients, contained = parse(data)
    safes = set(ingredients.keys())
    for allergen, ings in contained.items():
        for ing in ings:
            try:
                safes.remove(ing)
            except KeyError:
                pass
    if step == 1:
        return sum(ingredients_list.count(safe) for safe in safes)
    dangerous = {}
    while contained:
        for allergen, contained_into in contained.items():
            if len(contained_into) == 1:
                dangerous[allergen] = contained_into.pop()
                contained.pop(allergen)
                for contained_into in contained.values():
                    if dangerous[allergen] in contained_into:
                        contained_into.remove(dangerous[allergen])
                break
    return ",".join(k for v, k in sorted(dangerous.items()))


if __name__ == "__main__":
    data = open("input.txt").read()
    print(solve(data))
    print(solve(data, step=2))
