import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

message = input()
binaries = []
for ch in message:
    binaries.append(bin(ord(ch))[2:].zfill(7))

stringer = ""

zero = False
one = False

for binary in binaries:
    for char in binary:
        if int(char):
            if zero:
                zero = False
                stringer += " "
            
            if not one:
                one = True
                stringer += "0 "
            stringer += "0"
            
        else:
            if one:
                one = False
                stringer += " "
            
            if not zero:
                zero = True
                stringer += "00 "
            stringer += "0"

print(stringer)
