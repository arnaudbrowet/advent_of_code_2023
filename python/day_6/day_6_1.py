# import re
import numpy as np

# input_file = "small_input.txt"
input_file = "input.txt"
with open(f'./{input_file}', 'r') as f:
    data = f.read()

if data[-1]=='\n':
    data = data[:-1]



[utimes, udistances] = data.split('\n')

times = [int(d) for d in utimes.split(':')[1].split()]
distances = [int(d) for d in udistances.split(':')[1].split()]


nb_holds=[]
for (t, d ) in zip(times, distances):
    # break
    # solve quadratic
    a=-1
    b=t
    c=-d
    
    r = b**2-4*a*c
    if (r<0):
        raise Exception('invalid rho')
    
    sol1 = (-b-np.sqrt(r))/(2*a)
    sol2 = (-b+np.sqrt(r))/(2*a)
    
    left = np.ceil(min([sol1, sol2]))
    right = np.floor(max([sol1, sol2]))
    
    nb_holds.append(
        right-left+1
    )
    
    

solution = int(np.prod(nb_holds))
print('Solution: ', solution)