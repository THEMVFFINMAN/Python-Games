import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

msg = input().lower()
key = 'abcdefghijklmnopqrstuvwxyz'
wordnumbers = {}
wordnumbers["zero"] = "0"
wordnumbers["one"] = "1"
wordnumbers["two"] = "2"
wordnumbers["three"] = "3"
wordnumbers["four"] = "4"
wordnumbers["five"] = "5"
wordnumbers["six"] = "6"
wordnumbers["seven"] = "7"
wordnumbers["eight"] = "8"
wordnumbers["nine"] = "9"

def decrypt(n, ciphertext):
    result = ''

    for l in ciphertext:
        try:
            i = (key.index(l) - n) % 26
            result += key[i]
        except ValueError:
            result += l
    return result

decrypted = ""

for i in range(26):    
    rotted = decrypt(i, msg)
    if "the safe combination is:" in rotted:
        decrypted = rotted

decrypted = decrypted[25:].split("-")

solution = ""
for number in decrypted:
    solution = solution + wordnumbers[number]

print(solution)
