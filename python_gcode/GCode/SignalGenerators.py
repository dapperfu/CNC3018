# -*- coding: utf-8 -*-
import numpy as np
import scipy.signal

def sine(t, A=1, f=1, D=0):
    """    
    t: time
    A: the amplitude, the peak deviation of the function from zero.
    f: the ordinary frequency, the number of oscillations (cycles) that occur each second of time.
    D: non-zero center amplitude
    """
    sine_ = A*np.sin(
        2 * np.pi * f * t
    ) + D
    return sine_
    
def cosine(t, A=1, f=1, D=0):
    """    
    t: time
    A: the amplitude, the peak deviation of the function from zero.
    f: the ordinary frequency, the number of oscillations (cycles) that occur each second of time.
    D: non-zero center amplitude
    """
    cos_ = A*np.sin(
        2 * np.pi * f * t
    ) + D
    return cos_

def square(t, A=1, f=1, D=0):
    """    
    t: time
    A: the amplitude, the peak deviation of the function from zero.
    f: the ordinary frequency, the number of oscillations (cycles) that occur each second of time.
    D: non-zero center amplitude
    """
    square_ = A*scipy.signal.square(
        2 * np.pi * f * t
    ) + D
    return square_

def sawtooth(t, A=1, f=1, D=0):
    """    
    t: time
    A: the amplitude, the peak deviation of the function from zero.
    f: the ordinary frequency, the number of oscillations (cycles) that occur each second of time.
    D: non-zero center amplitude
    """
    sawtooth_ = A*scipy.signal.sawtooth(
        2 * np.pi * f * t,
        width=1,
    ) + D
    return sawtooth_

def triangle(t, A=1, f=1, D=0):
    """    
    t: time
    A: the amplitude, the peak deviation of the function from zero.
    f: the ordinary frequency, the number of oscillations (cycles) that occur each second of time.
    D: non-zero center amplitude
    """
    triangle_ = A*scipy.signal.sawtooth(
        2 * np.pi * f * t,
        width=0.5,
    ) + D
    return triangle_

signal_generators = [sine, cosine, square, sawtooth, triangle]