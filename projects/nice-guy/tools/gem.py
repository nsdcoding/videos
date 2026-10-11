import sys, base64, json, runpy
sys.argv=[sys.argv[0]]+sys.argv[1:]
m = runpy.run_path("/home/user/videos/skills/motion-video-style/scripts/vertex_assets.py")
vx = m["Vertex"]()
def ask(prompt, audio=None, model="gemini-2.5-flash"):
    parts=[]
    if audio: parts.append({"inlineData":{"mimeType":"audio/mp3","data":base64.b64encode(open(audio,"rb").read()).decode()}})
    parts.append({"text":prompt})
    if not vx.creds.valid: vx.creds.refresh(vx.Request())
    url=f"https://aiplatform.googleapis.com/v1/projects/{vx.project}/locations/global/publishers/google/models/{model}:generateContent"
    r=vx.requests.post(url,json={"contents":[{"role":"user","parts":parts}]},headers={"Authorization":f"Bearer {vx.creds.token}"},timeout=600)
    r.raise_for_status()
    return r.json()["candidates"][0]["content"]["parts"][0]["text"]
if __name__=="__main__":
    print(ask(sys.argv[2], sys.argv[1]))
