import re

verbose = False


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
        

# handle button
reset_sequence = []
is_loop = False
nbInLoop = None
totalPress = 1000
# while not is_loop:
for i in range(totalPress):
    nbPulses = dict(L = 0,H = 0,)
    pulses = [ ('button', 'L', 'broadcaster')]

    while pulses:
        (source, type, destination) = pulses.pop(0)
        
        vprint(source, f'- {type} -> {destination}')
        nbPulses[type] += 1

        if destination in modules:
            module = modules[destination]
            outPulses = modules[destination].handle_pulse(source, type)
            pulses += outPulses

    vprint()
    reset_sequence.append(nbPulses)
    if False not in [mod.is_initial() for mod in modules.values()]:
        is_loop = True
        if nbInLoop is None:
            nbInLoop = i+1


vprint()
vprint('Loop length', len(reset_sequence))

lows = sum([seq['L'] for seq in reset_sequence])
highs = sum([seq['H'] for seq in reset_sequence])

print('loop Length', nbInLoop if nbInLoop is not None else 'not reached')
print('Solution:', lows*highs)