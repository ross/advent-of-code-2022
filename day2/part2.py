#!/usr/bin/env python3

from sys import stdin

# precompute the ordinal values of A and X, minus one so that the results will
# be 1 through 3
ord_a = ord('A') - 1

total = 0
for row in stdin:
    opp, outcome = row.strip().split()
    # shift things to be 1-3
    opp = ord(opp) - ord_a
    if outcome == 'X':
        # lose, we need to play 1 less than our opponent
        you = opp - 1
        # if that results in a 0 we need to wrap around to scisors
        if you == 0:
            you = 3
        score = 0
    elif outcome == 'Y':
        # draw, just play what they played
        you = opp
        score = 3
    else:
        # win, we need to play one more than our opponent
        you = opp + 1
        # if that results in a 4 we need to wrap around to rock
        if you == 4:
            you = 1
        score = 6
    # this round's result is the score plus what you played
    total += score + you

print(total)
