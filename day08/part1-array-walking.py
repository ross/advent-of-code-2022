#!/usr/bin/env python3

from sys import stdin

# create 2d lists from input strings, first will hold the tree heights
trees = []
# second will mark whether we've seen this tree before (from another direction)
seen = []
for row in stdin:
    row = row.strip()
    row = [int(v) for v in row]
    trees.append(row)
    # initial we need False for each tree, this creates the correct length array
    # of Falses
    seen.append([False] * len(row))

n_y = len(trees)
n_x = len(trees[0])

visible = 0
# for each row
for y in range(n_y):
    row = trees[y]
    # for each col left to right
    tallest = -1
    for x in range(n_x):
        tree = row[x]
        if tree > tallest:
            # this tree is taller than any we've seen in this row from the left
            tallest = tree
            # any tree we see will be for the first time here
            visible += 1
            # mark it seen
            seen[y][x] = True
    # for each col right to left
    tallest = -1
    for x in range(n_x - 1, -1, -1):
        tree = row[x]
        if tree > tallest:
            # this tree is taller than any we've seen in this row from the right
            tallest = tree
            if not seen[y][x]:
                # we haven't seen this tree before from another direction
                visible += 1
            # and mark it visible
            seen[y][x] = True

# for each col
for x in range(n_x):
    # for each row top to bottom
    tallest = -1
    for y in range(n_y):
        tree = trees[y][x]
        if tree > tallest:
            # this tree is taller than any we've seen in this column from th top
            tallest = tree
            if not seen[y][x]:
                # we haven't seen this tree before from another direction
                visible += 1
            # and mark it visible
            seen[y][x] = True
    # for each row bottom to top
    tallest = -1
    for y in range(n_y - 1, -1, -1):
        tree = trees[y][x]
        if tree > tallest:
            # this tree is taller than any we've seen in this column from the
            # bottom
            tallest = tree
            if not seen[y][x]:
                # we haven't seen this tree before from another direction
                visible += 1
            # and mark it visible
            seen[y][x] = True

print(visible)
