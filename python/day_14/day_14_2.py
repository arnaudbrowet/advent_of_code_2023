### Generic 
# import re
import numpy as np

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
    
### Code start
mat = [r for r in data.split('\n')]

mat_as_str = lambda x: '<>'.join(x)

def transpose(M):
    return [ ''.join([r[c] for r in M ]) for c in range(len(M[0]))]    


def compute_load(M):
    load = 0
    nbRows = len(M)
    for rowIndex, row in enumerate(M):
        for c in row:
            if c=='O':
                load += nbRows-rowIndex
                
    return load

def shift_row(row, shiftDir):
    groups = row.split('#')
    
    nbO = [ (group.count('O'), len(group)) for group in groups]
    
    newGroups= [ ('.'*(l-n)*(shiftDir==1)) + 'O'*n + ('.'*(l-n)*(shiftDir==-1))  for n,l in nbO]
    
    return "#".join(newGroups)
    
    
def shift(M, dir):
    if dir=='N' or dir =='S':
        M = transpose(M)
            
    shiftDir = -1
    if dir=='S' or dir=='E':
        shiftDir = 1
        
    c=[shift_row(r, shiftDir) for r in M]
        
    if dir=='N' or dir =='S':
        return transpose(c)

    return c
            
            
# verify part 1
M = shift(mat, 'N')
load = compute_load(M)
vprint('load part 1',load)

# run part 2
cycle = []
cycleFound = False
nb_cycles = 1000000000
M = mat

run_cycle = 0
while not cycleFound or run_cycle<nb_cycles:
    M = shift(M, 'N')
    M = shift(M, 'W')
    M = shift(M, 'S')
    M = shift(M, 'E')
    
    new_mat_str = mat_as_str(M)
    
    if new_mat_str in cycle:
        cycleFound = True
        vprint(f'found a cycle after {run_cycle} steps')
        break    
    
    cycle.append(new_mat_str)
    run_cycle += 1
        

if not cycleFound:
    load = compute_load(M)

else:
    cycle_index = cycle.index(new_mat_str)
    cycle_length = len(cycle) - cycle_index

    pos_end_of_loops = (nb_cycles-cycle_index-1) % cycle_length

    end_map = cycle[cycle_index + pos_end_of_loops].split('<>')

    [compute_load(r.split('<>')) for r in cycle]
    load = compute_load(end_map)
    
print('Solution:', load)