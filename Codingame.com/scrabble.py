def value(c):
    if c in 'qz': return 10
    if c in 'jx': return 8
    if c in 'k': return 5
    if c in 'fhvwy': return 4
    if c in 'bcmp': return 3
    if c in 'dg': return 2
    return 1

n = int(input())
words = [input() for i in range(n)]
letters = input()

maxsum = 0
for w in words:
    wsum = 0
    for c in w:
        if w.count(c) > letters.count(c):
            wsum = 0
            break
        wsum += value(c)
    if wsum > maxsum:
        maxsum = wsum
        maxsumword = w

print(maxsumword)
