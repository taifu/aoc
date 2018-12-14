def after(recipes, pe1, pe2, after=None, search=None):
    if search is not None:
        search = [int(n) for n in str(search)]
        l_search = len(search)
    while True:
        new = recipes[pe1] + recipes[pe2]
        if new > 9:
            recipes.append(new // 10)
        recipes.append(new % 10)
        pe1 = (pe1 + recipes[pe1] + 1) % len(recipes)
        pe2 = (pe2 + recipes[pe2] + 1) % len(recipes)
        if after is not None:
            if len(recipes) > after + 10:
                return("".join(str(r) for r in recipes[after:after + 10]))
        else:
            if recipes[-l_search:] == search:
                return(len(recipes) - l_search)
            if new > 9 and recipes[-l_search - 1:-1] == search:
                return(len(recipes) - l_search - 1)


print(after([3, 7], 0, 1, after=380621))
print(after([3, 7], 0, 1, search=380621))
