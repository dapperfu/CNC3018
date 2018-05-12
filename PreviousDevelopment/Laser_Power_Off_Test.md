
# Laser Power Off Test

## Object
- Figure out at what voltage the laser resets the MCU

# Code:


```python
import GCode
import GRBL
cnc = GRBL.GRBL(port="/dev/cnc_3018")

print("Laser Mode: {}".format(cnc.laser_mode))
```

    Laser Mode: None


## Test Setup

Power Supply:
- CicuitSpecialists CSI3010SW

Position the paper & other things.


```python
import numpy as np
```


```python
def laser_on(pwm):
    if int(pwm) != np.uint8(pwm):
        raise(Exception("UINT8! {}".format(pwm)))
    # Set minimal power setting to focus and position laser
    cnc.cmd("M3 S{:03d}".format(np.uint8(pwm)))
    cnc.cmd("G1 F10") # Laser On

def laser_off():
    cnc.cmd("M5") # Laser off
```


```python
laser_on(255)
```

- ~18 volts.
