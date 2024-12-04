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

orthos = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
score = 0

for y in range(height):
    for x in range(width):
        if get_letter(grid, y, x) == "X":
            print("X found at", (y, x))
            
            for transform in orthos:
                print("trying transform", transform)
                
                m = (y + transform[1], x + transform[0])
                a = (y + transform[1] * 2, x + transform[0] * 2)
                s = (y + transform[1] * 3, x + transform[0] * 3)
                
                if get_letter(grid, *m) != "M":
                    print("didn't find M at", m, get_letter(grid, *m))
                    continue
                print("found M at", m)
                if get_letter(grid, *a) != "A":
                    print("didn't find A at", a, get_letter(grid, *a))
                    continue
                print("found A at", a)
                if get_letter(grid, *s) != "S":
                    print("didn't find S at", s, get_letter(grid, *s))
                    continue
                print("XMAS found at", (y, x), "using transform", transform) 
                score += 1

print(score)
                
                     

