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
rows = data.split('\n')
cols = [ [r[c] for r in rows ]for c in range(len(rows[0]))]

total_weight = 0
for col in cols:
    pos = 0
    
    weights=[]
    for rock_pos, rock in enumerate(col):
        if rock == '.':
            continue
        elif rock == '#':
            pos = rock_pos+1
        else:
            weights.append(len(col)-pos)
            pos +=1
    
    vprint(weights)
    total_weight += sum(weights)
    
print('Solution:', total_weight)