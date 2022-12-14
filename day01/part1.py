#!/usr/bin/env python3

from sys import stdin

elves = []
calories = 0
for row in stdin:
    row = row.strip()
    if not row:
        # next elf, regardless of what they're carring
        elves.append(calories)
        calories = 0
    else:
        calories += int(row)
# last elve, doesn't matter if they're carrying anything we'll count zeros
elves.append(calories)

most = max(elves)

print(most)
