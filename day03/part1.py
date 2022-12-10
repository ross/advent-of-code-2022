#!/usr/bin/env python3

from sys import stdin

# shift a-z to the correct priority (1-26)
ord_a = ord('a') - 1
# shift A-Z to the correct priority (27-52)
ord_A = ord('A') - 27

total = 0
for row in stdin:
    row = row.strip()
    # n / 2 is the compartment divider
    n = len(row)
    divider = int(n / 2)
    # everything from 0 through divider is the first compartment
    compartment_1 = set(row[:divider])
    # everything from divider through the end is the second compartment
    compartment_2 = set(row[divider:])
    # there's only one duplicated item the union of the two sets finds it
    (dup,) = compartment_1 & compartment_2
    if dup <= 'Z':
        # uppercase
        priority = ord(dup) - ord_A
    else:
        # lowercase
        priority = ord(dup) - ord_a
    total += priority

print(total)
