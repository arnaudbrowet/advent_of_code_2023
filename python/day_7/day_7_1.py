# import re
import numpy as np
import functools

# input_file = "small_input.txt"
input_file = "input.txt"
with open(f'./{input_file}', 'r') as f:
    data = f.read()

if data[-1]=='\n':
    data = data[:-1]


card_to_score = {
    '2' : 0,
    '3' : 1,
    '4' : 2,
    '5' : 3,
    '6' : 4,
    '7' : 5,
    '8' : 6,
    '9' : 7,
    'T' : 8,
    'J' : 9,
    'Q' : 10,
    'K' : 11,
    'A' : 12,
    
}
base_hands = [h.split() for h in data.split('\n')]

def parse_hand(hand):
    cards = list(hand)
    unique, base_counts = np.unique(cards, return_counts=True)
    
    counts = np.sort(base_counts)[::-1]
    hand_value = 0
    if (counts[0]==5): hand_value= 6
    if (counts[0]==4): hand_value= 5
    if (counts[0]==3 and counts[1]==2): hand_value= 4
    if (counts[0]==3 and counts[1]==1): hand_value= 3
    if (counts[0]==2 and counts[1]==2): hand_value= 2
    if (counts[0]==2 and counts[1]==1): hand_value= 1
    
    return [hand_value] + [card_to_score[c] for c in cards]

    
hands = [{'hand':h[0], 'bid':int(h[1]), "scores": parse_hand(h[0]) }for h in base_hands]

def compare_hands(hand1, hand2):
    s1 = hand1['scores']
    s2 = hand2['scores']
    ind = 0
    while ind < len(s1):
        if s1[ind]<s2[ind]:
            return -1
        if s1[ind]>s2[ind]:
            return 1
        ind +=1
        
hands.sort(key=functools.cmp_to_key(compare_hands))


winnings= [(i+1)*h['bid'] for i,h in enumerate(hands)]

    
    

solution = int(sum(winnings))
print('Solution: ', solution)