import functools

import time

@functools.cache
def dive_in(stone, depth, max_depth=75): 
    
    # print(depth, line)
    score = 0
    
    if depth==max_depth:
        return 1
            
    new_line = []
    
    strone = str(stone)
    length = len(strone)
    
    if stone==0:
        new_line.append(1)
    elif length % 2 == 0:
        new_line.extend([int(strone[0:length//2]), int(strone[length//2:])])
    else:
        new_line.append(stone*2024)

    for index, stone in enumerate(new_line):
        # print("diving in, index", index, "to depth", depth+1)
        score += dive_in(stone, depth+1)
    
    if depth < 10:
        print("depth", depth, "resolved", score)
    return score

with open("input", "r") as fh_in:
    data_in = fh_in.readlines()[0].strip()

print("data in", data_in)
score = 0 
for i in data_in.split(" "):
    score += dive_in(int(i), 0)

print(score)
