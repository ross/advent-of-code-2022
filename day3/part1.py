#!/usr/bin/env python3

from sys import stdin

ord_a = ord('a') - 1
ord_A = ord('A') - 27

total = 0
for row in stdin:
    row = row.strip()
    n = len(row)
    divider = int(n / 2)
    compartment_1 = set(row[:divider])
    compartment_2 = set(row[divider:])
    # there's only one duplicated item
    dup = list(compartment_1 & compartment_2)[0]
    if dup <= 'Z':
        # uppercase
        priority = ord(dup) - ord_A
    else:
        # lowercase
        priority = ord(dup) - ord_a
    total += priority

print(total)
