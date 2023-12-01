import re

# read data
with open('./input.txt', "r") as f:
    data = f.read()

data = data.lower()

# remove trailing line break
if data[-1]=="\n":
    data = data[:-1]

# remove all non digit characters
cleaned = re.sub(r"[^\d\n]", "", data) 

# extract first and last digit of each string
values = [entry[0] + entry[-1]  for entry in cleaned.split("\n")]

# compute the sum of values
solution = sum([int(v) for v in values])

print('Solution:', solution)