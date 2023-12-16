import re
# import numpy as np
def vprint(*messages, verbose=False):
    if not verbose: return
    if len(messages) == 1:
        print(messages[0])
    else:
        print(*messages)


# input_file = "small_input.txt"
input_file = "input.txt"
with open(f'./{input_file}', 'r') as f:
    data = f.read().strip()

# Code starts
def isIn(ray):
    return ray[0] >= 0 and ray[0] < nbRows and ray[1] >= 0 and ray[1] < nbCols

tiles = data.split('\n')
moveMap = {
    'u': (-1, 0),
    'd': (1, 0),
    'l': (0, -1),
    'r': (0, 1),
}
tilesMap = {
    '.': {
        'r': ('r',),
        'l': ('l',),
        'u': ('u',),
        'd': ('d',),
    },
    '-': {
        'r': ('r',),
        'l': ('l',),
        'u': ('l', 'r'),
        'd': ('l', 'r'),
    },
    '|': {
        'r': ('u', 'd'),
        'l': ('u', 'd'),
        'u': ('u',),
        'd': ('d',),
    },
    '/': {
        'r': ('u',),
        'l': ('d',),
        'u': ('r',),
        'd': ('l',),
    },
    '\\': {
        'r': ('d',),
        'l': ('u',),
        'u': ('l',),
        'd': ('r',),
    },
}

nbRows = len(tiles)
nbCols = len(tiles[0])

allStartingPos = sum([
    # 1st row
    [ ((0, p), 'd') for p in range(nbCols)],
    # last row
    [ ((nbRows-1, p), 'u') for p in range(nbCols)],
    # 1st col
    [ ((p, 0), 'r') for p in range(nbRows)],
    # 1st row
    [ ((p, nbCols-1), 'l') for p in range(nbRows)],
], [])

configuratioEnergy=[]
# for startCol in range(nbCols):
#     for secondary

# startingPos = (0,0)
# startingDirection = 'r'

# allStartingPos=[ ((0,3), 'd')]
for (startingPos, startingDirection) in allStartingPos:


    rays = [
        # position, direction, visited
        (startingPos, startingDirection )
    ]
    tilesVisited = [
        [set() for c in rows] for rows in tiles
    ]
    tilesVisited[startingPos[0]][startingPos[1]].add( startingDirection )



    while len(rays) > 0:
        ray = rays.pop(0)

        (pos, move) = ray

        tile = tiles[pos[0]][pos[1]]

        newMoves = tilesMap[tile][move]
        for newMove in newMoves:
            shift = moveMap[newMove]
            newPos = (pos[0]+shift[0], pos[1]+shift[1])

            if not isIn(newPos):
                continue
            
            tileVisited = tilesVisited[newPos[0]][newPos[1]]

            if newMove in tileVisited:
                continue

            tileVisited.add(newMove)
            rays.append( (newPos, newMove))

        # print(rays)
    # [ print(''.join(['#'if len(s)>0 else '.' for s in r]) ) for r in tilesVisited]

    energy = sum([ sum([1 if len(s)>0 else 0 for s in r]) for r in tilesVisited])

    configuratioEnergy.append(energy)

solution = max(configuratioEnergy)
print('Solution:', solution)
