import math

lon = input()
lat = input()
n = int(input())

defibs = []
distances = []
for i in range(n):
    defib = input().split(';')
    defibs.append(defib)
    latdiff = float(defib[5].replace(',','.')) - float(lat.replace(',','.'))
    x = (float(defib[4].replace(',','.')) - float(lon.replace(',','.'))) * math.cos(latdiff/2)
    y = latdiff
    d = math.sqrt(x ** 2 + y **2) * 6731
    distances.append(d)
    
print(defibs[distances.index(min(distances))][1])
