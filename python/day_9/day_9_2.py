import re

# input_file = "small_input.txt"
input_file = "input.txt"
with open(f'./{input_file}', 'r') as f:
    data = f.read()

if data[-1]=='\n':
    data = data[:-1]

sequences = data.split('\n')

predictions = []
for sequence in sequences:
    # break
    seq = [int(d) for d in sequence.split()]

    iterates = [seq]

    while True:
        if len(seq) ==1:
            raise Exception('invalid sequence length')
        
        if min(seq) ==0 and max(seq) == 0:
            break

        seq = [seq[i+1] - seq[i] for i in range(len(seq)-1)]

        iterates.append(seq)

    first_values = [s[0] for s in iterates]
    pred = 0
    for v in reversed(first_values):
        pred = v-pred

    predictions.append(pred)

solution = sum(predictions)
print('Solution: ', solution)