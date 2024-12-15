import numpy

class Done(Exception):
    pass
    

def get_involved_blocks(from_pos, transform):
    global grid
    
    blocks_to_check =[ (from_pos[0] + transform[0], from_pos[1] + transform[1])]
    print("starting blocks_to_check", blocks_to_check)
    blocks = [from_pos]
    x_only = transform[1] != 0 
    allowed = True
    blocks_checked = []
    
    while blocks_to_check:
        block_pos = blocks_to_check.pop(0)
        print("block_pos", block_pos, "blocks", blocks)
        if block_pos[0] in (0, grid.shape[0] - 1) or block_pos[1] in (0, grid.shape[1] - 1):
            allowed = False
            break
            
        block = grid[block_pos[0]][block_pos[1]]
        
        if block_pos in blocks_checked:
            continue
            
        blocks_checked.append(block_pos)
        

        if block=="#":
                allowed = False
                break
                
        if x_only:
            if block in ("[", "]"):
                blocks_to_check.append((block_pos[0] + transform[0], block_pos[1] + transform[1]))
                blocks.append(block_pos)
                               
            # elif block==".":
                    # all good but we should run out the other checks
                    # pass
        else:
            if block=="[":
                blocks_to_check.insert(0, (block_pos[0], block_pos[1] + 1))
                blocks_to_check.append((block_pos[0] + transform[0], block_pos[1] + transform[1]))
                blocks.append(block_pos)                
            elif block=="]":
                blocks_to_check.insert(0, (block_pos[0], block_pos[1] - 1))
                blocks_to_check.append((block_pos[0] + transform[0], block_pos[1] + transform[1]))
                blocks.append(block_pos)                
        print("blocks_to_check", blocks_to_check)
    print("involved blocks for block", from_pos, "transform", transform, ":", blocks, allowed)        
    return (blocks, allowed)
        
grid_lines = []

pos = (0, 0)
robot = []
commands = []
lookups = {"#": "##", "O": "[]", ".": "..", "@": "@." } 
x, y = 0, 0 
with open("input", "r") as fh:
    for line in fh:
        if "#" in line:
            l = list(line.strip())
            doubled = list("".join([lookups[i] for i in l]))
            grid_lines.append(doubled)
            if "@" in line:
                pos = [y, line.index("@") * 2]
                
        elif "<" in line:
            commands.extend(list(line.strip()))
        y += 1
        

grid = numpy.array(grid_lines)
transforms = { "<" : (0, -1), ">" : (0, 1), "^" : (-1, 0), "v" : (1, 0) } 
numpy.set_printoptions(edgeitems=1000, linewidth=100000, formatter=dict(float=lambda x: "%.3g" % x))
print(grid)

for command in commands:
    transform = transforms[command]
    from_pos = pos
    
    blocks, allowed = get_involved_blocks(from_pos, transform)
    
    if allowed:
        altered = []
        for block in reversed(blocks):
            to = (block[0] + transform[0], block[1] + transform[1])
            print("relocate", block, grid[block], "to", to, grid[to])

            grid[to[0]][to[1]] = grid[block[0]][block[1]]
            altered.append(to)
        
        for block in blocks:
            if block not in altered:
                grid[block[0]][block[1]] = "."
                
        prev_pos = pos
        pos = (from_pos[0] + transform[0], from_pos[1] + transform[1])
        print(command, "robot pos changed", prev_pos, pos)

    
    else:
        print(command, "bonk")
        
    print(grid)
    

score = 0

for y in range(grid.shape[0]):
    for x in range(grid.shape[1]):
        if grid[y][x] == "[":
            nx, ny = x, y
            
#            if y > (grid.shape[0]/2):
#                ny = grid.shape[0] - y - 1
#                
#            if x > (grid.shape[1]/2):
#                nx = grid.shape[1] - x - 2
            
            this_score = ((100*ny) + nx)
            print("box at", y, x, "rewritten to", ny, nx, "gives", this_score)
            score += this_score

print("overall score", score)

    
    