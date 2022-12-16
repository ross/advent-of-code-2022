#!/usr/bin/env python

from sys import stdin
import re

parser = re.compile(
    r'(?P<_id>\w+) has .* rate=(?P<rate>\d+); .* valves? (?P<neighbors>.*)$'
)
print('digraph cave {')
for line in stdin:
    match = parser.search(line)
    id = match.group('_id')
    rate = match.group('rate')
    neighbors = match.group('neighbors').split(', ')
    print(f'  "{id}" [label="{id} ({rate})"];')
    for neighbor in neighbors:
        print(f'  "{id}" -> "{neighbor}";')
print('}')
