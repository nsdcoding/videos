"""Key out a flat magenta background and split into parts.
key.py in.png outprefix [--min 3000] [--single]"""
import sys, numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage
src, pre = sys.argv[1], sys.argv[2]
single = "--single" in sys.argv
mn = int(sys.argv[sys.argv.index("--min")+1]) if "--min" in sys.argv else 3000
im = np.asarray(Image.open(src).convert("RGB")).astype(float)
h,w,_=im.shape
border=np.concatenate([im[:6].reshape(-1,3),im[-6:].reshape(-1,3),im[:,:6].reshape(-1,3),im[:,-6:].reshape(-1,3)])
bg=np.median(border,0)
r,g,b=im[...,0],im[...,1],im[...,2]
# magenta-ness: high R and B relative to G
mag=np.minimum(r,b)-g
bgmag=min(bg[0],bg[2])-bg[1]
d=np.linalg.norm(im-bg,axis=2)
a=np.clip((d-38)/40,0,1)
a=np.maximum(a, np.clip((bgmag*0.55-mag)/(bgmag*0.25),0,1))
mask=a>0.5
mask=ndimage.binary_fill_holes(ndimage.binary_opening(mask,iterations=2))
a=np.where(mask,np.maximum(a,ndimage.binary_erosion(mask,iterations=2)*1.0),0)
holes=mask&(mag>bgmag*0.45)
holes=ndimage.binary_opening(holes,iterations=2)
a=np.where(holes,0,a)
# despill
out=im.copy()
spill=np.clip(np.minimum(r,b)-g-10,0,None)*(a<1)
out[...,0]-=spill*0.6; out[...,2]-=spill*0.8
rgba=np.dstack([np.clip(out,0,255),a*255]).astype(np.uint8)
alpha=Image.fromarray(rgba[...,3]).filter(ImageFilter.GaussianBlur(0.7))
rgba[...,3]=np.asarray(alpha)
lab,n=ndimage.label(mask)
objs=ndimage.find_objects(lab)
parts=[(sl,(lab[sl]==i+1).sum(),i+1) for i,sl in enumerate(objs)]
parts=[p for p in parts if p[1]>=mn]
if single:
    ys=min(p[0][0].start for p in parts); ye=max(p[0][0].stop for p in parts)
    xs=min(p[0][1].start for p in parts); xe=max(p[0][1].stop for p in parts)
    Image.fromarray(rgba[max(0,ys-4):ye+4,max(0,xs-4):xe+4]).save(f"{pre}.png"); print(f"{pre}.png"); sys.exit()
parts.sort(key=lambda p:(p[0][1].start))
for k,(sl,sz,i) in enumerate(parts):
    ys,xs=sl; crop=rgba[max(0,ys.start-4):ys.stop+4,max(0,xs.start-4):xs.stop+4].copy()
    m=lab[max(0,ys.start-4):ys.stop+4,max(0,xs.start-4):xs.stop+4]
    crop[...,3]=np.where(ndimage.binary_dilation(m==i,iterations=3),crop[...,3],0)
    Image.fromarray(crop).save(f"{pre}_{k}.png"); print(f"{pre}_{k}.png",crop.shape[1],crop.shape[0])
