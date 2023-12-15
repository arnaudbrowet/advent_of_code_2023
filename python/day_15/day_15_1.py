import re
# import numpy as np

verbose = False
def vprint(*messages):
    if verbose:
        if len(messages) == 1:
            print(messages[0])
        else:
            print(*messages)

# input_file = "small_input.txt"
input_file = "input.txt"
with open(f'./{input_file}', 'r') as f:
    data = f.read().strip()

### Code starts
    
def computeHash(seq):
    v= 0
    for s in seq:
        v= ((v+ord(s))*17)%256
    return v

steps = data.split(',')
nbSteps = len(steps)

hashValues = []
for step in steps:
    hashValues.append(computeHash(step))


solution = sum(hashValues)
print('Solution:', solution)