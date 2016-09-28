n = int(input())
q = int(input())

mimetypes = {}
for i in range(n):
    ext, mt = input().split()
    mimetypes[ext.lower()] = mt

for i in range(q):
    fname = input()#.split('.')[-1]  # One file name per line.
    fname2 = (fname.split('.')[-1]).lower()

    if fname2 not in mimetypes or fname == fname2:
        print("UNKNOWN")
    else:
        print(mimetypes[fname2])
