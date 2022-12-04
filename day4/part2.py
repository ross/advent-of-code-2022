#!/usr/bin/env python3

from sys import stdin

contained = 0
for row in stdin:
    row = row.strip()
    a, b = row.split(',')
    a_start, a_end = (int(v) for v in a.split('-'))
    b_start, b_end = (int(v) for v in b.split('-'))
    if a_start <= b_start and b_start <= a_end:
        # b starts at or after a and before a ends, there's some overlap
        contained += 1
    elif b_start <= a_start and a_start <= b_end:
        # a starts at or after b and before b ends, there's some overlap
        contained += 1

print(contained)
