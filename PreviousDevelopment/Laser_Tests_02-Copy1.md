
# CNC Laser Power Settings Test 3


# Code:


```python
import GCode
import GRBL
```


```python
cnc = GRBL.GRBL(port="/dev/cnc_3018")

print("Laser Mode: {}".format(cnc.laser_mode))
```

    Laser Mode: 0.0



```python
cnc.laser_mode = 1
```

    ok



```python
from enum import IntEnum
class Tool(IntEnum):
    SPINDLE = 0
    LASER = 1
```


```python
from enum import IntEnum
class LaserPower(IntEnum):
    CONSTANT = 0
    DYNAMIC = 1
```


```python
LaserPower.CONSTANT
```




    <LaserPower.CONSTANT: 0>




```python
def init(power = LaserPower(0), feed = 200, laser = 25):
    program = GCode.GCode()
    program.G21() # Metric Units
    program.G91() # Absolute positioning.
    program.G1(F=feed) #
    if power==LaserPower.CONSTANT:
        program.M3(S=laser) # Laser settings
    else:
        program.M4(S=laser) # Laser settings
    return program
```


```python
def end():
    program = GCode.GCode()
    program.M5() # Laser settings.
    return program
```


```python
def square(size=20):    
    program = GCode.GCode()
    program.G1(X=size)
    program.G1(Y=size)
    program.G1(X=-size)
    program.G1(Y=-size)
    return program
```

## Test Setup

Position the paper & other things.


```python
cnc.cmd("M5") # Laser off
```




    ['ok', 'ok']




```python
# Set minimal power setting to focus and position laser
cnc.cmd("M3 S1")
cnc.cmd("G1 X0") # Laser On
```




    ['ok', 'ok']




```python
def pulse(pulse_duration=100):
    prog = GCode.GCode()
    prog.M5()
    prog.G1(X=0)
    prog.M3(S=255)
    prog.M4(P=pulse_duration)
    prog.G1(X=0)
    prog.M5()
    return prog
```


```python
pulse(100)
```




<b>M5</b> <i></i><br>
<b>G1</b> <i>X0</i><br>
<b>M3</b> <i>S255</i><br>
<b>M4</b> <i>P100</i><br>
<b>G1</b> <i>X0</i><br>
<b>M5</b> <i></i>




```python
cnc.run(pulse(100))
```

    ^C





    21.264846563339233




```python
test_run=GCode.GCode()
test_run.G21()
test_run.G91()
test_run.G0(F=500)
test_run.G1(F=500)
for test_num in range(16):
    pulse_duration = (test_num+1)*25
    test_run += pulse(pulse_duration)
    test_run.G0(X=5)
test_run+=end()
```


```python
test_run
```




<b>G21</b> <i></i><br>
<b>G91</b> <i></i><br>
<b>G0</b> <i>F500</i><br>
<b>G1</b> <i>F500</i><br>
<b>M5</b> <i></i><br>
<b>G1</b> <i>X0</i><br>
<b>M3</b> <i>S255</i><br>
<b>M4</b> <i>P25</i><br>
<b>G1</b> <i>X0</i><br>
<b>M5</b> <i></i><br>
<b>G0</b> <i>X5</i><br>
<b>M5</b> <i></i><br>
<b>G1</b> <i>X0</i><br>
<b>M3</b> <i>S255</i><br>
<b>M4</b> <i>P50</i><br>
<b>G1</b> <i>X0</i><br>
<b>M5</b> <i></i><br>
<b>G0</b> <i>X5</i><br>
<b>M5</b> <i></i><br>
<b>G1</b> <i>X0</i><br>
<b>M3</b> <i>S255</i><br>
<b>M4</b> <i>P75</i><br>
<b>G1</b> <i>X0</i><br>
<b>M5</b> <i></i><br>
<b>G0</b> <i>X5</i><br>
<b>M5</b> <i></i><br>
<b>G1</b> <i>X0</i><br>
<b>M3</b> <i>S255</i><br>
<b>M4</b> <i>P100</i><br>
<b>G1</b> <i>X0</i><br>
<b>M5</b> <i></i><br>
<b>G0</b> <i>X5</i><br>
<b>M5</b> <i></i><br>
<b>G1</b> <i>X0</i><br>
<b>M3</b> <i>S255</i><br>
<b>M4</b> <i>P125</i><br>
<b>G1</b> <i>X0</i><br>
<b>M5</b> <i></i><br>
<b>G0</b> <i>X5</i><br>
<b>M5</b> <i></i><br>
<b>G1</b> <i>X0</i><br>
<b>M3</b> <i>S255</i><br>
<b>M4</b> <i>P150</i><br>
<b>G1</b> <i>X0</i><br>
<b>M5</b> <i></i><br>
<b>G0</b> <i>X5</i><br>
<b>M5</b> <i></i><br>
<b>G1</b> <i>X0</i><br>
<b>M3</b> <i>S255</i><br>
<b>M4</b> <i>P175</i><br>
<b>G1</b> <i>X0</i><br>
<b>M5</b> <i></i><br>
<b>G0</b> <i>X5</i><br>
<b>M5</b> <i></i><br>
<b>G1</b> <i>X0</i><br>
<b>M3</b> <i>S255</i><br>
<b>M4</b> <i>P200</i><br>
<b>G1</b> <i>X0</i><br>
<b>M5</b> <i></i><br>
<b>G0</b> <i>X5</i><br>
<b>M5</b> <i></i><br>
<b>G1</b> <i>X0</i><br>
<b>M3</b> <i>S255</i><br>
<b>M4</b> <i>P225</i><br>
<b>G1</b> <i>X0</i><br>
<b>M5</b> <i></i><br>
<b>G0</b> <i>X5</i><br>
<b>M5</b> <i></i><br>
<b>G1</b> <i>X0</i><br>
<b>M3</b> <i>S255</i><br>
<b>M4</b> <i>P250</i><br>
<b>G1</b> <i>X0</i><br>
<b>M5</b> <i></i><br>
<b>G0</b> <i>X5</i><br>
<b>M5</b> <i></i><br>
<b>G1</b> <i>X0</i><br>
<b>M3</b> <i>S255</i><br>
<b>M4</b> <i>P275</i><br>
<b>G1</b> <i>X0</i><br>
<b>M5</b> <i></i><br>
<b>G0</b> <i>X5</i><br>
<b>M5</b> <i></i><br>
<b>G1</b> <i>X0</i><br>
<b>M3</b> <i>S255</i><br>
<b>M4</b> <i>P300</i><br>
<b>G1</b> <i>X0</i><br>
<b>M5</b> <i></i><br>
<b>G0</b> <i>X5</i><br>
<b>M5</b> <i></i><br>
<b>G1</b> <i>X0</i><br>
<b>M3</b> <i>S255</i><br>
<b>M4</b> <i>P325</i><br>
<b>G1</b> <i>X0</i><br>
<b>M5</b> <i></i><br>
<b>G0</b> <i>X5</i><br>
<b>M5</b> <i></i><br>
<b>G1</b> <i>X0</i><br>
<b>M3</b> <i>S255</i><br>
<b>M4</b> <i>P350</i><br>
<b>G1</b> <i>X0</i><br>
<b>M5</b> <i></i><br>
<b>G0</b> <i>X5</i><br>
<b>M5</b> <i></i><br>
<b>G1</b> <i>X0</i><br>
<b>M3</b> <i>S255</i><br>
<b>M4</b> <i>P375</i><br>
<b>G1</b> <i>X0</i><br>
<b>M5</b> <i></i><br>
<b>G0</b> <i>X5</i><br>
<b>M5</b> <i></i><br>
<b>G1</b> <i>X0</i><br>
<b>M3</b> <i>S255</i><br>
<b>M4</b> <i>P400</i><br>
<b>G1</b> <i>X0</i><br>
<b>M5</b> <i></i><br>
<b>G0</b> <i>X5</i><br>
<b>M5</b> <i></i>




```python
cnc.run(test_run)
```




    30.084847450256348




```python
cnc.status
```




    '<Idle|MPos:-123.276,0.000,2.800|Bf:15,127|FS:0,0|Ov:100,100,100>'


