import re

verbose = False


def vprint(*messages):
    if verbose:
        if len(messages) == 1:
            print(messages[0])
        else:
            print(*messages)


input_file = "small_input3.txt"
# input_file = "input.txt"
with open(f'./{input_file}', 'r') as f:
    data = f.read().strip()

# Code starts
map=set()
start=None
baseRows = data.split('\n')

rep=1
rows = [r*rep for _ in range(rep) for r in baseRows]

nbRows = len(rows)
nbCols = len(rows[0])
baseRows = nbRows/rep
baseCols = nbCols/rep

for i, r in enumerate(rows):
    for j, p in enumerate(r):
        if p =='S':
            if i>=baseRows*((rep+1)/2-1) and i<baseRows*(rep+1)/2 and j>=baseCols*((rep+1)/2-1) and j<baseCols*(rep+1)/2:
                start = (i,j)
            p='.'
        
        if p=='.':
            map.add((i,j))


startIndex = start[0]%2*start[1]%2
shifts = [(0,1), (0,-1), (1,0), (-1,0)]

pos = [(*start, 0)]

distanceMap = {start:0}

while pos:
    x,y,d = pos.pop(0)

    for shift in shifts:
        p = (x+shift[0],y+shift[1])
        if p in map and p not in distanceMap:
            distanceMap[p] = d+1
            pos.append((*p, d+1))


vis = [ ["#"*3 for _ in range(nbCols)] for _ in range(nbRows) ]

for p, d in distanceMap.items():
    vis[p[0]][p[1]]=f"{d:03d}"

for r in vis:
    print(r)

m=10
x = [1 for d in distanceMap.values() if d <= m and m%2 == d%2]
t = len(x)
print(t)

# oneStep={p:[] for p in map}
# towStep={p:[] for p in map}
# for pos in map:
#     for shiftOne in shifts:
#         pOne = (
#             (pos[0]+shiftOne[0])%nbRows,
#             pos[1]+shiftOne[1]%nbCols
#             )
#         if pOne in map:
#             oneStep[pos].append(pOne)

#         for shiftTwo in shifts:
#             pTwo = (
#                 (pOne[0]+shiftTwo[0])%nbRows,
#                 (pOne[1]+shiftTwo[1]) % nbCols
#                 )
#             if p in map:
#                 towStep[pos].append(pTwo)


# steps = 0
# positions=set([start])
# nbSteps = 64
# while steps < nbSteps:
#     steps += 1

#     newPos=set()

#     for pos in positions:
#         # break
#         for shift in :
#             p = (pos[0]+shift[0],pos[1]+shift[1])
#             if p in map:
#                 if map[p]== '.':
#                     newPos.add(p)

        
#     positions = newPos

# nbPositions = len(positions)
# print('Solution:', nbPositions)
    