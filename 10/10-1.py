import numpy

global_score = 0
grid_lines = []

def is_legal_position(position):
    global grid
    max_x, max_y = grid.shape
    return (0 <= position[0] < max_x) and (0 <= position[1] < max_y)
    
def stroll(position, value):
    global grid
    transforms = ((-1, 0), (1, 0), (0, -1), (0, 1))
    mountains = []
    if grid[tuple(position)]==value:
        if value==9:
            # ~ print("mountain found", position) 
            return [position]
        for xform in transforms:
            candidate = (position[0] + xform[0], position[1] + xform[1])
            if is_legal_position(candidate):
                mountains += stroll(candidate, value + 1)
    return mountains
    
with open("input", "r") as fh:
    for line in fh.readlines():
        if len(line.strip()):
            grid_lines.append([int(i) for i in list(line.strip())])

grid = numpy.array(grid_lines)
trailheads = numpy.transpose((grid==0).nonzero())

for trailhead in trailheads:
    trailhead_results = set(stroll(trailhead, 0))
    score = len(trailhead_results)
    
    print("trailhead", trailhead, "has mountains", trailhead_results, "score", score)
    
    global_score += score

print(global_score)
