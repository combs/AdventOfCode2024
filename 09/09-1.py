blocks = []
first_free = -1

def move_to_first_free(block, blocks):
    global first_free
    
    blocks[first_free] = blocks[block]
    blocks[block] = -1
    
    try:
        while blocks[first_free] != -1:
            first_free += 1
    except IndexError:
        print("Weird, we ran out of free blocks. That should not be possible")
    print("Next free block:", first_free)
    
def print_blocks(blocks):
    print("".join([str(i) if i > -1 else "." for i in blocks]))
    
def score_blocks(blocks):
    score = 0
    for block in range(first_free):
        if blocks[block] > -1:
            score += blocks[block]*block
    return score
        
        
with open("input", "r") as fh:
    for index, letter in enumerate(fh.readlines()[0].strip()):
        if index % 2 == 0:
            blocks.extend([(index // 2)] * int(letter)) 
        else:
            if index == 1:
                first_free = len(blocks) # Set initial value
            blocks.extend([ -1 ] * int(letter))
        
for block in reversed(range(len(blocks))):
    if blocks[block] != -1:
        move_to_first_free(block, blocks)
    if block <= first_free:
        print("are we done?")
        break
        
print_blocks(blocks)
print(score_blocks(blocks))
