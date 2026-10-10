#!/usr/bin/env python3
"""Generate images (Nano Banana) and voiceovers (Gemini TTS) on Vertex AI.

Needs GCP_SA_KEY_B64 in the environment (decoded to /tmp/sa.json automatically).

  python3 gen.py image "prompt" out.png [--aspect 16:9] [--ref ref.png]
  python3 gen.py voice "text" out.wav [--voice Kore] [--style "Say warmly:"]
  python3 gen.py batch scenes.json out_dir/

The implementation lives in the motion-video-style skill so the skill and the
repo share one copy: skills/motion-video-style/scripts/vertex_assets.py
"""
import os, runpy, sys

sys.argv[0] = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           "skills", "motion-video-style", "scripts", "vertex_assets.py")
runpy.run_path(sys.argv[0], run_name="__main__")
