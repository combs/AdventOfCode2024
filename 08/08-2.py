import itertools, numpy, string

frequencies = {}
max_x, max_y = 0, 0 
resonances = []

with open("input", "r") as fh:
    y = 0
    for line in fh.readlines():
        x = 0 
        for letter in line.strip():
            if letter in string.ascii_letters or letter in string.digits:
                frequencies[letter] = frequencies.get(letter, [])
                frequencies[letter].append((x, y))
            max_x = max(x, max_x)
            x += 1 
        max_y = max(y, max_y)
        y += 1 
        
for letter, antennae in frequencies.items():
    combos = itertools.permutations(antennae, 2)
    
    for combo in combos:
        delta = combo[0][0] - combo[1][0], combo[0][1] - combo[1][1]
        candidate = combo[1]
        while True:
            projection = (candidate[0] + delta[0], candidate[1] + delta[1])
            if not (0 <= projection[0] <= max_x):
                break
            if not (0 <= projection[1] <= max_y):
                break
            print(letter, "resonance accepted for", combo, ":", projection)
            resonances.append(projection)
            candidate = projection
        
resonances = set(resonances)
print(len(resonances))
