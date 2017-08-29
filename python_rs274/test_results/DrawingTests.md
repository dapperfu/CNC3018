
# Drawing Tests

## Object
- Play around with drawing things.

# Code:


```python
import GCode
import GRBL
import numpy as np
from utils import picture
cnc = GRBL.GRBL(port="/dev/cnc_3018")

print("Laser Mode: {}".format(cnc.laser_mode))

from enum import IntEnum
class Tool(IntEnum):
    SPINDLE = 0
    LASER = 1

from enum import IntEnum
class LaserPower(IntEnum):
    CONSTANT = 0
    DYNAMIC = 1

LaserPower.CONSTANT

def init(power = LaserPower(0), feed = 200, laser = 1):
    program = GCode.GCode()
    program.G20() # Metric Units
    program.G91() # Absolute positioning.
    program.G1(F=feed) #
    if power==LaserPower.CONSTANT:
        program.M3(S=laser) # Laser settings
    else:
        program.M4(S=laser) # Laser settings
    return program

def end():
    program = GCode.GCode()
    program.M5() # Laser settings.
    return program

def square(size=0.25):    
    program = GCode.GCode()
    program.G1(X=size)
    program.G1(Y=-size)
    program.G1(X=-size)
    program.G1(Y=size)
    return program
```

    Laser Mode: 1.0


## Test Setup

Power Supply:
- CicuitSpecialists CSI3010SW @ 12V
- PostIt Note Grid notes. .25" grid.

Position the paper & other things.


```python
def laser_on(pwm):
    if int(pwm) != np.uint8(pwm):
        raise(Exception("UINT8! {}".format(pwm)))
    # Set minimal power setting to focus and position laser
    cnc.cmd("M3 S{:03d}".format(np.uint8(pwm)))
    cnc.cmd("G1 X0 F10") # Laser On

def laser_off():
    cnc.cmd("M5") # Laser off
```


```python
init()
```




<b>G20</b> <i></i><br>
<b>G91</b> <i></i><br>
<b>G1</b> <i>F200</i><br>
<b>M3</b> <i>S1</i>




```python
cnc.run()
```




    0.414473295211792




```python
laser_on(1) # Position the axis by hand
```


```python
cnc.cmd("G0 F10 X0 Y0")
```




    ['ok', 'error:9']




```python
picture()
```


```python
laser_off()
```


```python
laser_on(1)
```


```python
cnc.reset()
```


```python
square(0.25)
```


```python
tests_x = 10
tests_y = 7
```


```python
cnc.run(init(laser=0.1)+square(0.25))
```


```python
np.linspace(0, 255, tests_x)
```


```python
np.linspace(50, 1, tests_y)
```


```python
def jogx(x=10):
    program = GCode.GCode()
    program.G0(X=x)
    cnc.run(program)
def jogy(y=10):
    program = GCode.GCode()
    program.G0(Y=y)
    cnc.run(program)
def jogz(z=10):
    program = GCode.GCode()
    program.G0(Z=z)
    cnc.run(program)
```


```python
jogx(-1)
```


```python
laser_on(1)
```


```python
square_size = 0.25
```

# Test Setup


```python
cnc.cmd("$G")[1]
```


```python
cnc.cmd("$#")[1]
```


```python
cnc.cmd("$$")
```


```python
cnc.cmd("$I")
```


```python
picture()
```


```python
for feed in np.linspace(50, 1, tests_y):
    for pwm in np.linspace(0, 255, tests_x):
        i = init(laser=np.uint8(pwm), feed=np.round(feed))
        s = square(square_size)
        laser_on(1)
        cnc.run(i+s)
        jogx(0.25)
    jogx(-1*2*tests_x*square_size)
    jogy(-square_size*2)
```


```python
cnc.cmd("!")
```


```python
laser_on(1)
```


```python
cnc.reset()
```


```python
laser_off()
```


```python

```
