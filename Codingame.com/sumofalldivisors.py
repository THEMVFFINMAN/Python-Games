from functools import reduce
n = int(input())
def factorGenerator(n):    
    return set(reduce(list.__add__, ([i, n//i] for i in range(1, int(n**0.5) + 1) if n % i == 0)))
final = 0
for i in range(1, n + 1):
    final += sum(list(factorGenerator(i)))
print(final)
