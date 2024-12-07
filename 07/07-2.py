import itertools

def add(a, b):
    return a+b

def mul(a, b):
    return a*b

def concat(a, b):
    return int(str(a) + str(b))

class Done(Exception):
    pass
        
equations = {}
ops = {"mul": mul, "add": add, "concat": concat}

with open("input", "r") as fh:
    for line in fh.readlines():
        if ": " not in line: 
            continue
        
        (left, right) = line.strip().split(": ")
        
        equations[int(left)] = [int(i) for i in right.split(" ")]
        
score = 0
for (desired_output, inputs) in equations.items():
    
    repeats = (len(inputs) - 1)
    
    if repeats==1:
        iterator = [[i] for i in list(ops.keys())]
    else:
        iterator = itertools.product(ops.keys(), repeat=repeats)
    
    # print("inputs", inputs, "repeats", repeats, "iterator", iterator)
    original_inputs = inputs.copy()
    try:
        for operator_list in iterator:
            inputs = original_inputs.copy()
            # print("trying", operator_list, inputs)
            output = inputs.pop(0)
            for operator in operator_list:
                prev = output
                operand = inputs.pop(0)
                output = ops[operator](output, operand)
                if output < prev:
                    print("trying", operator_list, inputs)
                    print(prev, operator, operand, output)
                    raise ValueError("How the heck did we go from " + str(output) + " to " + str(prev))
                if output > desired_output:
                    # print("too large, bye")
                    break
            if output==desired_output:
                score += desired_output
                print("Successful method for", desired_output, ":", operator_list, original_inputs)
                raise Done
        
    except Done:
        pass
        
print(score)
