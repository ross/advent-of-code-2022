#!/usr/bin/env python3

from sys import stdin


trees = []
for row in stdin:
    row = row.strip()
    row = [int(v) for v in row]
    trees.append(row)

inv_trees = list(list(v) for v in zip(*trees))


def look_out(run, height):
    if not run:
        # we were on an edge
        return 0
    for i, tree in enumerate(run):
        # run until we see a tree as tall as we are
        if tree >= height:
            break
    # then add one since we're zero indexed
    return i + 1


# for each tree
best = 0
for y in range(len(trees)):
    # we'll use the trees as read for left and right
    row = trees[y]
    for x in range(len(row)):
        # find the current tree's height
        height = row[x]

        # we'll use the inverse trees (columns are rows) for up and down,
        # we'll need to index with the column/x var of our current tree to get
        # the slice we're after
        inv_row = inv_trees[x]

        # to the left, everything before our column
        left = row[:x]
        left.reverse()
        left = look_out(left, height)

        # right, everythig after our column
        right = row[x + 1 :]
        right = look_out(right, height)

        # up, everything before our row
        up = inv_row[:y]
        up.reverse()
        up = look_out(up, height)

        # down, everything after our row
        down = inv_row[y + 1 :]
        down = look_out(down, height)

        score = left * right * up * down

        if score > best:
            best = score

print(best)
