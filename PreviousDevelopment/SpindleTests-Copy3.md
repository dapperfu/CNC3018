
# Spindle Cutting Tests

## Objective
- Play around with 'OEM' WeiTol NJ3.2001 Cutters.

## Test Setup

- Oak Board 63mm x 300mm x 19mm
- WeiTol NJ3.2001.
- CSI3010SW dialed all the way up: 31.6V

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

print("Laser Mode: {}".format(cnc.laser_mode))

def init(feed = 10):
    program = GCode.GCode()
    program.G21() # Metric Units
    program.G91() # Absolute positioning.
    program.G1(F=feed) 
    return program

def end():
    program = GCode.GCode()
    return program
```

    Laser Mode: 0.0



```python
cnc.cmd("?")
cnc.reset()
```


```python
cnc.cmd("!")
status1 = cnc.cmd("?")
```


```python
cnc.cmd("!")
cnc.reset()
status2 = cnc.cmd("?")
```


```python
for status in [status1, status2]:
    status_clean = [s for s in status if s != "ok"]
    print(status_clean)
    status_clean2 = [s.strip("<>") for s in status_clean]
    if len(status_clean2) != 1:
        raise Exception(status_clean2)
    status = status_clean2[0]
    print(status)
    stati = status.split("|")
    print(stati)
    print("")
```

    ['<Hold:0|MPos:-128.925,0.000,0.800|Bf:15,125|FS:0,0|WCO:0.000,0.000,0.000>']
    Hold:0|MPos:-128.925,0.000,0.800|Bf:15,125|FS:0,0|WCO:0.000,0.000,0.000
    ['Hold:0', 'MPos:-128.925,0.000,0.800', 'Bf:15,125', 'FS:0,0', 'WCO:0.000,0.000,0.000']
    
    ['<Idle|MPos:-128.925,0.000,0.800|Bf:15,127|FS:0,0|WCO:0.000,0.000,0.000>']
    Idle|MPos:-128.925,0.000,0.800|Bf:15,127|FS:0,0|WCO:0.000,0.000,0.000
    ['Idle', 'MPos:-128.925,0.000,0.800', 'Bf:15,127', 'FS:0,0', 'WCO:0.000,0.000,0.000']
    



```python
def test_program(feed=10):
    prog = GCode.GCode()
    prog.M3(S=10000)
    dZ = -0.1
    dX = 10
    X = 0
    Z = 0
    for loops in range(20):
        prog.G1(Z=dZ, F=1)
        prog.G1(X=dX, F=feed)
        X+=dX
        Z+=dZ
    prog.M3(S=0)
    prog.G0(Z=np.round(-Z, 4)) #TODO: Add this to core library.
    prog.G0(X=np.round(-X, 4))
    prog.G0(Z=2)
    return prog
```


```python
test_run = GCode.GCode()
# TODO: Get z-axis probe.
test_run+=init()
for XFeed in [50]:
    test_run += test_program(feed=XFeed)
```


```python
gcode_file = "SpindleTests-Copy3.gcode"
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




    ['G21', 'G91', 'G1 F10', 'M3 S10000', 'G1 Z-0.1 F1']




```python
picture()
```


![jpeg](SpindleTests-Copy3_files/SpindleTests-Copy3_14_0.jpeg)



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

    <Run|MPos:71.075,0.000,-0.521|Bf:12,127|FS:246,0|Ov:100,100,100>



    ---------------------------------------------------------------------------

    NameError                                 Traceback (most recent call last)

    <ipython-input-12-13835fa88bf3> in <module>()
          4         while 1:
          5             print(cnc.status)
    ----> 6             sleep(5)
          7     except KeyboardInterrupt as error:
          8         print("Feed Hold")


    NameError: name 'sleep' is not defined



```python
cnc.reset()
```


```python
picture()
```


![jpeg](SpindleTests-Copy3_files/SpindleTests-Copy3_18_0.jpeg)


# Test Aborted.

Cuts were way too aggressive.
