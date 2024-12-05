
all_values = []
orders = []
occur_befores = []

with open("input", "r") as fh:
    for line in fh.readlines():
        if "," in line:
            orders.append([int(i) for i in line.split(",")])
        elif "|" in line:
            goodies = tuple([ int(i) for i in line.split("|")])
            occur_befores.append(goodies)
            all_values.extend(goodies)

print(all_values)
score = 0

for order in orders:
    indices = {}
    for val in all_values:
        try:
            indices[val] = order.index(val)
        except ValueError:
            continue
    
    print(order)
    print(indices)
    
    goodness = True
    
    for rule in occur_befores:
        needle = rule[0]
        must_occur_before = rule[1]
        
        if (needle not in indices) or (must_occur_before not in indices):
            print("This rule does not apply:", rule)
            continue
        
        if indices[needle] < indices[must_occur_before]:
            print("Rule passed:", rule)
        else:
            print("DQed for rule", rule)
            goodness = False
    
    if goodness:
        middle = len(order) // 2  # 5 -> 2.5 -> 2 ; list[2] = middle
        score += order[middle]
            
print("Score is", score)
