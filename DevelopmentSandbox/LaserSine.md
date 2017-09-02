
# Laser Sine Tests

## Test Setup

# Code:


```python
import GCode
import GRBL
import numpy as np
from uuid import uuid4
import os
import sys
from time import sleep

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
    program.G0(X=0)
    return program
```

    ok
    Laser Mode: 1.0



```python
X = np.arange(0, 2*4*np.pi*10, 1)
test_run = GCode.GCode()
test_run+=init(feed=500)
test_run.G0(X=X[0])
test_run.M4(S=255)
for x in X:
    y = 20*np.sin(x/10)
    # Keep GRBL happy.
    x = np.round(x, 4)
    y = np.round(y, 4)
    
    test_run.G1(X=x, Y=y)
test_run+=end()
```


```python
gcode_file = "LaserSine.gcode"
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




    ['G21', 'G90', 'G92 Z0 Y0 X0', 'G1 F500', 'G0 X0.0']




```python
try:
    cnc.run(test_run)
except KeyboardInterrupt as error:
    print("Feed Hold")
    cnc.cmd("!")
    while 1:
        try:
            cnc.reset()
            break;
        except:
            sleep(2)
    print("^C")
```


```python
shift = GCode.GCode()
shift.G91()
shift.G0(X=np.round(10*np.pi/5, 4))
shift.G90()
```


```python
cnc.run(shift)
```




    0.31099891662597656


