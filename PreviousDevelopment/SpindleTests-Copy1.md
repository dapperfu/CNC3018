
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
def test_program(feed=10):
    prog = GCode.GCode()
    prog.M3(S=10000)
    prog.G0(Z=-2)
    dZ = -0.1
    dX = 20
    X = 0
    Z = 0
    for loops in range(10):
        prog.G1(Z=dZ, F=10)
        prog.G1(X=dX, F=feed)
        X+=dX
        Z+=dZ
    prog.M3(S=0)
    prog.G0(Z=-Z)
    prog.G0(X=-X)
    prog.G0(Z=2)
    return prog
```


```python
test_program()
```




<b>M3</b> <i>S10000</i><br>
<b>G0</b> <i>Z-2</i><br>
<b>G1</b> <i>F10 Z-0.1</i><br>
<b>G1</b> <i>X20 F10</i><br>
<b>G1</b> <i>F10 Z-0.1</i><br>
<b>G1</b> <i>X20 F10</i><br>
<b>G1</b> <i>F10 Z-0.1</i><br>
<b>G1</b> <i>X20 F10</i><br>
<b>G1</b> <i>F10 Z-0.1</i><br>
<b>G1</b> <i>X20 F10</i><br>
<b>G1</b> <i>F10 Z-0.1</i><br>
<b>G1</b> <i>X20 F10</i><br>
<b>G1</b> <i>F10 Z-0.1</i><br>
<b>G1</b> <i>X20 F10</i><br>
<b>G1</b> <i>F10 Z-0.1</i><br>
<b>G1</b> <i>X20 F10</i><br>
<b>G1</b> <i>F10 Z-0.1</i><br>
<b>G1</b> <i>X20 F10</i><br>
<b>G1</b> <i>F10 Z-0.1</i><br>
<b>G1</b> <i>X20 F10</i><br>
<b>G1</b> <i>F10 Z-0.1</i><br>
<b>G1</b> <i>X20 F10</i><br>
<b>M3</b> <i>S0</i><br>
<b>G0</b> <i>Z0.9999999999999999</i><br>
<b>G0</b> <i>X-200</i><br>
<b>G0</b> <i>Z2</i>




```python
import numpy as np
np.round(0.9999999999999999, 4)
```




    1.0




```python
def test_program(feed=10):
    prog = GCode.GCode()
    prog.M3(S=10000)
    prog.G0(Z=-2)
    dZ = -0.1
    dX = 20
    X = 0
    Z = 0
    for loops in range(10):
        prog.G1(Z=dZ, F=10)
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
# Lower head to touching part manually. 
# TODO: Get z-axis probe.
# Then lift by 2.
test_run.G0(Z=2)
for XFeed in [10, 25, 50]:
    test_run += test_program(feed=XFeed)
```


```python
test_run
```




<b>G0</b> <i>Z2</i><br>
<b>M3</b> <i>S10000</i><br>
<b>G0</b> <i>Z-2</i><br>
<b>G1</b> <i>F10 Z-0.1</i><br>
<b>G1</b> <i>X20 F10</i><br>
<b>G1</b> <i>F10 Z-0.1</i><br>
<b>G1</b> <i>X20 F10</i><br>
<b>G1</b> <i>F10 Z-0.1</i><br>
<b>G1</b> <i>X20 F10</i><br>
<b>G1</b> <i>F10 Z-0.1</i><br>
<b>G1</b> <i>X20 F10</i><br>
<b>G1</b> <i>F10 Z-0.1</i><br>
<b>G1</b> <i>X20 F10</i><br>
<b>G1</b> <i>F10 Z-0.1</i><br>
<b>G1</b> <i>X20 F10</i><br>
<b>G1</b> <i>F10 Z-0.1</i><br>
<b>G1</b> <i>X20 F10</i><br>
<b>G1</b> <i>F10 Z-0.1</i><br>
<b>G1</b> <i>X20 F10</i><br>
<b>G1</b> <i>F10 Z-0.1</i><br>
<b>G1</b> <i>X20 F10</i><br>
<b>G1</b> <i>F10 Z-0.1</i><br>
<b>G1</b> <i>X20 F10</i><br>
<b>M3</b> <i>S0</i><br>
<b>G0</b> <i>Z1.0</i><br>
<b>G0</b> <i>X-200</i><br>
<b>G0</b> <i>Z2</i><br>
<b>M3</b> <i>S10000</i><br>
<b>G0</b> <i>Z-2</i><br>
<b>G1</b> <i>F10 Z-0.1</i><br>
<b>G1</b> <i>X20 F25</i><br>
<b>G1</b> <i>F10 Z-0.1</i><br>
<b>G1</b> <i>X20 F25</i><br>
<b>G1</b> <i>F10 Z-0.1</i><br>
<b>G1</b> <i>X20 F25</i><br>
<b>G1</b> <i>F10 Z-0.1</i><br>
<b>G1</b> <i>X20 F25</i><br>
<b>G1</b> <i>F10 Z-0.1</i><br>
<b>G1</b> <i>X20 F25</i><br>
<b>G1</b> <i>F10 Z-0.1</i><br>
<b>G1</b> <i>X20 F25</i><br>
<b>G1</b> <i>F10 Z-0.1</i><br>
<b>G1</b> <i>X20 F25</i><br>
<b>G1</b> <i>F10 Z-0.1</i><br>
<b>G1</b> <i>X20 F25</i><br>
<b>G1</b> <i>F10 Z-0.1</i><br>
<b>G1</b> <i>X20 F25</i><br>
<b>G1</b> <i>F10 Z-0.1</i><br>
<b>G1</b> <i>X20 F25</i><br>
<b>M3</b> <i>S0</i><br>
<b>G0</b> <i>Z1.0</i><br>
<b>G0</b> <i>X-200</i><br>
<b>G0</b> <i>Z2</i><br>
<b>M3</b> <i>S10000</i><br>
<b>G0</b> <i>Z-2</i><br>
<b>G1</b> <i>F10 Z-0.1</i><br>
<b>G1</b> <i>X20 F50</i><br>
<b>G1</b> <i>F10 Z-0.1</i><br>
<b>G1</b> <i>X20 F50</i><br>
<b>G1</b> <i>F10 Z-0.1</i><br>
<b>G1</b> <i>X20 F50</i><br>
<b>G1</b> <i>F10 Z-0.1</i><br>
<b>G1</b> <i>X20 F50</i><br>
<b>G1</b> <i>F10 Z-0.1</i><br>
<b>G1</b> <i>X20 F50</i><br>
<b>G1</b> <i>F10 Z-0.1</i><br>
<b>G1</b> <i>X20 F50</i><br>
<b>G1</b> <i>F10 Z-0.1</i><br>
<b>G1</b> <i>X20 F50</i><br>
<b>G1</b> <i>F10 Z-0.1</i><br>
<b>G1</b> <i>X20 F50</i><br>
<b>G1</b> <i>F10 Z-0.1</i><br>
<b>G1</b> <i>X20 F50</i><br>
<b>G1</b> <i>F10 Z-0.1</i><br>
<b>G1</b> <i>X20 F50</i><br>
<b>M3</b> <i>S0</i><br>
<b>G0</b> <i>Z1.0</i><br>
<b>G0</b> <i>X-200</i><br>
<b>G0</b> <i>Z2</i>




```python
gcode_file = "SpindleTests-Copy1.gcode"
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




    ['G0 Z2', 'M3 S10000', 'G0 Z-2', 'G1 F10 Z-0.1', 'G1 X20 F10']




```python
picture()
```


![jpeg](SpindleTests-Copy1_files/SpindleTests-Copy1_13_0.jpeg)



```python
from time import sleep
```


```python
cnc.cmd("?")
```




    ['ok',
     '<Idle|MPos:20.000,0.000,0.020|Bf:15,127|FS:0,0|WCO:0.000,0.000,0.000>',
     'ok']




```python
cnc.reset()
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
        print("^C")
        break
    except:
        raise
```

    ^C



    ---------------------------------------------------------------------------

    AssertionError                            Traceback (most recent call last)

    <ipython-input-48-c54c312fb5fd> in <module>()
          3         cnc.run(test_run)
          4         while 1:
    ----> 5             print(cnc.status)
          6             sleep(5)
          7     except KeyboardInterrupt as error:


    ~/CNC3018/python_rs274/GRBL/__init__.py in status(self)
         68         """
         69         ret = self.cmd("?")
    ---> 70         assert(ret[-1] == 'ok')
         71         return ret[1]
         72 


    AssertionError: 



```python
picture()
```


![jpeg](SpindleTests-Copy1_files/SpindleTests-Copy1_18_0.jpeg)


# Test Aborted.

Cuts were way too aggressive.
