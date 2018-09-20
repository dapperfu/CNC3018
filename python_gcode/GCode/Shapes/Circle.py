# -*- coding: utf-8 -*-

import numpy as np

from .. import Line


class Circle(Line):
    def __init__(
        self, center=(0,0), radius=10, clockwise=True, *args, **kwargs
    ):
        self.len_side = len_side
        self.origin = origin

        kwargs["points"] = self._points

        super().__init__(*args, **kwargs)

    @property
    def _points(self):
        return np.array(
            [
                [self.origin[0], self.origin[1]],
                [self.origin[0] + self.len_side, self.origin[1]],
                [
                    self.origin[0] + self.len_side,
                    self.origin[1] + self.len_side,
                ],
                [self.origin[0], self.origin[1] + self.len_side],
                [self.origin[0], self.origin[1]],
            ]
        )

    def generate_gcode(self):
        self.points = self._points
        super().generate_gcode()

    @property
    def _cls(self):
        return self.__class__.__name__

    def __repr__(self):
        return "{}<O={}, L={}>".format(self._cls, self.origin, self.len_side)
