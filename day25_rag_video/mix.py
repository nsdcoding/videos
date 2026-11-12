"""Build the narration track (+ soft whooshes on big camera flights and a quiet pad), then cut per part."""
import json, wave, numpy as np, subprocess
SR = 48000
d = json.load(open('timing.json')); total = d['total']
out = np.zeros(int(total * SR) + SR, dtype=np.float64)
def load(path):
    with wave.open(path) as w:
        sr = w.getframerate(); x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float64) / 32768
    n = int(len(x) * SR / sr); return np.interp(np.linspace(0, len(x) - 1, n), np.arange(len(x)), x)
for l in d['lines']:
    x = load(f"audio/{l['id']}.wav"); i = int(l['start'] * SR); out[i:i + len(x)] += x * 0.95
rng = np.random.default_rng(7)
def whoosh(t0, dur, amp):
    n = int(dur * SR); noise = rng.standard_normal(n)
    # crude band-pass with moving averages, sweeping
    k1 = np.convolve(noise, np.ones(8) / 8, 'same'); k2 = np.convolve(noise, np.ones(60) / 60, 'same')
    band = k1 - k2; env = np.sin(np.linspace(0, np.pi, n)) ** 2
    i = int(t0 * SR); out[i:i + n] += band * env * amp
for c in d['cams']:
    if c['dip'] >= .2: whoosh(c['t0'] + .1, min(1.8, c['t1'] - c['t0']), 0.10 * c['dip'] / .35)
# quiet warm pad: slow chord changes every 8 s
t = np.arange(len(out)) / SR
chords = [[220.0, 277.18, 329.63], [196.0, 246.94, 293.66], [174.61, 220.0, 261.63], [196.0, 246.94, 329.63]]
pad = np.zeros_like(out); seg = 8.0
for k in range(int(total / seg) + 1):
    a, b = int(k * seg * SR), int(min(len(out), (k + 1.25) * seg * SR))
    tt = t[a:b] - k * seg; env = np.clip(tt / 2, 0, 1) * np.clip((seg * 1.25 - tt) / 2, 0, 1)
    for f in chords[k % 4]:
        pad[a:b] += env * (np.sin(2 * np.pi * f * t[a:b]) + .3 * np.sin(2 * np.pi * f * 2.003 * t[a:b])) / 3
out += pad * 0.012
fade = np.clip((total - t) / 3, 0, 1); out *= np.minimum(1, fade)
out = np.clip(out / max(1, np.abs(out).max() / 0.97), -1, 1)
pcm = (out * 32767).astype(np.int16)
with wave.open('mix.wav', 'wb') as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
print('mix.wav', round(len(out) / SR, 1), 's')
