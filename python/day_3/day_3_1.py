import re

with open('./input.txt', 'r') as f:
    data = f.read()

if data[-1]=='\n':
    data = data[:-1]

lines = data.split('\n')

valid_parts = []
for nb_line, line in enumerate(lines):
    # break
    # detect numbers
    numbers_iter = re.finditer(f"(\d+)", line)
    for m in numbers_iter:
        # break
        number = int(m.group())
        len_number = len(m.group())
        starting_pos = m.start()
        ending_pos = starting_pos+len_number
        # print(m.start(), m.group())

        # find sourrounding characters
        chars = ""
        if (nb_line>0):
            chars+=lines[nb_line-1][max(0,starting_pos-1):min(ending_pos+1, len(line)-1)]
        
        if (starting_pos>0):
            chars+=line[starting_pos-1]
        if (ending_pos < len(lines)-1):
            chars+=line[ending_pos]

        if (nb_line<len(lines)-1):
            chars+=lines[nb_line+1][max(starting_pos-1,0):min(ending_pos+1, len(line)-1)]

        is_symbol = re.search(r'([^.\d])', chars)

        if is_symbol is not None:
            # found a special char
            valid_parts.append(number)

solution = sum(valid_parts)
print('Solution: ', solution)