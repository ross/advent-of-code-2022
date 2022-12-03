#!/usr/bin/env python3

from sys import stdin

ord_a = ord('a') - 1
ord_A = ord('A') - 27

total = 0
group = []
for row in stdin:
    row = row.strip()
    # add a set of the contents of this pack to the running group
    group.append(set(row))
    if len(group) == 3:
        # we now have 3 elves, time to find the badge, the union of the 3 elves
        # sets of contents provides the common item
        common = list(group[0] & group[1] & group[2])[0]
        # convert it to a priority
        if common <= 'Z':
            # uppercase
            priority = ord(common) - ord_A
        else:
            # lowercase
            priority = ord(common) - ord_a
        total += priority
        # start a new group
        group = []

print(total)
