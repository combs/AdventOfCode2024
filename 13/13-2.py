import re
from tqdm import tqdm

machines = []

with open("input", "r") as fh:
    try:
        while True:
            line_a = fh.readline().strip()
            poo, x, y = line_a.split("+")
            x = ''.join(ch for ch in x if ch.isdigit())
            button_a = int(x), int(y)
            line_b = fh.readline().strip()
            poo, x, y = line_b.split("+")
            x = ''.join(ch for ch in x if ch.isdigit())
            button_b = int(x), int(y)
            line_prize = fh.readline().strip()
            poo, x, y = line_prize.split("=")
            x = ''.join(ch for ch in x if ch.isdigit())
            prize = int(x), int(y)
            poo = fh.readline()
            machines.append((prize, button_a, button_b))
    except EOFError:
        pass
    except ValueError:
        pass

#math.atan2(y,x)/math.pi*180
             
class Done(Exception):
    pass
    
costs = {}

print(machines)
for index, (prize, button_a, button_b) in enumerate(machines):
    cost = 0
    x, y = [0, 0]
    bigassify = 10000000000000
    prize = (prize[0] + bigassify, prize[1] + bigassify)
    print("seeking", prize, button_a, button_b)
    
    ratio = prize[0] / prize[1]
    ratio_a = button_a[0] / button_a[1]
    ratio_b = button_b[0] / button_b[1]
    pressed_a = 0
    pressed_b = 0 
    
    x = 0
    y = 0
    
    print("starting with pressed_a", pressed_a, "pressed_b", pressed_b, "for total xy", x, y, "with buttons", button_a, button_b)
    
    iterator = 0
    
    try:
        while x < prize[0] and y < prize[1]:
            iterator += 1
            if x==0 and y==0:
                if ratio > ratio_b:
                    button = "b"
                else:
                    button = "a"
            elif (x / y) > ratio:
                if ratio_a > ratio_b:
                    button = "b"
                else:
                    button = "a"
            else:
                if ratio_a > ratio_b:
                    button = "a"
                else:
                    button = "b"
            if button == "a":
#                print("a", x, y, pressed_a, pressed_b)
                num = int(max(1, (prize[0] - x) // 10000))
                pressed_a += num
                x += button_a[0] * num
                y += button_a[1] * num
            else:
#                print("b", x, y, pressed_a, pressed_b)            
                num = int(max(1, (prize[0] - x) // 10000))
                pressed_b += num
                x += button_b[0] * num
                y += button_b[1] * num
            
            if x == prize[0] and y == prize[1]:
                cost = (pressed_a * 3) + pressed_b
                costs[prize] = cost
                print("Converged on solution", cost, pressed_a, pressed_b)
                raise Done
        print("overflowed", prize, x, y)
    except Done:
        pass         
            
total_cost = sum(costs.values())
print("total cost", total_cost)

