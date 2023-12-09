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

    prediction = sum([ s[-1] for s in iterates])

    predictions.append(prediction)

solution = sum(predictions)
print('Solution: ', solution)