
# GCode Magics.


```python
import GCode
import GRBL
import numpy as np
from utils import picture
cnc = GRBL.GRBL(port="/dev/cnc_3018")
```


```python
print("Laser Mode: {}".format(cnc.laser_mode))
```

    Laser Mode: 1.0



```python
if cnc.laser_mode:
    cnc.laser_mode = False
```

    ok



```python
cnc.laser_mode
```




    1.0




```python
if cnc.laser_mode:
    cnc.laser_mode = 0
```

    ok



```python
cnc.laser_mode
```




    0.0




```python
program = GCode.GCode()
```


```python
program.G0
```


```python
from IPython.core.magic import register_cell_magic
```


```python
@register_cell_magic
def cmagic(line, cell):
    "my cell magic"
    return line, cell
```


```python
%%cmagic
G0
G1
G2
G3
```




    ('', 'G0\nG1\nG2\nG3')




```python
@register_cell_magic
def GCode(_, cell):
    commands = cell.splitlines()
    for command in commands:
        print(command)
    return None
```


```python
%%GCode
G0
G1
G2
G3
```

    G0
    G1
    G2
    G3



```python
@register_cell_magic
def CNC(_, cell):
    commands = cell.splitlines()
    cnc.run(commands)
    return None
```


```python
%%CNC
G0 X-1
```


```python
%%CNC
G0 X150 Y90
```


```python
%%CNC
G0 Y-90
```


```python
%%CNC
G91
G21
```


```python
%%CNC
M3 S1000
```


```python
%%CNC
G0 Y-25
```


```python
%%CNC
M3 S0
```
