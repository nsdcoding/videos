import sys, json, base64, os
sys.path.insert(0, "/home/user/videos/skills/motion-video-style/scripts")
import vertex_assets as va
va.ensure_deps(); va.ensure_key()
import google.auth, requests
from google.auth.transport.requests import Request
creds, project = google.auth.default(scopes=[va.SCOPE]); creds.refresh(Request())
H={"Authorization": f"Bearer {creds.token}", "x-goog-user-project": project}
if sys.argv[1]=="list":
    r=requests.get("https://texttospeech.googleapis.com/v1/voices?languageCode=hi-IN",headers=H)
    print(r.status_code); 
    for v in r.json().get("voices",[]):
        if "Chirp3" in v["name"]: print(v["name"], v["ssmlGender"])
    if r.status_code!=200: print(r.text[:500])
else:
    voice, text, out = sys.argv[2], sys.argv[3], sys.argv[4]
    body={"input":{"text":text},"voice":{"languageCode":"hi-IN","name":voice},
          "audioConfig":{"audioEncoding":"LINEAR16","sampleRateHertz":24000}}
    if len(sys.argv)>5: body["audioConfig"]["speakingRate"]=float(sys.argv[5])
    r=requests.post("https://texttospeech.googleapis.com/v1/text:synthesize",headers=H,json=body)
    if r.status_code!=200: sys.exit(r.text[:600])
    open(out,"wb").write(base64.b64decode(r.json()["audioContent"]))
    print("ok", out)
