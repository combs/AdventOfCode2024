import numpy

def lines_to_2d_array(lines):
    # width = len(lines[0])
    # height = len(lines)

    listified = [ list(line) for line in lines ]
    return numpy.array(listified)

def get_letter(grid, x, y):
    height, width = grid.shape

    if 0 <= x < width:
        if 0 <= y < height:
            return grid[y][x]
                
    return None

with open("input", "r") as fh:
    temp_lines = fh.readlines()
    lines = [ line.strip() for line in temp_lines ]

grid = lines_to_2d_array(lines)
height, width = grid.shape

score = 0

for y in range(height):
    for x in range(width):
        if get_letter(grid, y, x) == "A":
            print("A found at", (y, x))
            
            nw_to_se = ( get_letter(grid, y + 1, x + 1), get_letter(grid, y - 1, x - 1) )
            ne_to_sw = ( get_letter(grid, y - 1, x + 1), get_letter(grid, y + 1, x - 1) )
            
            acceptables = (("M", "S"), ("S", "M"))
            if nw_to_se in acceptables and ne_to_sw in acceptables:
                score += 1
            
print(score)
                
                     

