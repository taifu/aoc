import re

ABBA = re.compile(r"([a-z])([a-z])\2\1")
ABA = re.compile(r"(?=([a-z])([a-z])\1)")

tot_tls = tot_ssl = 0

for net in open("input").readlines():
    parts = net.strip().replace("]", "[").split("[")
    outside = " ".join([part for i, part in enumerate(parts) if i % 2 == 0])
    inside = " ".join([part for i, part in enumerate(parts) if i % 2 == 1])
    abba = [f for f in ABBA.findall(outside) if len(set(f)) == 2]
    abba_inside = [f for f in ABBA.findall(inside) if len(set(f)) == 2]
    aba = [m.groups() for m in ABA.finditer(outside) if len(set(m.groups())) == 2]
    if abba and not abba_inside:
        tot_tls += 1
    if aba:
        for c1, c2 in aba:
            if re.findall("{b}{a}{b}".format(a=c1, b=c2), inside):
                tot_ssl += 1
                break

print(tot_tls)
print(tot_ssl)
