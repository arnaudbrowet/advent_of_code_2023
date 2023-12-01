import re

# read data
with open('./input.txt', "r") as f:
    data = f.read()

data = data.lower()

# remove trailing line break
if data[-1]=="\n":
    data = data[:-1]

# number to string mapping
numbers={
"one":"1ne",
"two":"2wo",
"three":"3hree",
"four":"4our",
"five":"5ive",
"six":"6ix",
"seven":"7even",
"eight":"8ight",
"nine":"9ine",
}

# split a string & replace non digit character with zeros
split_with_zeros = lambda entry : [int(re.sub(r"[^\d]", "0", t)) for t in entry]

# convert a string to a number based on contained words
def parse_entry(entry):
    # remove digits
    non_digit_entry = re.sub(r"\d", "0", entry)
    non_digit_values = [0 for t in entry]
    
    for text, value in numbers.items():
        nv = non_digit_entry.replace(text, value)

        adder = split_with_zeros(nv)

        non_digit_values = [j + non_digit_values[i] for i,j in enumerate(adder)]

    sequence = ''.join([str(d) for d in non_digit_values])
    digit_entry = split_with_zeros(entry)
    
    result = [str(d + int(sequence[i])) for i, d in enumerate(digit_entry)]

    
    return ''.join(result).replace('0',"")
    

# split the data and convert
entries = data.split('\n')
converted = [parse_entry(entry) for entry in entries]

# extract first and last digit of each string
values = [entry[0] + entry[-1]  for entry in converted]

# compute the sum of values
solution = sum([int(v) for v in values])

print('Solution:', solution)

