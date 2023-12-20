import re
import math
verbose = True


def vprint(*messages):
    if verbose:
        if len(messages) == 1:
            print(messages[0])
        else:
            print(*messages)


# input_file = "small_input2.txt"
input_file = "input.txt"
with open(f'./{input_file}', 'r') as f:
    data = f.read().strip()

# Code starts
class Broadcaster():
    def __init__(self, name, outputs) -> None:
        self.name = name
        self.outputs=outputs

    def get_type(self)->str:
        return 'broadcaster'
    
    def handle_pulse(self, source, type)->[]:
        if type=='L':
            return [(self.name, 'L', out) for out in self.outputs]
        
        raise Exception('invalid Broadcaster input')

    def is_initial(self):
        return True
    
class FlipFlop():
    def __init__(self,name, outputs) -> None:
        self.status = False # on=True, off=False
        self.name = name
        self.outputs=outputs

    def get_type(self)->str:
        return 'flipflop'
    
    def handle_pulse(self, source, type)->[]:
        if type=='H':
            return []
        elif type=='L':
            self.status = not self.status
            outType = 'H' if self.status else 'L'
            return [(self.name, outType, out) for out in self.outputs]
        
        raise Exception('invalid FlipFlop input')
        
    def is_initial(self):
        return not self.status

class Conjuction():
    def __init__(self, name, outputs) -> None:
        self.name = name
        self.outputs=outputs
        self.inputs = {}

    def get_type(self)->str:
        return 'conjuction'
    
    def add_input(self, modName):
        self.inputs[modName]='L'

    def handle_pulse(self, source, type)->[]:
        if type not in ['L','H']:
            raise Exception('invalid Conjuction input')
        
        self.inputs[source]=type

        outType = 'L'
        if 'L' in self.inputs.values():
            outType = 'H'

        return [(self.name, outType, out) for out in self.outputs]
    
    def is_initial(self):
        return 'H' not in self.inputs.values()


modulesDefinition= [ [k for k in m.split(' -> ')] for m in data.split('\n')   ] 

modules = {}

# init the modules
for (modName, out) in modulesDefinition:
    outputs = out.split(', ')
    if modName == 'broadcaster':
        modules[modName] = Broadcaster(modName, outputs)

    elif modName[0] == '%':
        modules[modName[1:]] = FlipFlop(modName[1:], outputs)
    elif modName[0] == '&':
        modules[modName[1:]] = Conjuction(modName[1:], outputs)
    else:
        raise Exception('Invalid module')

# add input of conjuctions
for (modName, out) in modulesDefinition:
    outputs = out.split(', ')
    for output in outputs:
        if output not in modules:
            continue
        mod = modules[output]
        if mod.get_type() == 'conjuction':
            mod.add_input(modName[1:])
        

## OBSERVATION
## EACH OUTPUT FROM BROADCASTER IS IN SINGLE LOOP OF NODES
## SO COMPUTE THE BUTTON PRESS FOR EACH LOOP INDIVIDUALLY

inputLoopSolution = []

for start in modules['broadcaster'].outputs:
    # break

    # detect nodes in the loop
    add = [start]
    visited = set()
    endNode = None
    while add:
        node = add.pop(0)
        visited.add(node)
        if node in modules:
            out = modules[node].outputs
            add += list(set([p for p in out if p not in visited]))
            if 'lv' in out:
                # lv is the parent of rx so we stop on the node before
                endNode = node

    # handle button
    button_pressed = 0
    output_reached = False
    output = endNode

    nbForReset = None
    possibleButtonPressed = []

    while not output_reached:

        button_pressed += 1
        pulses = [ ('broadcaster', 'L', start)]

        while pulses:
            (source, type, destination) = pulses.pop(0)
            # vprint(source, f'- {type} -> {destination}')
            # nbPulses[type] += 1

            if destination == output and type == 'L':
                possibleButtonPressed.append(button_pressed)

            if destination != output:
                module = modules[destination]
                outPulses = modules[destination].handle_pulse(source, type)
                pulses += outPulses

        if False not in [mod.is_initial() for mod in modules.values()]:
            nbForReset = button_pressed
            output_reached = True

    print('reset in:', nbForReset)
    print('possible:', possibleButtonPressed)
    inputLoopSolution.append(possibleButtonPressed[0])

solution = math.lcm(*inputLoopSolution)

# vprint()
# vprint('Loop length', len(reset_sequence))

# lows = sum([seq['L'] for seq in reset_sequence])
# highs = sum([seq['H'] for seq in reset_sequence])

print('Solution:', solution)