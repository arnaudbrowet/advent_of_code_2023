from heapq import heappush, heappop

verbose = False


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

# Code starts
bricks = [r.split('~') for r in data.split('\n')]

brickList = []
for b in bricks:
    startS, endS = b
    
    start = [int(p) for p in startS.split(',')]
    end = [int(p) for p in endS.split(',')]

    # order by Z
    if start[-1] > end[-1]:
        start, end = end, start

    brickPositions=[
        (x, y, z) for x in range(start[0], end[0]+1) 
        for y in range(start[1], end[1]+1)
        for z in range(start[2], end[2]+1)
    ]
    brickFloors = [p for p in brickPositions if p[2]==start[2]]

    heappush(brickList, (start[2], brickPositions, brickFloors))

filledPositions={}
brickLayout={}
brickIndex = 0
while brickList:
    brickIndex += 1
    height, brickPositions, brickFloors = heappop(brickList)
    
    stop = False
    shift = 0
    while not stop and height-shift>1:
        # go down if possible
        canGoDown=True
        for p in brickFloors:
            if (p[0], p[1], p[2]-shift-1) in filledPositions:
                canGoDown=False
                break
        if canGoDown:
            shift += 1
        else:
            stop=True

    for p in brickPositions:
        filledPositions[
            (p[0], p[1], p[2]-shift)
        ] = brickIndex

    holdBy = set(
        [filledPositions[(p[0], p[1], p[2]-shift-1)] # if filledPositions[(p[0], p[1], p[2]-1)]!=brickIndex else None
            for p in brickFloors if (p[0], p[1], p[2]-shift-1) in filledPositions]
    )# - {None}
    
    brickLayout[brickIndex] = {
        'holds':set(),
        'holdBy': holdBy,
    }
    for b in holdBy:
        brickLayout[b]['holds'].add(brickIndex)


nbDisintegrate = 0
for brickIndex, support in brickLayout.items():
    canBeDisintegrate = True
    for brick in support['holds']:
        if len(brickLayout[brick]['holdBy'])<2:
            canBeDisintegrate = False
            break
    if canBeDisintegrate:
        nbDisintegrate += 1

print('Solution:', nbDisintegrate)