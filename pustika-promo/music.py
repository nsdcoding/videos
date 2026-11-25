import numpy as np, wave
SR=44100; D=21.0; N=int(SR*D); t=np.arange(N)/SR
L=np.zeros(N); Rr=np.zeros(N)
def hz(m): return 440*2**((m-69)/12)
def add(sig,start,pan=0.0,g=1.0):
    i=int(start*SR); n=min(len(sig),N-i)
    if n<=0: return
    L[i:i+n]+=sig[:n]*g*(1-pan)/1; Rr[i:i+n]+=sig[:n]*g*(1+pan)/1
rng=np.random.default_rng(3)
beat=0.625
chords=[[50,57,62,66,69],[45,52,57,61,64],[47,54,59,62,66],[43,50,55,59,62]] # D A Bm G
# pad
for ci in range(9):
    st=ci*2.5; ch=chords[ci%4]; n=int(2.9*SR); tt=np.arange(n)/SR
    env=np.minimum(tt/0.6,1)*np.minimum((2.9-tt)/0.5,1)
    s=np.zeros(n)
    for m in ch:
        f=hz(m+12)
        for d in (-0.12,0.12):
            ph=2*np.pi*f*(1+d/100)*tt
            s+=np.sin(ph)+0.25*np.sin(2*ph)+0.1*np.sin(3*ph)
    add(s*env*0.018,st)
# pluck arpeggio (from 2.9)
pat=[0,2,3,4,3,2,1,2]
for k in range(int((D-3)/(beat/2))):
    st=2.95+k*beat/2
    if st>19.6: break
    ch=chords[int(st//2.5)%4]; m=ch[pat[k%8]]+12
    n=int(0.9*SR); tt=np.arange(n)/SR; f=hz(m)
    s=(np.sin(2*np.pi*f*tt)+0.35*np.sin(4*np.pi*f*tt)*np.exp(-tt*8))*np.exp(-tt*5.5)
    add(s*0.05,st,pan=0.35*np.sin(k))
# bass
for k in range(int(D/1.25)):
    st=k*1.25
    if st<2.9 or st>19.5: continue
    m=chords[int(st//2.5)%4][0]-12; n=int(1.2*SR); tt=np.arange(n)/SR
    add(np.sin(2*np.pi*hz(m)*tt)*np.exp(-tt*2.2)*np.minimum(tt/0.01,1)*0.12,st)
# soft kick & shaker
for k in range(40):
    st=2.95+k*beat
    if st>19.0: break
    n=int(0.4*SR); tt=np.arange(n)/SR
    f=50+90*np.exp(-tt*30); add(np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-tt*9)*0.22,st)
    nz=rng.standard_normal(int(0.08*SR)); nz=np.diff(nz,prepend=0)*np.exp(-np.arange(len(nz))/SR*60)
    add(nz*0.02,st+beat/2,pan=0.3)
# whoosh
def whoosh(center,dur=0.9,g=0.18):
    n=int(dur*SR); tt=np.arange(n)/SR; nz=rng.standard_normal(n)
    # sweep lowpass via moving average with varying width
    env=np.sin(np.pi*tt/dur)**2
    out=np.zeros(n); acc=0; 
    a=0.02+0.25*np.sin(np.pi*tt/dur)
    for i in range(n): acc+=a[i]*(nz[i]-acc); out[i]=acc
    add(out*env*g*2.2,center-dur/2,pan=0)
for c in (2.75,6.85,12.4,15.85): whoosh(c)
# riser intro
n=int(2.6*SR); tt=np.arange(n)/SR; add(np.sin(2*np.pi*(200*tt+180*tt**2))*0.0+rng.standard_normal(n)*0.0,0)
# shimmer on logo
for i,m in enumerate([74,78,81,86,90]):
    n=int(1.6*SR); tt=np.arange(n)/SR; add(np.sin(2*np.pi*hz(m)*tt)*np.exp(-tt*3)*0.05,0.25+i*0.09,pan=(i-2)*0.25)
# boom at 3.0
n=int(1.5*SR); tt=np.arange(n)/SR; add(np.sin(2*np.pi*(40+60*np.exp(-tt*8))*tt)*np.exp(-tt*2.5)*0.35,2.95)
# pops
def pop(st,f=900,g=0.12):
    n=int(0.12*SR); tt=np.arange(n)/SR; add(np.sin(2*np.pi*(f+f*np.exp(-tt*40))*tt)*np.exp(-tt*35)*g,st,pan=0.2)
for i in range(6): pop(13.25+i*.13,700+i*80)
pop(8.35,600,.14); pop(9.5,800,.14); pop(10.05,1000,.08); pop(16.05,600,.14)
for k in range(13): pop(16.45+k*1.55/13*1.0,2400,0.03)   # typing ticks
for i in range(6): pop(19.05+i*.09,500+i*60,.08)
# final chord ring
ch=chords[0]; n=int(3*SR); tt=np.arange(n)/SR
add(sum(np.sin(2*np.pi*hz(m+12)*tt) for m in ch)*np.exp(-tt*1.2)*0.03,18.4)
mix=np.stack([L,Rr],1)
fade=np.ones(N); fade[-int(1.2*SR):]=np.linspace(1,0,int(1.2*SR)); mix*=fade[:,None]
mix/=np.abs(mix).max()/0.7
w=wave.open('music.wav','wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
w.writeframes((mix*32767).astype('<i2').tobytes()); w.close(); print('ok')
