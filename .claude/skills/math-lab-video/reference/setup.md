# Setting up a fresh container

```bash
apt-get update -qq && DEBIAN_FRONTEND=noninteractive apt-get install -y -qq libcairo2-dev libpango1.0-dev pkg-config \
  texlive-latex-base texlive-latex-extra texlive-fonts-recommended dvisvgm cm-super
pip install -q --ignore-installed setuptools          # the system setuptools cannot build the `srt` package
SETUPTOOLS_USE_DISTUTILS=local pip install -q srt
pip install -q manim google-auth requests
```

- Fonts: Inter and Inter Display must be installed (`fc-list | grep -i inter`); they were preinstalled in
  past sessions under /usr/share/fonts/opentype/inter/.
- Playwright + Chromium are preinstalled; run thumbs.py with `NODE_PATH=$(npm root -g) python3 thumbs.py`.
- Credentials: `GCP_SA_KEY_B64` (base64 service-account JSON) is decoded to /tmp/sa.json by tts.py and gen.py.
  - Text-to-Speech: works.
  - Speech-to-Text: disabled on the project so far; listen_check.py uses Gemini (`gemini-3-flash-preview`,
    location `global`) instead. Some clips only transcribe at 16 kHz; the script retries that automatically.
  - Images: `gemini-2.5-flash-image` works through `gen.py` (repo root); newer image models returned 404.
- Hugging Face and Whisper model downloads are blocked by the network proxy.
