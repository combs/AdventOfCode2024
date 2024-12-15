robots = {}
with open("input", "r") as fh:
    for index, line in enumerate(fh):
        if "=" in line:
            pos, vel = [thing.split("=")[1].split(",") for thing in line.strip().split(" ")]
            pos = tuple([int(i) for i in pos])
            vel = tuple([int(i) for i in vel])
            
            robots[index] = ({"pos":pos, "vel":vel})

#bounds = (11, 7)
bounds = (101, 103)

for step in range(100):
    for i, robot in robots.items():
        pos = (robot["pos"][0] + robot["vel"][0], robot["pos"][1] + robot["vel"][1])
        robots[i]["pos"] = (pos[0] % bounds[0], pos[1] % bounds[1])

quadrants = [ 0, 0, 0, 0 ]

for i, robot in robots.items():
    if robot["pos"][0] == bounds[0]//2:
        continue
    if robot["pos"][1] == bounds[1]//2:
        continue
        
    qx = min(robot["pos"][0] // (bounds[0]//2 ), 1)
    qy = min(robot["pos"][1] // (bounds[1]//2 ), 1)
    i = qx*2 + qy
    quadrants[i] += 1

#print(quadrants)
#print(robots)
#
print(quadrants[0]*quadrants[1]*quadrants[2]*quadrants[3])


        