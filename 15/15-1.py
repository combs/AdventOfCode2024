import numpy


def seek_run(from_pos, transform):
    global grid
    to_pos = (from_pos[0] + transform[0], from_pos[1] + transform[1]) 
    length = 1
    if grid[to_pos] == "#":
        return (from_pos, 0)
    try:
        print("checking", to_pos, grid[to_pos], grid[to_pos]=="O")
        while grid[to_pos] == "O":
            to_pos = (to_pos[0] + transform[0], to_pos[1] + transform[1]) 
            length += 1
            if to_pos[0] in (0, grid.shape[0] - 1) or to_pos[1] in (0, grid.shape[1] - 1) or grid[to_pos]=="#":
                print(to_pos, "has overrun the grid")
                
                raise IndexError
            print("ok to proceed", to_pos)
            
    except IndexError:
        # we have overrun the grid
        return (from_pos, 0)
    
    return (to_pos, length)
    
grid_lines = []

pos = (0, 0)
robot = []
commands = []

x, y = 0, 0 
with open("input", "r") as fh:
    for line in fh:
        if "#" in line:
            grid_lines.append(list(line.strip()))
            if "@" in line:
                pos = [y, line.index("@")]
                
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
    to_pos, length = seek_run(from_pos, transform)
    if length > 0:
        for i in range(length):
            to = (to_pos[0] - (transform[0] * (i)), to_pos[1] - ( transform[1] * (i)))
            fr = (to_pos[0] - (transform[0] * (i + 1)), to_pos[1] - ( transform[1] * (i + 1)))
            print("relocate", fr, grid[fr], "to", to, grid[to])
            grid[to[0]][to[1]] = grid[fr[0]][fr[1]]
        grid[from_pos[0]][from_pos[1]] = "."
        print(command, "moved", length, "squares from", from_pos, "to", to_pos)
        prev_pos = pos
        pos = (from_pos[0] + transform[0], from_pos[1] + transform[1])
        print("robot pos changed", prev_pos, pos)
    else:
        print(command, "bonk")
    
    print(grid)
    

score = 0

for y in range(grid.shape[0]):
    for x in range(grid.shape[1]):
        if grid[y][x]=="O":
            this_score = ((100*y) + x)
            print("box at", y, x, "gives", this_score)
            score += this_score

print("overall score", score)

    
    