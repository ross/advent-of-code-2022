#!/usr/bin/env python3

from sys import stdin

for row in stdin:
    # remove the trailing newline
    row = row.strip()
    # start from the 4th char, go until the end
    for i in range(4, len(row)):
        # our canidate is the 4 characters ending in i
        candidate = row[i - 4 : i]
        # create a set from the 4 canidate characters
        unique = set(candidate)
        # if there's more than 3 items in the set there's 4 unique characters
        # in the canidate
        if len(unique) > 3:
            # i is the desired location
            print(i)
            break
