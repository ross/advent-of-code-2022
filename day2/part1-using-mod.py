#!/usr/bin/env python3

from sys import stdin

# precompute the ordinal values of A and X to make them 0 through 2
ord_a = ord('A')
ord_x = ord('X')

total = 0
for row in stdin:
    opp, you = row.strip().split()
    # shift things to be 0-2
    opp = ord(opp) - ord_a
    you = ord(you) - ord_x
    if opp == you:
        # played the same, tie
        score = 3
    elif ((opp + 1) % 3) == you:
        # you won, you played the "next" after your opponent (with wrapping)
        score = 6
    else:
        # you lost, your opponent played the "next" value (with wrapping)
        score = 0
    # this round's result is the score plus what you played
    total += score + you + 1

print(total)
