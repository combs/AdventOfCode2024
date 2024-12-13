import scipy, numpy, skimage, itertools

import matplotlib.pyplot as plt
import mplcursors

lines_grid = []

with open("input", "r") as fh:
    for line in fh:
        if len(line) > 2:
            lines_grid.append([ord(i) for i in list(line.strip())])
    
        
grid = numpy.array(lines_grid, dtype=numpy.uint8)
values = numpy.unique(grid)
numpy.set_printoptions(edgeitems=1000, linewidth=100000, formatter=dict(float=lambda x: "%.3g" % x))
    
print(grid)

origins = {}
score = 0
all_contours = {}


for value in values:
    labeled, num_features = scipy.ndimage.label(grid==value)
    labeled_features = numpy.unique(labeled)
 
    for this_one in labeled_features:

        if this_one==0:
            continue
        # print("Looking for", this_one, "in\n", labeled[feature])
        isolated = (labeled == this_one)

        print("Isolated", this_one, ":")
        
        area = numpy.sum(isolated) 
        
        perim = 0
        
        shape = isolated.shape
     
        padded = numpy.pad(isolated, pad_width=1, mode='constant', constant_values=0)
        contours = skimage.measure.find_contours(padded)
        # print("padded to\n", padded)
        
        contour = contours[0]
        
        perim = 0
        x, y = contour[0]
        origin = (x, y)
        
        print("Contour x, y absolute origin:", x, y)
        
        for i in range(len(contour) - 1):
            left = contour[i]
            right = contour[i + 1]
            perim += numpy.sum(numpy.abs(left - right))
        
        for sub_contour in contours[1:]:
            sub_perim = 0
            for i in range(len(sub_contour) - 1):
                left = sub_contour[i]
                right = sub_contour[i + 1]
                sub_perim += numpy.sum(numpy.abs(left - right))
            print("INSIDE PERIM FOUND, ADDING", sub_perim)
            perim += sub_perim
            
        plottable = numpy.array([ [c[0], c[1] ] for c in contour] )
        
        if origin in origins:
            if area > origins[origin]["area"]:
                print("Replacing duplicate!", area , "bigger than", origins[origin]["area"])
            else:
                print("Skipping duplicate...")
                continue

        origins[origin] = {"area": area, "perim": perim, "perim": perim, "area": area, "contour": contour, "plottable": { "x": plottable[:, 1], "y": plottable[:, 0] } } 
        
        print("logged", str(value) + "-" + str(this_one)) 
            
        print("Origin", origin, "area", area, "perimeter", perim )
        assert perim >= 4
        assert pow(area, 0.5) <= perim
        
        
for key, val in origins.items():
    score += val["area"] * val["perim"]
    all_contours[key] = (val["plottable"])

#print(origins)

print("Overall score", score)

# Display the image and plot all contours found
fig, ax = plt.subplots()
ax.imshow(numpy.pad(grid, pad_width=1, mode='constant', constant_values=0), cmap=plt.cm.gray)

for key, val in all_contours.items():
    ax.plot("x", "y", "", fillstyle='full', color='r', data=val, label=key, linewidth=1)
    ax.fill(val["x"], val["y"], color=(0, 0, 1, 0.2), hatch='/')

mplcursors.cursor()
ax.axis('image')
ax.set_xticks([])
ax.set_yticks([])
plt.show()
