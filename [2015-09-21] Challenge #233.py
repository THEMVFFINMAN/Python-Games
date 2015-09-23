import copy, random

def make2dList(rows, cols):
    a=[]
    for row in xrange(rows):
        a += [[0]*cols]

    for i in range(len(a)):
        for j in range(len(a[i])):
            if str(a[i][j]) == '0':
                a[i][j] = ' '
    return a

f = open("bluep.txt","r")

single = []
full = []

for line in f:
    single = []
    for i in range(0, len(line)):
        if (line[i] != '\n'):
            single.append(line[i])

    full.append(single)

rows = len(full)
cols = len(full[0])

picture = make2dList(((rows * 2) + 1), (cols * 5))
centers = []

for i in range(len(full)):
    for j in range(len(full[i])):

        if full[i][j] == '*':
            center = [(i * 2 + 1), (2 * (2 * (j + 1)) - 1)]
            centers.append(center)

            for k in range (-1, 2):
                for l in range(-1, 2, 2):
                    if center[0] + l < len(picture) and center[1] + k < len(picture[0]):
                        picture[center[0] + l][center[1] + k] = "-"
                    
            for k in range(-1, 2, 2):
                for l in range(-2, 5, 4):
                    if center[0] + k < len(picture) and center[1] - l < len(picture[0]):
                        picture[center[0] + k][center[1] - l] = "+"
            if center[1] + 2 < len(picture[0]):
                picture[center[0]][center[1] + 2] = '|'
            picture[center[0]][center[1] - 2] = '|'

            if bool(random.getrandbits(1)):
                picture[center[0]][center[1]] = 'o'

picture2 = copy.deepcopy(picture)

for i in range(len(full)):
    for j in range(len(full[i])):
        if full[i][j] == '*':
            center = [(i * 2 + 1), (2 * (2 * (j + 1)) - 1)]
            if center[1] + 3 < len(picture[0]):
                if picture[center[0] - 1][center[1] + 3] == '-':
                    picture2[center[0]][center[1] + 2] = ' '
            if picture[center[0] - 3][center[1]] == "-":
                picture2[center[0] - 1][center[1] - 1] = " "
                picture2[center[0] - 1][center[1]] = " "
                if center[1] + 1 < len(picture[0]):
                    picture2[center[0] - 1][center[1] + 1] = " "
            
for i in range(len(picture2)):
    for j in range(len(picture2[i])):
        if picture2[i][j] == '+':
            if i + 1 < len(picture2) and i - 1 > -1 and j + 1 < len(picture2[0]) and j - 1 > -1:
                if picture2[i + 1][j] == ' ' and picture2[i - 1][j] == ' ' and picture2[i][j + 1] == ' ' and picture2[i][j - 1] == ' ':
                    picture2[i][j] = ' '

groundfloor = max(centers,key=lambda x:x[0])[0]
door = random.choice([item for item in centers if item[0] == groundfloor])

while picture2[door[0]][door[1]] == 'o':
    door = random.choice([item for item in centers if item[0] == groundfloor])

picture2[door[0]][door[1] - 1] = "|"
picture2[door[0]][door[1] + 1] = "|"

for line in picture2:
    print "".join(map(str,line))
