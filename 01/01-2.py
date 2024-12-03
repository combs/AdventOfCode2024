
lefts = []
rights = [] 

with open("input", "r") as fh:
    for line in fh.readlines():
        (left, right) = line.strip().split("   ")
        lefts.append(int(left))
        rights.append(int(right))

lefts = sorted(lefts)
rights = sorted(rights)

tally = 0
for (i, left) in enumerate(lefts):
    count = rights.count(left)
    tally += left * count
    
print(tally)

