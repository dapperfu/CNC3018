# -*- coding: utf-8 -*-


import numpy as np

from .GCode import GCode


class Program(GCode):
    """ A GCode Program Object """

    def __init__(self, lines=list(), feed=120, *args, **kwargs):
        self.lines = lines
        self.feed = feed

        super().__init__(*args, **kwargs)
        
        self.generate_gcode()

    def setup(self):
        self.buffer = list()
        self.G21()  # Metric Units
        self.G90()  # Absolute positioning.
        
        self.G28()
        self.G0(F=self.feed)
        self.G1(F=self.feed)
        self.M3(
            S=1
        )  # Set laser power so that movement can be seen, but does nothing.
        self.G92(X=0, Y=0, Z=0)  # I wasn't joking.

    def teardown(self):
        self.M5()  # Power down laser.
        self.G28()  # Move home.
        # pushover("Laser is done.")

    def generate_gcode(self):
        self.setup()
        list(map(lambda line: line.generate_gcode(), self.lines))
        for line in self.lines:
            self.buffer.extend(line.buffer)
        self.teardown()

    @property
    def jog_dist(self):
        jog_dists = list()
        for idx in range(1, len(self.lines)):
            # Jog to new startpoint
            dX = self.lines[idx].x_0 - self.lines[idx - 1].x_f
            dY = self.lines[idx].y_0 - self.lines[idx - 1].y_f
            d = np.sqrt(np.power(dX, 2) + np.power(dY, 2))
            jog_dists.append(d)

        # G28 returns to 0, 0.
        dX = 0 - self.lines[idx].x_f
        dY = 0 - self.lines[idx].y_f
        d = np.sqrt(np.power(dX, 2) + np.power(dY, 2))
        jog_dists.append(d)
        return np.sum(jog_dists)

    @property
    def jog_time(self):
        """ Return time spent jogging """
        jog_rate = self.feed / 60  # [mm/s]
        return self.jog_dist / jog_rate  # [s]

    @property
    def laserin_dist(self):
        """ Distance, in mm, the line spends cutting. """
        laserin = [line.dist for line in self.lines]
        return np.cumsum(laserin)[-1]

    @property
    def laserin_time(self):
        """ Duration, in s, the line spends cutting. """
        laserin = [line.time for line in self.lines]
        return np.sum(laserin)

    @property
    def dist(self):
        return self.jog_dist + self.laserin_dist

    @property
    def time(self):
        return self.jog_time + self.laserin_time

    def __repr__(self):
        return "Program<lines={}, dist={:.2f}mm, t={:.2f}s>".format(len(self.lines), self.dist, self.time)
