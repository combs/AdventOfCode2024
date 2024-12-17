import networkx, numpy
import matplotlib.pyplot

grid_verbose, grid_lines = [], []

pos = (0, 0)
robot = []
commands = []

x, y = 0, 0 
curr_dir = 1
positions = {}

to_consider = []

available_directions = { 0: (-1, 0), 1: (0, 1), 2: (1, 0), 3: (0, -1) }

def get_allowed(pos):
    global available_directions
    allowed = [0, 0, 0, 0]
    positions = []
    
    for dirno, direction in available_directions.items():
        candidate = pos[0] + direction[0], pos[1] + direction[1]
        positions.append(candidate)
        if (0 < candidate[0] < grid.shape[0] - 1) and (0 < candidate[1] < grid.shape[1] - 1):
            if grid[candidate[0]][candidate[1]]==".":
                allowed[dirno] = 1

    print(allowed, positions)
    
    return allowed, positions

weights = {}

def pos_dir_label(pos, direction):
    return str(pos[0]) + "x" + str(pos[1]) + "_" + str(direction)
    
def consider_points(start, start_dir):
    global available_directions, end, weights, positions, to_consider
    print("begin consider_points", start, curr_dir)
    proceed = True
    
    turns = 0
    steps = 0 
    pos = start
    direction = start_dir
    start_label = pos_dir_label(start, direction)
    
        
    while proceed:
        grid_traversed[pos[0]][pos[1]] = "X"
        
        c_dir, c_pos = get_allowed(pos)
        count = sum(c_dir)
        if pos[0] == end[0] and pos[1] == end[1]:
            print("Reached end")
            cost_for_leg = (turns * 1000) + steps
            weight_label = pos_dir_label(start, start_dir) + "..." + pos_dir_label(pos, direction)
            positions[pos_dir_label(start, start_dir)] = (start[1] + 0.25 * available_directions[start_dir][1], start[0] + 0.25 * available_directions[start_dir][0])
            positions["end"] = positions[pos_dir_label(pos, direction)] = pos[1], pos[0]
           
            weights[weight_label] = (pos_dir_label(start, start_dir), pos_dir_label(pos, direction), cost_for_leg)
            weights["end-" + str(direction)] = (pos_dir_label(pos, direction), "end" , 0)
            proceed = False
            continue
            
        print(pos, ":", count, "directions allowed:", [c_pos[i] for i in range(4) if c_dir[i]])
        assert count > 0
        if count == 1:
            if c_dir[direction]:
                steps += 1
                pos = c_pos[direction]
            else:
                print("Reached dead end", pos)
                proceed = False
        elif count == 2:
            if not c_dir[direction]:
                print("We must turn", pos, "heading", direction, "exits", c_dir)
                turns += 1 # It has to be 90 degrees. No u-turns poss
                # direction = [ i for i in c_dir if i != direction ][0]
                if c_dir[(direction + 1) % 4]:
                    direction = (direction + 1) % 4
                elif c_dir[(direction + 3) % 4]:
                    direction = (direction + 3) % 4
                print("Turned to direction", direction)
            steps += 1
            pos = c_pos[direction]
            print("Stepped to", pos, "going", direction)
            
        elif count > 2:
            if steps == 0:
                pos = c_pos[start_dir]
                print("Taking first step out of intersection", pos, start_dir)
                steps += 1
                continue
                
            print("Reached an intersection")
            
            for this_dir, allowed in enumerate(c_dir):
                
                extra_turns = abs(this_dir - direction)
                extra_turn_costs = [ 0, 1000, 2000, 1000 ]
                print("turning from", direction, "to", this_dir, "costs", extra_turn_costs[extra_turns])
                end_label = str(pos) + "-" + str(this_dir)
                cost_for_leg = (turns * 1000) + steps + extra_turn_costs[extra_turns]
                weight_label = pos_dir_label(start, start_dir) + "..." + pos_dir_label(pos, this_dir)
                positions[pos_dir_label(start, start_dir)] = (start[1] + 0.25 * available_directions[start_dir][1], start[0] + 0.25 * available_directions[start_dir][0])
                positions[pos_dir_label(pos, this_dir)] = ( pos[1] + 0.25 * available_directions[this_dir][1], pos[0] + 0.25 * available_directions[this_dir][0])
                
                if weight_label not in weights:
                    weights[weight_label] = (pos_dir_label(start, start_dir), pos_dir_label(pos, this_dir), cost_for_leg)
                    if allowed:
                        print("Will consider edge", weight_label)
                        to_consider.append((pos, this_dir))
                    
                else:
                    print("Already considered edge", weight_label)
                    
                for other_dir, allowed in enumerate(c_dir):
                    if this_dir == other_dir:
                        continue
                    costs = [ 0, 1000, 2000, 1000 ]
                    cost = costs[abs(this_dir - other_dir)]
                    
                    label = pos_dir_label(pos, this_dir) + "..." + pos_dir_label(pos, other_dir)
                    weights[label] = pos_dir_label(pos, this_dir), pos_dir_label(pos, other_dir), cost
                    positions[label] =  (pos[1] + 0.25 * available_directions[other_dir][1], pos[0] + 0.25 * available_directions[other_dir][0])
                    positions[pos_dir_label(pos, other_dir)] =  (pos[1] + 0.25 * available_directions[other_dir][1], pos[0] + 0.25 * available_directions[other_dir][0])
                    
                    print("at the intersection", pos, "you could turn from", this_dir, "to", other_dir, "for", cost)
            proceed = False
                    
    print("end consider_points", start, start_dir)

def weight_function(node1, node2, edge):
    return edge.get('weight', 0)
    

with open("input", "r") as fh:
    for line in fh:
        if "#" in line:
            line_list = list(line.strip())
            if "S" in line:
                x = line_list.index("S")
                start = [y, x]
                line_list[x] = "."
            if "E" in line:
                x = line_list.index("E")
                end = [y, x]
                line_list[x] = "."
            grid_lines.append(line_list)
            grid_verbose.append(list(line.strip()))
        y += 1

grid = numpy.array(grid_lines)
grid_traversed = numpy.array(grid_verbose)

print(grid)
print(grid.shape)
directions, points = get_allowed(start)
start_connections = []

positions["start"] = (start[1], start[0])
for direction_num, allowed in enumerate(directions):
    if allowed:
        print("Starting point", start, direction_num)
        costs = [ 0, 1000, 2000, 1000 ]
        cost = costs[abs(direction_num - 1)]
        print("cost from east starting direction to", direction_num, "is", cost)
        weights["start-" + pos_dir_label(start, direction_num)] = ("start", pos_dir_label(start, direction_num), cost)
        to_consider.append((start, direction_num))
        
        positions[pos_dir_label(start, direction_num)] = (start[1] + 0.25 * available_directions[direction_num][1], start[0] + 0.25 * available_directions[direction_num][0])

while to_consider:
    consider_points(*to_consider.pop(0))
    
graph = networkx.Graph()
print(weights)

for label, val in weights.items():
    print(val)
    graph.add_edge(val[0], val[1], weight=val[2])

print(grid_traversed)
print(graph)
networkx.draw_networkx(graph, pos=positions)
# networkx.draw_networkx_labels(graph, )

matplotlib.pyplot.axis([0, grid.shape[1], grid.shape[0], 0])
path = networkx.dijkstra_path(graph, "start", "end", weight="weight")
print(path)
print(networkx.path_weight(graph, path, weight="weight")) 
for i in range(len(path) - 1):
    print("cost from", path[i], "to", path[i+1], "is", networkx.path_weight(graph, path[i:i+2], weight="weight"))
    
matplotlib.pyplot.show()


