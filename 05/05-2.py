
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

score = 0

for order in orders:
    indices = cache_indices(order)
    
    goodness = True
    
    # First, we must scan to see which ones are correct
    
    for rule in occur_befores:
        needle = rule[0]
        must_occur_before = rule[1]
        
        if (needle not in indices) or (must_occur_before not in indices):
            continue # Rule does not apply
        
        if indices[needle] >= indices[must_occur_before]:
            goodness = False # DQed by this rule 
    
    if not goodness:
        new_order = [] # Instead of reordering, build the new order from scratch
        
        for new_val in order: # Get each number. "order" here is now a misnomer

            earliest_index = 99999999 # for later min() convenience
            indices = cache_indices(new_order) # not necessarily faster anymore

            # Let's go through each rule. For the "must occur before X" value,
            # let's check whether X is actually in the new order yet. 
            
            # If so, grab its index in the list, as an "insert before" placement
            
            # Iterate through all rules to get the earliest "insert before"
            
            # Then insert the value before the earliest "insert before"
            
            for rule in occur_befores: 
                if new_val==rule[0]: # Does this rule apply to this value?
                    if rule[1] not in indices:
                        continue 
                        # Rule's "must_go_before" not present yet, don't care
                        # MYSTERY: could this introduce a bug if the value is 
                        # introduced later? 
                    must_occur_before = indices[rule[1]]
                    earliest_index = min(earliest_index, must_occur_before)
                        
            if earliest_index != 99999999:
                new_order.insert(earliest_index, new_val)
            else: # If no rules apply, we don't care, throw it on the end.
                new_order.append(new_val)
                    
        middle = len(new_order) // 2  # 5 -> 2.5 -> 2 ; list[2] = middle
        score += new_order[middle]
                    
print("Score is", score)
