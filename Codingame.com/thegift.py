n = int(input())
c = int(input())
numbers = []
for i in range(n):
    numbers.append(int(input()))
if sum(numbers) < c:
    print("IMPOSSIBLE")
else:
    while sum(numbers) > c:
        numbers[numbers.index(max(numbers))] -= 1
    for number in sorted(numbers):
        print(number)
