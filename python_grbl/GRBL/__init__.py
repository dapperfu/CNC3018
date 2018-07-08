import serial
import time

run_states = ["Idle", "Run", "Hold", "Door", "Home", "Alarm", "Check"]



class GRBL(object):
    """
    Class for a GRBL controlled CNC.

    Tested on 1.1
    Developed on Chinese CNC 3018
    """

    BAUDRATE = 115200
    TIMEOUT = 60

    def __init__(self, port):
        """

        """
        self.serial = serial.Serial(
            port=port, baudrate=GRBL.BAUDRATE, timeout=0.10
        )

    def write(self, command_line=""):
        bytes_written = [0, 0]
        bytes_written[0] = self.serial.write("\n".encode())
        bytes_written[1] = self.serial.write(
            "{cmd}\n".format(cmd=command_line).encode()
        )
        return bytes_written

    def read(self, multiline=True, timeout=-1):

        if timeout is not -1:
            old_timeout = self.serial.timeout
            self.serial.timeout = timeout
        if multiline:
            responses = self.serial.readlines()
            responses = [response.decode().strip() for response in responses]
            return responses
        else:
            responses = self.serial.readline().decode().strip()
        if timeout is not -1:
            self.serial.timeout = old_timeout
        return responses

    def cmd(self, command_line, resp=True, multiline=True):
        self.serial.flushInput()
        self.write(command_line)
        if resp:
            return self.read(multiline=multiline)
        return None

    def reset(self, home=True):
        """ https://github.com/gnea/grbl/wiki/Grbl-v1.1-Commands#grbl-v11-realtime-commands
        """
        for t in range(GRBL.TIMEOUT):
            ret = self.cmd("\x18")
            if len(ret) > 0:
                return (t, ret)
                break
            time.sleep(1)
        if home:
            time.sleep(1)
            return self.home()
        return None

    def sleep(self):
        """ https://github.com/gnea/grbl/wiki/Grbl-v1.1-Commands#slp---enable-sleep-mode
        """
        ret = self.cmd("$SLP")
        assert ret[-1] == "ok"

    @property
    def status(self):
        """
        """
        ret = self.cmd("?")
        if len(ret) == 1:
            # Held
            return ret[0]
        elif len(ret) == 3:
            return ret[1]
        else:
            raise (Exception(ret))

        assert ret[-1] == "ok"

    def kill_alarm(self):
        """ https://github.com/gnea/grbl/wiki/Grbl-v1.1-Commands#x---kill-alarm-lock
        """
        ret = self.cmd("$X")
        assert ret[-1] == "ok"

    def home(self):
        """ https://github.com/gnea/grbl/wiki/Grbl-v1.1-Commands#h---run-homing-cycle
        """
        self.write("$H")

        for t in range(GRBL.TIMEOUT):
            ret = self.cmd("")
            if len(ret) == 2:
                assert ret[0] == "ok"
                assert ret[1] == "ok"
                return t
                break
            time.sleep(1)
        return None

    # Run
    def run(self, program, compact=True):
        if isinstance(program, str):
            program = program.splitlines()
        else:
            program = program.buffer

        # Strip whitespace and force letters to capital.
        program = [line.strip().upper() for line in program]
        # Save bits.
        if compact:
            program = [line.replace(" ", "") for line in program]

        t1 = time.time()
        self.serial.flushInput()

        # Create list to store the number of bytes we think are in memory.
        buffer_bytes = list()

        try:
            # For each line in the program"
            for program_line in program:
                bytes_written = self.write(program_line)
                buffer_bytes.extend(bytes_written)
                results = self.read(multiline=True, timeout=0.1)

                while len(results) == 0:
                    time.sleep(0.5)
                    results = self.read(multiline=True, timeout=0.1)

                for result in results:
                    if result == "ok":
                        try:
                            buffer_bytes.pop(0)
                        except:
                            # Miscounted byte counting, we're ahead.
                            pass
            for _ in range(GRBL.TIMEOUT):
                run_status=self.status.strip("<>").split("|")
                run_state = run_status[0]
                assert(run_state in run_states)
                if run_state is "Run":
                    print(run_state)
                    time.sleep(0.25)
                else:
                    break
        except KeyboardInterrupt:
            self.cmd("!")
            print("^C")
        return time.time() - t1


# https://github.com/gnea/grbl/wiki/Grbl-v1.1-Configuration#---view-grbl-settings
settings = [
    ("$0", "step_pulse"),
    ("$1", "step_idle_delay"),
    ("$2", "step_port_invert"),
    ("$3", "direction_port_invert"),
    ("$4", "step_enable_invert"),
    ("$5", "limit_pin_invert"),
    ("$6", "probe_pin_invert"),
    ("$10", "status_report"),
    ("$11", "junction_deviation"),
    ("$12", "arc_tolerance"),
    ("$13", "report_inches"),
    ("$20", "soft_limits"),
    ("$21", "hard_limits"),
    ("$22", "homing_cycle"),
    ("$23", "homing_dir_invert"),
    ("$24", "homing_feed"),
    ("$25", "homing_seek"),
    ("$26", "homing_debounce"),
    ("$27", "homing_pull_off"),
    ("$30", "max_spindle_speed"),
    ("$31", "min_spindle_speed"),
    ("$32", "laser_mode"),
    ("$100", "x_steps_mm"),
    ("$101", "y_steps_mm"),
    ("$102", "z_steps_mm"),
    ("$110", "x_max_rate"),
    ("$111", "y_max_rate"),
    ("$112", "z_max_rate"),
    ("$120", "x_acceleration"),
    ("$121", "y_acceleration"),
    ("$122", "z_acceleration"),
    ("$130", "x_travel"),
    ("$131", "y_travel"),
    ("$132", "z_travel"),
]


def grbl_getter_generator(cmd):
    def grbl_getter(self):
        config = self.cmd("$$", resp=True, multiline=True)
        for config_line in config:
            if config_line.startswith("$"):
                key, value = config_line.split("=")
                if key == cmd:
                    return float(value)
        return None

    return grbl_getter


def grbl_setter_generator(cmd):
    def grbl_setter(self, value):
        set_cmd = "{cmd}={value}".format(cmd=cmd, value=value)
        ret = self.cmd(set_cmd, resp=True, multiline=False)
        print(ret)

    return grbl_setter


for setting in settings:
    cmd = setting[0]
    name = setting[1]

    setter = grbl_setter_generator(cmd)
    getter = grbl_getter_generator(cmd)

    prop = property(fget=getter, fset=setter, doc=" ".join(name.split("_")))

    setattr(GRBL, name, prop)

# https://github.com/gnea/grbl/wiki/Grbl-v1.1-Commands#---view-gcode-parameters
gcode_parameters = [
    "G54",
    "G55",
    "G56",
    "G57",
    "G58",
    "G59",
    "G28",
    "G30",
    "G92",
    "TLO",
    "PRB",
]


def gcode_param_gen(parameter):
    def gcode_param(self):
        gcode_parameters = self.cmd("$#")  # View gcode parameters
        for gcode_parameter in gcode_parameters:
            if parameter in gcode_parameter:
                _, value = gcode_parameter.split(":")
                value = value.strip("]")
                values = value.split(",")
                values = [float(value) for value in values]

                return values
        return None

    return gcode_param


for parameter in gcode_parameters:
    fcn = gcode_param_gen(parameter)
    prop = property(fget=fcn)
    setattr(GRBL, parameter, prop)
