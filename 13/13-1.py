import re

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
            

costs = {}

print(machines)
for index, (prize, button_a, button_b) in enumerate(machines):
    cost = 0
    x, y = [0, 0]
    print("seeking", prize, button_a, button_b)
    print(type(button_a))
    for a in range(100):
        cost = a * 3
        x, y = button_a[0] * a, button_a[1] * a
        if x > prize[0] or y > prize[1]:
            print("blew past the prize on button a ", a, x, y)
            continue
            
        b = (prize[0] - x) / button_b[0]
        if b == int(b):
            if (b * button_b[1]) + y == prize[1]:
                print("can reach prize with", a, "A and", b, "B")
                cost += b 
                print("total cost", cost)
                costs[index] = min(costs.get(index, 9999999999), cost)
            else:
                print("y didn't work out", b * button_b[1], prize[1])
                
        # ~ else:
            # ~ print("not possible to reach with button b presses,", b)
            
            
total_cost = sum(costs.values())
print("total cost", total_cost)

