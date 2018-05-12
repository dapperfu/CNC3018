
# Spindle Cutting Tests

## Objective
- Play around with Dremel High Speed Cutter 115 in the ER11 spindle

## Test Setup

- Oak Board 63mm x 300mm x 19mm
- Dremel High Speed Cutter "Carving / Engraving" 115.
- CSI3010SW dialed all the way up.

# Code:


```python
import GCode
import GRBL
import numpy as np
from utils import picture
from uuid import uuid4
import os

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

    Laser Mode: None



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

    ['<Hold:0|MPos:-137.293,0.000,1.000|Bf:15,125|FS:0,0|Ov:100,100,100>']
    Hold:0|MPos:-137.293,0.000,1.000|Bf:15,125|FS:0,0|Ov:100,100,100
    ['Hold:0', 'MPos:-137.293,0.000,1.000', 'Bf:15,125', 'FS:0,0', 'Ov:100,100,100']
    
    ['<Idle|MPos:-137.293,0.000,1.000|Bf:15,127|FS:0,0|WCO:0.000,0.000,0.000>']
    Idle|MPos:-137.293,0.000,1.000|Bf:15,127|FS:0,0|WCO:0.000,0.000,0.000
    ['Idle', 'MPos:-137.293,0.000,1.000', 'Bf:15,127', 'FS:0,0', 'WCO:0.000,0.000,0.000']
    



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
test_program()
```




<b>M3</b> <i>S10000</i><br>
<b>G1</b> <i>Z-0.1 F1</i><br>
<b>G1</b> <i>X10 F10</i><br>
<b>G1</b> <i>Z-0.1 F1</i><br>
<b>G1</b> <i>X10 F10</i><br>
<b>G1</b> <i>Z-0.1 F1</i><br>
<b>G1</b> <i>X10 F10</i><br>
<b>G1</b> <i>Z-0.1 F1</i><br>
<b>G1</b> <i>X10 F10</i><br>
<b>G1</b> <i>Z-0.1 F1</i><br>
<b>G1</b> <i>X10 F10</i><br>
<b>G1</b> <i>Z-0.1 F1</i><br>
<b>G1</b> <i>X10 F10</i><br>
<b>G1</b> <i>Z-0.1 F1</i><br>
<b>G1</b> <i>X10 F10</i><br>
<b>G1</b> <i>Z-0.1 F1</i><br>
<b>G1</b> <i>X10 F10</i><br>
<b>G1</b> <i>Z-0.1 F1</i><br>
<b>G1</b> <i>X10 F10</i><br>
<b>G1</b> <i>Z-0.1 F1</i><br>
<b>G1</b> <i>X10 F10</i><br>
<b>G1</b> <i>Z-0.1 F1</i><br>
<b>G1</b> <i>X10 F10</i><br>
<b>G1</b> <i>Z-0.1 F1</i><br>
<b>G1</b> <i>X10 F10</i><br>
<b>G1</b> <i>Z-0.1 F1</i><br>
<b>G1</b> <i>X10 F10</i><br>
<b>G1</b> <i>Z-0.1 F1</i><br>
<b>G1</b> <i>X10 F10</i><br>
<b>G1</b> <i>Z-0.1 F1</i><br>
<b>G1</b> <i>X10 F10</i><br>
<b>G1</b> <i>Z-0.1 F1</i><br>
<b>G1</b> <i>X10 F10</i><br>
<b>G1</b> <i>Z-0.1 F1</i><br>
<b>G1</b> <i>X10 F10</i><br>
<b>G1</b> <i>Z-0.1 F1</i><br>
<b>G1</b> <i>X10 F10</i><br>
<b>G1</b> <i>Z-0.1 F1</i><br>
<b>G1</b> <i>X10 F10</i><br>
<b>G1</b> <i>Z-0.1 F1</i><br>
<b>G1</b> <i>X10 F10</i><br>
<b>M3</b> <i>S0</i><br>
<b>G0</b> <i>Z2.0</i><br>
<b>G0</b> <i>X-200</i><br>
<b>G0</b> <i>Z2</i>




```python
test_run = GCode.GCode()
# TODO: Get z-axis probe.
test_run+=init()
for XFeed in [50]:
    test_run += test_program(feed=XFeed)
```


```python
test_run
```




<b>G21</b> <i></i><br>
<b>G91</b> <i></i><br>
<b>G1</b> <i>F10</i><br>
<b>M3</b> <i>S10000</i><br>
<b>G1</b> <i>Z-0.1 F1</i><br>
<b>G1</b> <i>X10 F50</i><br>
<b>G1</b> <i>Z-0.1 F1</i><br>
<b>G1</b> <i>X10 F50</i><br>
<b>G1</b> <i>Z-0.1 F1</i><br>
<b>G1</b> <i>X10 F50</i><br>
<b>G1</b> <i>Z-0.1 F1</i><br>
<b>G1</b> <i>X10 F50</i><br>
<b>G1</b> <i>Z-0.1 F1</i><br>
<b>G1</b> <i>X10 F50</i><br>
<b>G1</b> <i>Z-0.1 F1</i><br>
<b>G1</b> <i>X10 F50</i><br>
<b>G1</b> <i>Z-0.1 F1</i><br>
<b>G1</b> <i>X10 F50</i><br>
<b>G1</b> <i>Z-0.1 F1</i><br>
<b>G1</b> <i>X10 F50</i><br>
<b>G1</b> <i>Z-0.1 F1</i><br>
<b>G1</b> <i>X10 F50</i><br>
<b>G1</b> <i>Z-0.1 F1</i><br>
<b>G1</b> <i>X10 F50</i><br>
<b>G1</b> <i>Z-0.1 F1</i><br>
<b>G1</b> <i>X10 F50</i><br>
<b>G1</b> <i>Z-0.1 F1</i><br>
<b>G1</b> <i>X10 F50</i><br>
<b>G1</b> <i>Z-0.1 F1</i><br>
<b>G1</b> <i>X10 F50</i><br>
<b>G1</b> <i>Z-0.1 F1</i><br>
<b>G1</b> <i>X10 F50</i><br>
<b>G1</b> <i>Z-0.1 F1</i><br>
<b>G1</b> <i>X10 F50</i><br>
<b>G1</b> <i>Z-0.1 F1</i><br>
<b>G1</b> <i>X10 F50</i><br>
<b>G1</b> <i>Z-0.1 F1</i><br>
<b>G1</b> <i>X10 F50</i><br>
<b>G1</b> <i>Z-0.1 F1</i><br>
<b>G1</b> <i>X10 F50</i><br>
<b>G1</b> <i>Z-0.1 F1</i><br>
<b>G1</b> <i>X10 F50</i><br>
<b>G1</b> <i>Z-0.1 F1</i><br>
<b>G1</b> <i>X10 F50</i><br>
<b>M3</b> <i>S0</i><br>
<b>G0</b> <i>Z2.0</i><br>
<b>G0</b> <i>X-200</i><br>
<b>G0</b> <i>Z2</i>




```python
gcode_file = "SpindleTests-Copy2.gcode"
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


![jpeg](SpindleTests-Copy2_files/SpindleTests-Copy2_15_0.jpeg)



```python
from time import sleep
```


```python
cnc.cmd("?")
```




    ['ok',
     '<Idle|MPos:-128.925,0.000,-1.200|Bf:15,127|FS:0,0|WCO:0.000,0.000,0.000>',
     'ok']




```python
cnc.reset()
```


```python
cnc.cmd("?")
```




    ['ok',
     '<Idle|MPos:-128.925,0.000,-1.200|Bf:15,127|FS:0,0|WCO:0.000,0.000,0.000>',
     'ok']




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

    <Run|MPos:71.075,0.000,-2.531|Bf:12,127|FS:246,0|Ov:100,100,100>
    <Run|MPos:18.079,0.000,-1.200|Bf:13,127|FS:800,0>
    <Run|MPos:-49.334,0.000,-1.200|Bf:13,127|FS:800,0>
    <Run|MPos:-116.768,0.000,-1.200|Bf:13,127|FS:800,0>
    <Idle|MPos:-128.925,0.000,0.800|Bf:15,127|FS:0,0>
    <Idle|MPos:-128.925,0.000,0.800|Bf:15,127|FS:0,0>
    <Idle|MPos:-128.925,0.000,0.800|Bf:15,127|FS:0,0>
    <Idle|MPos:-128.925,0.000,0.800|Bf:15,127|FS:0,0>
    <Idle|MPos:-128.925,0.000,0.800|Bf:15,127|FS:0,0>
    Feed Hold
    ^C



```python
cnc.reset()
```


```python
picture()
```


![jpeg](SpindleTests-Copy2_files/SpindleTests-Copy2_22_0.jpeg)


# Test Aborted.

Cuts were way too aggressive.
