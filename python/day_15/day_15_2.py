import re
# import numpy as np

verbose = True
def vprint(*messages):
    if verbose:
        if len(messages) == 1:
            print(messages[0])
        else:
            print(*messages)

input_file = "small_input.txt"
# input_file = "input.txt"
with open(f'./{input_file}', 'r') as f:
    data = f.read().strip()

### Code starts
    
def computeHash(seq):
    v= 0
    for s in seq:
        v= ((v+ord(s))*17)%256
    return v

def printBoxes(boxes):
    for boxIndex, box in enumerate(boxes):
        if box is None:
            continue
        content = [f'[{key} {value}]' for key , value in box.items()]
        if len(content)>0:
            vprint("Box", boxIndex, ' '.join(content))


boxes = [None]*256

printBoxes(boxes)
steps = data.split(',')
nbSteps = len(steps)

for step in steps:
    # break
    if (step[-1] == '-'):
        seq = step[:-1]
        seqBox = computeHash(seq)
        # remove lens
        box = boxes[seqBox]
        if box is None:
            continue
        if seq in box.keys():
            del boxes[seqBox][seq]

    else:
        (seq, focal) = re.match(r'(\w+)=(\d)', step).groups()
        seqBox = computeHash(seq)

        box = boxes[seqBox]
        if box is None:
            boxes[seqBox]= {seq: int(focal)}
        else:
            box[seq] = int(focal)

    vprint(step)
    printBoxes(boxes)
    vprint()

    
[
    [1+boxIndex for enumerate(box.items()) ] for boxIndex, box in enumerate(boxes) if box is not None]

# solution = sum(hashValues)
solution = 0
print('Solution:', solution)