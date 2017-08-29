
# Hand Code G

My attempt and creating G-code from a drawing.


```python
import GCode
import GRBL

cnc = GRBL.GRBL(port="/dev/cnc_3018")

print("Laser Mode: {}".format(cnc.laser_mode))
```

    Laser Mode: 1.0



```python
from enum import IntEnum
class LaserPower(IntEnum):
    CONSTANT = 0
    DYNAMIC = 1
    
def init(power = LaserPower(0), feed = 200, laser = 25):
    program = GCode.GCode()
    program.G21() # Metric Units
    program.G91() # Rel positioning.
    program.G1(F=feed) # Set the feed rate
    program.G0() # But keep the laser off.
    if power==LaserPower.CONSTANT:
        program.M3(S=laser) # Laser settings
    else:
        program.M4(S=laser) # Laser settings
    return program
```


```python
def end():
    program = GCode.GCode()
    program.M5() # Te
    return program
```


```python
def heart(scale = 1):
    p = GCode.GCode()
    p.G0(X=2, Y=0)
    p.G1(X=-2, Y=2)
    p.G2(X=2, Y=0, I=1, J=0)
    p.G2(X=2, Y=0, I=1, J=0)
    p.G1(X=-2, Y=-2)
    return p
```


```python
heart10 = heart(scale=1)
print(heart10)
```

    G0 X2 Y0
    G1 X-2 Y2
    G2 I1 J0 X2 Y0
    G2 I1 J0 X2 Y0
    G1 X-2 Y-2



```python
cnc.run(init(laser=5)+heart(scale=1)+end())
```




    4.737777233123779




```python
cnc.run(init(laser=100)+heart(scale=1)+end())
```




    4.738039255142212




```python
def heart(scale = 1):
    p = GCode.GCode()
    
    
    
    p.G0(X=2*scale, Y=0)
    p.G1(X=-2*scale, Y=2*scale)
    p.G2(X=2*scale, Y=0, I=1*scale, J=0)
    p.G2(X=2*scale, Y=0, I=1*scale, J=0)
    p.G1(X=-2*scale, Y=-2*scale)
    return p
```


```python
cnc.run(init(laser=100)+heart(scale=2)+end())
```




    7.24953031539917



## Lots of Hearts


```python
class SoftKill(Exception):
    pass
```


```python
for scale in [4, 8, 16, 32, 65]:
    try:
        cnc.run(init(laser=100)+heart(scale=scale)+end())
        cnc.cmd("G1 X{}".format(scale)) # Move over to edge of heart
        cnc.cmd("G1 X10") # Move another 10
    except KeyboardInterrupt:
        cnc.cmd("!")
        raise(SoftKill("Keyboard"))
```
