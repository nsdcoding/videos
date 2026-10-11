import re, json, subprocess, math
md = open("script.md").read().split("---",1)[1]
md = md.split("यह पुस्तक रॉबर्ट ग्लोवर की किताब के विचारों")[0] + "यह पुस्तक रॉबर्ट ग्लोवर की किताब के विचारों" + md.split("यह पुस्तक रॉबर्ट ग्लोवर की किताब के विचारों")[1]
sents=[]; sec=0
for para in [p.strip() for p in md.split("\n") if p.strip()]:
    if para.startswith("#"):
        sec+=1; sents.append({"text":para.lstrip("# ").strip(),"head":True,"sec":sec}); continue
    for s in re.split(r"(?<=[।?!])\s+", para):
        if s.strip(): sents.append({"text":s.strip(),"head":False,"sec":sec})
# silences
out=subprocess.run(["ffmpeg","-i","narration.mp3","-af","silencedetect=noise=-35dB:d=0.2","-f","null","-"],capture_output=True,text=True).stderr
st=[float(x) for x in re.findall(r"silence_start: ([\d.]+)",out)]; en=[float(x) for x in re.findall(r"silence_end: ([\d.]+)",out)]
dur=float(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0","narration.mp3"]))
sil=[(a,b) for a,b in zip(st,en)]
start0=sil[0][1] if sil[0][0]<0.05 else 0
B=[(a,b) for a,b in sil if a>0.05 and b<dur-0.05]+[(dur,dur)]
def L(s): return len(re.sub(r"\s","",s))+ 3*s.count(",")
total=sum(L(s["text"]) for s in sents); speech=dur-start0-sum(b-a for a,b in B)
rate=speech/total
n=len(sents); m=len(B); INF=1e18
# dp[i][j]: sentence i ends at boundary j
import numpy as np
dp=np.full((n,m),INF); bk=np.zeros((n,m),int)
cum=np.array([0]+[b-a for a,b in B]).cumsum()
def cost(i,t0,j,ws):
    d=B[j][0]-t0; e=rate*L(sents[i]["text"])
    pause=B[j][1]-B[j][0]
    return ((d-e)/math.sqrt(e+1))**2 - 6*min(pause,1.2)
for j in range(m):
    dp[0][j]=cost(0,start0,j,0)
for i in range(1,n):
    best=INF;bj=-1
    for j in range(m):
        # prev end k<j ; use window
        lo=max(0,j-25)
        for k in range(lo,j):
            if dp[i-1][k]>=INF: continue
            c=dp[i-1][k]+cost(i,B[k][1],j,0)
            if c<dp[i][j]: dp[i][j]=c; bk[i][j]=k
j=m-1; ends=[0]*n
for i in range(n-1,-1,-1):
    ends[i]=j; j=bk[i][j]
t=start0
for i,s in enumerate(sents):
    s["start"]=round(t,2); s["end"]=round(B[ends[i]][0],2); t=B[ends[i]][1]
json.dump(sents,open("timing.json","w"),ensure_ascii=False,indent=1)
print(n,"sentences",m,"boundaries rate",rate)
for s in sents[:10]+sents[-8:]: print(s["start"],s["end"],s["text"][:50])
