import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

l = int(input())
h = int(input())
t = input()

alphabet = []
elements = []
for i in range(h):
    alphabet.append("")
    elements.append([])
    row = input()
    alphabet[i] = row

for char in t:
    charnum = (ord(char.upper()) - 65) * l
    if charnum < 0:
        charnum = 26 * l

    for i in range(h):
        fixedrow = alphabet[i][charnum:charnum+l]
        elements[i].append(fixedrow)

for row in elements:
    added = ""
    for char in row:
        added += char
    print(added)
    

# Write an action using print
# To debug: print("Debug messages...", file=sys.stderr)
