import sys
import termios

def read_with_timeout():
    pass

fd = sys.stdin
a = termios.tcgetattr(fd)
# print(a)
atr = a[6]
for at in atr:
    print(at)
