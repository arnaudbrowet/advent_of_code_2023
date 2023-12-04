import re

with open('./input.txt', 'r') as f:
    data = f.read()

if data[-1]=='\n':
    data = data[:-1]

scores = []

cards = data.split('\n')
for card in cards:
    # break
    card_id, card_content = card.split(': ')
    winning, draws = card_content.split(' | ')

    winning_num = winning.split()
    draws_num = draws.split()

    nb_win = 0
    for digit in draws_num:
        if digit in winning_num:
            nb_win +=1

    if nb_win>0:
        scores.append(2**(nb_win-1))



solution = sum(scores)
print('Solution: ', solution)