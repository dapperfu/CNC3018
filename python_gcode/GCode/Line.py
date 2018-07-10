# -*- coding: utf-8 -*-
import numpy as np

from .GCode import GCode

a = 10  # [mm]. Shorest leg of the triangle will be 10 mm, 1 cm, 0.01 m long.
default_feed = 300  # mm/n
default_power = 150  # [dimensionless]


"""
# Default Line

Sane default for the ```draw_line``` command. Designed so that ```draw_line()``` does something that is easly measureable.

Draw a 30-60-90 triangle.

From: https://www.dummies.com/education/math/calculus/how-to-work-with-30-60-90-degree-triangles.

If you look at the 30:60:90-degree triangle in radians, it translates to the following:

$$\frac{\pi}{6}:\frac{\pi}{3}:\frac{\pi}{2}$$

In any 30-60-90 triangle, you see the following:

- The shortest leg is across from the 30-degree angle.

- The length of the hypotenuse is always two times the length of the shortest leg.

- You can find the long leg by multiplying the short leg by the square root of 3.

If you know one side of a 30-60-90 triangle, you can find the other two by using shortcuts. Here are the three situations you come across when doing these calculations:

- **Type 1**: You know the short leg (the side across from the 30-degree angle). Double its length to find the hypotenuse. You can multiply the short side by the square root of 3 to find the long leg.

- **Type 2**: You know the hypotenuse. Divide the hypotenuse by 2 to find the short side. Multiply this answer by the square root of 3 to find the long leg.

- **Type 3**: You know the long leg (the side across from the 60-degree angle). Divide this side by the square root of 3 to find the short side. Double that figure to find the hypotenuse.

Let:

- a: Shortest Side. Opposite 30$^o$ ($\frac{\pi}{6}$)
"""
default_points = np.array(
    [
        [0, 0],  # Start at origin.
        [a * np.sqrt(3), 0],  # Draw long side along X axis.
        [a * np.sqrt(3), a],  # Draw the short side parallel to Y axis.
        [0, 0],  # Return to origin. Draw hypotenuse.
    ]
)

def HorzLine(X0=0, Xf=10, Y=0, n_points=2):
    p = np.linspace(X0, Xf, n_points, endpoint=True)
    line_points = np.array([
        p,
        Y*np.ones(p.shape),
    ])
    return line_points.transpose()

def VertLine(X=0, Y0=0, Yf=10, n_points=2):
    p = np.linspace(Y0, Yf, n_points, endpoint=True)
    line_points = np.array([
        X*np.ones(p.shape),
        p,
    ])
    return line_points.transpose()


class Line(GCode):
    def __init__(
        self,
        points=default_points,
        feed=default_feed,
        power=default_power,
        dynamic_power=True,
        *args,
        **kwargs,
    ):
        self.points = points.squeeze()
        self.feed = feed
        self.power = power
        self.dynamic_power = dynamic_power

        super().__init__(*args, **kwargs)

        self.generate_gcode()
        
    def reverse(self):
        flip_n_reverseit = np.eye(self.points.shape[0])[:, ::-1]
        self.points=np.matmul(flip_n_reverseit, self.points)

    @property
    def X(self):
        return self.points[:, 0]

    @property
    def Y(self):
        return self.points[:, 1]

    @property
    def x_0(self):
        return self.points[0, 0]

    @property
    def y_0(self):
        return self.points[0, 1]

    @property
    def x_f(self):
        return self.points[-1, 0]

    @property
    def y_f(self):
        return self.points[-1, 1]

    def __repr__(self):
        return "Line<len={}mm, feed={}, power={}>".format(
            self.dist, self.feed, self.power
        )

    @property
    def dists(self):
        """ Distances traveled in each line segment """
        # For remaining points.
        dist_ = list()
        for idx in range(1, self.points.shape[0]):
            dX = self.points[idx][0] - self.points[idx - 1][0]
            dY = self.points[idx][1] - self.points[idx - 1][1]
            d = np.sqrt(np.power(dX, 2) + np.power(dY, 2))
            dist_.append(d)
        return dist_

    @property
    def dist(self):
        """ Total distance traveled. """
        return np.round(np.sum(self.dists), 5)

    @property
    def times(self):
        """ Amount of time spent drawing each line spegment.
        
        Does not take into consideration acceleration curves """
        rate = self.feed / 60  # [mm/s]
        return [dist / rate for dist in self.dists]

    @property
    def time(self):
        """ Total distance traveled. """
        return np.round(np.sum(self.times), 5)
    
    def set_power(self, power):
        self.power = power
    def set_points(self, points):
        self.points = points
    def set_feed(self, feed):
        self.feed = feed
    
    def generate_gcode(self):
        self.buffer = list()
        # Move to start of the line.
        self.G0(X=self.points[0, 0], Y=self.points[0, 1])

        # Set power.
        if self.dynamic_power:
            self.M4(S=self.power)
        else:
            self.M3(S=self.power)
            
        # For remaining points.
        for row_idx in range(1, self.points.shape[0]):
            self.G1(
                X=self.points[row_idx, 0],
                Y=self.points[row_idx, 1],
                F=self.feed,
            )
        self.M5()
