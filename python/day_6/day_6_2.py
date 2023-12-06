# import re
import numpy as np
import time

t1= time.time()

# input_file = "small_input.txt"
input_file = "input.txt"
with open(f'./{input_file}', 'r') as f:
    data = f.read()

if data[-1]=='\n':
    data = data[:-1]

[utimes, udistances] = data.split('\n')

run_time = int(utimes.split(':')[1].replace(' ', ''))
distance = int(udistances.split(':')[1].replace(' ', ''))

a=-1
b=run_time
c=-distance

r = b**2-4*a*c
if (r<0):
    raise Exception('invalid rho')

sol1 = (-b-np.sqrt(r))/(2*a)
sol2 = (-b+np.sqrt(r))/(2*a)

left = np.ceil(min([sol1, sol2]))
right = np.floor(max([sol1, sol2]))

nb_holds =  int(right-left+1)

print('Solution: ', nb_holds)

t2= time.time()
print('running time:', (t2-t1), 'ms')