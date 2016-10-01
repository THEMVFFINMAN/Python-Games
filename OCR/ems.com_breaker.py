import requests
from PIL import Image
from io import open as iopen
from pytesser import *
  
i = requests.get('http://www.ems.com.cn/ems/rand?0.33681450065245544') 
# Just a proof of concept, if you wanted to actually use this you'd have to scrape the page and input it correctly

with iopen('temp.png', 'wb') as file:
    file.write(i.content)

im = Image.open('temp.png')
im2 = Image.new("P", im.size, 255)
im3 = im2.load()


for i in range(0,im.size[0]):
    for j in range(0,im.size[1]):
        pixel = im.getpixel((i,j))
        
        if sum(pixel) > 400:
            im3[i,j] = 0

im2.save('result.png', 'PNG')
answer = image_to_string(im2)

print answer
