#!/usr/bin/env python3

from sys import stdin

overlaps = 0
for row in stdin:
    row = row.strip()
    # break into two parts
    a, b = row.split(',')
    # find the first's start and end
    a_start, a_end = (int(v) for v in a.split('-'))
    # find the seconds start and end
    b_start, b_end = (int(v) for v in b.split('-'))
    if a_start <= b_start and b_start <= a_end:
        # b starts at or after a and before a ends, there's some overlap
        overlaps += 1
    elif b_start <= a_start and a_start <= b_end:
        # a starts at or after b and before b ends, there's some overlap
        overlaps += 1

print(overlaps)
