import re

with open("input", "r") as fh:
    data = fh.read().strip()

pattern = r'(?:(mul)\(([0-9\-]+),([0-9\-]+)\))|(?:(do|don\'t)\(\))'
matches = re.findall(pattern, data)
score = 0

enabled = True
for match in matches:
    op = match[0] or match[3]
    if op=="mul":
        left, right = int(match[1]), int(match[2])
        if enabled:
            score += left * right
    elif op=="do":
        enabled = True
    elif op=="don't":
        enabled = False

print(score)
    

    
