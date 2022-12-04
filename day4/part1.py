#!/usr/bin/env python3

from sys import stdin

contained = 0
for row in stdin:
    row = row.strip()
    # break into two parts
    a, b = row.split(',')
    # find the first's start and end
    a_start, a_end = (int(v) for v in a.split('-'))
    # find the seconds start and end
    b_start, b_end = (int(v) for v in b.split('-'))
    if a_start <= b_start and b_start <= a_end and b_end <= a_end:
        # b is inside of or equal to a
        contained += 1
    elif b_start <= a_start and a_start <= b_end and a_end <= b_end:
        # a is inside of or equal to b
        contained += 1

print(contained)
