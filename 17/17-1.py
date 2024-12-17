import tqdm

class Done(Exception):
    pass
    
class Compy(object):
    a = 0
    b = 0
    c = 0
    pc = 0
    instrux = []
    
    def __init__(self, a=0, b=0, c=0, pc=0, instrux=[]):
        self.a, self.b, self.c, self.pc, self.instrux = a, b, c, pc, instrux
        print("COMPY ONLNIEE!!!")
        
    def compute(self):
        if self.pc >= len(self.instrux) - 1:
            print("We out of instrux")
            raise Done
        
        mapping = { 0: self._divide_a, 1: self._xor_b_and_literal, 2: self._modulo_to_b, 3: self._jump_if_not_zero, 4: self._xor_b_and_c, 5: self._output, 6: self._divide_a_into_b, 7: self._divide_a_into_c}
        labels = { 0: "adv", 1: "bxl", 2: "bst", 3: "jnz", 4: "bxc", 5: "out", 6: "bdv", 7: "cdv" }
        
        instruction, operand = self.instrux[self.pc:self.pc+2]
        print("before", labels[instruction], operand, "A", self.a, "B", self.b, "C", self.c, "PC", self.pc)
        retval = mapping[instruction](operand)
        print("after", labels[instruction], operand, "A", self.a, "B", self.b, "C", self.c, "PC", self.pc, "retval", retval)
        
        return retval
        
    
    def _lookup_combo_operand(self, operand):
        if 0 <= operand <= 3:
            return operand
        if operand==4:
            return self.a
        if operand==5:
            return self.b
        if operand==6:
            return self.c
        if operand > 6:
            raise ValueError("Illegal combo operand", operand)
            
    def _divide_a(self, operand):
        numerator = self.a
        divisor = pow(2, self._lookup_combo_operand(operand))
        self.a = numerator // divisor
        self.pc += 2
        
        
    def _divide_a_into_b(self, operand):
        numerator = self.a
        divisor = pow(2, self._lookup_combo_operand(operand))
        self.b = numerator // divisor
        self.pc += 2
        
    def _divide_a_into_c(self, operand):
        numerator = self.a
        divisor = pow(2, self._lookup_combo_operand(operand))
        self.c = numerator // divisor
        self.pc += 2
    
    def _xor_b_and_literal(self, operand):
        self.b = self.b ^ operand
        self.pc += 2
        
    def _xor_b_and_c(self, operand):
        self.b = self.b ^ self.c
        self.pc += 2

    def _modulo_to_b(self, operand):
        self.b = self._lookup_combo_operand(operand) & 7
        self.pc += 2
        
    def _jump_if_not_zero(self, operand):
        if self.a == 0:
            self.pc += 2
        else:
            self.pc = operand
    
    def _output(self, operand):
        self.pc += 2
        return self._lookup_combo_operand(operand) & 7
        
compy = Compy()

with open("input", "r") as fh:
    for line in fh:
        if "Register A: " in line:
            compy.a = int(line.strip().split("Register A: ")[1])
        elif "Register B: " in line:
            compy.b = int(line.strip().split("Register B: ")[1])
        elif "Register C: " in line:
            compy.c = int(line.strip().split("Register C: ")[1])
        elif "Program: " in line:
            compy.instrux = [int(i) for i in line.strip().split("Program: ")[1].split(",") ] 
        
outputs = []

try:
    with tqdm.tqdm() as pbar:
        while True:
            output = compy.compute()
            if output is not None:
                outputs.append(output)
            print (",".join([str(i) for i in outputs]))
            pbar.update()
            
except Done:
    print("All done!")

    print (",".join([str(i) for i in outputs]))
