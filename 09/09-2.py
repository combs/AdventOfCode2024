blocks = []
files = {}
first_free = -1

def find_first_free(blocks):
    global first_free
    try:
        while blocks[first_free] != -1:
            first_free += 1
    except IndexError:
        print("bad stuff happen looking for free block")
        
def find_first_free_span(length, blocks):
    global first_free
    candidate = first_free
    print("Seeking free span", length, "starting at", first_free)

    while candidate < len(blocks):
        try:
            while blocks[candidate] != -1:
                candidate += 1
        except IndexError:
            return None

        try:
            for offset in range(length):
                if blocks[candidate + offset] != -1:
                    candidate += 1 
                    raise ValueError
        except ValueError:
            continue
        except IndexError:
            candidate += 1
            continue
            
        print("Free span for length", length, "found at", candidate)
        return candidate
    return None
    
def move_file_to_first_free_span(file_id, blocks):
    global files
    position, length = files[file_id]
    
    if position <= first_free:
        print("file", file_id, "already earlier than first free block")
        return
    candidate = find_first_free_span(length, blocks)
    if candidate==None:
        print("no options for", file_id)
        return
    if position <= candidate:
        print("file", file_id, "cannot be improved upon by", candidate)
        return
    blocks[candidate:candidate+length] = [ file_id ] * length
    blocks[position:position+length] = [ -1 ] * length
    files[file_id] = (candidate, length)
    if candidate==first_free:
        find_first_free(blocks)
    print("file", file_id, "moved from", position, "to", candidate)
    
def print_blocks(blocks):
    print("".join([str(i) if i > -1 else "." for i in blocks]))
    
def score_blocks(blocks):
    score = 0
    for block in range(len(blocks)):
        if blocks[block] > -1:
            score += blocks[block]*block
    return score
        
        
with open("input", "r") as fh:
    for index, letter in enumerate(fh.readlines()[0].strip()):
        if index % 2 == 0:
            file_id = index // 2
            # before we add new blocks, len(blocks) will be index of new blocks
            files[file_id] = (len(blocks), int(letter))
            blocks.extend([file_id] * int(letter)) 
        else:
            if index == 1:
                first_free = len(blocks) # Set initial value
            blocks.extend([ -1 ] * int(letter))

for f in reversed(files.keys()):
    move_file_to_first_free_span(f, blocks)
    
print_blocks(blocks)
print(score_blocks(blocks))
