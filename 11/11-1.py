def do_cycle(line):
    new_line = []
    
    for stone in line:
        strone = str(stone)
        length = len(strone)
        
        if stone==0:
            new_line.append(1)
        elif length % 2 == 0:
            new_line.extend([int(strone[0:length//2]), int(strone[length//2:])])
        else:
            new_line.append(stone*2024)
    
    return new_line
    

with open("input", "r") as fh:
    line = fh.readlines()[0]
    stones =  [ int(i) for i in line.strip().split(" ")]
print(stones)


for cycle in range(25):
    stones = do_cycle(stones)
    # ~ print(cycle, stones)

print(len(stones))
            
