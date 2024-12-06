
import numpy

class EscapeException(ValueError):
    pass
        
class Turtle(object):
    direction = 0
    grid = numpy.zeros((10,10), dtype=str)
    position = [0, 0]
    # I am used to including these redundantly as class-level defs from Cython
    
    def __init__(self, *args, **kwargs):
        self.position = kwargs.get("position", [4, 5])
        self.direction = kwargs.get("direction", 0)
        self.grid = kwargs.get("grid", numpy.zeros((10,10), dtype=str).fill("."))

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
        return next_pos
                
    def move(self):
        next_position = self.get_next_position()
        print(self.position, self.direction, next_position, self.grid.shape)
        if (next_position[0] < 0) or (next_position[1] < 0) or (next_position[0] >= self.grid.shape[0]) or (next_position[1] >= self.grid.shape[1]):
            raise EscapeException
        self.grid[self.position[0], self.position[1]] = "X"
        if self.grid[next_position[0], next_position[1]] == "#":
            self.direction = (self.direction + 1) % 4
        self.position = self.get_next_position()
        
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
        
print(grid)
print(numpy.array(grid))
guard = Turtle(position=turtle_pos, direction=turtle_dir, grid=numpy.array(grid))

try:
    while True:
        guard.move()
        print(guard.grid)
except EscapeException:
    print("We have escaped!", guard.count_moves() + 1)
    
