#!/usr/bin/env python3

from sys import stdin

for row in stdin:
    # remove the trailing newline
    row = row.strip()
    # start from the 14th char, go until the end
    for i in range(14, len(row)):
        # our canidate is the 14 characters ending in i
        candidate = row[i - 14 : i]
        # create a set from the 14 canidate characters
        unique = set(candidate)
        # if there's more than 13 items in the set there's 4 unique characters
        # in the canidate
        if len(unique) > 13:
            # i is the desired location
            print(i)
            break
