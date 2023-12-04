import re

with open('./input.txt', 'r') as f:
    data = f.read()

if data[-1]=='\n':
    data = data[:-1]

lines = data.split('\n')



def detect(input_line, start, direction):
    num = ''
    p = start + direction
    
    # print(start, direction)
    # print(p, char)
    while p>=0 and p<len(input_line):
        char = input_line[p]

        if not char.isdigit():
            break

        if direction>0:
            num += char
        else:
            num = char + num

        # print(num)
        
        p = p + direction
        
        # print(p, char)

    return num


gears = []

for nb_line, line in enumerate(lines):
    # break
    # detect *
    stars_iter = re.finditer(f"(\*)", line)

    for star in stars_iter:
        # break
        pos = star.start()
        # print(pos)

        numbers=[]
        #top 
        if (nb_line>0):
            cur_line = lines[nb_line-1]
            mid = cur_line[pos]

            if mid.isdigit():
                l = detect(cur_line, pos, -1)
                r = detect(cur_line, pos, 1)
                numbers.append( int( l+mid+r))
                
            else:
                left = cur_line[pos-1]
                if left.isdigit():
                    l = detect(cur_line, pos-1, -1)
                    numbers.append( int( l+left))
                
                right = cur_line[pos+1]
                if right.isdigit():
                    r = detect(cur_line, pos+1, 1)
                    numbers.append( int( right+r))
        
        # left side
        l = detect(line, pos, -1)
        if len(l)>0:
            numbers.append(int(l))
        # right side
        r = detect(line, pos, 1)
        if len(r)>0:
            numbers.append(int(r))

        #bottom 
        if (nb_line<len(lines)-1):
            cur_line = lines[nb_line+1]
            mid = cur_line[pos]

            if mid.isdigit():
                l = detect(cur_line, pos, -1)
                r = detect(cur_line, pos, 1)
                numbers.append( int( l+mid+r))
                
            else:
                left = cur_line[pos-1]
                if left.isdigit():
                    l = detect(cur_line, pos-1, -1)
                    numbers.append( int( l+left))
                
                right = cur_line[pos+1]
                if right.isdigit():
                    r = detect(cur_line, pos+1, 1)
                    numbers.append( int( right+r))
        
        # print(nb_line, pos)
        # print(numbers)
        if (len(numbers)==2):
            gears.append(numbers[0]*numbers[1])


        

solution = sum(gears)
print('Solution: ', solution)