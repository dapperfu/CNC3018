
# Laser Cutting Tests

## Test Setup

# Code:


```python
import GCode
import GRBL
import numpy as np
from uuid import uuid4
import os
import sys

sys.path.append("..")
from utils import picture
```


```python
cnc = GRBL.GRBL(port="/dev/cnc_3018")
cnc.laser_mode = 1

print("Laser Mode: {}".format(cnc.laser_mode))

def init(feed = 100):
    program = GCode.GCode()
    program.G21() # Metric Units
    program.G90() # Relative positioning.
    program.G92(X=0, Y=0, Z=0) # Zero on where we put the workpiece
    program.G1(F=feed) 
    return program

def end():
    program = GCode.GCode()
    program.M5()
    return program
```

    ok
    Laser Mode: 1.0



```python
def laser_on(pwm=1):
    if int(pwm) != np.uint8(pwm):
        raise(Exception("UINT8! {}".format(pwm)))
    # Set minimal power setting to focus and position laser
    cnc.cmd("M3 S{:03d}".format(np.uint8(pwm)))
    cnc.cmd("G1 F10") # Laser On

def laser_off():
    cnc.cmd("M5") # Laser off
```


```python
def pulse(pulse_duration=100):
    prog = GCode.GCode()
    prog.M5()
    prog.G91()
    prog.G0(X=0)
    prog.M3(S=255)
    prog.G1(X=0)
    prog.G4(U=pulse_duration)
    prog.G0(X=0)
    prog.G90()
    prog.M5()
    return prog
```


```python
cnc.run(init()+pulse(100)+end())
```




    1.4474668502807617




```python
cnc.run(init()+pulse(500)+end())
```




    1.2418253421783447




```python
cnc.run(init()+pulse(1000)+end())
```




    1.2426557540893555




```python
test_run = GCode.GCode()
# TODO: Get z-axis probe.
test_run+=init(feed=200)
for i in range(3, 10):
    Xs = np.linspace(0,10,i)
    for X in Xs:
        test_run.G0(X=np.round(X, 4))
        test_run+=pulse(1)
```


```python
test_run
```




<b>G21</b> <i></i><br>
<b>G90</b> <i></i><br>
<b>G92</b> <i>X0 Y0 Z0</i><br>
<b>G1</b> <i>F200</i><br>
<b>G0</b> <i>X0.0</i><br>
<b>M5</b> <i></i><br>
<b>G91</b> <i></i><br>
<b>G0</b> <i>X0</i><br>
<b>M3</b> <i>S255</i><br>
<b>G1</b> <i>X0</i><br>
<b>G4</b> <i>U1</i><br>
<b>G0</b> <i>X0</i><br>
<b>G90</b> <i></i><br>
<b>M5</b> <i></i><br>
<b>G0</b> <i>X5.0</i><br>
<b>M5</b> <i></i><br>
<b>G91</b> <i></i><br>
<b>G0</b> <i>X0</i><br>
<b>M3</b> <i>S255</i><br>
<b>G1</b> <i>X0</i><br>
<b>G4</b> <i>U1</i><br>
<b>G0</b> <i>X0</i><br>
<b>G90</b> <i></i><br>
<b>M5</b> <i></i><br>
<b>G0</b> <i>X10.0</i><br>
<b>M5</b> <i></i><br>
<b>G91</b> <i></i><br>
<b>G0</b> <i>X0</i><br>
<b>M3</b> <i>S255</i><br>
<b>G1</b> <i>X0</i><br>
<b>G4</b> <i>U1</i><br>
<b>G0</b> <i>X0</i><br>
<b>G90</b> <i></i><br>
<b>M5</b> <i></i><br>
<b>G0</b> <i>X0.0</i><br>
<b>M5</b> <i></i><br>
<b>G91</b> <i></i><br>
<b>G0</b> <i>X0</i><br>
<b>M3</b> <i>S255</i><br>
<b>G1</b> <i>X0</i><br>
<b>G4</b> <i>U1</i><br>
<b>G0</b> <i>X0</i><br>
<b>G90</b> <i></i><br>
<b>M5</b> <i></i><br>
<b>G0</b> <i>X3.3333</i><br>
<b>M5</b> <i></i><br>
<b>G91</b> <i></i><br>
<b>G0</b> <i>X0</i><br>
<b>M3</b> <i>S255</i><br>
<b>G1</b> <i>X0</i><br>
<b>G4</b> <i>U1</i><br>
<b>G0</b> <i>X0</i><br>
<b>G90</b> <i></i><br>
<b>M5</b> <i></i><br>
<b>G0</b> <i>X6.6667</i><br>
<b>M5</b> <i></i><br>
<b>G91</b> <i></i><br>
<b>G0</b> <i>X0</i><br>
<b>M3</b> <i>S255</i><br>
<b>G1</b> <i>X0</i><br>
<b>G4</b> <i>U1</i><br>
<b>G0</b> <i>X0</i><br>
<b>G90</b> <i></i><br>
<b>M5</b> <i></i><br>
<b>G0</b> <i>X10.0</i><br>
<b>M5</b> <i></i><br>
<b>G91</b> <i></i><br>
<b>G0</b> <i>X0</i><br>
<b>M3</b> <i>S255</i><br>
<b>G1</b> <i>X0</i><br>
<b>G4</b> <i>U1</i><br>
<b>G0</b> <i>X0</i><br>
<b>G90</b> <i></i><br>
<b>M5</b> <i></i><br>
<b>G0</b> <i>X0.0</i><br>
<b>M5</b> <i></i><br>
<b>G91</b> <i></i><br>
<b>G0</b> <i>X0</i><br>
<b>M3</b> <i>S255</i><br>
<b>G1</b> <i>X0</i><br>
<b>G4</b> <i>U1</i><br>
<b>G0</b> <i>X0</i><br>
<b>G90</b> <i></i><br>
<b>M5</b> <i></i><br>
<b>G0</b> <i>X2.5</i><br>
<b>M5</b> <i></i><br>
<b>G91</b> <i></i><br>
<b>G0</b> <i>X0</i><br>
<b>M3</b> <i>S255</i><br>
<b>G1</b> <i>X0</i><br>
<b>G4</b> <i>U1</i><br>
<b>G0</b> <i>X0</i><br>
<b>G90</b> <i></i><br>
<b>M5</b> <i></i><br>
<b>G0</b> <i>X5.0</i><br>
<b>M5</b> <i></i><br>
<b>G91</b> <i></i><br>
<b>G0</b> <i>X0</i><br>
<b>M3</b> <i>S255</i><br>
<b>G1</b> <i>X0</i><br>
<b>G4</b> <i>U1</i><br>
<b>G0</b> <i>X0</i><br>
<b>G90</b> <i></i><br>
<b>M5</b> <i></i><br>
<b>G0</b> <i>X7.5</i><br>
<b>M5</b> <i></i><br>
<b>G91</b> <i></i><br>
<b>G0</b> <i>X0</i><br>
<b>M3</b> <i>S255</i><br>
<b>G1</b> <i>X0</i><br>
<b>G4</b> <i>U1</i><br>
<b>G0</b> <i>X0</i><br>
<b>G90</b> <i></i><br>
<b>M5</b> <i></i><br>
<b>G0</b> <i>X10.0</i><br>
<b>M5</b> <i></i><br>
<b>G91</b> <i></i><br>
<b>G0</b> <i>X0</i><br>
<b>M3</b> <i>S255</i><br>
<b>G1</b> <i>X0</i><br>
<b>G4</b> <i>U1</i><br>
<b>G0</b> <i>X0</i><br>
<b>G90</b> <i></i><br>
<b>M5</b> <i></i><br>
<b>G0</b> <i>X0.0</i><br>
<b>M5</b> <i></i><br>
<b>G91</b> <i></i><br>
<b>G0</b> <i>X0</i><br>
<b>M3</b> <i>S255</i><br>
<b>G1</b> <i>X0</i><br>
<b>G4</b> <i>U1</i><br>
<b>G0</b> <i>X0</i><br>
<b>G90</b> <i></i><br>
<b>M5</b> <i></i><br>
<b>G0</b> <i>X2.0</i><br>
<b>M5</b> <i></i><br>
<b>G91</b> <i></i><br>
<b>G0</b> <i>X0</i><br>
<b>M3</b> <i>S255</i><br>
<b>G1</b> <i>X0</i><br>
<b>G4</b> <i>U1</i><br>
<b>G0</b> <i>X0</i><br>
<b>G90</b> <i></i><br>
<b>M5</b> <i></i><br>
<b>G0</b> <i>X4.0</i><br>
<b>M5</b> <i></i><br>
<b>G91</b> <i></i><br>
<b>G0</b> <i>X0</i><br>
<b>M3</b> <i>S255</i><br>
<b>G1</b> <i>X0</i><br>
<b>G4</b> <i>U1</i><br>
<b>G0</b> <i>X0</i><br>
<b>G90</b> <i></i><br>
<b>M5</b> <i></i><br>
<b>G0</b> <i>X6.0</i><br>
<b>M5</b> <i></i><br>
<b>G91</b> <i></i><br>
<b>G0</b> <i>X0</i><br>
<b>M3</b> <i>S255</i><br>
<b>G1</b> <i>X0</i><br>
<b>G4</b> <i>U1</i><br>
<b>G0</b> <i>X0</i><br>
<b>G90</b> <i></i><br>
<b>M5</b> <i></i><br>
<b>G0</b> <i>X8.0</i><br>
<b>M5</b> <i></i><br>
<b>G91</b> <i></i><br>
<b>G0</b> <i>X0</i><br>
<b>M3</b> <i>S255</i><br>
<b>G1</b> <i>X0</i><br>
<b>G4</b> <i>U1</i><br>
<b>G0</b> <i>X0</i><br>
<b>G90</b> <i></i><br>
<b>M5</b> <i></i><br>
<b>G0</b> <i>X10.0</i><br>
<b>M5</b> <i></i><br>
<b>G91</b> <i></i><br>
<b>G0</b> <i>X0</i><br>
<b>M3</b> <i>S255</i><br>
<b>G1</b> <i>X0</i><br>
<b>G4</b> <i>U1</i><br>
<b>G0</b> <i>X0</i><br>
<b>G90</b> <i></i><br>
<b>M5</b> <i></i><br>
<b>G0</b> <i>X0.0</i><br>
<b>M5</b> <i></i><br>
<b>G91</b> <i></i><br>
<b>G0</b> <i>X0</i><br>
<b>M3</b> <i>S255</i><br>
<b>G1</b> <i>X0</i><br>
<b>G4</b> <i>U1</i><br>
<b>G0</b> <i>X0</i><br>
<b>G90</b> <i></i><br>
<b>M5</b> <i></i><br>
<b>G0</b> <i>X1.6667</i><br>
<b>M5</b> <i></i><br>
<b>G91</b> <i></i><br>
<b>G0</b> <i>X0</i><br>
<b>M3</b> <i>S255</i><br>
<b>G1</b> <i>X0</i><br>
<b>G4</b> <i>U1</i><br>
<b>G0</b> <i>X0</i><br>
<b>G90</b> <i></i><br>
<b>M5</b> <i></i><br>
<b>G0</b> <i>X3.3333</i><br>
<b>M5</b> <i></i><br>
<b>G91</b> <i></i><br>
<b>G0</b> <i>X0</i><br>
<b>M3</b> <i>S255</i><br>
<b>G1</b> <i>X0</i><br>
<b>G4</b> <i>U1</i><br>
<b>G0</b> <i>X0</i><br>
<b>G90</b> <i></i><br>
<b>M5</b> <i></i><br>
<b>G0</b> <i>X5.0</i><br>
<b>M5</b> <i></i><br>
<b>G91</b> <i></i><br>
<b>G0</b> <i>X0</i><br>
<b>M3</b> <i>S255</i><br>
<b>G1</b> <i>X0</i><br>
<b>G4</b> <i>U1</i><br>
<b>G0</b> <i>X0</i><br>
<b>G90</b> <i></i><br>
<b>M5</b> <i></i><br>
<b>G0</b> <i>X6.6667</i><br>
<b>M5</b> <i></i><br>
<b>G91</b> <i></i><br>
<b>G0</b> <i>X0</i><br>
<b>M3</b> <i>S255</i><br>
<b>G1</b> <i>X0</i><br>
<b>G4</b> <i>U1</i><br>
<b>G0</b> <i>X0</i><br>
<b>G90</b> <i></i><br>
<b>M5</b> <i></i><br>
<b>G0</b> <i>X8.3333</i><br>
<b>M5</b> <i></i><br>
<b>G91</b> <i></i><br>
<b>G0</b> <i>X0</i><br>
<b>M3</b> <i>S255</i><br>
<b>G1</b> <i>X0</i><br>
<b>G4</b> <i>U1</i><br>
<b>G0</b> <i>X0</i><br>
<b>G90</b> <i></i><br>
<b>M5</b> <i></i><br>
<b>G0</b> <i>X10.0</i><br>
<b>M5</b> <i></i><br>
<b>G91</b> <i></i><br>
<b>G0</b> <i>X0</i><br>
<b>M3</b> <i>S255</i><br>
<b>G1</b> <i>X0</i><br>
<b>G4</b> <i>U1</i><br>
<b>G0</b> <i>X0</i><br>
<b>G90</b> <i></i><br>
<b>M5</b> <i></i><br>
<b>G0</b> <i>X0.0</i><br>
<b>M5</b> <i></i><br>
<b>G91</b> <i></i><br>
<b>G0</b> <i>X0</i><br>
<b>M3</b> <i>S255</i><br>
<b>G1</b> <i>X0</i><br>
<b>G4</b> <i>U1</i><br>
<b>G0</b> <i>X0</i><br>
<b>G90</b> <i></i><br>
<b>M5</b> <i></i><br>
<b>G0</b> <i>X1.4286</i><br>
<b>M5</b> <i></i><br>
<b>G91</b> <i></i><br>
<b>G0</b> <i>X0</i><br>
<b>M3</b> <i>S255</i><br>
<b>G1</b> <i>X0</i><br>
<b>G4</b> <i>U1</i><br>
<b>G0</b> <i>X0</i><br>
<b>G90</b> <i></i><br>
<b>M5</b> <i></i><br>
<b>G0</b> <i>X2.8571</i><br>
<b>M5</b> <i></i><br>
<b>G91</b> <i></i><br>
<b>G0</b> <i>X0</i><br>
<b>M3</b> <i>S255</i><br>
<b>G1</b> <i>X0</i><br>
<b>G4</b> <i>U1</i><br>
<b>G0</b> <i>X0</i><br>
<b>G90</b> <i></i><br>
<b>M5</b> <i></i><br>
<b>G0</b> <i>X4.2857</i><br>
<b>M5</b> <i></i><br>
<b>G91</b> <i></i><br>
<b>G0</b> <i>X0</i><br>
<b>M3</b> <i>S255</i><br>
<b>G1</b> <i>X0</i><br>
<b>G4</b> <i>U1</i><br>
<b>G0</b> <i>X0</i><br>
<b>G90</b> <i></i><br>
<b>M5</b> <i></i><br>
<b>G0</b> <i>X5.7143</i><br>
<b>M5</b> <i></i><br>
<b>G91</b> <i></i><br>
<b>G0</b> <i>X0</i><br>
<b>M3</b> <i>S255</i><br>
<b>G1</b> <i>X0</i><br>
<b>G4</b> <i>U1</i><br>
<b>G0</b> <i>X0</i><br>
<b>G90</b> <i></i><br>
<b>M5</b> <i></i><br>
<b>G0</b> <i>X7.1429</i><br>
<b>M5</b> <i></i><br>
<b>G91</b> <i></i><br>
<b>G0</b> <i>X0</i><br>
<b>M3</b> <i>S255</i><br>
<b>G1</b> <i>X0</i><br>
<b>G4</b> <i>U1</i><br>
<b>G0</b> <i>X0</i><br>
<b>G90</b> <i></i><br>
<b>M5</b> <i></i><br>
<b>G0</b> <i>X8.5714</i><br>
<b>M5</b> <i></i><br>
<b>G91</b> <i></i><br>
<b>G0</b> <i>X0</i><br>
<b>M3</b> <i>S255</i><br>
<b>G1</b> <i>X0</i><br>
<b>G4</b> <i>U1</i><br>
<b>G0</b> <i>X0</i><br>
<b>G90</b> <i></i><br>
<b>M5</b> <i></i><br>
<b>G0</b> <i>X10.0</i><br>
<b>M5</b> <i></i><br>
<b>G91</b> <i></i><br>
<b>G0</b> <i>X0</i><br>
<b>M3</b> <i>S255</i><br>
<b>G1</b> <i>X0</i><br>
<b>G4</b> <i>U1</i><br>
<b>G0</b> <i>X0</i><br>
<b>G90</b> <i></i><br>
<b>M5</b> <i></i><br>
<b>G0</b> <i>X0.0</i><br>
<b>M5</b> <i></i><br>
<b>G91</b> <i></i><br>
<b>G0</b> <i>X0</i><br>
<b>M3</b> <i>S255</i><br>
<b>G1</b> <i>X0</i><br>
<b>G4</b> <i>U1</i><br>
<b>G0</b> <i>X0</i><br>
<b>G90</b> <i></i><br>
<b>M5</b> <i></i><br>
<b>G0</b> <i>X1.25</i><br>
<b>M5</b> <i></i><br>
<b>G91</b> <i></i><br>
<b>G0</b> <i>X0</i><br>
<b>M3</b> <i>S255</i><br>
<b>G1</b> <i>X0</i><br>
<b>G4</b> <i>U1</i><br>
<b>G0</b> <i>X0</i><br>
<b>G90</b> <i></i><br>
<b>M5</b> <i></i><br>
<b>G0</b> <i>X2.5</i><br>
<b>M5</b> <i></i><br>
<b>G91</b> <i></i><br>
<b>G0</b> <i>X0</i><br>
<b>M3</b> <i>S255</i><br>
<b>G1</b> <i>X0</i><br>
<b>G4</b> <i>U1</i><br>
<b>G0</b> <i>X0</i><br>
<b>G90</b> <i></i><br>
<b>M5</b> <i></i><br>
<b>G0</b> <i>X3.75</i><br>
<b>M5</b> <i></i><br>
<b>G91</b> <i></i><br>
<b>G0</b> <i>X0</i><br>
<b>M3</b> <i>S255</i><br>
<b>G1</b> <i>X0</i><br>
<b>G4</b> <i>U1</i><br>
<b>G0</b> <i>X0</i><br>
<b>G90</b> <i></i><br>
<b>M5</b> <i></i><br>
<b>G0</b> <i>X5.0</i><br>
<b>M5</b> <i></i><br>
<b>G91</b> <i></i><br>
<b>G0</b> <i>X0</i><br>
<b>M3</b> <i>S255</i><br>
<b>G1</b> <i>X0</i><br>
<b>G4</b> <i>U1</i><br>
<b>G0</b> <i>X0</i><br>
<b>G90</b> <i></i><br>
<b>M5</b> <i></i><br>
<b>G0</b> <i>X6.25</i><br>
<b>M5</b> <i></i><br>
<b>G91</b> <i></i><br>
<b>G0</b> <i>X0</i><br>
<b>M3</b> <i>S255</i><br>
<b>G1</b> <i>X0</i><br>
<b>G4</b> <i>U1</i><br>
<b>G0</b> <i>X0</i><br>
<b>G90</b> <i></i><br>
<b>M5</b> <i></i><br>
<b>G0</b> <i>X7.5</i><br>
<b>M5</b> <i></i><br>
<b>G91</b> <i></i><br>
<b>G0</b> <i>X0</i><br>
<b>M3</b> <i>S255</i><br>
<b>G1</b> <i>X0</i><br>
<b>G4</b> <i>U1</i><br>
<b>G0</b> <i>X0</i><br>
<b>G90</b> <i></i><br>
<b>M5</b> <i></i><br>
<b>G0</b> <i>X8.75</i><br>
<b>M5</b> <i></i><br>
<b>G91</b> <i></i><br>
<b>G0</b> <i>X0</i><br>
<b>M3</b> <i>S255</i><br>
<b>G1</b> <i>X0</i><br>
<b>G4</b> <i>U1</i><br>
<b>G0</b> <i>X0</i><br>
<b>G90</b> <i></i><br>
<b>M5</b> <i></i><br>
<b>G0</b> <i>X10.0</i><br>
<b>M5</b> <i></i><br>
<b>G91</b> <i></i><br>
<b>G0</b> <i>X0</i><br>
<b>M3</b> <i>S255</i><br>
<b>G1</b> <i>X0</i><br>
<b>G4</b> <i>U1</i><br>
<b>G0</b> <i>X0</i><br>
<b>G90</b> <i></i><br>
<b>M5</b> <i></i>




```python
gcode_file = "LaserCut.gcode"
```


```python
test_run.save(gcode_file)

del test_run
test_run = GCode.GCode()

test_run.load(gcode_file)
```


```python
test_run.buffer[0:5]
```




    ['G21', 'G90', 'G92 X0 Y0 Z0', 'G1 F200', 'G0 X0.0']




```python
from time import sleep
```


```python
while 1:
    try:
        cnc.run(test_run)
        while 1:
            print(cnc.status)
            sleep(5)
    except KeyboardInterrupt as error:
        print("Feed Hold")
        cnc.cmd("!")
        while 1:
            try:
                cnc.reset()
                break;
            except:
                pass
        print("^C")
        break
    except:
        raise
```

    <Idle|MPos:10.000,0.000,0.000|Bf:15,127|FS:0,0|WCO:0.000,0.000,0.000>
    <Idle|MPos:10.000,0.000,0.000|Bf:15,127|FS:0,0|Ov:100,100,100>
    <Idle|MPos:10.000,0.000,0.000|Bf:15,127|FS:0,0>
    <Idle|MPos:10.000,0.000,0.000|Bf:15,127|FS:0,0>
    <Idle|MPos:10.000,0.000,0.000|Bf:15,127|FS:0,0>
    <Idle|MPos:10.000,0.000,0.000|Bf:15,127|FS:0,0>
    <Idle|MPos:10.000,0.000,0.000|Bf:15,127|FS:0,0>
    <Idle|MPos:10.000,0.000,0.000|Bf:15,127|FS:0,0>
    <Idle|MPos:10.000,0.000,0.000|Bf:15,127|FS:0,0>
    <Idle|MPos:10.000,0.000,0.000|Bf:15,127|FS:0,0>
    <Idle|MPos:10.000,0.000,0.000|Bf:15,127|FS:0,0|WCO:0.000,0.000,0.000>
    Feed Hold
    ^C

