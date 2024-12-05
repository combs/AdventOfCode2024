
def cache_indices(order):
    global all_values
    indices = {}
    for val in all_values:
        try:
            indices[val] = order.index(val)
        except ValueError:
            continue
    return indices
    
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
    indices = cache_indices(order)
    
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
    
    if not goodness:
        new_order = []
        for new_val in order:
            earliest_index = 99999999
            indices = cache_indices(new_order)
            for rule in occur_befores:
                if new_val==rule[0]:
                    if rule[1] not in indices:
                        print("Rule does not apply", rule)
                        continue
                    index_applies = indices[rule[1]]
                    if index_applies != None:
                        earliest_index = min(earliest_index, index_applies)
            if earliest_index != 99999999:
                new_order.insert(earliest_index, new_val)
            else:
                new_order.append(new_val)
                    
        middle = len(new_order) // 2  # 5 -> 2.5 -> 2 ; list[2] = middle
        score += new_order[middle]
                    

            
print("Score is", score)
