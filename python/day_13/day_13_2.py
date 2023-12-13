# import re
import numpy as np
import functools

# input_file = "small_input.txt"
input_file = "input.txt"
with open(f'./{input_file}', 'r') as f:
    data = f.read()

if data[-1]=='\n':
    data = data[:-1]
    

patterns = data.split('\n\n')

scores = []

for pattern in patterns:
    # break
    pat = np.array([ [c for c in r] for r in pattern.split('\n')])
    
    nb_rows, nb_cols = pat.shape
    
    # find column reflection
    reflection_column = None
    for c in range(nb_cols-1):
        reflection_length = min(c+1, nb_cols-c-1)
        
        left = pat[:, c-reflection_length+1:c+1]
        right = pat[:, c+1:c+1+reflection_length]
        
        left_flip = np.flip(left,1)
        
        compare = left_flip == right
        
        nbFalse = np.size(compare)- np.count_nonzero(compare)
        
        if nbFalse == 1:
            # found reflection in column
            reflection_column = c
            break
        
    if reflection_column is not None:
        scores.append(reflection_column+1)
        continue
    
    
    # find column reflection
    reflection_row = None
    for c in range(nb_rows-1):
        reflection_length = min(c+1, nb_rows-c-1)
        
        top = pat[ c-reflection_length+1:c+1,:]
        bottom = pat[c+1:c+1+reflection_length,:]
        
        top_flip = np.flip(top,0)
        
        compare = top_flip == bottom
        
        nbFalse = np.size(compare)- np.count_nonzero(compare)
        
        if nbFalse == 1:
            # found reflection in column
            reflection_row = c
            break
        
    if reflection_row is not None:
        scores.append(100*(reflection_row+1))
        continue

    raise Exception('no reflection found')

solution = sum(scores)
print('solution:', solution)