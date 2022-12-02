#!/usr/bin/env python3

from sys import stdin

ord_a = ord('A') - 1
ord_x = ord('X') - 1

total = 0
for row in stdin:
    opp, outcome = row.strip().split()
    opp = ord(opp) - ord_a
    outcome = ord(outcome) - ord_x
    if outcome == 1:
        # lose
        you = opp - 1
        if you == 0:
            you = 3
        score = 0
    elif outcome == 2:
        # draw
        you = opp
        score = 3
    else:
        # win
        you = opp + 1
        if you == 4:
            you = 1
        score = 6
    total += score + you

print(total)
