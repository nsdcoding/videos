/motion-video-style Make the Day 02 video, "The Soldier Who Kept Fighting WWII Until 1974", as a test of the new v3 build format. Make a sample first.

INPUTS (Google Drive, History folder 1wL4BrjzbdDr4LQk4qkLft2Xo9fVtYbC5):
- BUILD_SPEC.md (v3) at the History root: these are the standing instructions. Follow them exactly. Ignore every file whose name starts with "SUPERSEDED - do not use".
- Folder "Day 02 - The Soldier Who Kept Fighting WWII Until 1974" (1py-dA19qE1waVXiY3UMvoy8Lqd0mUbdU): narration.md (the script, 62 segments) and build.json (v3: cast, sets, props, photos, beats).
- The same build.json is in the repo at history/v3/out/day02.build.json, and its source at history/v3/days/day02.py. Check with: python3 history/v3/validate.py history/v3/out/day02.build.json 62

REPO: nsdcoding/videos, branch claude/optimistic-galileo-5hcjvt. Put the work in day02/ (build/, audio/, images/, out/), the same layout as day01/. day01/build/ (audio.py, engine.py, render.py, write_out.py, fetch_from_runner.py) is the working Day 01 pipeline. Reuse it, and add what v3 needs:
- Character sheets first, then each pose generated with the sheet as reference.
- Poses and props generated on flat magenta #FF00FF, then keyed out and split into rigs (body, head, arms).
- Sets as full-bleed plates, arranged as places in one continuous world.
- Photo cards: never cropped or altered, a caption on every card whose photo has one, low_res photos at native size.
- Energy per beat (high, calm, still). Every pause of 2000 ms or more is completely still and silent.
Style and motion reference: the Nice Guy and Mind Tricks videos in projects/ on branch claude/epic-thompson-bf40cy.

AUDIO: Google Chirp 3 HD, en-US-Chirp3-HD-Charon, speaking_rate 0.92, plain text per segment (no SSML), silences from pause_after. Credentials come from GCP_SA_KEY_B64, decoded to /tmp/sa.json. Never print, commit or copy the key. Images: Nano Banana through skills/motion-video-style/scripts/vertex_assets.py, with the v3 style lock from BUILD_SPEC §3.1 appended verbatim to every prompt.

PHOTOS: Wikimedia rate-limits this sandbox (429). Fetch the originals from a GitHub Actions runner the same way as .github/workflows/fetch-archival.yml and day01/build/fetch_from_runner.py, committing them to day02/archival/. Never substitute a different file.

HARD RULES (from the build file's notes):
- Onoda and everyone else are cartoons with vague faces. Real faces appear only in real photos.
- No drawn violence anywhere: no shooting, no victims, no firefights.
- s25–s27 (the islanders who were killed) is one still beat on the empty rice field: no cast, no props, no graphics, no motion.
- Nothing generated is photoreal, a likeness of a real person, graphic, or contains text.
- On a broken photo URL, a refused generation, or anything else in BUILD_SPEC §9: stop and tell me. Never work around it silently.

PROCESS:
1. Generate the cast character sheets and show them to me before making any poses.
2. Render a 60–90 second sample covering s01–s08 (the cold open and title), with audio and subtitles. Send it to me and STOP until I approve it.
3. After approval, render the full video to day02/out/ with subtitles.srt, credits.txt, description.txt (with chapter timestamps) and checklist.md. If the mp4 is too large to upload in one piece, split it into parts.
4. Commit and push everything except the mp4. Don't open a PR.
