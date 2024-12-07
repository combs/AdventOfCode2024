
import numpy
from tqdm import tqdm

class EscapeException(ValueError):
    pass

class InfinityLoopException(ValueError):
    pass
        
class Turtle(object):
    
    def __init__(self, *args, **kwargs):
        self.direction = kwargs.get("direction", 0)
        self.fast_forward = kwargs.get("fast_forward", False)
        self.grid = kwargs.get("grid", numpy.zeros((10,10), dtype=str).fill("."))
        self.position = kwargs.get("position", [4, 5])
        self.log = []

    def count_moves(self):
        return (self.grid == "X").sum()
        
    def get_next_position(self):
        next_pos = self.position.copy()
        if self.direction==0:
            next_pos[0] -= 1
        elif self.direction==1:
            next_pos[1] += 1
        elif self.direction==2:
            next_pos[0] += 1
        elif self.direction==3:
            next_pos[1] -= 1
            
        if (next_pos[0] < 0) or (next_pos[1] < 0) or (next_pos[0] >= self.grid.shape[0]) or (next_pos[1] >= self.grid.shape[1]):
            raise EscapeException
        return next_pos
                
    def move(self):
        ff = self.fast_forward
        
        next_position = self.get_next_position()
        # print(self.position, self.direction, next_position, self.grid.shape)
        
        # self.grid[self.position[0], self.position[1]] = "X"
        if not ff:
            self.grid[self.position[0], self.position[1]] = "X"
            while self.grid[next_position[0], next_position[1]] == "#":
                self.direction = (self.direction + 1) % 4
                next_position = self.get_next_position()
            self.position = self.get_next_position()
            self.grid[self.position[0], self.position[1]] = "X"
        else:
            while self.grid[self.get_next_position()[0], self.get_next_position()[1]] != "#":
                self.position = self.get_next_position()
                self.grid[self.position[0], self.position[1]] = "X"
            self.grid[self.position[0], self.position[1]] = "X"
            while self.grid[self.get_next_position()[0], self.get_next_position()[1]] == "#":
                self.direction = (self.direction + 1) % 4

            self.position = self.get_next_position()
            self.grid[self.position[0], self.position[1]] = "X"
            
        if (self.position, self.direction) in self.log:
            raise InfinityLoopException
        self.log.append( (self.position, self.direction))
        
turtle_dir = 0
turtle_pos = [0, 0]

grid = []
with open("input", "r") as fh:
    y = 0
    for line in fh.readlines():
        line_list = list(line.strip())
        dirs = ("^", ">", "v", "<") # North is 0, east 1, south 2, west 3
        for direction, character in enumerate(dirs):
            try:
                x = line_list.index(character)
                turtle_dir = direction
                line_list[x] = "."
                turtle_pos = [y, x]
                print("Guard found at", turtle_pos, turtle_dir)
            except ValueError:
                pass
                
        grid.append(line_list)
        y += 1
        
guard = Turtle(position=turtle_pos, direction=turtle_dir, grid=numpy.array(grid), fast_forward=True)
try:
    while True:
        guard.move()
except EscapeException:
    print("We have escaped!", guard.count_moves())
    
score = 0

potential_walls = []

print(guard.grid.shape)
for ix in range(guard.grid.shape[0]):
    for iy in range(guard.grid.shape[1]):
        if guard.grid[iy, ix] == "X":
            if iy==turtle_pos[0] and ix==turtle_pos[1]:
                print("ignoring start pos", turtle_pos)
            else:
                potential_walls.append((iy, ix))
            
pbar = tqdm(potential_walls)
successful_walls = []

for pw in pbar:

    guard = Turtle(position=turtle_pos, direction=turtle_dir, grid=numpy.array(grid), fast_forward=True)
    
    try:
        guard.grid[pw[0], pw[1]] = "#"
    except IndexError:
        print("illegal wall")
        continue    

    try:
        while True:
            guard.move()
    except EscapeException:
        continue
    except InfinityLoopException:
        successful_walls.append(pw)
        
        pbar.set_description(str(pw))
        continue


print(len(set(successful_walls)))    

