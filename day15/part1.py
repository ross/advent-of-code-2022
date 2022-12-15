#!/usr/bin/env python

from sys import argv, stdin
import re


def manhattan_distance(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)


class Sensor:
    def __init__(self, sensor_x, sensor_y, beacon_x, beacon_y):
        self.x = int(sensor_x)
        self.y = int(sensor_y)
        self.beacon_x = int(beacon_x)
        self.beacon_y = int(beacon_y)
        self.distance = manhattan_distance(
            self.x, self.y, self.beacon_x, self.beacon_y
        )

    def __repr__(self):
        return f'<{self.x:6d}, {self.y:6d}> -> {self.beacon_x:6d}, {self.beacon_y:6d}'


class Cave:
    def __init__(self, sensors):
        self.sensors = sensors

    def unavailable(self, y):
        cells = set()
        for sensor in self.sensors:
            # how far is the sensor from the desired row
            dy = abs(sensor.y - y)
            if dy > sensor.distance:
                # we're not interested in this one
                continue
            # how big a swath will it make in this row
            dx = sensor.distance - dy
            # mark the cells, both forward and back from the sensor's x
            for dx in range(dx + 1):
                cells.add(sensor.x - dx)
                cells.add(sensor.x + dx)

        # remove any marked cells that are actually beacons or sensors
        for sensor in self.sensors:
            if sensor.y == y:
                cells.discard(sensor.x)
            if sensor.beacon_y == y:
                cells.discard(sensor.beacon_x)

        # the number of cells remaining is the marked count we're after
        return len(cells)


parser = re.compile(
    r'x=(?P<sensor_x>-?\d+), y=(?P<sensor_y>-?\d+):.* x=(?P<beacon_x>-?\d+), y=(?P<beacon_y>-?\d+)'
)
sensors = []
for line in stdin:
    match = parser.search(line)
    sensor = Sensor(**match.groupdict())
    sensors.append(sensor)

cave = Cave(sensors)
unavailable = cave.unavailable(int(argv[1]))
print(f'unavailable={unavailable}')
