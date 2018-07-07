# -*- coding: utf-8 -*-


import numpy as np


class GCode(object):
    NEWLINE = "\n"

    def __init__(self, file=None, machine=None, buffer=None):
        self.machine = machine
        if file is not None:
            self.load(file)

        if buffer is None:
            self.buffer = list()
        else:
            self.buffer = buffer

    @property
    def code(self):
        return GCode.NEWLINE.join(self.buffer)

    def load(self, filename):
        with open(filename, "r") as fid:
            data = fid.read()
        self.buffer = data.splitlines()

    def save(self, filename):
        with open(filename, "w") as fid:
            print(str(self), file=fid)

    def __str__(self):
        return self.code

    def __repr__(self):
        return "<GCode>[cmds={}]".format(len(self.buffer))

    def _repr_html_(self):
        html = list()
        for cmd_line in self.buffer:
            cmd, *args = cmd_line.split(" ")
            html_line = "<b>{cmd}</b> <i>{args}</i>".format(
                cmd=cmd, args=" ".join(args)
            )
            html.append(html_line)
        return "<br>\n".join(html)

    def __add__(self, other):
        buffer = self.buffer
        buffer2 = other.buffer

        buffer.extend(buffer2)

        return GCode(machine=self.machine, buffer=buffer)

    def __iter__(self):
        """ __iter__ function """
        for i in range(len(self.buffer)):
            yield (self.buffer[i])

    def run(self):
        """ run the program on the given machine """
        if self.machine is None:
            raise Exception("No machine to run on")
        self.machine.run(self)

    def optimise(self):
        """ Create the best GCode possible. """
        raise (NotImplementedError("TODO:"))


numeric_types = (
    int,
    np.int8,
    np.int16,
    np.int32,
    np.int64,
    np.float,
    np.float16,
    np.float32,
    np.float64,
    np.float128,
)


def cmd_factory(cmd, doc=None):
    """ Factory to create GCode Command Functions. """

    def cmd_fcn(self, **kwargs):
        args = list()

        for key, value in kwargs.items():
            if isinstance(value, numeric_types):
                value = np.round(value, 4)
            args.append("{key}{value}".format(key=key, value=value))

        cmd_str = "{cmd} {args}".format(cmd=cmd, args=" ".join(args))
        # For commands with no arguments.
        cmd_str = cmd_str.strip()
        self.buffer.append(cmd_str)

    return cmd_fcn


# Good core to start with.
commands = list()
# GCodes
for code in [0, 1, 2, 3, 4, 20, 21, 28, 90, 91, 92]:
    commands.append("G{code}".format(code=code))
# MCodes
for code in [0, 1, 2, 3, 4, 5, 6]:
    commands.append("M{code}".format(code=code))

for command in commands:
    setattr(GCode, command, cmd_factory(command))
