from PIL import Image
from PIL import ImageFont, ImageDraw
import os

fnt = ImageFont.truetype('19198.otf', 14)
folder = 'color/'
for i in range(1, 10):
    obj = Image.open('ex.png')
    draw = ImageDraw.Draw(obj)
    draw.text((11,5), str(i),fill='#111', font=fnt)
    obj.save(folder+str(i)+'.png')

for i in range(10, 20):
    obj = Image.open('ex.png')
    draw = ImageDraw.Draw(obj)
    draw.text((9,5), str(i),fill='#111', font=fnt)
    obj.save(folder+str(i)+'.png')

for i in range(20, 73):
    obj = Image.open('ex.png')
    draw = ImageDraw.Draw(obj)
    draw.text((8,5), str(i),fill='#111', font=fnt)
    obj.save(folder+str(i)+'.png')
