import sys
import math
from collections import deque

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

l, c, n = [int(i) for i in input().split()]
d = deque()
for i in range(n):
    d.appendleft(int(input()))
    
print(l, c, n, d, file=sys.stderr)

full = False
dirhams = 0
people_on_ride = 0
times_per_day = 0
groups_on_ride = 0
while not full:
    next_group = d.pop()
    
    if groups_on_ride == n or people_on_ride + next_group > l:
        times_per_day += 1
        dirhams += people_on_ride
        people_on_ride = 0
        groups_on_ride = 0
        d.append(next_group)
        if times_per_day == c:
            full = True
    elif people_on_ride + next_group <= l:
        people_on_ride += next_group
        d.appendleft(next_group)
        groups_on_ride += 1
        
# Write an action using print
# To debug: print("Debug messages...", file=sys.stderr)

print(dirhams)
