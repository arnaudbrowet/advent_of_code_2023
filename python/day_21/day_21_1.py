import re

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

# Code starts
map={}
start=None
for i, r in enumerate(data.split('\n')):
    for j, p in enumerate(r):
        if p =='S':
            start = (i,j)
            p='.'
        map[(i,j)] = p


steps = 0
positions=set([start])
nbSteps = 6
while steps < nbSteps:
    steps += 1

    newPos=set()

    for pos in positions:
        # break
        for shift in [
            (0,1), (0,-1), (1,0), (-1,0)
        ]:
            p = (pos[0]+shift[0],pos[1]+shift[1])
            if p in map:
                if map[p]== '.':
                    newPos.add(p)

        
    positions = newPos

nbPositions = len(positions)
print('Solution:', nbPositions)
    