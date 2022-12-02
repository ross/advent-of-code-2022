#!/usr/bin/env python3

from sys import stdin

precident = {
    # rock
    1: 3,
    # paper
    2: 1,
    # scissors
    3: 2,
}

ord_a = ord('A') - 1
ord_x = ord('X') - 1

total = 0
for row in stdin:
    opp, you = row.strip().split()
    opp = ord(opp) - ord_a
    you = ord(you) - ord_x
    if opp == you:
        # played the same, tie
        score = 3
    elif precident[you] == opp:
        # you won
        score = 6
    else:
        score = 0
    total += score + you

print(total)
