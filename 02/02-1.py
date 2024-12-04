
lefts = []
rights = [] 

def validate(vals):
    
    bads = 0
    direction = 0 
    og_vals = vals.copy()
    
    left = vals.pop(0)
    
    for right in vals:
        diff = left - right
        if diff < -3 or diff > 3:
            print(left, "to", right, "delta", diff, "too extreme")
            bads += 1
        
        if diff == 0 :
            print("no change", left, right)
            bads += 1
            
        if direction == 0:
            direction = diff
            print(left, "to", right, "direction is now", direction)
            
        else:
            if direction < 0:
                if diff > 0:
                    print(left, "to", right, "reversed direction", diff, direction)
                    bads += 1
            else:
                if diff < 0:
                    print(left, "to", right, "reversed direction", diff, direction)
                    bads += 1
        
        left = right
        
    print(bads, "bads for", og_vals)
    return 1 * (bads == 0)
    
score = 0

with open("input", "r") as fh:
    for line in fh.readlines():
        vals = [ int(v) for v in line.split() ] 
        
        score += validate(vals)
        
print(score)
