
import struct
f = open( "/dev/input/event20", "rb" ); # Open the file in the read-binary mode
while 1:
  data = f.read(24)
  print(struct.unpack('4IHHI',data))
