n = int(input())

seconds = []
strings = []
for i in range(n):
    t = input()
    strings.append(t)
    t = t.split(":")
    seconds.append(int(t[0]) * 3600 + int(t[1]) * 60 + int(t[2]))

print(strings[seconds.index(min(seconds))])
