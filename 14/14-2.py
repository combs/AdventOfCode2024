import numpy, time
from PIL import Image
from tqdm import tqdm

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

numpy.set_printoptions(edgeitems=1000, linewidth=100000, formatter=dict(float=lambda x: "%.3g" % x))

for index in tqdm(range(1000000000)):
    pixgrid = numpy.zeros((bounds[0], bounds[1]),dtype=bool)
    
    for i, robot in robots.items():
        pos = (robot["pos"][0] + robot["vel"][0], robot["pos"][1] + robot["vel"][1])
        robots[i]["pos"] = (pos[0] % bounds[0], pos[1] % bounds[1])
        pixgrid[robot["pos"]] = 1
    

    busy_rows = pixgrid.sum(axis=1)
    
    longies = numpy.sum(busy_rows > 20)
    
    if longies > 5:
        print(str(index + 1) + ".png")
        Image.fromarray(pixgrid).save(str(index + 1) + ".png")
        
    




        