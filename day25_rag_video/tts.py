import base64, json, os, sys, time
KEY="/tmp/sa.json"
if not os.path.exists(KEY):
    open(KEY,"wb").write(base64.b64decode(os.environ["GCP_SA_KEY_B64"])); os.chmod(KEY,0o600)
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]=KEY
import google.auth, requests
from google.auth.transport.requests import Request
creds, project = google.auth.default(scopes=["https://www.googleapis.com/auth/cloud-platform"])
def tok():
    if not creds.valid: creds.refresh(Request())
    return creds.token
def list_voices(lang):
    r=requests.get("https://texttospeech.googleapis.com/v1/voices",params={"languageCode":lang},headers={"Authorization":"Bearer "+tok(),"x-goog-user-project":project})
    return r
def synth(text, out, voice="en-US-Chirp3-HD-Charon", rate=1.0):
    lang="-".join(voice.split("-")[:2])
    body={"input":{"text":text},"voice":{"languageCode":lang,"name":voice},
          "audioConfig":{"audioEncoding":"LINEAR16","sampleRateHertz":24000,"speakingRate":rate}}
    for a in range(6):
        r=requests.post("https://texttospeech.googleapis.com/v1/text:synthesize",json=body,
            headers={"Authorization":"Bearer "+tok(),"x-goog-user-project":project},timeout=120)
        if r.status_code==200:
            open(out,"wb").write(base64.b64decode(r.json()["audioContent"])); return
        print(r.status_code, r.text[:300], file=sys.stderr)
        if r.status_code not in (429,500,503): sys.exit(1)
        time.sleep(2**a*2)
    sys.exit("failed")
if __name__=="__main__":
    if sys.argv[1]=="list":
        r=list_voices(sys.argv[2]); print(r.status_code)
        if r.status_code==200: print([v["name"] for v in r.json().get("voices",[]) if "Chirp3" in v["name"]])
        else: print(r.text[:500])
    else:
        synth(sys.argv[2], sys.argv[3], sys.argv[4] if len(sys.argv)>4 else "en-US-Chirp3-HD-Charon")
