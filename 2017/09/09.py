import re

data = open("input").read().strip()

data = re.sub("!.", "", data)
garbage = re.findall("<[^>]*>", data)
data = re.sub("<[^>]*>", "", data)
data = re.sub(",", "", data)

tot = 0
value = 0
for p in data:
    if p == "{":
        value += 1
    elif p == "}":
        tot += value
        value -= 1

print(tot)
print(sum(len(l) - 2 for l in garbage))
