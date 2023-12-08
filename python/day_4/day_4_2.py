import re

with open('./input.txt', 'r') as f:
    data = f.read()

if data[-1]=='\n':
    data = data[:-1]

scores = []

cards = data.split('\n')
nb_cards = [1 for c in cards]

for card_index, card in enumerate(cards):
    
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

    for add in range(nb_win):
        new_index = card_index+add+1
        if new_index < len(nb_cards):
            nb_cards[new_index] += nb_cards[card_index]



solution = sum(nb_cards)
print('Solution: ', solution)