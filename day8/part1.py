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

visible = 0
# rotating trees 90d clockwise, 4 times lets us look from all directions with
# code that only knows how to look left to right.
for _ in range(4):
    # for each row
    for y in range(len(trees)):
        row_trees = trees[y]
        row_seen = seen[y]
        tallest = -1
        # for each column
        for x in range(len(row_trees)):
            height = row_trees[x]
            # this tree is the tallest we've seen so far
            if height > tallest:
                # record that
                tallest = height
                # if we haven't counted it as visible before (from another
                # direction)
                if not row_seen[x]:
                    # count it now
                    visible += 1
                    # and mark it as seen
                    row_seen[x] = True

    # rotate the 2d arrays 90 degrees clockwise, so we'll be coming from
    # another direction on the next time around
    # See https://stackoverflow.com/a/8421412 for a thorough explination, we
    # have an extra tweak to convert the rows returned from zip as tuple into
    # lists
    trees = list(list(v) for v in zip(*trees[::-1]))
    seen = list(list(v) for v in zip(*seen[::-1]))

print(visible)
