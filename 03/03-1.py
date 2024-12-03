import re

with open("input", "r") as fh:
    data = fh.read().strip()

pattern = r'mul\(([0-9\-]+),([0-9\-]+)\)'   
matches = re.findall(pattern, data)
score = 0

for match in matches:
    left, right = [ int(i) for i in match ] 
    score += left * right

print(score)    
    

    
