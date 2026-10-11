import sys
from PIL import Image, ImageDraw
fs=sys.argv[2:]; H=220
ims=[Image.open(f) for f in fs]; ims=[im.resize((max(1,int(im.width*H/im.height)),H)) for im in ims]
W=1800; rows=[]; x=0; row=[]
for f,im in zip(fs,ims):
    if x+im.width>W: rows.append(row); row=[]; x=0
    row.append((f,im)); x+=im.width+10
rows.append(row)
c=Image.new('RGBA',(W,len(rows)*(H+20)),(60,110,200,255)); d=ImageDraw.Draw(c)
for r,row in enumerate(rows):
    x=0
    for f,im in row:
        c.alpha_composite(im.convert('RGBA'),(x,r*(H+20))); d.text((x+2,r*(H+20)+H+4),f.split('/')[-1],fill='white'); x+=im.width+10
c.save(sys.argv[1])
