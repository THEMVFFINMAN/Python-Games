import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

n = int(input())  # the number of temperatures to analyse
temps = input()  # the n temperatures expressed as integers ranging from -273 to 5526

# Write an action using print
# To debug: print("Debug messages...", file=sys.stderr)
min2 = list(map(int, temps.split()))

if not min2:
    print(0)
else:
    
    test = min(min2, key=lambda x:abs(x-0))

    min2.remove(test)
    
    if min2:
        test2 = min(min2, key=lambda x:abs(x-0))
        if abs(test) == abs(test2):
            print(max(test, test2))
        else:
            print(test)
    else:
        print(test)
