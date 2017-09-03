# python_cnc3018
Python Dump for figuring out Inexpensive Aliexpress CNC3018

# Examples:


## Grbl

Create a GRBL instance. ```port``` is the GRBL board serial devie.


    import GRBL
    grbl = GRBL.GRBL(port = "/dev/cnc_3018")
    
    # Get laser_mode
    print(grbl.laser_mode)
    1.0
    
    # Turn off laser_mode
    grbl.laser_mode=0
    
Resetting Grbl:

    grbl.cmd("\x18") # ^R
    grbl.reset()
    
Send something to Grbl:

    # $$ and $x=val - View and write Grbl settings
    grbl.cmd("$$")

    $G - View gcode parser state
    grbl.cmd("$G")
    
    # Jog to position X=0, Y=0
    
    grbl.cmd("G0X0Y0")
    
    # Set mm mode.
    
    grbl.cmd("G1")
    
Most of the [Grbl settings](https://github.com/gnea/grbl/wiki/Grbl-v1.1-Configuration#grbl-settings) are added as object parameters.

    # Get the Grbl settings w/cmd
    grbl.cmd("$$")
    
    # Get laser mode ($32)
    
    grbl.laser_mode
    
    # Set laser mode.
    
    grbl.laser_mode = 1
    
Run a GCode program or list of commands.

    grbl.run(["G21", "G91", "G1 X5 Y5 F100"])
  
## GCode
  
Programatically create [G-Code programs](https://en.wikipedia.org/wiki/G-code) with Python.

    program = GCode.GCode()
    program.G0(X=0, Y=0) # Jog to (0, 0).
    
Draw a square:

    def square(size=20):
        program = GCode.GCode()
        program.G1(X=size)
        program.G1(Y=size)
        program.G1(X=-size)
        program.G1(Y=-size)
        return program

Draw sine wave:

    X = np.arange(0, 2*4*np.pi*10, 1)
    test_run = GCode.GCode()
    test_run.G0(X=X[0])
    test_run.M4(S=255)
    for x in X:
        y = 20*np.sin(x/10)
        # Keep GRBL happy.
        x = np.round(x, 4)
        y = np.round(y, 4)
        
     test_run.G1(X=x, Y=y)
        
Save program to gcode file.

    test_run.save('my.gcode')
    
## GRBL & GCode

Combining the above:

    cnc = GRBL.GRBL(port="/dev/cnc_3018")
    
Create init & end programs:
    
    def init(feed = 10):
        program = GCode.GCode()
        program.G21() # Metric Units
        program.G91() # Absolute positioning.
        program.G1(F=feed) 
        return program
    
    def end():
        program = GCode.GCode()
        return program

Square Program:

    def square(size=10):    
        program = GCode.GCode()
        program.M3(S=255) # Laser on full power
        program.G1(X=size) # Draw square.
        program.G1(Y=-size)
        program.G1(X=-size)
        program.G1(Y=size)
        program.M5() # Laser on.
        return program
        
Create a program to draw a row of boxes testing feed speeds on laser engraving.


    size = 10 # mm
    program = GCode.GCode()
    for feed in [50, 100, 200, 500]:
        program += init(feed=feed)
        program += square(size=size)
        program.G0(X=size*2)
        
    program += end()
    cnc.run(program);

# Installation

Clone repository:

    git clone https://github.com/jed-frey/CNC3018.git
    cd CNC3018
    
Install tools to generate markdown and pdfs. [optional]
    
    # Install Debian/Ubuntu packages for generating PDFs & Markdown.
    make dev
    
or 

    # For generating PDFs and Markdown.
    sudo apt-get install texlive-xetex pandoc
    # For udev.
	sudo cp 42-cnc.rules /etc/udev/rules.d/
	
Create virtual environment. [optional]

    make venv
    
Install requirements and setup python_grbl and python_gcode in development mode.

    make venv_init