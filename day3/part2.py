#!/usr/bin/env python3

from sys import stdin

ord_a = ord('a') - 1
ord_A = ord('A') - 27

total = 0
group = []
for row in stdin:
    row = row.strip()
    group.append(set(row))
    if len(group) == 3:
        common = list(group[0] & group[1] & group[2])[0]
        if common <= 'Z':
            # uppercase
            priority = ord(common) - ord_A
        else:
            # lowercase
            priority = ord(common) - ord_a
        total += priority
        group = []

print(total)
