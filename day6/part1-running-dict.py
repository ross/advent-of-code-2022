#!/usr/bin/env python3

from sys import stdin

# this supports multiple stream, one per line
for row in stdin:
    # remove the trailing newline
    row = row.strip()
    # characters we've seen and where we've most recently seen them
    seen = {}
    i = 0
    n = len(row)
    # indicates that we've seen a duplicate and thus are not considering
    # anything until we're past this point
    dup_until = 0
    while i < n:
        # grab our next character
        ch = row[i]
        # if we're far enough along to have a match
        if i > 3:
            # we need to consider the character that should be leaving this
            # round
            maybe_leaving = row[i - 4]
            # was it last seen at the point that's now leaving
            if seen[maybe_leaving] == i - 4:
                # yes, so remove it from seen
                del seen[maybe_leaving]
        # if we've already seen the current character we have a dup
        if ch in seen:
            # remember the point at which we saw the most recent dup, we can't
            # have a marker until we're past that point
            dup_until = seen[ch]
        # record that we've seen the current character
        seen[ch] = i
        # if we're not in the middle of a dup and we've seen 4 distinct
        # characters
        if i > dup_until and len(seen) > 3:
            # we have a marker
            print(i + 1)
            # we're done with this stream
            break
        i += 1
