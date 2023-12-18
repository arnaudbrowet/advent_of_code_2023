import re
# from heapq import heappop, heappush

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


def hexToDig(hex):
    nbDig = int(f"0x{hex[:-1]}", 16)
    direction = None
    if color[-1] == '0':
        direction = 'R'
    elif color[-1] == '1':
        direction = 'D'
    elif color[-1] == '2':
        direction = 'L'
    elif color[-1] == '3':
        direction = 'U'
    else:
        raise Exception('invalid color direction')

    return direction, nbDig


directionMap = {
    'R': (0, 1),
    'L': (0, -1),
    'D': (1, 0),
    'U': (-1, 0),
}
steps = data.split('\n')
digs = []

point = (0, 0)
xlimits = (0, 0)
ylimits = (0, 0)
for step in steps:
    # break
    direction, nbDig, color = re.match(r'(\w) (\d+) \(#(\w+)\)', step).groups()
    nbDig = int(nbDig)

    # direction, nbDig = hexToDig(color)
    digs.append(
        (direction, *point, nbDig)
    )
    shift = directionMap[direction]
    point = (
        point[0]+shift[0]*nbDig,
        point[1]+shift[1]*nbDig,
    )
    xlimits = (
        min(xlimits[0], point[1]),
        max(xlimits[1], point[1])
    )
    ylimits = (
        min(ylimits[0], point[0]),
        max(ylimits[1], point[0])
    )
first = digs[0]
last = digs[-1]
if first[0] == last[0]:
    raise Exception('Consecutive first dig not handled')

verticalQueues = [
    (d[2], d[1], d[2], d[3]) for d in digs if d[0] == 'D'
]+[
    (d[2], d[1]-d[3], d[2], d[3]) for d in digs if d[0] == 'U'
]

rowBreak=set()
for v in verticalQueues:
    rowBreak.add(v[1])
    rowBreak.add(v[1]+v[3])

rowBreak = list(rowBreak)
rowBreak.sort()

horizontalQueues = [
    (d[1], d[1], d[2], d[3]) for d in digs if d[0] == 'R'
]+[
    (d[1], d[1], d[2]-d[3], d[3]) for d in digs if d[0] == 'L'
]

columnBreak=set()
for v in horizontalQueues:
    columnBreak.add(v[2])
    columnBreak.add(v[2]+v[3])

columnBreak = list(columnBreak)
columnBreak.sort()

# iterates on triangles
nbInside = 0

for i in range(len(rowBreak)-1):
    # break
    rowStart = rowBreak[i]
    rowEnd = rowBreak[i+1]
    
    rowShift = 1
    if i == len(rowBreak)-2:
        # do not remove on last row
        rowShift=0

    inside = False

    colShift=0
    # add in length of border to inside
    # nbInside += rowEnd-rowStart+1-rowShift
    for j in range(len(columnBreak)-1):
        # break
        colStart = columnBreak[j]
        colEnd = columnBreak[j+1]

        verticals = filter(lambda x: x[0]==colStart, verticalQueues)
        trueLeft = False
        for vert in verticals:
            if rowStart>=vert[1] and rowEnd<=vert[1]+vert[3]:
                trueLeft = True
                break

        if trueLeft:
            inside = not inside

        if inside:
            nbSquare = (rowEnd-rowStart+1-rowShift)*(colEnd-colStart+1-colShift)
            nbInside+=nbSquare
            if colShift==0:
                colShift=1

            # print(i, j , (rowStart, colStart), (rowEnd, colEnd), nbSquare, nbInside )
            # print('*')
        else:
            colShift=0
            # add top border
            trueTop = False
            horizontals = filter(lambda x: x[0]==rowStart, horizontalQueues)
            for hor in horizontals:
                if colStart>=hor[2] and colEnd<=hor[2]+hor[3]:
                    trueTop = True
                    break
            if trueTop:
                # print('Truetop')
                nbInside += colEnd-colStart+1-1
        # print(i, j , (rowStart, colStart), (rowEnd, colEnd), inside, nbInside )
        
        # if inside:
            # print()
            # square = (rowEnd-rowStart-1)*(colEnd-colStart-1)
            # inside+=square
            
        # is the left border a true border

    # print('row', i , rowStart-ylimits[0]+1, rowEnd-ylimits[0]+1, nbInside)
print(nbInside)