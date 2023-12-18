import re
from heapq import heappop, heappush
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

# Code starts
def isIn(path):
    return path[0] >= 0 and path[0] < nbRows and path[1] >= 0 and path[1] < nbCols


moveMap = {
    'u': (-1, 0),
    'd': (1, 0),
    'l': (0, -1),
    'r': (0, 1),
}
allowedMoves = {
    'o': ('l', 'r', 'u', 'd'),
    'u': ('l', 'r', 'u'),
    'd': ('l', 'r', 'd'),
    'l': ('l', 'u', 'd'),
    'r': ('r', 'u', 'd'),
}
blocks = [[int(col) for col in row]for row in data.split('\n')]

# blocks = [[c for c in rows[0:3]]for rows in blocks[:5]]
nbRows = len(blocks)
nbCols = len(blocks[0])
# print(nbRows, nbCols)

moves=[
    # score , point, direction
    (0, (0,0), 'o')
]
visited = set()

solved = None
nbIterations = 0
while solved is None:
    
    score, point, direction = heappop(moves)
    # print(score, point)

    if point[0]==nbRows-1 and point[1]==nbCols-1:
        print('found!!', point)
        print('nbIerations', nbIterations)
        solved = score
        break

    if (point[0], point[1], direction) in visited:
        continue

    nbIterations+=1
    
    vprint(score, point, direction)
    lastDirection = direction[-1]

    dirs = list(allowedMoves[lastDirection])

    if len(direction)==3:
        dirs.pop(dirs.index(lastDirection))

    # consider the point visited
    visited.add((point[0], point[1], direction) )

    # found_end = False
    for dir in dirs:
        # break
        shift = moveMap[dir]
        newPoint = (point[0]+shift[0], point[1]+shift[1])
        if not isIn(newPoint):
            continue
        if newPoint[0] == 0 and newPoint[1] == 0:
            continue

        # break
        newDirection = dir if dir!=lastDirection else direction+dir

        if (newPoint[0], newPoint[1], newDirection) in visited:
            # vprint(f'new Pos in visited, {newPos} [{newDir}]')
            continue
        
        blockCost = blocks[newPoint[0]][newPoint[1]]
        newScore = score + blockCost
        # newHistory = previousMoves + [(dir,blockCost)]
        heappush(moves, (newScore, newPoint, newDirection))

        # if (newPos, newDir) in  moves:
        #     # print('this direction is in the list')
        #     posInMoves = moves[(newPos, newDir)]
        #     if posInMoves[0] > newCost:
        #         moves[(newPos, newDir)] = [newCost, newHistory]
        # else:
        #     moves[ (newPos, newDir)] = [newCost, newHistory]
        # moves.append(newMove)

    vprint('moves', moves)
    vprint('visited', visited)
    vprint('')

vprint(solved)

# sol = [ [ '.' for r in rows] for rows in blocks]
# p=[0,0]
# t=0
# for x in solved[3]:
#     d1, d2 = moveMap[x[0]]
#     p = [p[0]+d1, p[1]+d2]
#     block = blocks[p[0]][p[1]]

#     t+= block
#     # sol[p[0]][p[1]] = f'{blocks[p[0]][p[1]]}'
    
#     sol[p[0]][p[1]] = 'x'
#     print(p, block, t)
#     # break

# a = [print(''.join(r)) for r in sol]

# a = [print(''.join([str(k) for k in r])) for r in blocks]
# # optimalPath = find_minimum_path()
print('Solution:', solved)
